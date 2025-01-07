import screen as s
screen=s.new_screen()   
new_floor=s.floor(screen)

player = new_floor.list_of_rect[int(s.dimensions[1]/48)][int(s.dimensions[0]/48)]
screen.display_current_rects(new_floor.list_of_rect,player)
while True:
    screen.display_current_rects(new_floor.list_of_rect,player)
    screen.update()
    screen.screen.fill((0,0,0))
    screen.fps.tick(60)
    player=new_floor.get_relevant_keys(player)