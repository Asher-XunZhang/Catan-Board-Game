def blit_position_transfer(surface1, surface2):
    centerx = surface1.get_width()/2 - surface2.get_width()/2
    centery = surface1.get_height()/2 - surface2.get_height()/2
    return (centerx, centery)