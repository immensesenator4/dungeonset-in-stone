import random
from screen import*
class dungeon(object):
    def __init__(dungeon,x,y,screen):
        dungeon.floor= random.randint(3,7)
        dungeon.size=x*y
        dungeon.time=0
        dungeon.max_time= random.randint(dungeon.size*4,dungeon)
        dungeon.floors=[]
        dungeon.screen=screen
        dungeon.currentfloor=0

class floor(object):
    def __init__(self,screen:new_screen):
        list_of_rect=[]
        x_detirminer=random.randint(200,400)
        y_detirminer=(random.randint(200,400))
        for y in range(0,y_detirminer):
            temp_list=[]
            for x in range(0,x_detirminer):
                temp_list.append(block(x*24,y*24,(0,0,0),screen))
            list_of_rect.append(temp_list)
            self.list_of_rect=list_of_rect
        for y in range(0,len(self.list_of_rect)):
            for x in range(0,len(list_of_rect[y])):
                self.list_of_rect[y][x].old_color=(10,70,90)
        self.wall_demolisher(x_detirminer,y_detirminer) 
        self.screen=screen
        self.functions={}
    def see_radious(self,new_pos,radius):
        flat_var=0-radius
        new_posy=self.find_listnumswith(new_pos)[0]
        newposx=self.find_listnumswith(new_pos)[1]
        for y in range(flat_var,radius):
            for x in range(flat_var,radius):
            
                self.list_of_rect [new_posy+y] [newposx+x].color=self.list_of_rect [new_posy+y] [newposx+x].old_color
    def find_listnums(self,player):
        relevant_info=self.screen.get_relevant_info(self.list_of_rect)
        for i in range(0,len(relevant_info)):
            for x in range(0,len(relevant_info[i])):
                if relevant_info[i][x]== player:
                    return [i,x]
    def find_listnumswith(self,player):
        
        for i in range(0,len(self.list_of_rect)):
            for x in range(0,len(self.list_of_rect[i])):
                if self.list_of_rect[i][x]== player:
                    return [i,x]
    def change_player_pos(self,old_pos,new_pos):
            old_posy=self.find_listnumswith(old_pos)[0]
            oldposx=self.find_listnumswith(old_pos)[1]
            self.list_of_rect [old_posy] [oldposx].color=self.list_of_rect [old_posy] [oldposx].old_color
            self.list_of_rect [self.find_listnumswith(new_pos)[0]][self.find_listnumswith(new_pos)[1]].color=(10,90,70)

    def get_relevant_keys(self,player): 
        events = pygame.event.get()
        key = pygame.key.get_pressed() 
        
                
        if key[pygame.K_w]: 
            temp_anew=self.screen.get_relevant_info(self.list_of_rect)[abs(self.find_listnums(player)[0]-1)][self.find_listnums(player)[1]]
            if temp_anew.is_wall== False:
                self.see_radious(player,5)
                self.change_player_pos(player,temp_anew)
                self.move((player.x_cord,player.y_cord),(temp_anew.x_cord,temp_anew.y_cord))
                player = temp_anew

        if key[pygame.K_s]:
            temp_anew=self.screen.get_relevant_info(self.list_of_rect)[self.find_listnums(player)[0]+1][self.find_listnums(player)[1]]
            if temp_anew.is_wall== False:
                self.see_radious(player,5)
                self.change_player_pos(player,temp_anew)
                self.move((player.x_cord,player.y_cord),(temp_anew.x_cord,temp_anew.y_cord))
                player = temp_anew
            
        if key[pygame.K_a]:
            temp_anew=self.screen.get_relevant_info(self.list_of_rect)[self.find_listnums(player)[0]][abs(self.find_listnums(player)[1]-1)]
            if temp_anew.is_wall== False:
                self.see_radious(player,5)
                self.change_player_pos(player,temp_anew)
                self.move((player.x_cord,player.y_cord),(temp_anew.x_cord,temp_anew.y_cord))
                player= temp_anew
            
        if key[pygame.K_d]:
            temp_anew=self.screen.get_relevant_info(self.list_of_rect)[self.find_listnums(player)[0]][self.find_listnums(player)[1]+1]
            if temp_anew.is_wall== False:
                self.see_radious(player,5)
                self.change_player_pos(player,temp_anew)
                self.move((player.x_cord,player.y_cord),(temp_anew.x_cord,temp_anew.y_cord))
                player = temp_anew
                        
        return player
    def key(self,functions:tuple,*keys:int,args:tuple=()):
        events = pygame.event.get()
        key = pygame.key.get_pressed()
        count=0
        for ifstatement in keys:
            if key[ifstatement]and len(args)>0 :
                 self.functions[functions[count]](args[count])
            elif key[ifstatement]:
                self.functions[functions[count]]()
            count+=1
    def add_func(Self,new_func,name:str):
        Self.functions[name]=new_func
    def move(self,cord1:tuple,cord2:tuple):
        
        tupleofdestiny=[]
        for i in range(0,len(cord1)):
            tupleofdestiny.append(cord1[i]-cord2[i])
    
        for y in range(0,len(self.list_of_rect)):
            for x in range(0,len(self.list_of_rect[y])):
                
                    
                    
                self.list_of_rect[y][x].x_cord+=tupleofdestiny[0]
                self.list_of_rect[y][x].x2+=tupleofdestiny[0]
                    
                
                        
                self.list_of_rect[y][x].y_cord+=tupleofdestiny[1]
                self.list_of_rect[y][x].y2+=tupleofdestiny[1]
    def wall_demolisher(self,x_s:int,y_s:int):
        x=int(dimensions[0]/48)
        y=int(dimensions[1]/48)
        self.list_of_rect[abs(y)-1][abs(x)-1].is_wall=False
        self.list_of_rect[abs(y)-1][abs(x)-1].old_color=(50,70,100)
        self.list_of_rect[abs(y)-1][abs(x)-1].ocupation="down floor"
        size = int((x_s*y_s)/random.randint(4,16))
        while size!=0:
            s=random.randint(0,4)
            match s:
                case 0:
                    if y <0:
                        y+=1
                    else:
                        y-=1
                case 1:
                    if y>y_s-2:
                        y-=1
                    else:
                        y+=1
                case 2:
                    if x<=0:
                        x+=1
                    else:
                        x-=1
                case 3:
                    if x>x_s-2:
                        x-=1
                    else:
                        x+=1
            try:
                if self.list_of_rect[abs(y)][abs(x)].is_wall==True:
                        self.list_of_rect[abs(y)][abs(x)].is_wall=False
                        self.list_of_rect[abs(y)][abs(x)].old_color=(90,70,10)
                        size-=1
                        if size <=0:
                            self.list_of_rect[abs(y)][abs(x)].old_color=(10,100,70)
                            self.list_of_rect[abs(y)][abs(x)].ocupation="down floor"
            except:
                    print(y,len(self.list_of_rect))

                    time.sleep(1)