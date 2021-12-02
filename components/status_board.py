from label import *

class StatusBoard:
    Image = {
        "wool": "../resources/img/wool.png",
        "lumber": "../resources/img/lumber.png",
        "grain": "../resources/img/grain.png",
        "brick": "../resources/img/brick.png",
        "ore": "../resources/img/ore.png",
    }
    Color = {
        "wool": (76, 153, 0),
        "lumber": (153, 76, 0),
        "grain": (204, 102, 0),
        "brick": (178, 34, 34),  # (205, 92, 92),
        "ore": (160,160,160),  # (224,224,224),
    }
    def __init__(self, super_surface_object):
        self.super_surface_object = super_surface_object
        self.super_surface = super_surface_object.surface
        self.height = 50
        self.width = self.super_surface.get_width() * 0.3
        self.x = 20
        self.y = self.super_surface_object.main_board.y + self.super_surface_object.main_board.height + 20
        self.resources = {
            "lumber": 0,
            "brick": 0,
            "wool": 0,
            "grain": 0,
            "ore": 0,
        }
        self.resources_display = {}
        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill(LIGHTBLUE)

        self.draw_board()

    def draw_board(self):
        each_space_width = self.width / 5
        each_cell_width = each_space_width * 2/3
        each_gap_width = each_space_width * 1/6
        each_cell_height = self.height * 2/3

        recource_keys = list(self.resources.keys())
        for i in range(len(recource_keys)):
            resource = recource_keys[i]
            self.resources_display[resource] = {}
            image_label = pygame.image.load(self.Image[resource]).convert_alpha()
            image_label = pygame.transform.scale(image_label, (int(each_cell_height), int(each_cell_height)))
            pygame.pixelarray.PixelArray(image_label).replace(BLACK, self.Color[resource])
            imageRect = image_label.get_rect()
            img_surface = pygame.Surface((imageRect.width, imageRect.height))
            img_surface.blit(image_label, blit_position_transfer(img_surface, image_label))
            pygame.pixelarray.PixelArray(img_surface).replace(BLACK, self.Color[resource])
            img_surface.set_colorkey(TRASPARENT)
            self.resources_display[resource]["image"] = img_surface
            self.surface.blit(img_surface, blit_position_transfer(self.surface, img_surface, i/5 + 2/30, 1/2))
            self.resources_display[resource]["value"] = Label(self, str(self.resources[resource]), GRAY, 16, i/5 + 17/120, 1/2)
        self.update()

    def update(self):
        rect = self.super_surface.blit(self.surface, (self.x, self.y))
        pygame.display.update(rect)

    def hide(self):
        self.surface.fill(DARKSKYBLUE)
        self.update()

    def remove(self):
        self.hide()
        # del self

    def update_info(self):
        new_resources = self.super_surface_object.real_player.resources
        for resource in new_resources:
            if self.resources[resource] != new_resources[resource]:
                self.resources[resource] = new_resources[resource]
                if new_resources[resource] > 0:
                    color = BLACK
                else:
                    color = GRAY
                label = self.resources_display[resource]["value"]
                x, y = label.x, label.y
                label.remove()
                del label
                label = Label(self, str(new_resources[resource]), color, 16, x, y, False)
                self.resources_display[resource]["value"] = label


