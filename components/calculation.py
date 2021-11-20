cursor_state = "normal"
def blit_position_transfer(surface1, surface2, x = 1/2, y = 1/2):
    new_x = surface1.get_width()*x - surface2.get_width()/2
    new_y = surface1.get_height()*y - surface2.get_height()/2
    return (new_x, new_y)
