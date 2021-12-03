import pygame
from main_board import MainBoard
from operation_board import OperationBoard
from random import *
from player import Player
from dice import *
from constant import *
from city import *
from color import *
from status_board import StatusBoard
from img_button import ImgButton
from scores_board import ScoreBoard

class Window:
    def __init__(self):
        pygame.init()
        clock = pygame.time.Clock()
        scree_hight = 800
        screen_width = 1280
        screen = pygame.display.set_mode((screen_width, scree_hight))
        screen.fill((0, 191, 255))
        self.surface = screen
        self.winner_points = 10

        pygame.display.set_caption("Catan")
        self.restart_button = ImgButton(self, "../resources/img/button/restart.png", 50, x=screen_width-100, y= 50, proportion = False)

        self.main_board = MainBoard(self)
        self.hexes = self.main_board.hexes_infos()


        self.operation_board = OperationBoard(self)
        self.operation_board.change_board_type("Build")

        self.status_board = StatusBoard(self)


        # User input for player color, settlement locations
        my_player = Player(self, BLUE)

        self.ai_player_list = [Player(self, PURPLE), Player(self, RED), Player(self, BLACK)]
        self.all_player_list = self.ai_player_list + [my_player]
        self.score_board = ScoreBoard(self)
        # set cursor style
        global cursor_state
        cursor_state = "normal"
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        is_opbhover = False
        is_mbhover = False
        is_restarthover = False
        is_over = False
        self.round = 1
        self.real_player = my_player
        self.current_player = my_player
        pygame.display.flip()
        while True:
            clock.tick(20)
            if (not is_mbhover) & (not is_opbhover):
                is_restarthover = self.restart_button_check()
            if (self.operation_board is not None) & (not is_over):
                if self.operation_board.type == "Init":
                    is_opbhover = False
                    is_over = self.ai_action()
                else:
                    if (not is_mbhover) & (not is_restarthover):
                        is_opbhover = self.operation_board.check_hover(pygame.mouse.get_pos())

            # Settlement button operations. Checks for cursor hover and clicks and changes color
            if (not is_opbhover) & (not is_restarthover) & (not is_over):
                if self.operation_board.type == "Build":
                    is_mbhover = self.main_board.check_hover(pygame.mouse.get_pos(), self.current_player)

            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()

            pygame.display.update()

    def ai_action(self):
        if self.check_over():
            return True
        for ai_player in self.ai_player_list:
            self.current_player = ai_player
            if self.round == 1:
                self.ai_build_settlement()
                self.score_board.update_info(self.current_player)
                self.ai_build_settlement()
                self.score_board.update_info(self.current_player)
            else:
                self.ai_dice_roll()
                continue_settlement = True
                while continue_settlement:
                    if randint(1, 3) == 3:   ## 2/3 chance to build a road
                        break
                    continue_settlement = self.ai_build_settlement()
                    self.score_board.update_info(self.current_player)
                continue_road = True
                while continue_road:
                    if randint(1, 3) == 3:    ## 2/3 chance to build a road
                        break
                    continue_road = self.ai_build_road()
            if self.check_over():
                return True
        self.round += 1
        self.current_player = self.real_player
        self.operation_board.change_board_type("Roll")
        return False

    def ai_dice_roll(self):
        async def waiting_animation(time):
            await asyncio.sleep(time)
        asyncio.run(waiting_animation(0.2))
        dice1 = Dice(self.operation_board, 3/10, 1/2)
        dice2 = Dice(self.operation_board, 7/10, 1/2)
        self.operation_board.update()
        value1 = randint(1, 6)
        value2 = randint(1, 6)
        total = value1 + value2
        async def roll_animation():
            global cursor_state
            cursor_state = "wait"
            await asyncio.gather(dice1.roll(value1), dice2.roll(value2))
        asyncio.run(roll_animation())
        asyncio.run(waiting_animation(1))

        focus_hexes = self.hexes[total]
        self.main_board.hexes_shrink(focus_hexes)
        for hex in focus_hexes:
            if hex.type != "desert":
                resource_type = Resource[hex.type]
                for player in hex.settlements.keys():
                    for settlement in hex.settlements[player]:
                        if settlement.type == "settlement":
                            player.resources[resource_type] += 1
                        elif settlement.type == "city":
                            player.resources[resource_type] += 1 # IDK WHY the add_value here would added the resource in double,
                                                                 # it should be 2 but I have to put 1 here.
                self.status_board.update_info()
        dice1.remove()
        dice2.remove()

    def ai_build_settlement(self):
        async def waiting_animation(time):
            await asyncio.sleep(time)
        asyncio.run(waiting_animation(0.3))
        chooseable_settlement_list = self.current_player.chooseable_settlement_buttons
        if len(chooseable_settlement_list) == 0:
            return False
        choose = randint(0,len(chooseable_settlement_list)-1)
        clicked_settlement = chooseable_settlement_list[choose]
        if (self.round > 1) | (self.current_player.settlement > 1):
            if clicked_settlement.type == "initial":
                update_type = "settlement"
            elif clicked_settlement.type == "settlement":
                update_type = "city"
            cost_dict = CostList[update_type]
            player_resources_copy = self.current_player.resources.copy()
            for resource in cost_dict:
                if player_resources_copy[resource] >= cost_dict[resource]:
                    player_resources_copy[resource] -= cost_dict[resource]
                else:
                    return False
            self.current_player.resources = player_resources_copy
        clicked_settlement.update_type(self.current_player)
        if clicked_settlement.type == "settlement":
            self.current_player.settlement += 1
            for other_player in self.get_other_player():
                if clicked_settlement in other_player.chooseable_settlement_buttons:
                    other_player.chooseable_settlement_buttons.remove(clicked_settlement)
            for connected_settlement in self.main_board.settlement_settlement_button[clicked_settlement]:
                if connected_settlement in self.current_player.chooseable_settlement_buttons:
                    self.current_player.chooseable_settlement_buttons.remove(connected_settlement)
            ## add the corresponding road to self.super_surface_object.current_player.chooseable_road_buttons
            for road_button in self.main_board.settlement_road_button[clicked_settlement]:
                if road_button not in self.current_player.chooseable_road_buttons:
                    self.current_player.chooseable_road_buttons.append(road_button)
        elif clicked_settlement.type == "city":
            self.current_player.city += 1
            self.current_player.chooseable_settlement_buttons.remove(clicked_settlement)
        # add the player to the hex here and change the clicked_settlement.player to player and use the player's color
        for hex in self.main_board.settlement_points[(clicked_settlement.x + 10,
                                           clicked_settlement.y + 10)]:  # 10 is the settlement_radius in the draw_settlement function
            if not (self.current_player in hex.settlements):
                hex.settlements[self.current_player] = []
            hex.settlements[self.current_player].append(clicked_settlement)
        self.main_board.update()
        return True

    def ai_build_road(self):
        async def waiting_animation(time):
            await asyncio.sleep(time)
        asyncio.run(waiting_animation(0.3))
        chooseable_road_list = self.current_player.chooseable_road_buttons
        if len(chooseable_road_list) == 0:
            return False
        choose = randint(0, len(chooseable_road_list) - 1)
        clicked_road = chooseable_road_list[choose]
        if clicked_road.type == "initial":
            update_type = "road"
        else:
            return False
        cost_dict = CostList[update_type]
        player_resources_copy = self.current_player.resources.copy()
        for resource in cost_dict:
            if player_resources_copy[resource] >= cost_dict[resource]:
                player_resources_copy[resource] -= cost_dict[resource]
            else:
                return False
        self.current_player.resources = player_resources_copy
        clicked_road.update_type()
        if clicked_road.type == "road":
            self.current_player.road += 1
            self.current_player.chooseable_road_buttons.remove(clicked_road)
            for connected_road_button in self.main_board.road_road_button[clicked_road]:
                if connected_road_button not in self.current_player.chooseable_road_buttons:
                    self.current_player.chooseable_road_buttons.append(connected_road_button)
            for other_player in self.get_other_player():
                if clicked_road in other_player.chooseable_road_buttons:
                    other_player.chooseable_road_buttons.remove(clicked_road)
            for settlement_button in self.main_board.road_settlement_button[clicked_road]:
                for other_player in self.get_other_player():
                    if settlement_button in other_player.chooseable_settlement_buttons:
                        other_player.chooseable_settlement_buttons.remove(settlement_button)
        clicked_road.display_settlement_button()
        info = self.main_board.road_points[(clicked_road.x + clicked_road.radius, clicked_road.y + clicked_road.radius)]
        pygame.draw.line(self.main_board.surface, self.current_player.color, info[0], info[1], 5)
        self.main_board.draw_points()  # avoid covering the settlements
        return True

    def get_other_player(self):
        other_player_list = self.all_player_list.copy()
        other_player_list.remove(self.current_player)
        return other_player_list

    def check_points(self):
        for player in self.all_player_list:
            if player.get_total_points() >= self.winner_points:
                return player
        return None

    def check_over(self):
        winner = self.check_points()
        if winner is not None:
            if winner == self.real_player:
                self.operation_board.change_board_type("Error", "You win!", back_button=False)
            else:
                self.operation_board.change_board_type("Error", "Player " + str(
                    self.all_player_list.index(winner) + 1) + " win!", back_button=False)
            return True
        else:
            return False

    def restart_button_check(self):
        is_hover = self.restart_button.check_click(pygame.mouse.get_pos())
        if is_hover:
            if pygame.mouse.get_pressed()[0]:
                self.__init__()
                return
        return is_hover


    def update(self):
        pass





if __name__ == '__main__':
    game = Window()
