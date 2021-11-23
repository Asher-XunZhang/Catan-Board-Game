from dice import *
from button import *
from random import *
from img_button import *
from label import *

# OperationType = {
#     "RollDice":"Roll Dice",
#     "ExchangeResource" : "Exchange",
#     "RobResource": "Rob" ,
#     "FinishTurn" : "Finish"
# }

class OperationBoard:
    def __init__(self, super_surface_object):
        self.type = "Init"
        self.super_surface_object = super_surface_object
        self.super_surface = super_surface_object.surface
        self.height = self.super_surface.get_height() * 0.3
        self.width = self.super_surface.get_width() * 0.3
        self.x = self.super_surface.get_width() - self.width - 30
        self.y = self.super_surface.get_height() - self.height - 30
        self.button = None
        self.resources = ["lumber", "brick", "wool", "grain", "ore"]
        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill(LIGHTBLUE)

        self.draw_board()

    def change_board_type(self, type):
        resources_num = len(self.resources)
        segment_num = resources_num * 2
        if (type == "Roll"):
            self.type = "Roll"
            if self.button != None:
                self.button.remove()
            self.button = Button(self, 'Roll Dice', BLACK, x = 1/2, y = (segment_num-1)/segment_num, front_size = 24)
        elif (type == "Trade"):
            self.type = "Trade"
            if self.button != None:
                self.button.remove()
            self.trade_list = {}
            self.infos = {}
            self.add_trade_ui()
            self.button = Button(self, 'Exchange', BLACK, x = 1/2, y = (segment_num-1)/segment_num, front_size = 24)
        elif (type == "Rob"):
            self.type = "Rob"
            if self.button != None:
                self.button.remove()
            self.button = Button(self, 'Rob', BLACK, x = 1/2, y = (segment_num-1)/segment_num, front_size = 24)
            #TODO: Add Rob Resource UI
        elif (type == "Finish"):
            self.type = "Finish"
            if self.button != None:
                self.button.remove()
            self.button = Button(self, 'Finish', BLACK, x = 1/2, y = (segment_num-1)/segment_num, front_size = 24)
            # TODO: Add Rob Resource UI
        else:
            self.type = "Init"
            if self.button != None:
                self.button.remove()
        print(self.__dict__.keys())
        self.update()

    def draw_board(self):
        rect = self.super_surface.blit(self.surface, (self.x, self.y))
        pygame.display.update(rect)

    def update(self):
        self.draw_board()

    def hide(self):
        if self.button is not None:
            self.button.remove()
            self.button = None
            del self.button
            self.button = None
        self.surface.fill(DARKSKYBLUE)
        self.update()

    def remove(self):
        self.hide()
        # del self

    def check_hover(self, position):
        x = position[0] - self.x
        y = position[1] - self.y
        is_hover = False
        is_hover = is_hover | self.main_button_check_hover((x, y))
        if self.type == "Trade":
            is_hover = is_hover | self.trade_check_hover((x,y))
        elif self.type == "Rob":
            pass
            #is_hover = is_hover | self.rob_check_hover((x,y)) #TODO: Add Rob Resource UI special button hover check function
        elif self.type == "Finish":
            pass
            #is_hover = is_hover | self.finish_check_hover((x,y)) #TODO: Add Finish UI special button hover check function
        return is_hover

    def main_button_check_hover(self, position):
        x = position[0]
        y = position[1]
        is_main_button_hover = False

        async def wait():
            await asyncio.sleep(0.2)

        if (self.button is not None):
            if self.button.check_click((x,y)):
                is_main_button_hover = True
                newcolor = RED
            else:
                newcolor = BLACK
            if self.button.color != newcolor:
                self.change_button_color(newcolor)
            if is_main_button_hover:
                if pygame.mouse.get_pressed()[0]:
                    if self.type == "Roll":
                        self.roll_dice(self.super_surface_object.main_board, self.super_surface_object.hexes)
                        asyncio.run(wait())
                        self.change_board_type("Trade")
                    elif self.type == "Trade":
                        asyncio.run(wait())
                        old_stats = self.super_surface_object.status_board.resources
                        for resource in self.resources:
                            self.super_surface_object.status_board.change_info(resource,
                                                                               old_stats[resource] + self.infos[resource])
                        self.remove_trade_ui()
                        self.change_board_type("Rob")
                    elif self.type == "Rob":
                        asyncio.run(wait())
                        self.change_board_type("Finish")
                    elif self.type == "Finish":
                        asyncio.run(wait())
                        self.change_board_type("Init")
                        global cursor_state
                        cursor_state = "normal"
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        return is_main_button_hover

    def change_button_color(self, color):
        self.button.change(color = color)

    ######################################## "Roll Dice Type Methods" ############################################
    def roll_dice(self, main_board, hexes):
        dice1 = Dice(self, 1/4, 5/12)
        dice2 = Dice(self, 3/4, 5/12)
        self.update()
        value1 = randint(1, 6)
        value2 = randint(1, 6)
        total = value1 + value2
        async def roll_animation():
            global cursor_state
            cursor_state = "wait"
            await asyncio.gather(dice1.roll(value1), dice2.roll(value2))
        asyncio.run(roll_animation())

        async def waiting_animation():
            await asyncio.sleep(1)
        asyncio.run(waiting_animation())

        main_board.hexes_shrink(hexes[total])

        self.button.check_click(pygame.mouse.get_pos())
        dice1.remove()
        dice2.remove()
        self.update()
        return total

    ######################################## "Trade Type Methods" ############################################

    def trade_check_hover(self, position):
        x = position[0]
        y = position[1]
        is_trade_button_hover = False
        if len(self.trade_list) > 0:
            is_update_trade_info = False
            # resources = list(self.trade_list.keys())
            for resource in self.trade_list.keys():
                for img_button_type in self.trade_list[resource]["buttons"].keys():
                    img_button = self.trade_list[resource]["buttons"][img_button_type]
                    is_trade_button_hover = img_button.check_click((x,y))
                    if is_trade_button_hover:
                        newcolor = RED
                    else:
                        newcolor = BLACK
                    if img_button.color != newcolor:
                        img_button.change_color(newcolor)
                    if is_trade_button_hover:
                        if pygame.mouse.get_pressed()[0]:
                            label = self.trade_list[resource]["label"]
                            x, y = label.x, label.y
                            new_value = int(label.text)
                            label.remove()
                            del label
                            if img_button_type == "plus":
                                new_value += 1
                            elif img_button_type == "minus":
                                new_value -= 1
                            if new_value > 0:
                                new_color = FORESTGREEN
                            elif new_value < 0:
                                new_color = CRIMSON
                            else:
                                new_color = BLACK
                            label = Label(self, str(new_value), new_color, 20, x, y, False)
                            self.trade_list[resource]["label"] = label
                            async def wait():
                                await asyncio.sleep(0.1)
                            asyncio.run(wait())
                        break
                if is_trade_button_hover:
                    break
            self.infos = {}
            for resource in self.resources:
                self.infos[resource] = int(self.trade_list[resource]["label"].text)
            #     is_update_trade_info = is_update_trade_info | (self.trade_list[resource]["label"].text != "0")
            # if is_update_trade_info:
            #     pass
                 #TODO: update the player's infomation by using super_interface_object.current_player
                # print(infos)
        return is_trade_button_hover


    def add_trade_ui(self):
        resources_num = len(self.resources)
        segment_num = resources_num * 2
        img_size = 20

        resouce_label = None
        for i in range(resources_num):
            if (i == 0):
                porprotion = True
                x = 1/6
                y = 1/segment_num
            else:
                porprotion = False
                x = resouce_label.x
                y = resouce_label.y + img_size * 2
            resouce_label = Label(self, self.resources[i], BLACK, 18, x, y, porprotion)

        plusButton, minusButton = None, None
        for i in range(resources_num):
            if (i == 0):
                porprotion = True
                x1, x2 = 3/6, 5/6
                y1, y2 = 1/segment_num, 1/segment_num
            else:
                porprotion = False
                x1, x2 = plusButton.x, minusButton.x
                y1, y2 = plusButton.y + plusButton.height * 2, minusButton.y + minusButton.height * 2
            plusButton = ImgButton(self, "../resources/img/button/plus.png", img_size, x1, y1, porprotion)
            minusButton = ImgButton(self, "../resources/img/button/minus.png", img_size, x2, y2, porprotion)
            self.trade_list[self.resources[i]] = {}
            self.trade_list[self.resources[i]]["buttons"] = {"plus":plusButton, "minus":minusButton}

        label = None
        for i in range(resources_num):
            if (i == 0):
                porprotion = True
                x = 4/6
                y = 1/segment_num
            else:
                porprotion = False
                x = label.x
                y = label.y + img_size * 2
            label = Label(self, '0', BLACK, 20, x, y, porprotion)
            self.trade_list[self.resources[i]]["label"] = label

    def remove_trade_ui(self):
        for resource in self.trade_list:
            self.trade_list[resource]["buttons"]["plus"].remove()
            self.trade_list[resource]["buttons"]["minus"].remove()
            self.trade_list[resource]["label"].remove()
        del self.trade_list
        del self.infos
        self.surface.fill(LIGHTBLUE)
        self.update()





