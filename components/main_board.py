from hexagon import *
from robber import *
from settlement import *
import random
from calculation import *


class MainBoard:
    def __init__(self, surface):
        self.side = min(surface.get_width(), surface.get_height())*3/4
        self.height = self.side
        self.width = self.side
        self.super_surface = surface
        self.surface = pygame.Surface((self.side, self.side))
        position = blit_position_transfer(self.super_surface, self.surface)
        self.x = position[0]
        self.y = position[1]
        self.surface.set_colorkey(TRASPARENT)


        self.settlement_buttons = []
        self.settlement_points = {}
        self.hexes = []


        self.draw_board()
        self.calc_settlement_points()
        self.draw_settlement_points()

        self.update()



    def draw_board(self):
        x, y = self.surface.get_width()/2, self.surface.get_height()/2
        side = self.surface.get_width()*4/9
        self.hex = pygame.draw.polygon(self.surface, LIGHTBLUE, [
            (x + side * cos(2 * pi * i / 6),y + side * sin(2 * pi * i / 6))
            for i in range(6)
        ])
        element = []
        element += ["pasture"] * 4 + ["forest"] * 4 + ["field"] * 4 + ["hill"] * 3 + ["mountain"] * 3
        random.shuffle(element)
        random.shuffle(element)
        element.insert(9, "desert")

        num = [2] + [12] + [3, 4, 5, 6, 8, 9, 10, 11] * 2
        random.shuffle(num)
        random.shuffle(num)
        num.insert(9, 7)
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
            if(i <= 2):
                hex = Hexagon(self.surface, self, i, num[i], element[i], hex_side, ((i-0)*2*hex_side + initX, initY))
            elif( 3 <= i <= 6):
                hex = Hexagon(self.surface, self, i, num[i], element[i], hex_side, ((i-3)*2*hex_side + initX - hex_side, 2*hex_side+initY-15))
            elif( 7 <= i <= 11):
                hex = Hexagon(self.surface, self, i, num[i], element[i], hex_side, ((i-7)*2*hex_side + initX - hex_side*2, 4*hex_side+initY-30))
            elif( 12 <= i <= 15):
                hex = Hexagon(self.surface, self, i, num[i], element[i], hex_side, ((i-12)*2*hex_side + initX - hex_side, 6*hex_side+initY-45))
            else:
                hex = Hexagon(self.surface, self, i, num[i], element[i], hex_side, ((i-16)*2*hex_side + initX, 8*hex_side+initY-60))
            self.hexes[num[i]].append(hex)


    def get_sett_buttons(self):
        return self.settlement_buttons

    def hexes_infos(self):
        return self.hexes

    # Find settle points
    def calc_settlement_points(self):
        # hex_points_board = []
        hex_points_board = {}
        # Obtain all corner points
        for i in range(2,13):
            for hex in self.hexes[i]:
                hex_points = hex.get_corner()
                # Give hex to settlements
                for j in hex_points:
                    points_x = (j[0] + hex.x)
                    points_y = (j[1] + hex.y)
                    hex_points_board[(points_x, points_y)] = []
                    hex_points_board[(points_x, points_y)].append(hex)
        # Delete corner points duplicates
        for corner_t in hex_points_board.keys():
            add = True
            for sett_t in self.settlement_points.keys():
                if (abs(sett_t[0] - corner_t[0]) < 2) and (abs(sett_t[1] - corner_t[1]) < 2):
                    self.settlement_points[sett_t].append(hex_points_board[corner_t])
                    add = False
                    break
            if (add):
                self.settlement_points[corner_t] = []
                self.settlement_points[corner_t].append(hex_points_board[corner_t])

    def draw_settlement_points(self):
        if len(self.settlement_buttons) <= 0:
            radius = 10
            for i in self.settlement_points.keys():
                # new_sett_button = Settlement(self, radius, DARKSKYBLUE, LIGHTCYAN, i[0]-radius, i[1]-radius)
                new_sett_button = Settlement(self, radius, LIGHTBLUE, LIGHTCYAN, i[0]-radius, i[1]-radius)
                self.settlement_buttons.append(new_sett_button)
        else:
            for settlement in self.settlement_buttons:
                settlement.update_together()
        self.update()

    def check_hover(self, position):
        x = position[0] - self.x
        y = position[1] - self.y
        is_hover = False
        clicked_settlement = None
        async def check_settlement_hover():
            tasks = [settlement.check_hover((x, y)) for settlement in self.settlement_buttons]
            return await asyncio.gather(*tasks)
        results = asyncio.run(check_settlement_hover())
        for result in results:
            is_hover = is_hover | result[0]
            if result[0]:
                clicked_settlement = result[1]
                break
        global cursor_state
        if is_hover:
            if clicked_settlement.type != "city":
                if pygame.mouse.get_pressed()[0]:
                    for event in pygame.event.get():
                        cursor_state = "clicked"
                        pygame.mouse.set_cursor(pygame.cursors.tri_left)
                        clicked_settlement.update_type()
                        break
                    # clicked_settlement.display_settlement_button()
                    #TODO: add the player to the hex here
                elif cursor_state != "hand":
                    cursor_state = "hand"
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            if cursor_state != "normal":
                cursor_state = "normal"
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