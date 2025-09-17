import pygame,sys
from pygame.locals import *
import random
import time
pygame.init()
# dimensions = pygame.display.get_desktop_sizes()
# dimensions = (int(dimensions[0][0]/36)*36,int(dimensions[0][1]/36)*36)
dimensions = pygame.display.get_desktop_sizes()[0]

class new_screen(object):
    def __init__(self,isscreen=False): 
        dimensions=(1080,1080)
        self.dimensions = pygame.display.get_desktop_sizes()[0]
        if isscreen:
            self.screen = pygame.display.set_mode(dimensions)
        else:
            self.screen=None
        self.fps = pygame.time.Clock()
    def createScreen(self):
        self.screen = pygame.display.set_mode(dimensions)

    def display_current_rects(self,rect_list:list):
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
class block(object):
    def __init__(self,x_cord:int,y_cord:int,color:tuple,screen:new_screen,ocupation=None):
        self.is_wall=True
        self.x_cord=x_cord
        self.y_cord=y_cord
        self.y2=y_cord+24
        self.x2=x_cord+24
        self.color=color
        self.screen=screen
        self.ocupation=ocupation
        self.old_color= color
    def resetScreen(self, newScreen:new_screen):
        self.screen=newScreen
    def show(self):
        pygame.draw.rect(self.screen.screen,self.color,(self.x_cord,self.y_cord,24,24))



                    

    
