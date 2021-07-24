# -*- coding: utf-8 -*-
"""
Created on Sun Jul 11 17:46:25 2021

@author: Boran

1. 坦克类
    移动
    射击
    显示坦克的方法
2. 子弹类
    移动
    显示子弹的方法
3. 墙壁类
    是否可以通过
4. 爆炸效果类
    展示爆炸效果
5. 音效类
    播放音乐
6. 主类
    开始游戏
    结束游戏
7. 左上角输出敌方坦克数量

"""


import pygame
import sys
import time,random

# 窗口大小常量
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500
# 窗口背景颜色
BG_COLOR = pygame.Color(255, 255, 255)
# 字体颜色
TEXT_COLOR = pygame.Color(0, 0, 0)
# 墙壁布局
WALL_LOCATION = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]

# 敌方坦克位置
NPC_LOCATION = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]
# 敌方坦克同向移动步长
ENEMY_MOVE_STEP = random.randint(1, 250)
# 我方坦克速度
MY_SPEED = 10
# 敌方坦克速度
ENEMY_SPEED = 20
# 子弹速度
BULLET_SPEED = 30
# NPC队友伤害开关(npc会自杀)
REALITY_BULLET = False
# 墙壁生命
WALL_HP = 5
LAST_STACK = []
# 随机最大值，最小值为1，当值小于5时npc坦克射击
ENEMY_SHOT_LET = 100
# 随机最大值，最小值为1，当值小于5时npc坦克寻找player
FIND_THINK = 5
# 我方坦克生命
MY_HP = 100
# 敌方坦克生命
ENEMY_HP = 3


# 开始界面
class Hello():
    def __init__(self):       
        pygame.display.init()
        self.window = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        pygame.display.set_caption("坦克大战1.0")
        # 展示图片
        image = pygame.image.load('images/hello.gif')
        self.rect = image.get_rect()
        self.rect.top = 0
        self.rect.left = 0
        self.window.blit(image, self.rect)
        pygame.display.update()
        while True:
            time.sleep(0.05)
            flag = self.getEvent()
            if(flag == 1):
                pygame.display.quit()
                MainGame().startGame()
            if(flag == 2):
                pygame.display.quit()
                GameDesign()
    def getEvent(self):
        eventList = pygame.event.get()
        for event in eventList:
            if event.type == pygame.QUIT:
                pygame.display.quit()
                sys.exit()
        buttons = pygame.mouse.get_pressed()
        x1, y1 = pygame.mouse.get_pos()
        
        # print('x1:'+str(x1)+',y1:'+str(y1))
        if x1 >= 238 and x1 <= 455 and y1 >= 235 and y1 <=283:
            if buttons[0]:
                print('开始游戏')
                return 1
            
        elif x1 >= 238 and x1 <= 455 and y1 >= 335 and y1 <=383:
            if buttons[0]:
                print('设计地图')
                return 2
# 地图设计界面
class GameDesign():
    
    def __init__(self):       
        pygame.display.init()
        self.window = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT + 100])
        pygame.display.set_caption("坦克大战1.0 - 地图设计")
        
        
        self.action = ''
        self.last = ['',0,0]
        self.lastStack = LAST_STACK
        self.lastStack.append(self.last)
        
        while True:
            time.sleep(0.1)
            flag = self.getEvent()
            if(flag == 1):
                pygame.display.quit()
                time.sleep(0.25)
                MainGame().startGame()
            self.window.fill(BG_COLOR)
            self.showWallAndNPCAndBG()
            pygame.display.update()
    def getEvent(self):
        eventList = pygame.event.get()
        for event in eventList:
            if event.type == pygame.QUIT:
                pygame.display.quit()
                sys.exit()
        buttons = pygame.mouse.get_pressed()
        x1, y1 = pygame.mouse.get_pos()
        
        # print('x1:'+str(x1)+',y1:'+str(y1))
        if x1 >= 43 and x1 <= 120 and y1 >= 513 and y1 <=590:
            if buttons[0]:
                print('墙壁设计')
                self.action = 'wall'
            
        elif x1 >= 223 and x1 <= 297 and y1 >= 513 and y1 <=590:
            if buttons[0]:
                print('npc布置')
                self.action = 'npc'
        elif x1 >= 408 and x1 <= 475 and y1 >= 513 and y1 <=590:
            if buttons[0]:
                print('取消')
                self.cancel()
        elif x1 >= 585 and x1 <= 668 and y1 >= 513 and y1 <=590:
            if buttons[0]:
                print('开始游戏')
                return 1
        elif x1 >= 0 and x1 <= SCREEN_WIDTH and y1 >= 0 and y1 <= SCREEN_HEIGHT:
            if buttons[0]:
                if(self.action == 'wall'):
                    self.addWall(x1, y1)
                if(self.action == 'npc'):
                    self.addNPC(x1, y1)
                
    def addWall(self, x, y):
        # 当该位置没有位置也没有墙的时候可以放置
        if NPC_LOCATION[y // 50][x // 50] == 0 and  WALL_LOCATION[y // 50][x // 50] == 0:
            WALL_LOCATION[y // 50][x // 50] = 1
            last = ['wall', y//50, x //50]
            self.lastStack.append(last)
            print(self.lastStack)
        
        # print(WALL_LOCATION)
        
    def addNPC(self, x, y):
        # 当该位置没有位置也没有墙的时候可以放置
        if NPC_LOCATION[y // 50][x // 50] == 0 and  WALL_LOCATION[y // 50][x // 50] == 0:
            NPC_LOCATION[y // 50][x // 50] = 1
            last = ['npc', y//50, x //50]
            self.lastStack.append(last)
            print(self.lastStack)

        # print(NPC_LOCATION)
    
    def cancel(self):
        print(self.lastStack)
        if not len(self.lastStack) == 0:
            last = self.lastStack.pop()
            print(last)
            if last[0] == 'npc' :
                NPC_LOCATION[last[1]][last[2]] = 0
            if last[0] == 'wall' :
                WALL_LOCATION[last[1]][last[2]] = 0  
        
    def showWallAndNPCAndBG(self):
        # 展示图片
        image = pygame.image.load('images/design.gif')
        self.rect = image.get_rect()
        self.rect.top = 0
        self.rect.left = 0
        self.window.blit(image, self.rect)
        
        my_tank = pygame.image.load('images/up.gif')
        self.my_rect = image.get_rect()
        self.my_rect.top = SCREEN_HEIGHT - 50
        self.my_rect.left = SCREEN_WIDTH/2 - 25
        self.window.blit(my_tank, self.my_rect)
        
        for y in range(len(NPC_LOCATION)):
            for x in range(len(NPC_LOCATION[0])):
                if NPC_LOCATION[y][x] == 1:
                    image = pygame.image.load('images/edown.gif')
                    self.rect = image.get_rect()
                    self.rect.top = y * 50
                    self.rect.left = x * 50
                    self.window.blit(image, self.rect)
        for y in range(len(WALL_LOCATION)):
            for x in range(len(WALL_LOCATION[0])):
                if WALL_LOCATION[y][x] == 1:
                    image = pygame.image.load('images/wall1.gif')
                    self.rect = image.get_rect()
                    self.rect.top = y * 50
                    self.rect.left = x * 50
                    self.window.blit(image, self.rect)
            
# 主界面
class MainGame():
    window = None
    my_tank = None
    enemyTankList = []
    enemyTankCount = 0
    myBulletList = []
    enemyBulletList = []
    explodeList = []
    wallList = []
    def __init__(self):
        pass
    def startGame(self):
        # 加载主窗口
        pygame.display.init()
        # 显示主窗口，返回值是显示出来的窗口surface对象
        MainGame.window = pygame.display.set_mode([SCREEN_WIDTH,SCREEN_HEIGHT + 100])
        # 设置窗口标题
        pygame.display.set_caption("坦克大战1.0")
        # 初始化坦克,不需要一直创建，只需要在游戏开始时创建一次
        # 仅仅是创建，并没有显示
        self.createMyTank()
        # 初始化敌方坦克
        self.createEnemyTank()
        # 创建墙壁
        self.createWall()
        
        
        # 暂时感觉应该是不断刷新
        while True:
            time.sleep(0.05)
            MainGame.window.fill(BG_COLOR)
            # 时刻检测事件
            self.showBack()
            self.getEvent()
            # 在10，10 的位置安置获取到的文字图层
            MainGame.window.blit(self.getTextSurface("敌方坦克剩余数量：%d"%len(MainGame.enemyTankList)),(10, 10))
            
            # 展示己方坦克
            if MainGame.my_tank and MainGame.my_tank.live:   
                MainGame.my_tank.displayTank()
            else:
                del MainGame.my_tank
                MainGame.my_tank = None
            """
            * 原教学视频是用了一个停止标志，只要四个键中有一个按键停止，坦克便会停止移动，这样会给操作来一种迟钝感
            * 于是对代码进行了改进：
            *     将原来的一个停止标记改为四个，则每一个按键操作都对应的一个停止标记
            *     当该按键按下时，对该按键的停止标记置假，松开置真
            *     只有在所有的按键都松开时，坦克才停止移动，这样一个按键的松开就不会影响别的按键操作
            """
            if  MainGame.my_tank and MainGame.my_tank.live:
                # 在10，600 的位置安置血量
                MainGame.window.blit(self.getTextSurface("HP ：%d"%MainGame.my_tank.hp),(600, 10))
                if (not MainGame.my_tank.stopUp or not MainGame.my_tank.stopDown or
                    not MainGame.my_tank.stopLeft or not MainGame.my_tank.stopRight):
                    MainGame.my_tank.move()
                    # 检测我方坦克是否碰到墙壁
                MainGame.my_tank.hitWall()
                MainGame.my_tank.myTankHitEnemyTank()
                if MainGame.my_tank.hp == 1:
                    MainGame.my_tank.images = MainGame.my_tank.brokenImages
            # 展示敌方坦克
            self.blitEnemyTank()
            # 循环遍历我方坦克子弹
            self.blitMyBullet()
            # 循环遍历敌方坦克子弹
            self.blitEnemyBullet()
            # 循环遍历爆炸列表
            self.blitExplode()
            # 循环遍历墙壁列表
            self.blitWall()
            pygame.display.update()
    def showBack(self):
        back = pygame.image.load('images/back.gif')
        backRect = back.get_rect()
        backRect.left = 0
        backRect.top = SCREEN_HEIGHT
        MainGame.window.blit(back, backRect)
        
        
    def endGame(self):
        # 如果不加quit语句窗口会一直显示且未响应
        pygame.display.quit()
        sys.exit()
    def getTextSurface(self, text):
        # 初始化字体
        pygame.font.init()
        # print(pygame.font.get_fonts())
        # 获取字体
        font = pygame.font.SysFont('microsoftyaheimicrosoftyaheiui', 18)
        # 获取文字图层
        textSurface = font.render(text, False, TEXT_COLOR)
        return textSurface
    def getEvent(self):
        buttons = pygame.mouse.get_pressed()
        x1, y1 = pygame.mouse.get_pos()
        # print('x1:'+str(x1)+',y1:'+str(y1))
        if y1 > SCREEN_HEIGHT and y1 < SCREEN_HEIGHT + 100:
            if buttons[0]:
                pygame.display.quit()
                Hello()
                print('返回主界面')
        # 获取当前发生的事件的列表
        eventList = pygame.event.get()
        for event in eventList:
            if event.type == pygame.QUIT:
                self.endGame()
            
            if event.type == pygame.KEYUP:
                if  MainGame.my_tank and MainGame.my_tank.live:
                    if (event.key == pygame.K_UP or event.key == pygame.K_w):
                        MainGame.my_tank.stopUp = True
                        # MainGame.my_tank.move()
                        # print("坦克向上移动")
                    elif (event.key == pygame.K_DOWN or event.key == pygame.K_s):
                        MainGame.my_tank.stopDown = True
                        # MainGame.my_tank.move()
                        # print("坦克向下移动")
                    elif (event.key == pygame.K_LEFT or event.key == pygame.K_a):
                        MainGame.my_tank.stopLeft = True
                        # MainGame.my_tank.move()
                        # print("坦克向左移动")
                    elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d):
                        MainGame.my_tank.stopRight = True
                        # MainGame.my_tank.move()
                        # print("坦克向右移动")
            if event.type == pygame.KEYDOWN:
                if  MainGame.my_tank and MainGame.my_tank.live:
                    if (event.key == pygame.K_UP or event.key == pygame.K_w):
                        MainGame.my_tank.direction = 'UP'
                        MainGame.my_tank.stopUp = False
                        # MainGame.my_tank.move()
                        # print("坦克向上移动")
                    elif (event.key == pygame.K_DOWN or event.key == pygame.K_s):
                        MainGame.my_tank.direction = 'DOWN'
                        MainGame.my_tank.stopDown = False
                        # MainGame.my_tank.move()
                        # print("坦克向下移动")
                    elif (event.key == pygame.K_LEFT or event.key == pygame.K_a):
                        MainGame.my_tank.direction = 'LEFT'
                        MainGame.my_tank.stopLeft = False
                        # MainGame.my_tank.move()
                        # print("坦克向左移动")
                    elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d):
                        MainGame.my_tank.direction = 'RIGHT'
                        MainGame.my_tank.stopRight = False
                        # MainGame.my_tank.move()
                        # print("坦克向右移动")
                    # 非移动操作
                    # 发射子弹
                    if (event.key == pygame.K_SPACE):
                        if len(MainGame.myBulletList) < 2:
                            print('biu ~')
                            myBullet = Bullet(MainGame.my_tank)
                            MainGame.myBulletList.append(myBullet)
                # 重生
                if not (MainGame.my_tank and MainGame.my_tank.live):
                    if(event.key == pygame.K_RETURN):
                        print('i am back')
                        self.createMyTank()
                if(event.key == pygame.K_p):
                        print('new one')
                        self.createOneEnemyTank()
    # 创建我方坦克                     
    def createMyTank(self):
        MainGame.my_tank = MyTank(SCREEN_WIDTH/2 - 25, SCREEN_HEIGHT - 50)
    # 创建敌方坦克
    def createEnemyTank(self):
        for y in range(len(NPC_LOCATION)):
            for x in range(len(NPC_LOCATION[0])):
                print('x:'+str(x))
                if NPC_LOCATION[y][x] == 1:
                    print('here x:'+str(x) + ' y:'+str(y))
                    top_ = y * 50
                    left_ = x * 50
                    speed_ = ENEMY_SPEED
                    stop_ = False
                    enemy = EnemyTank(left_, top_, speed_, stop_)
                    MainGame.enemyTankList.append(enemy)
       
    # 创建一个敌方坦克
    def createOneEnemyTank(self):
        top_ = 0
        left_ = 50
        speed_ = ENEMY_SPEED
        stop_ = False
        enemy = EnemyTank(left_, top_, speed_, stop_)
        MainGame.enemyTankList.append(enemy)
    # 展示敌方坦克
    def blitEnemyTank(self):
        for enemyTank in MainGame.enemyTankList:
            if(not enemyTank.live):
                MainGame.enemyTankList.remove(enemyTank)
                del(enemyTank)
                continue
            enemyTank.displayTank()
            enemyTank.randMove()
            enemyTank.hitWall()
            # 坦克相撞检测
            if  MainGame.my_tank and MainGame.my_tank.live:
                enemyTank.enemyTankHitMyTank()
            enemyBullet = enemyTank.shot()
            if enemyBullet:
                MainGame.enemyBulletList.append(enemyBullet)
            if enemyTank.hp == 1:
                enemyTank.images = enemyTank.brokenImages
    # 展示我方子弹
    def blitMyBullet(self):
        for myBullet in MainGame.myBulletList:
            myBullet.myBulletHitEnemyTank()
            myBullet.bulletHitWall()
            myBullet.displayBullet()
            myBullet.move()
            myBullet.myBulletHitEnemyBullet()
            if(not myBullet.live):
                MainGame.myBulletList.remove(myBullet)
                
    # 展示敌方子弹
    def blitEnemyBullet(self):
        for enemyBullet in MainGame.enemyBulletList:
            
            enemyBullet.enemyBulletHitMyTank()
            enemyBullet.bulletHitWall()
            if REALITY_BULLET:
                enemyBullet.myBulletHitEnemyTank()
            enemyBullet.displayBullet()
            enemyBullet.move()
            enemyBullet.enemyBulletHitMyBullet()
            if(not enemyBullet.live):
                MainGame.enemyBulletList.remove(enemyBullet)
    # 展示爆炸
    def blitExplode(self):
        for explode in MainGame.explodeList:
            if explode.live:
                explode.displayExplode()
            else:
                MainGame.explodeList.remove(explode)
    # 创建墙壁
    def createWall(self):
        wallLoc = WALL_LOCATION
        for y in range(len(wallLoc)):
            for x in range(len(wallLoc[0])):
                if wallLoc[y][x] == 1:
                    print('x:'+str(x)+',y:'+str(y))
                    wall = Wall(x*50, y*50)
                    MainGame.wallList.append(wall)
    # 展示墙壁
    def blitWall(self):
        for wall in MainGame.wallList:
            if wall.hp > 0:
                wall.displayWall()
            else:
                MainGame.wallList.remove(wall)
                del(wall)
        
    
# 精灵项
class SpriteItem(pygame.sprite.Sprite):
    def __init__(self):
       # Call the parent class (Sprite) constructor
       pygame.sprite.Sprite.__init__(self)
       
# 总 坦克类  
class Tank(SpriteItem):
    def __init__(self):
        self.oldLeft = self.rect.left
        self.oldTop = self.rect.top
      
    # 移动
    def move(self):
        self.oldLeft = self.rect.left
        self.oldTop = self.rect.top
        if self.direction == 'LEFT':
            if self.rect.left > 0:
                self.rect.left -= self.speed
            elif(self.rect.left <= 0):
                self.rect.left = 0
                self.changeDirection()
        elif self.direction == 'RIGHT':
            if self.rect.left < SCREEN_WIDTH - self.rect.height:
                self.rect.left += self.speed
            elif(self.rect.left >= SCREEN_WIDTH - self.rect.height):
                self.rect.left = SCREEN_WIDTH - self.rect.height
                self.changeDirection()
        elif self.direction == 'UP':
            if self.rect.top > 0:
                self.rect.top -= self.speed
            elif(self.rect.top <= 0):
                self.rect.top = 0
                self.changeDirection()
        elif self.direction == 'DOWN':
            if self.rect.top < SCREEN_HEIGHT - self.rect.height:
                self.rect.top += self.speed
            elif(self.rect.top >= SCREEN_HEIGHT - self.rect.height):
                self.rect.top = SCREEN_HEIGHT - self.rect.height
                self.changeDirection()
    # shot
    def shot(self):
        pass
    # 空的一个改方向方法
    def changeDirection(self):
        pass
    # show
    def displayTank(self):
        self.image = self.images[self.direction]
        MainGame.window.blit(self.image, self.rect)
    # 检测坦克墙壁碰撞
    def hitWall(self):
        for wall in MainGame.wallList:
            if pygame.sprite.collide_rect(self, wall):
                self.stay()
                self.changeDirection()
    def stay(self):
        self.rect.left = self.oldLeft
        self.rect.top = self.oldTop
        
    # NPC坦克撞玩家坦克
    def enemyTankHitMyTank(self):
        if pygame.sprite.collide_rect(self, MainGame.my_tank):
            self.stay()
            self.shot()
            
    # 玩家坦克撞NPC坦克
    def myTankHitEnemyTank(self):
        for enemyTank in MainGame.enemyTankList:
            if pygame.sprite.collide_rect(self, enemyTank):
                self.stay()
# 我方坦克
class MyTank(Tank):
    def __init__(self, left_, top_):
        
        
        self.images = {
            'UP':pygame.image.load('images/up.gif'),
            'DOWN':pygame.image.load('images/down.gif'),
            'LEFT':pygame.image.load('images/left.gif'),
            'RIGHT':pygame.image.load('images/right.gif'),
        
        }
        self.brokenImages = {
            'UP':pygame.image.load('images/broken/up.gif'),
            'DOWN':pygame.image.load('images/broken/down.gif'),
            'LEFT':pygame.image.load('images/broken/left.gif'),
            'RIGHT':pygame.image.load('images/broken/right.gif'),
        
        }
        self.direction = 'UP'
        self.image = self.images[self.direction]
        # 获取区域
        self.rect = self.image.get_rect()
        # 设置区域
        self.rect.left = left_
        self.rect.top = top_
        self.speed = MY_SPEED
        self.stopUp = True
        self.stopDown = True
        self.stopLeft = True
        self.stopRight = True
        self.live = True
        self.hp = MY_HP
        super(MyTank, self).__init__()
# 敌方坦克
class EnemyTank(Tank):
    def __init__(self, left_, top_, speed_, stop_):
        
        self.images = {
            'UP':pygame.image.load('images/eup.gif'),
            'DOWN':pygame.image.load('images/edown.gif'),
            'LEFT':pygame.image.load('images/eleft.gif'),
            'RIGHT':pygame.image.load('images/eright.gif'),
        
        }
        self.brokenImages = {
            'UP':pygame.image.load('images/broken/eup.gif'),
            'DOWN':pygame.image.load('images/broken/edown.gif'),
            'LEFT':pygame.image.load('images/broken/eleft.gif'),
            'RIGHT':pygame.image.load('images/broken/eright.gif'),
        
        }
        # 随机生成敌方坦克
        self.direction = self.randDirection()
        self.image = self.images[self.direction]
        self.rect = self.image.get_rect()
        self.rect.left = left_
        self.rect.top = top_
        self.speed = speed_
        self.stop = stop_
        self.moveStep = ENEMY_MOVE_STEP
        self.live = True
        self.hp = ENEMY_HP
        super(EnemyTank, self).__init__()
        
    # 改变方向
    def changeDirection(self):
        self.direction = self.randDirection()
        self.moveStep = ENEMY_MOVE_STEP
    def randDirection(self):
        num = random.randint(1,4)
        if(num == 1):
            return 'UP'
        elif(num == 2):
            return 'DOWN'
        elif(num == 3):
            return 'LEFT'
        elif(num == 4):
            return 'RIGHT'
    def randMove(self):
        if (self.moveStep > 0):
            self.move()
            think = random.randint(1, FIND_THINK)
            if(think < 5):
                self.findMyTank()
            self.moveStep -= 1
        else:
            self.changeDirection()
    # 寻找玩家坦克
    def findMyTank(self):
        if MainGame.my_tank and MainGame.my_tank.live:
            edt = self.rect.top
            edl = self.rect.left
            mdt = MainGame.my_tank.rect.top
            mdl = MainGame.my_tank.rect.left
            think = random.randint(1, 2)
            if(think == 1):
                if edt > mdt:
                    self.direction = 'UP'
                if edt < mdt:
                    self.direction = 'DOWN'
                if edt == mdt:
                    self.shot()
            if(think == 2):
                if edl > mdl:
                    self.direction = 'LEFT'
                if edl < mdl :
                    self.direction = 'RIGHT'
                if edl == mdl:
                    self.shot()
            self.moveStep = ENEMY_MOVE_STEP
            self.shot()
    def shot(self):
        flag = random.randint(1,ENEMY_SHOT_LET)
        if(flag < 10):
            print('be careful ~')
            return Bullet(self)
        
        
# 子弹类
class Bullet(SpriteItem):
    def __init__(self, tank):
        self.image = pygame.image.load('images/bullet.gif')
        self.direction = tank.direction
        self.rect = self.image.get_rect()
        self.speed = BULLET_SPEED
        self.live = True
        self.shape = True
        if self.direction == 'LEFT':
            self.rect.left = tank.rect.left - self.rect.width
            self.rect.top = tank.rect.top + tank.rect.height / 2 - self.rect.height / 2
        elif self.direction == 'RIGHT':
            self.rect.left = tank.rect.left + tank.rect.width
            self.rect.top = tank.rect.top + tank.rect.height / 2 - self.rect.height / 2
        elif self.direction == 'UP':
            self.rect.left = tank.rect.left + tank.rect.width / 2 - self.rect.width / 2
            self.rect.top = tank.rect.top - self.rect.height
        elif self.direction == 'DOWN':
            self.rect.left = tank.rect.left + tank.rect.width / 2 - self.rect.width / 2
            self.rect.top = tank.rect.top + tank.rect.height
    # 
    def move(self):
        if self.direction == 'LEFT':
            if self.rect.left > 0:
                self.rect.left -= self.speed
                # 子弹击中四周动画优化，下同
                if self.rect.left < 0 + BULLET_SPEED + 1:
                    if self.shape:
                        self.image = pygame.image.load('images/brokenBullet.gif')
                        self.shape = False
            else:
                self.live = False
        elif self.direction == 'RIGHT':
            if self.rect.left < SCREEN_WIDTH - self.rect.height:
                self.rect.left += self.speed
                if self.rect.left > SCREEN_WIDTH - self.rect.width - BULLET_SPEED + 1:
                    if self.shape:   
                        self.image = pygame.image.load('images/brokenBullet.gif')
                        self.shape = False
            else:
                self.live = False
        elif self.direction == 'UP':
            if self.rect.top > 0:
                self.rect.top -= self.speed
                if self.rect.top < 0 + BULLET_SPEED + 1:
                    if self.shape:
                        self.image = pygame.image.load('images/brokenBullet.gif')
                        self.shape = False
            else:
                self.live = False
        elif self.direction == 'DOWN':
            if self.rect.top < SCREEN_HEIGHT - self.rect.height:
                self.rect.top += self.speed
                if self.rect.top > SCREEN_HEIGHT - self.rect.height - BULLET_SPEED + 1:
                    if self.shape:
                        self.image = pygame.image.load('images/brokenBullet.gif')
                        self.shape = False
            else:
                self.live = False
    def displayBullet(self):
        MainGame.window.blit(self.image, self.rect)
    # 玩家子弹撞向敌方坦克
    def myBulletHitEnemyTank(self):
        # 循环遍历地方坦克列表，判断是否碰撞
        for enemyTank in MainGame.enemyTankList:
            if pygame.sprite.collide_rect(enemyTank, self):
                enemyTank.hp -= 1
                self.live = False
                print("pia!")
                if(enemyTank.hp == 0):
                    enemyTank.live = False
                    # 创建爆炸对象
                    explode = Explode(enemyTank)
                    # 将爆炸添加到爆炸列表
                    MainGame.explodeList.append(explode)
                if self.shape:
                    self.image = pygame.image.load('images/brokenBullet.gif')
                    self.shape = False
    # 敌方子弹击中我方坦克
    def enemyBulletHitMyTank(self):
        if  MainGame.my_tank and MainGame.my_tank.live:
            if pygame.sprite.collide_rect(MainGame.my_tank, self):
                MainGame.my_tank.hp -= 1
                self.live = False
                print("a!")
                if(MainGame.my_tank.hp == 0):
                    MainGame.my_tank.live = False
                    self.live = False
                    # 创建爆炸对象
                    explode = Explode(MainGame.my_tank)
                    # 将爆炸添加到爆炸列表
                    MainGame.explodeList.append(explode)
                if self.shape:
                    self.image = pygame.image.load('images/brokenBullet.gif')
                    self.shape = False
    # 子弹撞墙
    def bulletHitWall(self):
        for wall in MainGame.wallList:
            if pygame.sprite.collide_rect(self, wall):
                print("hong ~!")
                wall.hp -= 1
                self.live = False
                if self.shape:
                    self.image = pygame.image.load('images/brokenBullet.gif')
                    self.shape = False
    def myBulletHitEnemyBullet(self):
        for bullet in MainGame.enemyBulletList:
            if pygame.sprite.collide_rect(bullet, self):
                print("ding ~")
                bullet.live = False
                self.live = False
                if bullet.shape:
                    bullet.image = pygame.image.load('images/brokenBullet.gif')
                    bullet.shape = False
                if self.shape:
                    self.image = pygame.image.load('images/brokenBullet.gif')
                    self.shape = False
    def enemyBulletHitMyBullet(self):
        for bullet in MainGame.myBulletList:
            if pygame.sprite.collide_rect(bullet, self):
                print("ding ~")
                bullet.live = False
                self.live = False
                if bullet.shape:
                    bullet.image = pygame.image.load('images/brokenBullet.gif')
                    bullet.shape = False
                if self.shape:
                    self.image = pygame.image.load('images/brokenBullet.gif')
                    self.shape = False
            

# 墙壁类
class Wall():
    def __init__(self, left_, top_):
        self.image = pygame.image.load('images/wall1.gif')
        self.rect = self.image.get_rect()
        self.rect.left = left_
        self.rect.top = top_
        self.live = True
        self.hp = WALL_HP
    def displayWall(self):
        MainGame.window.blit(self.image, self.rect)
# 爆炸类
class Explode():
    def __init__(self, tank):
        self.rect = tank.rect
        self.images = [
            pygame.image.load('images/blast0.gif'),
            pygame.image.load('images/blast1.gif'),
            pygame.image.load('images/blast2.gif'),
            pygame.image.load('images/blast3.gif'),
            pygame.image.load('images/blast4.gif'),
            pygame.image.load('images/blast5.gif'),
        ]
        self.step = 0
        self.image = self.images[self.step]
        self.live = True
    def displayExplode(self):
        if self.step < len(self.images):
            self.image = self.images[self.step]
            self.step += 1
            MainGame.window.blit(self.image, self.rect)
        else:
            self.live = False
            self.step = 0
# 音乐类
class Music():
    def __init__(self, filename):
        pygame.mixer.init()
        self.filename = filename
        pygame.mixer.music.load(filename)
    def playMusic(self):
        pygame.mixer.music.play()
if __name__ == '__main__':
    Hello()
    # MainGame().startGame()
    # MainGame().getTextSurface()
    