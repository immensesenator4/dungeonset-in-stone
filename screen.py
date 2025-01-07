import pygame,sys
from pygame.locals import *
import random
import time
import keyboard
pygame.init()
# dimensions = pygame.display.get_desktop_sizes()
# dimensions = (int(dimensions[0][0]/36)*36,int(dimensions[0][1]/36)*36)
dimensions = pygame.display.get_desktop_sizes()[0]

class new_screen:
    def __init__(self): 
        dimensions=(1080,1080)
        dimensions = pygame.display.get_desktop_sizes()[0]
        self.screen = pygame.display.set_mode(dimensions)
        self.fps = pygame.time.Clock()
    def display_current_rects(self,rect_list:list,player):
        relevant_info=self.get_relevant_info(rect_list)
        for sub in relevant_info:
            for list in sub:
                list.show()
    def update(self):
        pygame.display.update()
    def get_relevant_info(self,rect:list):
        relevant_info=[]
        for i in range(0,len(rect)):
            temp_relevant_info=[]
            for list in rect[i]:
                if (list.x_cord>=0 and list.y_cord>=0) and (list.x2<=dimensions[0] and list.y2<=dimensions[1]):
                    temp_relevant_info.append(list)
            
            if len(temp_relevant_info) != 0:
                relevant_info.append(temp_relevant_info)
            
                
        return relevant_info
    def get_mouse(self,rect:list,player):
        relevant_info = self.get_relevant_info(rect)
        pos= pygame.mouse.get_pos()
        for list in relevant_info:
            for z in list:
                if z[0][0] <= pos[0]<=z[1][0]and z[0][1]<= pos[1] <= z[1][1]:
                    if pos[0]>=player[0][0]-23 and player[1][0]+24>=pos[0]and  pos[1]>=player[0][1]-23 and player[1][1]+24>=pos[1] and not(z==player)and False in z:
                        
                        return True,z
                    else:
                        return False,z
        return False,player
class block:
    screen=new_screen
    def __init__(self,x_cord:int,y_cord:int,color:tuple,screen:new_screen,ocupation=None):
        self.is_wall=True
        self.x_cord=x_cord
        self.y_cord=y_cord
        self.y2=y_cord+24
        self.x2=x_cord+24
        self.color=color
        self.screen=screen
    def show(self):
        pygame.draw.rect(self.screen.screen,self.color,(self.x_cord,self.y_cord,24,24))

class floor():
    def __init__(self,screen:new_screen):
        list_of_rect=[]
        x_detirminer=random.randint(200,400)
        y_detirminer=(random.randint(200,400))
        for y in range(0,y_detirminer):
            temp_list=[]
            for x in range(0,x_detirminer):
                temp_list.append(block(x*24,y*24,(10,70,90),screen))
            list_of_rect.append(temp_list)
            self.list_of_rect=list_of_rect
        self.wall_demolisher(x_detirminer,y_detirminer) 
        self.screen=screen
        self.functions={}
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
            self.list_of_rect [self.find_listnumswith(old_pos)[0]][self.find_listnumswith(old_pos)[1]].color=(90,70,10)
            self.list_of_rect [self.find_listnumswith(new_pos)[0]][self.find_listnumswith(new_pos)[1]].color=(10,90,70)

    def get_relevant_keys(self,player): 
        key = pygame.key.get_pressed() 

                
        if key[pygame.K_w]: 
            temp_anew=self.screen.get_relevant_info(self.list_of_rect)[abs(self.find_listnums(player)[0]-1)][self.find_listnums(player)[1]]
            if temp_anew.is_wall== False:
                self.change_player_pos(player,temp_anew)
                self.move((player.x_cord,player.y_cord),(temp_anew.x_cord,temp_anew.y_cord))
                player = temp_anew

        if key[pygame.K_s]:
            temp_anew=self.screen.get_relevant_info(self.list_of_rect)[self.find_listnums(player)[0]+1][self.find_listnums(player)[1]]
            if temp_anew.is_wall== False:
                self.change_player_pos(player,temp_anew)
                self.move((player.x_cord,player.y_cord),(temp_anew.x_cord,temp_anew.y_cord))
                player = temp_anew
            
        if key[pygame.K_a]:
            temp_anew=self.screen.get_relevant_info(self.list_of_rect)[self.find_listnums(player)[0]][abs(self.find_listnums(player)[1]-1)]
            if temp_anew.is_wall== False:
                self.change_player_pos(player,temp_anew)
                self.move((player.x_cord,player.y_cord),(temp_anew.x_cord,temp_anew.y_cord))
                player= temp_anew
            
        if key[pygame.K_d]:
            temp_anew=self.screen.get_relevant_info(self.list_of_rect)[self.find_listnums(player)[0]][self.find_listnums(player)[1]+1]
            if temp_anew.is_wall== False:
                self.change_player_pos(player,temp_anew)
                self.move((player.x_cord,player.y_cord),(temp_anew.x_cord,temp_anew.y_cord))
                player = temp_anew
                        
        return player
    def key(self,functions:tuple,*keys:int):
        key = pygame.key.get_pressed()
        count=0
        for ifstatement in keys:
            if key[ifstatement]:
                self.functions[functions[count]]
            count+=1
    def add_func(Self,new_func,name:str):
        Self.functions[name]=new_func()
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
        x=0
        y=0
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
                        self.list_of_rect[abs(y)][abs(x)].color=(90,70,10)
                        size-=1
            except:
                    print(y,len(self.list_of_rect))

                    time.sleep(1)

                    

    
