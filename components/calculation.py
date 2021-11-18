cursor_state = "normal"
def blit_position_transfer(surface1, surface2, x = 1/2, y = 1/2):
    centerx = surface1.get_width()*x - surface2.get_width()/2
    centery = surface1.get_height()*y - surface2.get_height()/2
    return (centerx, centery)