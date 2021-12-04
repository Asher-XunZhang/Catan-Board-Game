import pygame.cursors

from hexagon import *
from robber import *
from settlement import *
import random
from calculation import *
from road import *

class MainBoard:
    def __init__(self, super_surface_object):
        self.super_surface_object = super_surface_object
        self.super_surface = super_surface_object.surface
        self.side = min(self.super_surface.get_width(), self.super_surface.get_height()) * 3 / 4
        self.height = self.side
        self.width = self.side
        self.surface = pygame.Surface((self.side, self.side))
        position = blit_position_transfer(self.super_surface, self.surface)
        self.x = position[0]
        self.y = position[1]
        self.surface.set_colorkey(TRASPARENT)

        self.settlement_buttons = []
        self.settlement_points = {}
        self.road_buttons = []
        self.road_points = {}
        self.settlement_road_position = {} # store the road position that the settlement position is connected to -> settlement_position : [road_position]
        self.settlement_road_button = {} # store the road button that the settlement button is connected to
        self.road_settlement_button = {} # store the settlement button that the road button is connected to
        self.road_road_button = {} # store the road button that the road button is connected to
        self.settlement_settlement_button = {} # store the settlement button that the settlement button is connected to

        self.draw_board()
        self.calc_settlement_points()
        self.draw_points()

        self.update()

    def draw_board(self):
        x, y = self.surface.get_width() / 2, self.surface.get_height() / 2
        side = self.surface.get_width() * 4 / 9
        self.hex = pygame.draw.polygon(self.surface, LIGHTBLUE, [
            (x + side * cos(2 * pi * i / 6), y + side * sin(2 * pi * i / 6))
            for i in range(6)
        ])
        element = []
        element += ["pasture"] * 4 + ["forest"] * 4 + ["field"] * 4 + ["hill"] * 3 + ["mountain"] * 3 + ["desert"]
        random.shuffle(element)
        random.shuffle(element)
        # element.insert(9, "desert") # if need te dersert always be the center hex, uncomment this line and delete ["desert"] in the third line of code above

        num = [2] + [12] + [3, 4, 5, 6, 8, 9, 10, 11] * 2 + [7]
        random.shuffle(num)
        random.shuffle(num)
        # num.insert(9, 7) # if need te dersert always be the center hex, uncomment this line and delete [7] in the third line of code above
        self.hexes = {
            2: [],
            3: [],
            4: [],
            5: [],
            6: [],
            7: [],
            8: [],
            9: [],
            10: [],
            11: [],
            12: []
        }
        initX, initY = 150, 80
        hex_side = 50

        for i in range(19):
            if (i <= 2):
                hex = Hexagon(self.surface, self, i, num[i], element[i], hex_side,
                              ((i - 0) * 2 * hex_side + initX, initY))
            elif (3 <= i <= 6):
                hex = Hexagon(self.surface, self, i, num[i], element[i], hex_side,
                              ((i - 3) * 2 * hex_side + initX - hex_side, 2 * hex_side + initY - 15))
            elif (7 <= i <= 11):
                hex = Hexagon(self.surface, self, i, num[i], element[i], hex_side,
                              ((i - 7) * 2 * hex_side + initX - hex_side * 2, 4 * hex_side + initY - 30))
            elif (12 <= i <= 15):
                hex = Hexagon(self.surface, self, i, num[i], element[i], hex_side,
                              ((i - 12) * 2 * hex_side + initX - hex_side, 6 * hex_side + initY - 45))
            else:
                hex = Hexagon(self.surface, self, i, num[i], element[i], hex_side,
                              ((i - 16) * 2 * hex_side + initX, 8 * hex_side + initY - 60))
            self.hexes[num[i]].append(hex)

    def get_sett_buttons(self):
        return self.settlement_buttons

    def hexes_infos(self):
        return self.hexes

    # Find settle points
    def calc_settlement_points(self):
        # hex_points_board = []
        points_hex_board = {}
        hex_points_board = {}
        # Obtain all corner points
        for i in range(2, 13):
            for hex in self.hexes[i]:
                hex_points = hex.get_corner()
                hex_points_board[hex] = hex_points
                # Give hex to settlements
                for j in hex_points:
                    points_x = (j[0] + hex.x)
                    points_y = (j[1] + hex.y)
                    points_hex_board[(points_x, points_y)] = hex

        hex_justify_points = {}
        for i in range(2, 13):
            for hex in self.hexes[i]:
                hex_justify_points[hex] = []

        # Delete duplicate points
        for corner_t in points_hex_board.keys():
            add = True
            for sett_t in self.settlement_points.keys():
                if (abs(sett_t[0] - corner_t[0]) < 2) and (abs(sett_t[1] - corner_t[1]) < 2):
                    self.settlement_points[sett_t].append(points_hex_board[corner_t])
                    hex_justify_points[points_hex_board[corner_t]].append(sett_t)
                    add = False
                    break
            if (add):
                self.settlement_points[corner_t] = []
                self.settlement_points[corner_t].append(points_hex_board[corner_t])
                hex_justify_points[points_hex_board[corner_t]].append(corner_t)

        for hex in list(hex_justify_points.keys()):
            corner_points = hex_justify_points[hex]
            for i in range(len(corner_points)):
                if i == (len(corner_points) - 1):
                    point_1 = corner_points[i]
                    point_2 = corner_points[0]
                    x = (point_1[0] + point_2[0]) / 2
                    y = (point_1[1] + point_2[1]) / 2
                else:
                    point_1 = corner_points[i]
                    point_2 = corner_points[i + 1]
                    x = (point_1[0] + point_2[0]) / 2
                    y = (point_1[1] + point_2[1]) / 2
                if point_1 not in self.settlement_road_position:
                    self.settlement_road_position[point_1] = []
                if point_2 not in self.settlement_road_position:
                    self.settlement_road_position[point_2] = []
                self.settlement_road_position[point_1].append((x, y))
                self.settlement_road_position[point_2].append((x, y))
                self.road_points[(x, y)] = (point_1, point_2, hex)

    def draw_points(self):
        if len(self.settlement_buttons) <= 0:
            settlement_radius = 10
            for i in self.settlement_points.keys():
                new_sett_button = Settlement(self, settlement_radius, LIGHTBLUE, LIGHTCYAN, i[0] - settlement_radius, i[1] - settlement_radius)
                self.settlement_buttons.append(new_sett_button)
            road_radius = 6
            for i in self.road_points.keys():
                new_road_button = Road(self, road_radius, LIGHTBLUE, BLACK, i[0] - road_radius, i[1] - road_radius)
                self.road_buttons.append(new_road_button)

            for settlement_button in self.settlement_buttons:
                road_list = self.settlement_road_position[(settlement_button.x+settlement_radius, settlement_button.y+settlement_radius)]
                self.settlement_road_button[settlement_button] = []
                for road_button in self.road_buttons:
                    if (road_button.x + road_radius, road_button.y + road_radius) in road_list:
                        self.settlement_road_button[settlement_button].append(road_button)
                        if road_button not in self.road_settlement_button:
                            self.road_settlement_button[road_button] = []
                        if settlement_button not in self.road_settlement_button[road_button]:
                            self.road_settlement_button[road_button].append(settlement_button)
            for settlement_button in self.settlement_buttons:
                for road_button in self.settlement_road_button[settlement_button]:
                    if road_button not in self.road_road_button:
                        self.road_road_button[road_button] = []
                    the_other_connected_roads = self.settlement_road_button[settlement_button].copy()
                    the_other_connected_roads.remove(road_button)
                    for other_road in the_other_connected_roads:
                        if other_road not in self.road_road_button[road_button]:
                            self.road_road_button[road_button].append(other_road)
                the_other_settlement = self.settlement_buttons.copy()
                the_other_settlement.remove(settlement_button)
                for other_settlement in the_other_settlement:
                    if len([road_button for road_button in self.settlement_road_button[settlement_button] if road_button in self.settlement_road_button[other_settlement]]) > 0:
                        if settlement_button not in self.settlement_settlement_button:
                            self.settlement_settlement_button[settlement_button] = []
                        self.settlement_settlement_button[settlement_button].append(other_settlement)
        else:
            for settlement in self.settlement_buttons:
                settlement.update_together()
            for road in self.road_buttons:
                if road.type != "road":
                    road.update_together()
        self.update()

    def check_hover(self, position, player=None):
        x = position[0] - self.x
        y = position[1] - self.y
        global cursor_state
        is_hover = False
        clicked_settlement = None

        async def check_settlement_hover():
            tasks = [settlement.check_hover((x, y)) for settlement in self.super_surface_object.current_player.chooseable_settlement_buttons]
            return await asyncio.gather(*tasks)
        settlement_results = asyncio.run(check_settlement_hover())
        for result in settlement_results:
            is_hover = is_hover | result[0]
            if result[0]:
                clicked_settlement = result[1]
                break
        if is_hover:
            if clicked_settlement.type != "city":
                if pygame.mouse.get_pressed()[0]:
                    for event in pygame.event.get():
                        cursor_state = "clicked"
                        if (self.super_surface_object.round <= 1):
                            if clicked_settlement.type == "settlement":
                                self.super_surface_object.operation_board.remove_build_type_ui()
                                self.super_surface_object.operation_board.change_board_type("Error",
                                                                                            "Your resources are NOT enough!")
                                return False
                            if  (self.super_surface_object.current_player.settlement == 2):
                                self.super_surface_object.operation_board.remove_build_type_ui()
                                self.super_surface_object.operation_board.change_board_type("Error",
                                                                                            "Only can build two settlements!")
                                return False
                        if (self.super_surface_object.round > 1) | (self.super_surface_object.current_player.settlement > 1):
                            if clicked_settlement.type == "initial":
                                update_type = "settlement"
                            elif clicked_settlement.type == "settlement":
                                update_type = "city"
                            cost_dict = CostList[update_type]
                            player_resources_copy = player.resources.copy()
                            for resource in cost_dict:
                                if player_resources_copy[resource] >= cost_dict[resource]:
                                    player_resources_copy[resource] -= cost_dict[resource]
                                else:
                                    self.super_surface_object.operation_board.remove_build_type_ui()
                                    self.super_surface_object.operation_board.change_board_type("Error", "Your resources are NOT enough!")
                                    return False
                            player.resources = player_resources_copy
                            self.super_surface_object.status_board.update_info()
                        clicked_settlement.update_type(self.super_surface_object.current_player)
                        if clicked_settlement.type == "settlement":
                            player.settlement += 1
                            self.super_surface_object.score_board.update_info(self.super_surface_object.current_player)
                            for other_player in self.super_surface_object.get_other_player():
                                if clicked_settlement in other_player.chooseable_settlement_buttons:
                                    other_player.chooseable_settlement_buttons.remove(clicked_settlement)
                            for connected_settlement in self.settlement_settlement_button[clicked_settlement]:
                                if connected_settlement in player.chooseable_settlement_buttons:
                                    player.chooseable_settlement_buttons.remove(connected_settlement)
                            ## add the corresponding road to self.super_surface_object.current_player.chooseable_road_buttons
                            for road_button in self.settlement_road_button[clicked_settlement]:
                                if road_button not in player.chooseable_road_buttons:
                                    player.chooseable_road_buttons.append(road_button)
                        elif clicked_settlement.type == "city":
                            player.city += 1
                            player.settlement -= 1
                            self.super_surface_object.score_board.update_info(self.super_surface_object.current_player)
                        # add the player to the hex here and change the clicked_settlement.player to player and use the player's color
                        for hex in self.settlement_points[(clicked_settlement.x + 10, clicked_settlement.y + 10)]: # 10 is the settlement_radius in the draw_settlement function
                            if not (player in hex.settlements):
                                hex.settlements[player] = []
                            hex.settlements[player].append(clicked_settlement)
                        break
                elif cursor_state != "hand":
                    cursor_state = "hand"
        else:
            if cursor_state != "normal":
                cursor_state = "normal"

        async def check_road_hover():
            tasks = [road.check_hover((x, y)) for road in self.super_surface_object.current_player.chooseable_road_buttons]
            return await asyncio.gather(*tasks)
        if not is_hover:
            road_results = asyncio.run(check_road_hover())
            clicked_road = None
            for result in road_results:
                is_hover = is_hover | result[0]
                if result[0]:
                    clicked_road = result[1]
                    break
            if is_hover:
                if clicked_road.type != "road":
                    if pygame.mouse.get_pressed()[0]:
                        for event in pygame.event.get():
                            cursor_state = "clicked"
                            if self.super_surface_object.round == 1:
                                self.super_surface_object.operation_board.remove_build_type_ui()
                                self.super_surface_object.operation_board.change_board_type("Error",
                                                                                            "Build two settlements first!")
                                return False
                            if clicked_road.type == "initial":
                                update_type = "road"
                            cost_dict = CostList[update_type]
                            player_resources_copy = player.resources.copy()
                            for resource in cost_dict:
                                if player_resources_copy[resource] >= cost_dict[resource]:
                                    player_resources_copy[resource] -= cost_dict[resource]
                                else:
                                    self.super_surface_object.operation_board.remove_build_type_ui()
                                    self.super_surface_object.operation_board.change_board_type("Error",
                                        "Your resources are NOT enough!")
                                    return False
                            player.resources = player_resources_copy
                            self.super_surface_object.status_board.update_info()
                            clicked_road.update_type()
                            if clicked_road.type == "road":
                                player.road += 1
                                self.super_surface_object.current_player.chooseable_road_buttons.remove(clicked_road)
                                for other_player in self.super_surface_object.get_other_player():
                                    if clicked_road in other_player.chooseable_road_buttons:
                                        other_player.chooseable_road_buttons.remove(clicked_road)
                                for connected_road_button in self.road_road_button[clicked_road]:
                                    if connected_road_button not in player.chooseable_road_buttons:
                                        player.chooseable_road_buttons.append(connected_road_button)
                                for settlement_button in self.road_settlement_button[clicked_road]:
                                    for other_player in self.super_surface_object.get_other_player():
                                        if settlement_button in other_player.chooseable_settlement_buttons:
                                            other_player.chooseable_settlement_buttons.remove(settlement_button)
                            clicked_road.display_settlement_button()
                            info = self.road_points[(clicked_road.x + clicked_road.radius, clicked_road.y + clicked_road.radius)]
                            pygame.draw.line(self.surface, self.super_surface_object.current_player.color, info[0], info[1], 5)
                            self.draw_points() # avoid covering the settlements
                            break
                    elif cursor_state != "hand":
                        cursor_state = "hand"
            else:
                if cursor_state != "normal":
                    cursor_state = "normal"
        cursor_type = (pygame.mouse.get_cursor().data)[0]
        if is_hover:
            if cursor_state == "clicked":
                if cursor_type !=pygame.cursors.tri_left:
                    pygame.mouse.set_cursor(pygame.cursors.tri_left)
            if cursor_state == "hand":
                if cursor_type != pygame.SYSTEM_CURSOR_HAND:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            if cursor_type != pygame.SYSTEM_CURSOR_ARROW:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        self.update()
        return is_hover

    def hexes_shrink(self, hexes):
        async def shrink_hexes():
            tasks = [hex.shrink() for hex in hexes]
            await asyncio.gather(*tasks)
        asyncio.run(shrink_hexes())

    def update(self):
        rect = self.super_surface.blit(self.surface, (self.x, self.y))
        pygame.display.update(rect)
