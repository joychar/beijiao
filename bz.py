import pygame
import sys
import os
import json
from collections import defaultdict

# 初始化pygame
pygame.init()
screen_info = pygame.display.Info()
SCREEN_WIDTH = screen_info.current_w
SCREEN_HEIGHT = screen_info.current_h
FPS = 30
# 加载图片
PIC = "pic"
PICTURES = {
        'floor0': pygame.transform.scale(pygame.image.load(PIC + "/floor0.png"), (32, 32)),
        'wall0': pygame.transform.scale(pygame.image.load(PIC + "/wall0.png"), (32, 32)),
        'sidewall0': pygame.transform.scale(pygame.image.load(PIC + "/sidewall0.png"), (32, 32)),
        'table0': pygame.transform.scale(pygame.image.load(PIC + "/table0.png"), (96, 96)),
        'table1': pygame.transform.scale(pygame.image.load(PIC + "/table1.png"), (96, 96)),
        'table2': pygame.transform.scale(pygame.image.load(PIC + "/table2.png"), (96, 96)),
        'table3': pygame.transform.scale(pygame.image.load(PIC + "/table3.png"), (96, 96)),
        'table4': pygame.transform.scale(pygame.image.load(PIC + "/table4.png"), (96, 96)),
        'table5': pygame.transform.scale(pygame.image.load(PIC + "/table5.png"), (96, 96)),
        'table6': pygame.transform.scale(pygame.image.load(PIC + "/table6.png"), (96, 96)),
        'table7': pygame.transform.scale(pygame.image.load(PIC + "/table7.png"), (96, 96)),

        'flower0': pygame.transform.scale(pygame.image.load(PIC + "/flower0.png"), (32, 32)),
        'flower1': pygame.transform.scale(pygame.image.load(PIC + "/flower1.png"), (32, 32)),
        'flower2': pygame.transform.scale(pygame.image.load(PIC + "/flower2.png"), (32, 32)),
        'flower3': pygame.transform.scale(pygame.image.load(PIC + "/flower3.png"), (32, 64)),
        'flower4': pygame.transform.scale(pygame.image.load(PIC + "/flower4.png"), (32, 64)),
        'flower5': pygame.transform.scale(pygame.image.load(PIC + "/flower5.png"), (64, 96)),
        'flower6': pygame.transform.scale(pygame.image.load(PIC + "/flower6.png"), (64, 96)),   
        'flower7': pygame.transform.scale(pygame.image.load(PIC + "/flower7.png"), (64, 64)),

        'gold0': pygame.transform.scale(pygame.image.load(PIC + "/gold0.png"), (64, 64)),
        'sun0': pygame.transform.scale(pygame.image.load(PIC + "/sun0.png"), (64, 64)),
        'flower': pygame.transform.scale(pygame.image.load(PIC + "/flower.png"), (64, 64)),
        'income0': pygame.transform.scale(pygame.image.load(PIC + "/income0.png"), (64, 64)),

        'button': pygame.transform.scale(pygame.image.load(PIC + "/button.png"), (128, 64)),
        'item_case0': pygame.transform.scale(pygame.image.load(PIC + "/item_case0.png"), (256, 128)),
        'shuzhikuang0': pygame.transform.scale(pygame.image.load(PIC + "/shuzhikuang0.png"), (192, 64)),
}

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BROWN = (139, 69, 19)
CREAM = (247, 223, 194)
WORD = (172, 136, 58)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# 创建游戏窗口
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("北角麻将馆")
clock = pygame.time.Clock()

# 初始化游戏状态
running = True
seted = False
gameover = False
item_id = 0
warehoused = False
shoped = False
moved=False
wallheight = 8
#游戏变量
money = 3000  # 初始资金
day = 1       # 天数
rent = 3000   # 房租
next_rent = 30000   # 房租
income = 0    # 收入
flower = 0    # 鲜花
floor_furniture = 1
floorwidth = 14
floorheight = 10
wallwidth = floorwidth
floors = [[0 for i in range(floorwidth)] for j in range(floorheight)]
sidewallheight = floorheight + wallheight
floor_zero = ((SCREEN_WIDTH/2-(floorwidth*16)), (SCREEN_HEIGHT/2-(floorheight*16)+32*4))
# 仓库储存物品
warehouse = [0] * 16
#存储地板家具信息
floor_info = defaultdict(lambda: None)
#延迟
delay_time = 10
delay_start = False
can_delay = False

# 场景参数
max_floorwidth = 30

#读档修改游戏状态
def load_game():
    global money, day, rent, next_rent, income, flower, floor_furniture, floorwidth, floorheight, wallwidth, floors, sidewallheight, floor_zero, warehouse, floor_info
    save_dir = os.path.join(os.getenv('LOCALAPPDATA'), 'bzmjg')
    save_path = os.path.join(save_dir, 'savegame.json')
    if(os.path.exists(save_path)):
        try:
            with open(save_path, 'r') as f:
                game_state = json.load(f)
                money = game_state['money']
                day = game_state['day']
                rent = game_state['rent']
                next_rent = game_state['next_rent']
                income = game_state['income']
                flower = game_state['flower']
                floor_furniture = game_state['floor_furniture']
                floorwidth = game_state['floorwidth']
                floorheight = game_state['floorheight']
                wallwidth = game_state['wallwidth']
                floors = game_state['floors']
                sidewallheight = game_state['sidewallheight']
                floor_zero = game_state['floor_zero']
                warehouse = game_state['warehouse']
                old_floor_info = game_state['floor_info']
                floor_info = defaultdict(lambda: None)
                #把旧floor_info插入到floor_info中
                for key, value in old_floor_info.items():
                    floor_info[int(key)] = value
        except FileNotFoundError:
            pass
#读档
load_game()

#存档
def save_game():
    global money, day, rent, next_rent, income, flower, floor_furniture, floorwidth, floorheight, wallwidth, floors, sidewallheight, floor_zero, warehouse, floor_info    # 读取有的！none，的floor_info再插入json
    old_floor_info = {}
    for i in range(len(floor_info)):
        if floor_info[i] != None:
            old_floor_info[i] = floor_info[i]
    #读取C盘用户名
    save_dir = os.path.join(os.getenv('LOCALAPPDATA'), 'bzmjg')
    os.makedirs(save_dir, exist_ok=True) #没有就创建
    save_path = os.path.join(save_dir, 'savegame.json')
    with open(save_path, 'w') as f:
        game_state = {
            'money' : money,  # 初始资金
            'day' : day,       # 天数
            'rent' : rent,   # 房租
            'next_rent' : next_rent,   # 房租
            'income' : income,    # 收入
            'flower' : flower,    # 鲜花
            'floor_furniture' : floor_furniture,
            'floorwidth' : floorwidth,
            'floorheight' : floorheight,
            'wallwidth' : wallwidth,
            'floors' : floors,
            'sidewallheight' : sidewallheight,
            'floor_zero' : floor_zero,
            'warehouse' : warehouse,
            'floor_info' : old_floor_info
        } 
        json.dump(game_state,f)

def new_game():
    save_dir = os.path.join(os.getenv('LOCALAPPDATA'), 'bzmjg')
    save_path = os.path.join(save_dir, 'savegame.json')
    if(os.path.exists(save_path) ):
        os.remove(save_path)

# 商品列表
class Table:
    def __init__(self, name, price, img, length, width, desc, income):
        self.name = name
        self.price = price
        self.img = img
        self.length = length
        self.width = width
        self.desc = desc
        self.income = income

items = {
    0: Table("麻将桌普通", 1000, PICTURES['table0'], 3, 3, "一张麻将桌，可以用来打麻将。", 40),
    1: Table("麻将桌精品", 1500, PICTURES['table1'], 3, 3, "一张麻将桌，可以用来打麻将。", 50),
    2: Table("麻将桌豪华", 2000, PICTURES['table2'], 3, 3, "一张麻将桌，可以用来打麻将。", 70),
    3: Table("麻将桌顶级", 2500, PICTURES['table3'], 3, 3, "一张麻将桌，可以用来打麻将。", 80),
    4: Table("麻将桌超级", 3000, PICTURES['table4'], 3, 3, "一张麻将桌，可以用来打麻将。", 100),
    5: Table("麻将桌无限", 3500, PICTURES['table5'], 3, 3, "一张麻将桌，可以用来打麻将。", 110),
    6: Table("麻将桌神秘", 4000, PICTURES['table6'], 3, 3, "一张麻将桌，可以用来打麻将。", 130),
    7: Table("麻将桌神圣", 5000, PICTURES['table7'], 3, 3, "一张麻将桌，可以用来打麻将。", 160),

    8: Table("鲜花", 500, PICTURES['flower0'], 1, 1, "一朵鲜花，可以用来装饰。", 1),
    9: Table("鲜花", 500, PICTURES['flower1'], 1, 1, "一朵鲜花，可以用来装饰。", 1),
    10: Table("鲜花", 500, PICTURES['flower2'], 1, 1, "一朵鲜花，可以用来装饰。", 1),
    11: Table("鲜花", 2000, PICTURES['flower3'], 1, 2, "一朵鲜花，可以用来装饰。", 4),
    12: Table("鲜花", 2000, PICTURES['flower4'], 1, 2, "一朵鲜花，可以用来装饰。", 4),
    13: Table("鲜花", 16000, PICTURES['flower5'],2, 3, "一朵鲜花，可以用来装饰。", 32),
    14: Table("鲜花", 16000, PICTURES['flower6'], 2, 3, "一朵鲜花，可以用来装饰。", 32),
    15: Table("鲜花", 72100, PICTURES['flower7'], 2, 2, "一朵鲜花，可以用来装饰。", 150),
}

# 字体
font = pygame.font.SysFont('simhei', 24)
font_500 = pygame.font.SysFont('simhei', 500)
font_20 = pygame.font.SysFont('simhei', 20)
font_18 = pygame.font.SysFont('simhei', 18)
font_16 = pygame.font.SysFont('simhei', 16)

def draw_background():
    """绘制场景"""
    screen.fill(BLACK)  # 背景色

    #绘制左栏
    pygame.draw.rect(screen, WORD, ((0, 0, (SCREEN_WIDTH/2)-max_floorwidth*16-32, SCREEN_HEIGHT)))

    #绘制右栏
    pygame.draw.rect(screen, WORD, ((SCREEN_WIDTH/2)+max_floorwidth*16+32, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
    
    # 绘制地板
    for i in range(floorwidth):
        for j in range(floorheight):
            screen.blit(PICTURES['floor0'], (i*32+(SCREEN_WIDTH/2-(floorwidth*16)), j*32+(SCREEN_HEIGHT/2-(floorheight*16)+32*4)))
    # 绘制墙壁
    for i in range(wallwidth):
        for j in range(wallheight):
            screen.blit(PICTURES['wall0'], (i*32+(SCREEN_WIDTH/2-(wallwidth*16)), j*32+(SCREEN_HEIGHT/2-(wallheight*32)-(floorheight*16)+32*4)))
    # 绘制侧墙
    for i in range(sidewallheight):
        screen.blit(PICTURES['sidewall0'], (SCREEN_WIDTH/2-(32)-(floorwidth*16), i*32+(SCREEN_HEIGHT/2-(floorheight*16)-(wallheight*32)+32*4)))
        screen.blit(PICTURES['sidewall0'], (SCREEN_WIDTH/2+(floorwidth*16), i*32+(SCREEN_HEIGHT/2-(floorheight*16)-(wallheight*32)+32*4)))

def draw_button(x, y, w, h, text):
    btn = pygame.Rect(x, y, w, h)    
    screen.blit(PICTURES['button'], btn)
    btn_text = font.render(text, True, BLACK)
    screen.blit(btn_text, (x + 30, y + 20))

def draw_state(x, y, dir, state, text):
    screen.blit(PICTURES['shuzhikuang0'], (x, y))
    # 显示金钱图标
    screen.blit(PICTURES[dir], (x-6, y))
    money_text = font_20.render(f"{text}:{state}", True, BLACK)
    screen.blit(money_text, (x + 46, y + 20))

def draw_ui():
    """绘制用户界面"""

    # 显示金钱
    draw_state(8, 8, 'gold0', money, "金钱")

    # 显示天数
    draw_state(3*64+16, 8, 'sun0', day, "天数")
    
    # 显示环境
    draw_state(8, 8+64+8, 'flower', flower, "环境")

    # 显示收入
    draw_state(3*64+16, 8+64+8, 'income0', income, "收入")

    # 显示房租
    draw_state(8, 8+64+8+64+8, 'gold0', rent, "房租")

    draw_state(3*64+16, 8+64+8+64+8, 'gold0', next_rent, "扩大后")
    
    # 绘制下一天按钮
    draw_button(SCREEN_WIDTH-150, 0, 120, 50, "下一天")

    # 绘制商店
    draw_button(SCREEN_WIDTH-250, 0, 120, 50, "商店")

    #绘制仓库
    draw_button(SCREEN_WIDTH-350, 0, 120, 50, "仓库")
    
    # 绘制扩大
    draw_button(SCREEN_WIDTH-450, 0, 120, 50, "扩大")
    
#绘制仓库
def draw_warehouse():
    # 仓库变红字
    btn_text = font.render("仓库", True, RED)
    screen.blit(btn_text, (SCREEN_WIDTH-320, 20))

    use = font_16.render("使用", True, BLACK)
    sell = font_16.render("出售", True, BLACK)
    
    for i in range(8):
        screen.blit(PICTURES['item_case0'], (SCREEN_WIDTH-450, 64+i*128))
        screen.blit(PICTURES['item_case0'], (SCREEN_WIDTH-450+256-32, 64+i*128))

        screen.blit(use, (SCREEN_WIDTH-450+130, 64+i*128+28))
        screen.blit(sell, (SCREEN_WIDTH-450+130, 64+i*128+28+52))

        screen.blit(use, (SCREEN_WIDTH-450+130 + 256-32, 64+i*128+28))
        screen.blit(sell, (SCREEN_WIDTH-450+130 + 256-32, 64+i*128+28+52))

    # 绘制物品
    for i in range(16):
        if warehouse[i] > 0:
            if i < 8:
                screen.blit(items[i].img, (SCREEN_WIDTH-450+(128-items[i].length*32)/2, 64+i*128+(128-items[i].width*32)/2))
                #在做下角标注数量
                num_text = font_16.render(f"{warehouse[i]}", True, BLACK)
                #计算文本宽度
                num_text_width = num_text.get_width()
                num_text_height = num_text.get_height()
                screen.blit(num_text, (1488+64+16-num_text_width/2, 82+64+16-num_text_height/2+(i)*128))
            if i >= 8:
                screen.blit(items[i].img, (1712+46-(items[i].length*16), 82+46+(i-8)*128-(items[i].width*16)))
                num_text = font_16.render(f"{warehouse[i]}", True, BLACK)
                num_text_width = num_text.get_width()
                num_text_height = num_text.get_height()
                screen.blit(num_text, (1712+64+16-num_text_width/2, 82+64+16-num_text_height/2+(i-8)*128))
                

def  draw_shop():
    # 商店变红字
    btn_text = font.render("商店", True, RED)
    screen.blit(btn_text, (SCREEN_WIDTH-220, 20))

    buy_to_use = font_16.render("购买并使用", True, BLACK)
    buy_to_warehouse = font_16.render("购买到仓库", True, BLACK)

    for i in range(8):
        screen.blit(PICTURES['item_case0'], (SCREEN_WIDTH-450, 64+i*128))
        screen.blit(PICTURES['item_case0'], (SCREEN_WIDTH-450+256-32, 64+i*128))   

        screen.blit(buy_to_use, (SCREEN_WIDTH-450+130, 64+i*128+28))
        screen.blit(buy_to_warehouse, (SCREEN_WIDTH-450+130, 64+i*128+28+52))

        screen.blit(buy_to_use, (SCREEN_WIDTH-450+130 + 256-32, 64+i*128+28))
        screen.blit(buy_to_warehouse, (SCREEN_WIDTH-450+130 + 256-32, 64+i*128+28+52))

    # 绘制物品
    items_length = len(items)
    for i in range(items_length):    
        #麻将桌
        if i < 8:
            screen.blit(items[i].img, (SCREEN_WIDTH-450+(128-items[i].length*32)/2, 64+i*128+(128-items[i].width*32)/2))
            #在左上角标注价格
            price_text = font_16.render(f"{items[i].price}", True, BLACK)
            income_text = font_16.render(f"{items[i].income}", True, BLACK)
            price_text_width = price_text.get_width()
            price_text_height = price_text.get_height()
            screen.blit(price_text, (1488+16-price_text_width/2, 82+16-price_text_height/2+(i)*128))
            screen.blit(income_text, (1488+16-price_text_width/2+64, 82+16-price_text_height/2+(i)*128))

        # 绘制花卉
        if i >= 8:
            screen.blit(items[i].img, (1712+46-(items[i].length*16), 82+46+(i-8)*128-(items[i].width*16)))   
            price_text = font_16.render(f"{items[i].price}", True, BLACK)
            income_text = font_16.render(f"{items[i].income}", True, BLACK)
            price_text_width = price_text.get_width()
            price_text_height = price_text.get_height()
            screen.blit(price_text, (1712+16-price_text_width/2, 82+16-price_text_height/2+(i-8)*128))
            screen.blit(income_text, (1712+16-price_text_width/2+64, 82+16-price_text_height/2+(i-8)*128)) 

def next_day():
    global day, money, income, gameover
    flower_score_income = int((income * flower)/100)
    day += 1
    money += income + flower_score_income  # 每天增加元
    if day % 30 == 0:
        money = money - rent  # 每30天减少2000元
    # 结算收入
    #存档
    if money < 0:
        gameover = True
    save_game()

def expand():
    global floorwidth, floorheight, wallwidth, sidewallheight, floor_zero, floors, rent, money, next_rent
    floorwidth += 4
    floorheight += 4
    wallwidth = floorwidth
    sidewallheight = floorheight + wallheight
    # 租金
    level_1 = 3000
    level_2 = 30000
    level_3 = 8_0000
    level_4 = 16_0000
    level_5 = 34_0000

    if rent == level_1:
        money -= level_1
        rent = level_2
        next_rent = level_3
    elif rent == level_2:
        money -= level_2
        rent = level_3
        next_rent = level_4
    elif rent == level_3:
        money -= level_3
        rent = level_4
        next_rent = level_5
    elif rent == level_4:
        money -= level_4
        rent = level_5
        next_rent = '最大'

    floor_zero = ((SCREEN_WIDTH/2-(floorwidth*16)), (SCREEN_HEIGHT/2-(floorheight*16)+32*4)) #记录地板左上角坐标
    # 让floors列表扩大同时把旧的东西复制过来
    new_floors = [[0 for i in range(floorwidth)] for j in range(floorheight)]
    for i in range(floorheight):
        for j in range(floorwidth):
            if i < floorheight-4 and j < floorwidth-4:
                new_floors[i][j] = floors[i][j]
            else:
                new_floors[i][j] = 0
    floors = new_floors

def item_move():
    if moved:
        mouse_pos = pygame.mouse.get_pos()
        #加个绿边框
        pygame.draw.rect(screen, GREEN, (mouse_pos[0]-8, mouse_pos[1]-8, 16, 16),2)
        #下方圈起来的地方也变绿
        pygame.draw.circle(screen, GREEN, (mouse_pos[0]-8+8, mouse_pos[1]-8+8), 8, 2)
        if mouse_pos[0] > floor_zero[0] and mouse_pos[1] > floor_zero[1] and mouse_pos[0] < floor_zero[0]+floorwidth*32 and mouse_pos[1] < floor_zero[1]+floorheight*32:
            length = items[item_id].length
            width = items[item_id].width
            x = int(( mouse_pos[0] - floor_zero[0] ) // 32) - int(length/2)
            y = int(( mouse_pos[1] - floor_zero[1] ) // 32) - int(width/2)
            pygame.draw.rect(screen, GREEN, (x*32+floor_zero[0], y*32+floor_zero[1], length*32, width*32))
            if x < 0 or y  < 0 or x+length > floorwidth or y+width > floorheight: 
                pygame.draw.rect(screen, RED, (x*32+floor_zero[0], y*32+floor_zero[1], length*32, width*32))
            if (x >= 0 and y >= 0 and x+(length-1) < floorwidth and y+(width-1) < floorheight):
                for i in range(x, x+length):
                    for j in range(y, y+width):    
                        if not floors[j][i] == 0:
                            pygame.draw.rect(screen, RED, (i*32+floor_zero[0], j*32+floor_zero[1], 32, 32))                   
            screen.blit(items[item_id].img, (x*32+floor_zero[0], y*32+floor_zero[1]))

    # 绘制家具
def draw_furniture():
    for i in range(len(floor_info)):
        if floor_info[i] != None:
            if floor_info[i][2] < 8:
               screen.blit(PICTURES["table"+str(floor_info[i][2])], (floor_zero[0]+floor_info[i][0]*32, floor_zero[1]+floor_info[i][1]*32))
            if floor_info[i][2] >= 8:
               screen.blit(PICTURES["flower"+str(floor_info[i][2]-8)], (floor_zero[0]+floor_info[i][0]*32, floor_zero[1]+floor_info[i][1]*32))

def check(i, j,table_id):
    for x in range(i, i+items[table_id].length):
        for y in range(j, j+items[table_id].width):
            if (x >= 0 and y >= 0 and x < floorwidth and y < floorheight):
                if floors[y][x] != 0:
                    return False
    return True

def draw_set():
    # 绘制设置
    pygame.draw.rect(screen, (28, 31, 34), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.draw.rect(screen, (WHITE), (SCREEN_WIDTH/2 - 10, 0, 20, SCREEN_HEIGHT))
    quit_text = font_500.render("退出", True, WHITE)
    quit_text_height = quit_text.get_height()
    screen.blit(quit_text, (0,(SCREEN_HEIGHT-quit_text_height)/2))

    new_game_text = font_500.render("删档", True, WHITE)
    screen.blit(new_game_text, (SCREEN_WIDTH/2 + 10,(SCREEN_HEIGHT-quit_text_height)/2))
    if gameover:
        description_text = font.render("当前资金不足，游戏结束，请删档重新开始，或者退出", True, WHITE)
        description_text_width = description_text.get_width()
        screen.blit(description_text, (SCREEN_WIDTH/4 - description_text_width/2, (SCREEN_HEIGHT)/8))

# 绘制描述
def draw_descript():
    if not seted:
        text = font.render("1.按ESC键进入设置(退出或者删档)再按", True, WHITE)
        text_height = text.get_height()
        texts = [
            font.render("一次ESC返回游戏", True, WHITE),
            font.render("2.在仓库或商店点击使用后，划到地面上", True, WHITE),
            font.render("点击左键放置物品，右键取消放置，放回", True, WHITE),
            font.render("仓库", True, WHITE),
            font.render("3当点击物品不移动时，点击物品左上角", True, WHITE),
            font.render("4.物品左上角为价格，右上角为收益，右", True, WHITE),
            font.render("右下角为数量", True, WHITE),
            font.render("5.环境分会增加百分之（环境分）的收入", True, WHITE),
            font.render("6.点击下一天按钮，增加一天，然后存档", True, WHITE),
            font.render("7.点击扩大按钮，会增加房屋面积，收一", True, WHITE),
            font.render("次当前房租，增加房租为扩大后", True, WHITE),
            font.render("8.每30天交次房租", True, WHITE),
            font.render("9.出售物品，半价出售", True, WHITE),
            font.render("10.当金钱不足时，游戏结束", True, WHITE)
        ]
        screen.blit(text, (8, 8+64+8+64+8+64+8))
        for i in range(len(texts)):
            screen.blit(texts[i], (8, 8+64+8+64+8+64+8+(i+1)*(text_height+8)))

def new_game_and_default_state():
    global day, money, income, flower, warehouse, floor_info, floor_furniture, floorwidth, floorheight, wallwidth, floors, sidewallheight, floor_zero, rent, next_rent
    new_game()
    money = 3000  # 初始资金
    day = 1       # 天数
    rent = 3000   # 房租
    next_rent = 30000
    income = 0    # 收入
    flower = 0    # 鲜花
    floor_furniture = 1
    floorwidth = 14
    floorheight = 10
    wallwidth = floorwidth
    floors = [[0 for i in range(floorwidth)] for j in range(floorheight)]
    sidewallheight = floorheight + wallheight
    floor_zero = ((SCREEN_WIDTH/2-(floorwidth*16)), (SCREEN_HEIGHT/2-(floorheight*16)+32*4))
    # 仓库储存物品
    warehouse = [0] * 16
    #存储地板家具信息
    floor_info = defaultdict(lambda: None)

# 游戏主循环
while running:
    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                seted = not seted
            if event.key == pygame.K_j and seted:
                money += 1000000000
        elif money < 0:
                gameover = True
                if event.type == pygame.MOUSEBUTTONDOWN and gameover:
                    mouse_pos = pygame.mouse.get_pos()
                    new_game_btn = pygame.Rect(SCREEN_WIDTH/2, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
                    quit_btn = pygame.Rect(0, 0, SCREEN_WIDTH/2, SCREEN_HEIGHT)
                    if quit_btn.collidepoint(mouse_pos):
                        running = False
                    if new_game_btn.collidepoint(mouse_pos):
                        new_game_and_default_state()
                        gameover = False    
        elif event.type == pygame.MOUSEBUTTONDOWN and seted:
            mouse_pos = pygame.mouse.get_pos()
            new_game_btn = pygame.Rect(SCREEN_WIDTH/2, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
            quit_btn = pygame.Rect(0, 0, SCREEN_WIDTH/2, SCREEN_HEIGHT)
            if quit_btn.collidepoint(mouse_pos):
                running = False
            if new_game_btn.collidepoint(mouse_pos):
                new_game_and_default_state()
        elif event.type == pygame.MOUSEBUTTONDOWN and not seted:
            mouse_pos = pygame.mouse.get_pos()
            next_day_btn = pygame.Rect(SCREEN_WIDTH-150, 0, 120, 50)    # 定义下一天按钮
            expand_btn = pygame.Rect(SCREEN_WIDTH-450, 0, 120, 50)      # 定义扩大按钮
            warehouse_btn = pygame.Rect(SCREEN_WIDTH-350, 0, 120, 50)   # 定义仓库按钮
            shop_btn = pygame.Rect(SCREEN_WIDTH-250, 0, 120, 50)        # 定义商店按钮

            if moved == False and next_day_btn.collidepoint(mouse_pos):    # 点击下一天按钮
                next_day()
            if moved == False and expand_btn.collidepoint(mouse_pos) and floorwidth < max_floorwidth:  # 点击扩大按钮
                expand()
            if moved == False and warehouse_btn.collidepoint(mouse_pos):  # 点击仓库按钮
                shoped = False
                warehoused = True
            if moved == False and shop_btn.collidepoint(mouse_pos):       # 点击商店按钮
                warehoused = False
                shoped = True
            
            if moved == False and shoped or warehoused:
                # 定义16个购买使用物品的按钮
                up_btns = [None] * 16
                down_btns = [None] * 16

                for i in range(16):
                    if i < 8:
                        up_btns[i] = pygame.Rect(1596, 82+128*(i), 92, 32)
                        down_btns[i] = pygame.Rect(1596, 138+128*(i), 92, 32)
                    else:    
                        up_btns[i] = pygame.Rect(1820, 82+128*(i-8), 92, 32)
                        down_btns[i] = pygame.Rect(1820, 138+128*(i-8), 92, 32)
                                
                #点击按钮触发购买事件
                for i in range(16):
                    if up_btns[i].collidepoint(mouse_pos) and shoped:
                        if moved == False and money >= items[i].price:
                            money -= items[i].price
                            item_id = i
                            moved=True

                    if moved == False and up_btns[i].collidepoint(mouse_pos) and warehoused:  
                        if warehouse[i] > 0:
                            warehouse[i] -= 1
                            item_id = i
                            moved=True

                for i in range(16):
                    if moved == False and down_btns[i].collidepoint(mouse_pos) and shoped:
                        if money >= items[i].price:
                            money -= items[i].price
                            warehouse[i] += 1
                        
                    if moved == False and down_btns[i].collidepoint(mouse_pos) and warehoused:
                        # 出售
                        if warehouse[i] > 0:
                            money += int(items[i].price/2)
                            warehouse[i] -= 1

            # 点击floor区域物品move
            if not moved:
                # 同时鼠标点击了floor区域内
                if event.button == 1:
                    if mouse_pos[0] > floor_zero[0] and mouse_pos[1] > floor_zero[1] and mouse_pos[0] < floor_zero[0]+floorwidth*32 and mouse_pos[1] < floor_zero[1]+floorheight*32:
                        
                        x = int(( mouse_pos[0] - floor_zero[0] ) // 32) - int(1/2)
                        y = int(( mouse_pos[1] - floor_zero[1] ) // 32) - int(1/2)
                        if floors[y][x] !=0:
                            # 修改item_id
                            number = floors[y][x]
                            item_id = floor_info[number-1][2]
                            length = items[item_id].length
                            width = items[item_id].width

                            if (x >= 0 and y >= 0 and x+length-1 < floorwidth and y+width-1 < floorheight):
                                furniture_x = floor_info[number-1][0]
                                furniture_y = floor_info[number-1][1]
                                for i in range(furniture_x, furniture_x+length):
                                    for j in range(furniture_y, furniture_y+width):    
                                        if not floors[j][i] == 0:
                                            floors[j][i] = 0
                                # 删除floor_info中的物品
                                floor_info.pop(number-1)
                                # 物品被拿起且是麻将桌，income减少
                                if item_id < 8:
                                    income -= items[item_id].income
                                elif item_id >= 8:
                                # 物品被拿起且是花，flower减少
                                    flower -= items[item_id].income
                                    
                                moved=True
                                delay_start = pygame.time.get_ticks()  # 记录开始时间 延迟用

            #物品放置    
            if moved and (pygame.time.get_ticks() - delay_start > delay_time): #and 延迟逻辑
                mouse_pos = pygame.mouse.get_pos()
                #在地板上放置物品
                if mouse_pos[0] > floor_zero[0] and mouse_pos[1] > floor_zero[1] and mouse_pos[0] < floor_zero[0]+floorwidth*32 and mouse_pos[1] < floor_zero[1]+floorheight*32:
                    #鼠标再点击一次放置物品      
                    if event.button == 1 and (pygame.time.get_ticks() - delay_start > delay_time): #and 延迟逻辑
                        length = items[item_id].length
                        width = items[item_id].width
                        x = int(( mouse_pos[0] - floor_zero[0] ) // 32) - int(length/2)
                        y = int(( mouse_pos[1] - floor_zero[1] ) // 32) - int(width/2)
                        if (x >= 0 and y >= 0 and x+length-1 < floorwidth and y+width-1 < floorheight):
                            if(check(x, y, item_id)):
                                for k in range(x, x+items[item_id].length):
                                    for l in range(y, y+items[item_id].width):
                                        floors[l][k] = floor_furniture
                                floor_info[floor_furniture-1] = (x, y, item_id)
                                floor_furniture += 1
                                # 物品放置完成且是麻将桌，income增加 
                                if item_id < 8:
                                    income += items[item_id].income
                                elif item_id >= 8:
                                    flower += items[item_id].income
                                    
                                moved=False      
                    if event.button == 3:
                        # 物品放置取消，仓库加入物品
                        warehouse[item_id] += 1
                        moved=False

    draw_background()
    draw_ui()
    draw_furniture()
    draw_descript()
    
    if warehoused:
        draw_warehouse()
    if shoped:
        draw_shop()
    item_move()

    if seted:
        draw_set()
    # 更新显示
    if gameover:
        draw_set()
    pygame.display.flip()
    
    # 控制帧率
    clock.tick(FPS)

# 退出游戏
pygame.quit()
sys.exit()
