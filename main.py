from dungeon  import*
from screen import *
from entity import *
screen=new_screen()   
new_dungeon=dungeon(screen)
new_build = building_blocks("me",0,0,0,0,0,0,0,0,0,0,0,0,0,0)
def hi(message):
    print(message)
new_dungeon.initiate_dungeon()
screen.display_current_rects(new_dungeon.floors[new_dungeon.currentfloor].list_of_rect)
new_dungeon.add_func(new_build.search,"search")
while True:
    new_dungeon.checker()
    new_dungeon.key(("search",""),pygame.K_f,args=((new_dungeon.floors[new_dungeon.currentfloor]),""))
    screen.display_current_rects(new_dungeon.floors[new_dungeon.currentfloor].list_of_rect)
    screen.update()
    screen.screen.fill((0,0,0))
    screen.fps.tick(60)
    player=new_dungeon.floors[new_dungeon.currentfloor].get_relevant_keys()