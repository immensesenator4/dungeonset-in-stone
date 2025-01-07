from dungeon  import*
from screen import *
from entity import *
screen=new_screen()   
new_floor=floor(screen)
new_build = building_blocks("me",0,0,0,0,0,0,0,0,0,0,0,0,0,0)
def hi(message):
    print(message)
player = new_floor.list_of_rect[int(dimensions[1]/48)][int(dimensions[0]/48)]
screen.display_current_rects(new_floor.list_of_rect,player)
new_floor.add_func(new_build.search,"search")
while True:
    new_floor.key(("search",""),pygame.K_f,args=((new_floor),""))
    screen.display_current_rects(new_floor.list_of_rect,player)
    screen.update()
    screen.screen.fill((0,0,0))
    screen.fps.tick(60)
    player=new_floor.get_relevant_keys(player)