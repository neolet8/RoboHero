"""
University of Helsinki Advanced Course in Programming (Python MOOC 2023)
Final project, by Gözdenur Demir, 16 Oct 2023
"""
import pygame,random

class Sprite:
    def __init__(self, spname: str, xc: int, yc: int, image:str, speed:int):
        self.spname = spname
        self.xc = xc
        self.yc = yc
        self.image=image
        self.dir=1
        self.speed=speed

    def move_sprite(self):
        self.xc+=self.dir*self.speed
        if self.xc>=600:
            self.dir=-1
        if self.xc<=0:
            self.dir=1

    def __str__(self):
        return f"{self.spname},{self.xc},{self.yc},{self.image}, Speed:{self.speed}"

class Coin:
    def __init__(self, coname: str, xc: int, yc: int, image:str):
        self.coname = coname
        self.xc = xc
        self.yc = yc
        self.image=image

class Robo:
    def __init__(self, roname: str, xc: int, yc: int, image:str):
        self.roname = roname
        self.xc = xc
        self.yc = yc
        self.image=image

class RoboHero:
    def __init__(self):
        pygame.init()
        self.to_right=False
        self.to_left=False
        self.to_up=False
        self.to_down=False
        self.height=480
        self.width=640
        self.score=0
        self.move_robot=True
        self.d=2
        self.princess=False
        self.no_touch=True
        self.window=pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("RoboHero")

        self.make_robot()
        self.make_sprite()
        self.make_coin()
        self.main_loop()

    def main_loop(self):
        while True:
          self.draw_window()
          self.check()

    def make_robot(self):
        x=self.width/2-pygame.image.load("robot.png").get_width()/2
        y=self.height-pygame.image.load("robot.png").get_height()
        self.robot=Robo("Robo",x,y,"robot.png")

    def make_sprite(self):
        self.k=None
        self.sprite_gang=[]
        for i in range(3):
            self.k=(Sprite(f"Sprite{i}",random.randint(0,600),random.randint(5,self.height-150),"monster.png",random.randint(1,10)))
            self.sprite_gang.append(self.k)
        return self.sprite_gang

    def make_coin(self):
        self.km=None    
        self.treasure=[]
        for i in range(12):
            self.km=(Coin(f"Gold{i}",random.randint(0,600),random.randint(20,self.height-60),"coin.png"))
            self.treasure.append(self.km)
        return self.treasure

    def check(self):
        for event in pygame.event.get():
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_LEFT:
                    self.to_left=True
                if event.key==pygame.K_RIGHT:
                    self.to_right=True
                if event.key==pygame.K_UP:
                    self.to_up=True
                if event.key==pygame.K_DOWN:
                    self.to_down=True
                if event.key==pygame.K_F2:
                    RoboHero()
                if event.key==pygame.K_ESCAPE:
                    quit()  

            if event.type==pygame.KEYUP:
                if event.key==pygame.K_LEFT:
                    self.to_left=False
                if event.key==pygame.K_RIGHT:
                    self.to_right=False
                if event.key==pygame.K_UP:
                    self.to_up=False
                if event.key==pygame.K_DOWN:
                    self.to_down=False
            if event.type==pygame.QUIT:
                exit()

        if self.move_robot:
            if self.to_right:
                self.move(2,0)
            if self.to_left:
                self.move(-2,0)
            if self.to_up:
                self.move(0,-2)
            if self.to_down:
                self.move(0,2)
                
            if self.robot.xc+pygame.image.load(self.robot.image).get_width()>=self.width:
                self.to_right=False
                self.robot.xc=self.width-pygame.image.load(self.robot.image).get_width()
            if self.robot.xc<=0:
                self.to_left=False
                self.robot.xc=0
            if self.robot.yc<=0:
                self.to_up=False
                self.robot.yc=0
            if self.robot.yc+pygame.image.load(self.robot.image).get_height()>=self.height:
                self.to_down=False
                self.robot.yc=self.height-pygame.image.load(self.robot.image).get_height()

    def move(self, movex, movey):
        self.robot.xc=self.robot.xc+movex
        self.robot.yc=self.robot.yc+movey
        if movey==0:
            return self.robot.xc
        if movex==0:
            return self.robot.yc

    def draw_window(self):
        wd=pygame.image.load(self.robot.image).get_width()
        hd=pygame.image.load(self.robot.image).get_height()
        self.window.fill((100,100,100))
        door=pygame.image.load("door.png")
        self.window.blit(door,(self.width/2-door.get_width()/2,12))
        self.window.blit(pygame.image.load(self.robot.image),(self.robot.xc, self.robot.yc))
        
        pygame.draw.rect(self.window, (0,0,0), (0, 6, self.width, 20))
        pygame.draw.rect(self.window, (0,0,0), (0, 30, self.width/2-16, 40))
        pygame.draw.rect(self.window, (0,0,0), (self.width/2+16, 30, self.width, 40))
        
        game_font = pygame.font.SysFont("Arial", 18, bold=True, italic=False)
        game_font_2 = pygame.font.SysFont("Arial", 18, bold=True, italic=True)
        game_font_3 = pygame.font.SysFont("Arial", 24, bold=True, italic=False)

        for i in self.sprite_gang:
            self.window.blit(pygame.image.load(i.image), (i.xc, i.yc))
            if i.xc in range(int(self.robot.xc-int(wd/self.d)), int(self.robot.xc+int(wd/self.d))) and i.yc in range(int(self.robot.yc-int(hd/self.d)), int(self.robot.yc+int(hd/self.d))):
                self.no_touch=False
                self.move_robot=False
            if self.no_touch==True and not self.princess:
                i.move_sprite()
            
        if self.no_touch==False:
            pygame.draw.rect(self.window, (255,0,255), (self.width/2-120, self.height/2-5, self.width/2-75, self.height/2-200))
            warning=game_font_3.render("YOU LOST :( TRY AGAIN!", True, (0,0,0))
            self.window.blit(warning, (self.width/2-115,self.height/2))

        for j in self.treasure:
            self.window.blit(pygame.image.load(j.image), (j.xc, j.yc))  
            if j.xc in range(int(self.robot.xc-int(wd/self.d)), int(self.robot.xc+int(wd/self.d))) and j.yc in range(int(self.robot.yc-int(hd/self.d)), int(self.robot.yc+int(hd/self.d))):
                self.treasure.remove(j)
                self.score+=1

        if self.robot.xc in range(int(self.width/2-int(door.get_width()/2)),int(self.width/2+int(door.get_width()/2))) and self.robot.yc in range(0,20) :
            warning2=game_font_3.render("YOU SAVED THE PRINCESS!<3", True, (255, 0, 255))
            self.move_robot=False
            self.window.blit(warning2, (self.width/2-150,self.height/2))
            warning2=game_font_3.render(f"Total score: {self.score} ", True, (255, 0, 255))
            self.window.blit(warning2, (self.width/2-70,self.height/2+50))
            self.princess=True

        if not self.princess:
            text= game_font.render(f"score: {self.score}  ", True, (255,255,255))
            self.window.blit(text, (565,5))
            text2= game_font_2.render(f"save the princess", True, (255, 0, 255))
            self.window.blit(text2, (self.width/2-63,5))

        game_text=game_font.render("F2=new game",True,(255,255,0))
        self.window.blit(game_text,(110,30))

        game_text=game_font.render("Esc=exit game", True,(255,255,0))
        self.window.blit(game_text,(430,30))
        pygame.display.flip()
    
if __name__=="__main__":
    RoboHero()
