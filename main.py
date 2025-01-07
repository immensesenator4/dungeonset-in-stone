import screen as s
screen=s.new_screen()   
new_floor=s.floor(screen)
def hi(message):
    print(message)
player = new_floor.list_of_rect[int(s.dimensions[1]/48)][int(s.dimensions[0]/48)]
screen.display_current_rects(new_floor.list_of_rect,player)
new_floor.add_func(hi,"hi")
while True:
    new_floor.key(("hi",""),s.pygame.K_f,args=(("what"),""))
    screen.display_current_rects(new_floor.list_of_rect,player)
    screen.update()
    screen.screen.fill((0,0,0))
    screen.fps.tick(60)
    player=new_floor.get_relevant_keys(player)