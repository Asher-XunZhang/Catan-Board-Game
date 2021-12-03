from label import *

class ScoreBoard:
    def __init__(self, super_surface_object):
        self.super_surface_object = super_surface_object
        self.super_surface = super_surface_object.surface
        self.height = 50
        self.width = self.super_surface.get_width() * 0.3
        self.x = 20
        self.y = 20
        self.player_list = self.super_surface_object.all_player_list
        self.player_display = {}
        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill(LIGHTBLUE)

        self.draw_board()

    def draw_board(self):
        length = len(self.player_list)
        for i in range(length):
            player = self.player_list[i]
            self.player_display[player] = Label(self, str(player.get_total_points()), player.color, 16, i/length + 17/120, 1/2)
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

    def update_info(self, player):
        if player in self.player_display:
            label = self.player_display[player]
            x, y = label.x, label.y
            label.remove()
            del label
            label = Label(self, str(player.get_total_points()), player.color, 16, x, y, False)
            self.player_display[player] = label