import pygame
import os
import random
import asyncio

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0
pygame.display.set_caption("Scared of the dark")

MainMenuImage = pygame.image.load(os.path.join("Assets","MainMenuImage.png"))
HowToPlayImage = pygame.image.load(os.path.join("Assets","HowToPlayMenu.png"))
BackButtonImage = pygame.image.load(os.path.join("Assets","BackButton.png"))
PlayImage = pygame.image.load(os.path.join("Assets","PlayButton.png"))
HowToPlayButton = pygame.image.load(os.path.join("Assets","HowToPlayButton.png"))
PlayerImage = pygame.image.load(os.path.join("Assets","Player.png"))
SwitchSound = pygame.mixer.Sound(os.path.join("Assets","ClickedOnSwitch.wav"))
HitSound = pygame.mixer.Sound(os.path.join("Assets","Hit.wav"))
DeathTimer = 5 # In seconds
DoSomethingEvey = 5
Points = 0

RoomImage = pygame.image.load(os.path.join("Assets","RoomSOTD.png"))
kitchenDark = pygame.image.load(os.path.join("Assets","KitchenDark.png"))
livingRoomDark = pygame.image.load(os.path.join("Assets","LivingRoomDark.png"))
parentsRoomDark = pygame.image.load(os.path.join("Assets","ParentsRoomDark.png"))
hallwayDark = pygame.image.load(os.path.join("Assets","HallwayDark.png"))
kidsRoomDark = pygame.image.load(os.path.join("Assets","KidsRoomDark.png"))
SwitchSideways = pygame.image.load(os.path.join("Assets","SwitchSideWays.png"))
SwitchNotSideways = pygame.image.load(os.path.join("Assets","SwitchNotSideWays.png"))

CurrentState = "MainMenu"
def Respawn():
    global Points
    room.x = 0
    room.y = 0
    for i in theDark.RoomOn:
        theDark.RoomOn[i] = False
    switchKids.Pressed = 0
    switchParents.Pressed = 0
    switchHallway.Pressed = 0
    switchLive.Pressed = 0
    switchKitchen.Pressed = 0
    theDark.DoSomethingEveryCount = DoSomethingEvey
    player.DeathTimerCount = DeathTimer
    player.Hsp = 0
    player.Vsp = 0
    Points = 0
    HitSound.play()

# Check if you collide with a given object and add the offset to the offset so you can get an raycast effect (i guess?)
def collide(obj1, obj2, XPlus = 0, YPlus = 0):
    offset_x = obj2.x - obj1.x + XPlus
    offset_y = obj2.y - obj1.y + YPlus
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None
def Coldie(obj1,obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None
def DrawText(text,font,text_col,x,y,Scale):
    img = font.render(text,True,text_col)
    screen.blit(pygame.transform.scale_by(img,Scale),(x,y))

PointsFont = pygame.font.SysFont(None,30,bold = True,italic = True)

class Room():
    def __init__(self):
        self.mask = pygame.mask.from_surface(RoomImage)
        self.x = 0
        self.y = 0
        self.Image = pygame.image.load(os.path.join("Assets","RoomSOTDFloorTextures.png"))
    def Update(self):
        # Just Move everything to the player easy peasy
        self.x -= player.Hsp
        self.y -= player.Vsp
        screen.blit(self.Image,(self.x,self.y))
        screen.blit(RoomImage,(self.x,self.y))

def WhenInDarkDo(obj):
    obj.InDark = True
    obj.DeathTimerCount -= dt
class Player():
    def DarkShit(self):
        # You all are gonna hate me for what im gonna do now
        self.InDark = False
        if Coldie(kitchenDarkk,self):
            if theDark.RoomOn[0]:
                WhenInDarkDo(self)
        if Coldie(livingRomDarkk,self):
            if theDark.RoomOn[1]:
                WhenInDarkDo(self)
        if Coldie(hallwayDarkk,self):
            if theDark.RoomOn[2]:
                WhenInDarkDo(self)
        if Coldie(ParentsDark,self):
            if theDark.RoomOn[3]:
                WhenInDarkDo(self)
        if Coldie(kidsRoomDarkk,self):
            if theDark.RoomOn[4]:
                WhenInDarkDo(self)
        if self.InDark == False and self.DeathTimerCount < DeathTimer:
            self.DeathTimerCount += dt
        if self.DeathTimerCount < 0:
            Respawn()
        
    def FlipShit(self):
        if self.Vsp >= 1:
            screen.blit(self.Image, (self.x,self.y))
            self.CurrentFacing = self.Image
            self.PiorityDisplay = True
        if self.Vsp <= -1:
            screen.blit(self.ImageFlipY, (self.x,self.y))
            self.CurrentFacing = self.ImageFlipY
            self.PiorityDisplay = True
        if self.Hsp >= 1 and self.PiorityDisplay == False:
            screen.blit(self.ImageFlipX, (self.x,self.y))
            self.CurrentFacing = self.ImageFlipX
        if self.Hsp <= -1 and self.PiorityDisplay == False:
            screen.blit(self.ImageNotFlipX, (self.x,self.y))
            self.CurrentFacing = self.ImageNotFlipX
        if self.Vsp == 0 and self.Hsp == 0:
            screen.blit(self.CurrentFacing, (self.x,self.y))
        self.PiorityDisplay = False

    def __init__(self, StartPos):
        self.x = StartPos.x
        self.y = StartPos.y
        self.MoveSpeed = 300
        self.Hsp = 0
        self.Vsp = 0
        # Get the mask for pixel perfect collisions
        self.Image = PlayerImage
        self.ImageFlipX = pygame.transform.rotate(self.Image,90)
        self.ImageNotFlipX = pygame.transform.rotate(self.Image,-90)
        self.ImageFlipY = pygame.transform.flip(self.Image,0,1)
        self.mask = pygame.mask.from_surface(self.Image)
        self.DeathTimerCount = DeathTimer
        self.CurrentFacing = self.Image
        self.PiorityDisplay = False
    def Update(self, DT):
        keys = pygame.key.get_pressed()
        # Check keys
        KeyLeft = keys[pygame.K_a]
        KeyRight = keys[pygame.K_d]
        KeyUp = keys[pygame.K_w]
        KeyDown = keys[pygame.K_s]
        self.MoveX = int(KeyRight) - int(KeyLeft)
        self.MoveY = int(KeyDown) - int(KeyUp)

        # Take the MoveX/Y and multiply it by movespeed so it will return -/+MoveSpeed then multiply it by delta time so it will be the same dosent
        # matter how fast your pc is
        self.Hsp = (self.MoveX * self.MoveSpeed) * DT
        self.Vsp = (self.MoveY * self.MoveSpeed) * DT

        # Collisions
        # Check if the next position will collide with the room if it does you can only move 1 pixel per second till you get there
        if collide(room,self, self.Hsp,0):
            if collide(room,self, self.MoveX,0) == False:
                self.x += self.MoveX * DT
            self.Hsp = 0

        if collide(room,self, 0,self.Vsp):
            if collide(room,self, 0,self.Vsp) == False:
                self.y += self.MoveY * DT
            self.Vsp = 0
        
        self.DarkShit()
        self.FlipShit()
        
class KitchenDark():
    def __init__(self):
        self.x = room.x+2.029
        self.y = room.y
        self.mask = pygame.mask.from_surface(kitchenDark)
    def Update(self):
        self.x = room.x+2.029
        self.y = room.y
        if (theDark.RoomOn[0]):
            screen.blit(kitchenDark,(self.x,self.y))
class LivingRoomDark():
    def __init__(self):
        self.x = room.x+777.642
        self.y = room.y
        self.mask = pygame.mask.from_surface(livingRoomDark)
    def Update(self):
        if (theDark.RoomOn[1]):
            self.x = room.x+777.642-118
            self.y = room.y
            screen.blit(livingRoomDark,(self.x,self.y))
class HallwayDark():
    def __init__(self):
        self.x = room.x+2.029
        self.y = room.y+1072.699-150
        self.mask = pygame.mask.from_surface(hallwayDark)
    def Update(self):
        if (theDark.RoomOn[2]):
            self.x = room.x+2.029
            self.y = room.y+1072.699-146
            screen.blit(hallwayDark,(self.x,self.y))
class ParentsRoomDark():
    def __init__(self):
        self.x = room.x+2.029
        self.y = room.y+1597.699
        self.mask = pygame.mask.from_surface(parentsRoomDark)
    def Update(self):
        if (theDark.RoomOn[3]):
            self.x = room.x+2.029
            self.y = room.y+1597.699-224
            screen.blit(parentsRoomDark,(self.x,self.y))
class KidsRoomDark():
    def __init__(self):
        self.x = room.x+1026.500-160
        self.y = room.y+1597.699
        self.mask = pygame.mask.from_surface(kidsRoomDark)
    def Update(self):
        if (theDark.RoomOn[4]):
            self.x = room.x+1026.500-160
            self.y = room.y+1597.699-224
            screen.blit(kidsRoomDark,(self.x,self.y))
def SwitchThing(switch):
    global Points
    for i in theDark.RoomsShit:
        if i != switch.Num:
            if theDark.RoomsShit[i-1] > 0:
                switch.Pressed = 0
    if collide(switch,player):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_f] and switch.Pressed != 1 and theDark.RoomOn[switch.Num] == True:
            switch.Pressed += 1
            theDark.RoomOn[switch.Num] = False
            Points = Points
            Points += 1
            SwitchSound.play()
class SwitchKitchen():
    def __init__(self):
        self.x = room.x+1026.500-160
        self.y = room.y+1597.699
        self.Pressed = 0
        self.mask = pygame.mask.from_surface(SwitchSideways)
        self.Num = 0
    def Update(self):
        self.x = room.x+112.974-80
        self.y = room.y+920.571-180
        SwitchThing(self)
        screen.blit(SwitchSideways,(self.x,self.y))
class SwitchLive():
    def __init__(self):
        self.Pressed = 0
        self.x = room.x+2003.233
        self.y = room.y+852.500
        self.Image = SwitchSideways
        self.Image = pygame.transform.flip(self.Image,1,0)
        self.mask = pygame.mask.from_surface(self.Image)
        self.Num = 1
    def Update(self):
        self.x = room.x+2003.233-300
        self.y = room.y+852.500-210
        SwitchThing(self)
        screen.blit(self.Image,(self.x,self.y))
class SwitchHallway():
    def __init__(self):
        self.Pressed = 0
        self.x = room.x+1026.500-160
        self.y = room.y+1597.699
        self.Image = SwitchNotSideways
        self.Image = pygame.transform.flip(self.Image,0,1)
        self.mask = pygame.mask.from_surface(self.Image)
        self.Num = 2
    def Update(self):
        self.x = room.x+796.060-500
        self.y = room.y+1571.661-260
        SwitchThing(self)
        screen.blit(self.Image,(self.x,self.y))
class SwitchParents():
    def __init__(self):
        self.Pressed = 0
        self.x = room.x+1026.500-160
        self.y = room.y+1597.699
        self.mask = pygame.mask.from_surface(SwitchNotSideways)
        self.Num = 3
    def Update(self):
        self.x = room.x+796.060-100
        self.y = room.y+1671.540-270
        SwitchThing(self)
        screen.blit(SwitchNotSideways,(self.x,self.y))
class SwitchKids():
    def __init__(self):
        self.Pressed = 0
        self.x = room.x+1026.500-300
        self.y = room.y+1597.699
        self.Image = SwitchSideways
        self.Image = pygame.transform.flip(self.Image,1,0)
        self.mask = pygame.mask.from_surface(self.Image)
        self.Num = 4
    def Update(self):
        self.x = room.x+1997.040-300
        self.y = room.y+1989.421-300
        SwitchThing(self)
        screen.blit(self.Image,(self.x,self.y))

class TheDark():
    def __init__(self):
        #              Kitchen LiveRoom Hallway ParentsRoom KidsRoom
        self.RoomOn = [False,False,False,False,False]
        self.DoSomethingEveryCount = DoSomethingEvey
        self.PoopCount = 0
    def Update(self):
        self.RoomsShit = [switchKitchen.Pressed,switchLive.Pressed,switchHallway.Pressed,switchParents.Pressed,switchKids.Pressed]
        if self.DoSomethingEveryCount <= 0:
            random.random()
            if random.randint(0,100) < 80:
                # Choose Random Light to turn off
                self.DoSomethingEveryCount = DoSomethingEvey
                random.random()
                sex = random.randint(0,4)
                for i in self.RoomOn:
                    if self.RoomOn[i]:
                        self.PoopCount += 1
                if self.PoopCount <= 4:
                    while self.RoomOn[sex] == True:
                        random.random()
                        sex = random.randint(0,4)
                self.PoopCount = 0
                self.RoomOn[sex] = True
            else:
                # Black Out
                for i in self.RoomOn:
                    self.RoomOn[i] = False
        if self.DoSomethingEveryCount > 0:
            self.DoSomethingEveryCount -= dt

player = Player(pygame.Vector2((screen.get_width() / 2)-(PlayerImage.get_width() /2), screen.get_height() / 2))
room = Room()
theDark = TheDark()
kidsRoomDarkk = KidsRoomDark()
kitchenDarkk = KitchenDark()
livingRomDarkk = LivingRoomDark()
hallwayDarkk = HallwayDark()
ParentsDark = ParentsRoomDark()
switchKids = SwitchKids()
switchHallway = SwitchHallway()
switchLive = SwitchLive()
switchParents = SwitchParents()
switchKitchen = SwitchKitchen()

def CheckIfMouseHovering(X,Y,Image):
    MousePos = pygame.mouse.get_pos()
    if MousePos[0] < X+Image.get_width() and MousePos[0] > X:
        if MousePos[1] < Y+Image.get_height() and MousePos[1] > Y:
            return True
        else:
            return False
    else:
        return False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    MousePos = pygame.mouse.get_pos()
    screen.fill("purple")
    #Check if you started playing the game
    if CurrentState == "Play":
        theDark.Update()
        room.Update()
        player.Update(dt)
        switchParents.Update()
        switchHallway.Update()
        switchKids.Update()
        switchKitchen.Update()
        switchLive.Update()
        kidsRoomDarkk.Update()
        kitchenDarkk.Update()
        livingRomDarkk.Update()
        hallwayDarkk.Update()
        ParentsDark.Update()
        DrawText("Points " + str(Points),PointsFont,(0,0,0),0,0,3)
    if CurrentState == "MainMenu":
        screen.blit(MainMenuImage,(0,0))
        screen.blit(PlayImage,(850,300))
        screen.blit(HowToPlayButton,(850,500))
        if CheckIfMouseHovering(850,300,PlayImage):
            if pygame.mouse.get_pressed()[0]:
                CurrentState = "Play"
        if CheckIfMouseHovering(850,500,HowToPlayButton):
            if pygame.mouse.get_pressed()[0]:
                CurrentState = "HowToPlay"
    if CurrentState == "HowToPlay":
        screen.blit(HowToPlayImage,(0,0))
        screen.blit(BackButtonImage,(872.052,7.589))
        if CheckIfMouseHovering(872,7.589,BackButtonImage):
            if pygame.mouse.get_pressed()[0]:
                CurrentState = "MainMenu"
    pygame.display.flip()

    dt = clock.tick(60) / 1000

pygame.quit()