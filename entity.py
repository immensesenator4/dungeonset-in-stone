import pygame, sys
#  dungeon in stone 
from argparse import Action
import time
import random
from dungeon import*
from screen import*
class building_blocks(object):
    def __init__(build,name:str,cons:int,musclemass:int,muscle_density:int,teq:int,bonedensity:int,magic_pow:int,magic_teq:int,height:int,will_power:int,likability:int,visualacuity:int,bloodensity:int,motor_control:int, hand_eye_cordination:int) -> None:                                                      
        build.x=0
        build.y=0
        build.tile =6
        build.bloodensity=bloodensity
        build.visualacuity=visualacuity
        build.will_power = will_power
        build.motor_control = motor_control
        build.hand_eye_cordination=hand_eye_cordination
        build.magic_pow=magic_pow
        build.magicteq = magic_teq
        build.likability=likability
        build.height=height
        build.charisma=will_power+likability
        build.magic = build.magic_pow*build.magicteq
        build.bonedensity= bonedensity
        build.defense = (bonedensity/2)+(0.05*musclemass)
        build.mucslemass=musclemass
        build.muscle_density=muscle_density
        build.strength=musclemass*muscle_density
        build.equipweight=0
        build.dex = build.motor_control*build.hand_eye_cordination
        build.cons=cons
        build.teq=teq
        build.max_hp=build.cons*2
        build.hp = build.max_hp
        build.weight = (build.cons/10)+(build.strength*0.35)*((height/(72)))
        build.carrycapacity = build.weight*2
        build.equipbonus=0
        build.attack= ((build.strength+build.equipbonus)*build.teq)*0.05
        build.hunger=100
        build.thirst=100
        build.damage=0
        build.vision = visualacuity
        build.blood=100
        build.max_stamina= build.blood*bloodensity
        build.stamina= build.max_stamina
        build.regenration = 0.0001*build.max_hp
        build.dodge = build.dex/100
        build.time = 0
        build.damage_reduction=1
        build.ingury = None
        build.enemy_list=[]
        build.name=name
    def __str__(build):
        return f"hp {build.hp}/{build.max_hp}, {build.name}"
    def get_enemies(build):
        for enemy in build.enemy_list:
            print(enemy,end=" ")
    def damage_action(build):
        print("you have",len(build.enemy_list),"amount of enemies chose 1",end=" ")
        build.get_enemies()
        print()
        target=int(input())-1
        print(build.enemy_list[target])
        build.enemy_list[target].damage+=build.attack
        print(build.enemy_list[0].damage)
        pass
    def ingurystate(build):
        if build.hp<= build.max_hp*25/100:
            return "heavy"
        elif build.hp<= build.max_hp*50/100:
            return "moderate"
        elif build.hp<= build.max_hp*75/100: 
            return"medium"
        elif build.hp<build.max_hp*99.9/100:
            return "light"
        else:
            return "healthy"
    def action(build,reaction):
        deffend=False
        Dodge= False
        build.hp += build.regenration
        if build.hp>build.max_hp:
            build.hp=build.max_hp
        if reaction == "sleep":
            slider =0
            if build.ingury == True:
                build.hp +=slider*(build.max_hp*0.10)/4
                build.stamina+= (build.max_stamina*0.1)/4
            else:
                build.hp +=slider*(build.max_hp*0.10)
                build.stamina+= slider*(build.max_stamina*0.1)
        elif reaction == "movement":
            build.time+=3
            direction = input()
            if direction == "right":
                build.y+=6
            elif direction == "left":
                build.y-=6
            elif direction == "down":
                build.x+=6
            elif direction:
                build.x -= 6
        elif reaction == "attack":
            #damage
            build.damage_action()
            build.time+=6
            pass
        elif reaction =="defend":
            pass
            build.time+=6
            deffend=True
            #halvez damage b4 armor reduction
        elif reaction == "search":
            build.time+=12
            #4tiles wide a 2x2 tile behind me 3x4 tile to the side and a 4x4 tile infront of me around me  halved search radious 1/4 if severe
            pass
        elif reaction == "dodge":
            build.time+=6
            chance = random.randint(0,100)/100

            if build.dodge>=chance:
                Dodge=True
                print("success")
            
        elif reaction == "loot":
            build.time+=30
        else:
            build.time+=6
        build.dodged(Dodge)
        build.defend(deffend)
        build.take_damage()
        build.injury_intpreteter()
    def injury_intpreteter(build):
        build.injury = build.ingurystate()
    def action_economy(build,action):
        
        if build.time<=0:
            build.action(action)
        else:
            build.time-=6
        
    def defend(build,affector):
        if affector:
            build.damage/=2
        build.damage*= build.damage_reduction
        build.damage-=build.defense
    def dodged(build,affector):
        if affector == True:
            build.damage=0
    def take_damage(build):
        build.hp-=build.damage
        build.damage=0
    def search(build,floor:floor):
        
        for y in range(0,len(floor.list_of_rect)):
            for x in range(0,len(floor.list_of_rect[y])):
                floor.list_of_rect[y][x].color=floor.list_of_rect[y][x].old_color
    def add_time(build,dungeon):
        dungeon.time+=build.time
        build.time=0
class Player(building_blocks):
    def __init__(play,name, cons, musclemass, muscle_density, teq, bonedensity, magic_pow, magic_teq, height, will_power, likability, visualacuity, bloodensity, motor_control, hand_eye_cordination,level) -> None:
        super().__init__(name,cons, musclemass, muscle_density, teq, bonedensity, magic_pow, magic_teq, height, will_power, likability, visualacuity, bloodensity, motor_control, hand_eye_cordination)
        #add difent spawn for barb in the dungeon
        play.essance = {}
        play.level=level
        play.active_skills = {}
        play.skill_level = {}
        play.magic_skills={}
        play.magic_skill_level ={}
        play.passive_skills={}

class Barbarian(Player):
    def __init__(barb, name, cons, musclemass, muscle_density, teq, bonedensity, magic_pow, magic_teq, height, will_power, likability, visualacuity, bloodensity, motor_control, hand_eye_cordination, level) -> None:
        super().__init__(name,cons, musclemass, muscle_density, teq, bonedensity, magic_pow, magic_teq, height, will_power, likability, visualacuity, bloodensity, motor_control, hand_eye_cordination, level)
        barb.defense+=(1/4*barb.cons)
        barb.active_skills_list =[]
        barb.passive_skills_list=[]
        barb.active_skills["agro"] = "enmies atrget u*"
        barb.passive_skills["endure"]=":damage reduced by 1%"
    def ingurystate(barb):
        if barb.hp<=barb.max_hp*0.25:
            return "heavy"
        else:
            return "healthy"
    def leveler(barb):
        barb.cons+=10
        barb.dex+=10
        barb.will_power+=10
        barb.strength+=20
        barb.charisma=barb.will_power+barb.likability
        barb.max_hp=barb.cons*2
        barb.hp = barb.max_hp
        barb.weight = (barb.cons/10)+(barb.strength*0.35)*(barb.height/72)
        barb.carrycapacity = barb.weight*2
        barb.equipbonus=0
        barb.hunger=100
        barb.thirst=100
        barb.damage=0
        barb.blood=100
        barb.stamina= barb.max_stamina
        barb.regenration = 0.0001*barb.max_hp
        barb.dodge = barb.dex/1000
        barb.attack= ((barb.strength+barb.equipbonus)*barb.teq)*0.05
        barb.defense+=(1/4*barb.cons)
       
    
class Explorer(Player):
    def __init__(expl,name, cons, musclemass, muscle_density, teq, bonedensity, magic_pow, magic_teq, height, will_power, likability, visualacuity, bloodensity, motor_control, hand_eye_cordination, level) -> None:
        super().__init__(name,cons, musclemass, muscle_density, teq, bonedensity, magic_pow, magic_teq, height, will_power, likability, visualacuity, bloodensity, motor_control, hand_eye_cordination, level)#double expllloreres passive search radous and search radius  and make it so theyu can see obsticles
class Mage(Player):
    pass
class Fighter(Player):
    pass
class Rogue(Player):
    pass
class spirit_Mage(Player):
    pass
class spirit_warrior(Player):
    pass
