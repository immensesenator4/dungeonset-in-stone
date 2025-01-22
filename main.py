from dungeon  import*
from screen import *
from entity import *
from host import Host
from client import client
s=input("host client or none")

if s=="host":
    h=Host(2,23)
    screen=new_screen()   
    new_dungeon=dungeon(screen)
    h.store_obj(screen,"screen")
    h.store_obj(new_dungeon,"dungeon")
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
        new_dungeon.floors[new_dungeon.currentfloor].time=new_dungeon.add_time(new_dungeon.floors[new_dungeon.currentfloor].time)
        on=new_dungeon.time_checker()
elif s == "client":
    c=client(23)
    new_dungeon=c.receive_obj("dungeon",dungeon,{"screen":pygame.display.set_mode(pygame.display.get_desktop_sizes()[0]),"fps":pygame.time.Clock()})
    new_build = building_blocks("me",0,0,0,0,0,0,0,0,0,0,0,0,0,0)
    def hi(message):
        print(message)
    screen=new_dungeon.screen
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
        new_dungeon.floors[new_dungeon.currentfloor].time=new_dungeon.add_time(new_dungeon.floors[new_dungeon.currentfloor].time)
        on=new_dungeon.time_checker()

else:
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
        new_dungeon.floors[new_dungeon.currentfloor].time=new_dungeon.add_time(new_dungeon.floors[new_dungeon.currentfloor].time)
        on=new_dungeon.time_checker()
    