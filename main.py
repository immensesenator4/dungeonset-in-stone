from dungeon  import*
from screen import *
from entity import *
screen=new_screen()   
new_dungeon=dungeon(screen)
new_build = building_blocks("me",0,0,0,0,0,0,0,0,0,0,0,0,0,0)
def hi(message):
    print(message)
screen.display_current_rects(new_dungeon.floors[new_dungeon.currentfloor].list_of_rect)
new_dungeon.add_func(new_build.search,"search")
new_dungeon.add_func(new_dungeon.add_time,"time")
on=True
while on:
    new_dungeon.checker()
    new_dungeon.key(("search","time"),pygame.K_f,pygame.K_f,args=((new_dungeon.floors[new_dungeon.currentfloor]),(30)))
    screen.display_current_rects(new_dungeon.floors[new_dungeon.currentfloor].list_of_rect)
    screen.update()
    screen.screen.fill((0,0,0))
    screen.fps.tick(60)
    player=new_dungeon.floors[new_dungeon.currentfloor].get_relevant_keys()
    new_build.time=new_dungeon.add_time(0)
    on=new_dungeon.time_checker()
    