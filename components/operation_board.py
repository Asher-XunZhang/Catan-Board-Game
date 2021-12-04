from dice import *
from button import *
from random import *
from img_button import *
from label import *

# OperationType = {
#   "Roll",
#   "Trade",
#   "Build",
#   "Error",
#   "Buy",
#   "Init",
# }

class OperationBoard:
    ButtonImg = {
        "plus" : "../resources/img/button/plus.png",
        "minus" : "../resources/img/button/minus.png",
        "roll" : "../resources/img/button/roll.png",
        "trade" : "../resources/img/button/trade.png",
        "back" : "../resources/img/button/back.png",
        "buy" : "../resources/img/button/buy.png",
        "build" : "../resources/img/button/build.png",
        "finish" : "../resources/img/button/finish.png"
    }
    def __init__(self, super_surface_object):
        self.type = "Init"
        self.super_surface_object = super_surface_object
        self.super_surface = super_surface_object.surface
        self.height = self.super_surface.get_height() * 0.3
        self.width = self.super_surface.get_width() * 0.3
        self.x = self.super_surface.get_width() - self.width - 30
        self.y = self.super_surface.get_height() - self.height - 30
        self.main_button = {}
        self.resources = ["lumber", "brick", "wool", "grain", "ore"]
        self.surface = pygame.Surface((self.width, self.height))
        pygame.draw.rect(self.surface, LIGHTBLUE, (0, 0, self.width, self.height), border_radius=30)
        self.surface.set_colorkey(TRASPARENT)

        self.draw_board()

    def change_board_type(self, type, message = "Error", back_button = True):
        resources_num = len(self.resources)
        segment_num = resources_num * 2
        if (type == "Roll"):
            self.type = "Roll"
            self.clean_main_button()
            self.main_button["Roll"] = ImgButton(self, self.ButtonImg["roll"], 100, x = 1/2, y = 1/2)

        elif (type == "Operate"):
            self.type = "Operate"
            self.clean_main_button()
            if self.super_surface_object.round > 1:
                self.main_button["Trade"] = ImgButton(self, self.ButtonImg["trade"], 50, x = 1/4, y = 1/3)
                self.main_button["Buy"] = ImgButton(self, self.ButtonImg["buy"], 50, x = 3/4, y = 1/3)
            self.main_button["Build"] = ImgButton(self, self.ButtonImg["build"], 50, x=2 / 4, y=1 / 3)
            self.main_button["Finish"] = ImgButton(self, self.ButtonImg["finish"], 50, x = 3/4, y = 3/4)

        elif (type == "Trade"):
            self.type = "Trade"
            self.clean_main_button()
            self.trade_list = {}
            self.infos = {}
            self.add_trade_ui()
            self.main_button["Trade"] = Button(self, 'Exchange', BLACK, x = 1/2, y = (segment_num-1)/segment_num, front_size = 24)
            self.main_button["Back"] = ImgButton(self, self.ButtonImg["back"], 30, x = 1/9, y = (segment_num-1)/segment_num)

        elif (type == "Build"):
            self.type = "Build"
            self.clean_main_button()
            self.add_build_type_ui()
            self.main_button["Back"] = ImgButton(self, self.ButtonImg["back"], 30, x = 1/9, y = (segment_num-1)/segment_num)

        elif (type == "Buy"):
            self.type = "Buy"
            self.clean_main_button()
            self.main_button["Buy"] = ImgButton(self, self.ButtonImg["buy"], 40, x = 1/2, y = (segment_num-1)/segment_num)
            self.main_button["Back"] = ImgButton(self, self.ButtonImg["back"], 30, x=1 / 9,
                                                 y=(segment_num - 1) / segment_num)

        elif (type == "Error"):
            self.clean_main_button()
            self.prev_type = self.type
            self.type = "Error"
            self.label = Label(self, message, RED, 20, 1/2, 1/2)
            if back_button:
                self.main_button["Back"] = ImgButton(self, self.ButtonImg["back"], 30, x=1 / 9,
                                                     y=(segment_num - 1) / segment_num)
        else:
            self.type = "Init"
            self.clean_main_button()
            global cursor_state
            cursor_state = "normal"
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        self.update()

    def draw_board(self):
        rect = self.super_surface.blit(self.surface, (self.x, self.y))
        pygame.display.update(rect)

    def update(self):
        self.draw_board()

    def hide(self, hide_all = False):
        self.clean_main_button()
        if hide_all:
            self.surface.fill(DARKSKYBLUE)
        else:
            pygame.draw.rect(self.surface, LIGHTBLUE, (0, 0, self.width, self.height), border_radius=30)
        self.update()

    def remove(self):
        self.hide(hide_all=True)
        # del self

    def check_hover(self, position):
        x = position[0] - self.x
        y = position[1] - self.y
        is_hover = False
        is_hover = is_hover | self.main_button_check_hover((x, y))

        ## special cases for some types
        if self.type == "Trade":
            is_hover = is_hover | self.trade_check_hover((x,y))
        if not is_hover:
            global cursor_state
            cursor_state = "normal"
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        return is_hover

    def main_button_check_hover(self, position):
        x = position[0]
        y = position[1]
        is_main_button_hover = False

        async def wait():
            await asyncio.sleep(0.2)

        if len(self.main_button) > 0:
            for main_button in list(self.main_button.keys()):
                button = self.main_button[main_button]
                if button.check_click((x,y)):
                    is_main_button_hover = True
                    newcolor = RED
                else:
                    newcolor = BLACK
                if button.color != newcolor:
                    button.change(color = newcolor)
                if is_main_button_hover:
                    if pygame.mouse.get_pressed()[0]:
                        asyncio.run(wait())
                        if self.type == "Roll":
                            self.roll_dice(self.super_surface_object.main_board, self.super_surface_object.hexes)
                            self.change_board_type("Operate")

                        elif self.type == "Operate":
                            if main_button == "Trade":
                                self.change_board_type("Trade")
                            elif main_button == "Build":
                                self.change_board_type("Build")
                            elif main_button == "Buy":
                                self.change_board_type("Buy")
                            elif main_button == "Finish":
                                if self.super_surface_object.round <= 1:
                                    count_settlement = 0
                                    for settlement in self.super_surface_object.main_board.settlement_buttons:
                                        if settlement.type == "settlement":
                                            count_settlement += 1
                                    if count_settlement != 2:
                                        self.change_board_type("Error","Build two settlements firstly!")
                                        return is_main_button_hover
                                self.change_board_type("Init")

                        elif self.type == "Trade":
                            asyncio.run(wait())
                            if main_button == "Trade":
                                positive_num = 0
                                negative_num = 0
                                for values in self.infos.values():
                                    if values > 0:
                                        positive_num += 1
                                    elif values < 0:
                                        negative_num += 1
                                if (positive_num == 0) & (negative_num > 0):
                                    self.remove_trade_ui()
                                    self.change_board_type("Error", "Must receive resources!")
                                    return is_main_button_hover
                                elif (negative_num == 0) & (positive_num > 0):
                                    self.remove_trade_ui()
                                    self.change_board_type("Error", "Must give resources!")
                                    return is_main_button_hover
                                for resource in self.resources:
                                    self.super_surface_object.current_player.resources[resource] += self.infos[resource]
                                self.super_surface_object.status_board.update_info()
                            self.remove_trade_ui()
                            self.change_board_type("Operate")
                        elif self.type == "Build":
                            asyncio.run(wait())
                            self.remove_build_type_ui()
                            if main_button == "Buy":
                                self.change_board_type("Buy")
                            else:
                                self.change_board_type("Operate")
                        elif self.type == "Buy":
                            asyncio.run(wait())
                            if main_button == "Back":
                                self.change_board_type("Operate")
                            else:
                                self.change_board_type("Error", "This feature is pending development!")

                        elif self.type == "Error":
                            if main_button == "Back":
                                prev_type = self.prev_type
                                self.remove_error_ui()
                                self.change_board_type(prev_type)
                    break
        return is_main_button_hover

    def clean_main_button(self):
        if len(self.main_button) > 0:
            for main_button in list(self.main_button.keys()):
                self.main_button[main_button].remove()
                del self.main_button[main_button]
        self.main_button = {}

    ######################################## "Roll Dice Type Methods" ############################################
    def roll_dice(self, main_board, hexes):
        self.clean_main_button()
        async def waiting_animation(time):
            await asyncio.sleep(time)
        asyncio.run(waiting_animation(0.2))
        dice1 = Dice(self, 3/10, 1/2)
        dice2 = Dice(self, 7/10, 1/2)
        self.update()
        value1 = randint(1, 6)
        value2 = randint(1, 6)
        total = value1 + value2
        async def roll_animation():
            global cursor_state
            cursor_state = "wait"
            await asyncio.gather(dice1.roll(value1), dice2.roll(value2))
        asyncio.run(roll_animation())

        asyncio.run(waiting_animation(1))
        focus_hexes = hexes[total]
        main_board.hexes_shrink(focus_hexes)
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
                self.super_surface_object.status_board.update_info()
        self.main_button_check_hover(pygame.mouse.get_pos())
        dice1.remove()
        dice2.remove()
        self.update()
        # return total

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
                            old_value = int(label.text)
                            new_value = int(label.text)
                            label.remove()
                            del label
                            if img_button_type == "plus":
                                new_value += 1
                            elif img_button_type == "minus":
                                new_value -= 1
                                if (self.super_surface_object.current_player.resources[resource] < abs(new_value)) & (old_value <= 0):
                                    self.remove_trade_ui()
                                    self.change_board_type("Error", "You don't have enough " + resource)
                                    return is_trade_button_hover
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
        return is_trade_button_hover


    def add_trade_ui(self):
        resources_num = len(self.resources)
        segment_num = resources_num * 2
        img_size = 20

        resouce_label = None
        for i in range(resources_num):
            if (i == 0):
                proportion = True
                x = 1/5
                y = 1/segment_num
            else:
                proportion = False
                x = resouce_label.x
                y = resouce_label.y + img_size * 2
            resouce_label = Label(self, self.resources[i], BLACK, 18, x, y, proportion)

        plusButton, minusButton = None, None
        for i in range(resources_num):
            if (i == 0):
                proportion = True
                x1, x2 = 2/5, 4/5
                y1, y2 = 1/segment_num, 1/segment_num
            else:
                proportion = False
                x1, x2 = plusButton.x, minusButton.x
                y1, y2 = plusButton.y + plusButton.height * 2, minusButton.y + minusButton.height * 2
            plusButton = ImgButton(self, self.ButtonImg["plus"], img_size, x1, y1, proportion)
            minusButton = ImgButton(self, self.ButtonImg["minus"], img_size, x2, y2, proportion)
            self.trade_list[self.resources[i]] = {}
            self.trade_list[self.resources[i]]["buttons"] = {"plus":plusButton, "minus":minusButton}

        label = None
        for i in range(resources_num):
            if (i == 0):
                proportion = True
                x = 3/5
                y = 1/segment_num
            else:
                proportion = False
                x = label.x
                y = label.y + img_size * 2
            label = Label(self, '0', BLACK, 20, x, y, proportion)
            self.trade_list[self.resources[i]]["label"] = label

    def remove_trade_ui(self):
        for resource in self.trade_list:
            self.trade_list[resource]["buttons"]["plus"].remove()
            self.trade_list[resource]["buttons"]["minus"].remove()
            self.trade_list[resource]["label"].remove()
        del self.trade_list
        del self.infos
        pygame.draw.rect(self.surface, LIGHTBLUE, (0, 0, self.width, self.height), border_radius=30)
        self.update()

    ######################################## "Build Type Methods" ############################################
    def add_build_type_ui(self):
        CostList = {
            "settlement": {"lumber": 1, "brick": 1, "wool": 1, "grain": 1},
            "city"      : {"grain": 2, "ore": 3},
            "road"      : {"lumber":1, "brick":1},
            "devCard"   : {"wool":1, "grain":1, "ore":1}
        }
        display_titles = {"Road":"road", "Settlement":"settlement", "City":"city", "Development":"devCard"}
        titile_names = ["Road", "Settlement", "City", "Development"]
        segment_num = len(CostList) + 2
        border_width = 2
        img_size = 25
        gap_width = 0.5 * img_size
        gap_height = self.height / segment_num
        for i in range(segment_num - 1):
            left_point = ( border_width , (self.height-border_width) * (i+1) / segment_num)
            right_point = (self.width - border_width, (self.height-border_width) * (i+1) / segment_num)
            pygame.draw.aaline(self.surface, BLACK, left_point, right_point)
            curr_y = (self.height-border_width) * (i) / segment_num
            if (i == 0):
                Label(self, "BUILD COSTS", BLACK, 20, 1/2, 1/(segment_num + 8))
            else:
                title_name = titile_names[i-1]
                label = Label(self, title_name, BLACK, 20, left_point[0] + border_width, curr_y, False)
                if i == segment_num - 2:
                    buy_button_height = floor(gap_height*2/3)
                    self.main_button["Buy"] = ImgButton(self, self.ButtonImg["buy"], buy_button_height, x= label.x + label.width + gap_width, y=curr_y+buy_button_height/4, proportion=False)
                curr_y += gap_height/2 - img_size/2
                total_num = sum(list(CostList[display_titles[title_name]].values()))
                curr_x = self.width - total_num * (img_size + gap_width)
                for resource in list(CostList[display_titles[title_name]].keys()):
                    for num in range(CostList[display_titles[title_name]][resource]):
                        image = pygame.image.load(ImageResource[resource]).convert_alpha()
                        image = pygame.transform.scale(image, (img_size, img_size))
                        self.surface.blit(image, (curr_x, curr_y))
                        curr_x += (img_size + gap_width)
        self.update()

    def remove_build_type_ui(self):
        pygame.draw.rect(self.surface, LIGHTBLUE, (0, 0, self.width, self.height), border_radius=30)
        self.update()

    ######################################## "ERROR Type Methods" ############################################
    def add_error_ui(self):
        pass

    def remove_error_ui(self):
        del self.prev_type
        del self.label
        pygame.draw.rect(self.surface, LIGHTBLUE, (0, 0, self.width, self.height), border_radius=30)
        self.update()




