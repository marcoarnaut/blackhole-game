import pygame
from random import randint
import time
from time import sleep as wait
import numpy as np
import pygame.gfxdraw   
pygame.init()
pygame.font.init()


font = pygame.font.SysFont('Comic Sans MS', 30)
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
FPS = 60
pygame.display.set_caption("Blackhole")
space_pressed = 0
action = "menu"
entered = "0"
cooldown, esccooldown, cooldown0, explosion_time, cooldown1, cooldown2, cooldown3, cooldown4, cooldown5, cooldown6, cooldown7, cooldown8, cooldown9, bcooldown = 0,0,0,0,0,0,0,0,0,0,0,0,0,0
entered_volume = 0
color_swap_cooldown = 0
fps_counter_switch_cooldown = 0
entered_blackhole_power = 0
buy_cooldown, graphics_switch_cooldown = 0, 0
window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
empty_icon = pygame.Surface((1, 1))
pygame.display.set_icon(empty_icon)
clock = pygame.time.Clock()
clicked = 0
objects = []
blackholes = []
count = 500
screen_pixel = 0
if WIDTH > 1800:
    screen_pixel = 2
elif WIDTH > 1400:
    screen_pixel = 1
size_min = 1+screen_pixel #1
size_limit = 5+screen_pixel #5
start = 0
y_step = 0
x_step = 0
points_received = False
menu_generated = False
map_color = 0
map_col_num = 0.1
start_time = 0
bg_objects = []
bg_objects_count = 5
bg_toggle = True
bg_toggle_text = "On"
explosion_time = 0
offset_time = 0
sticky = 0.25 #keyboard_sticking_cooldown
current_fps = 0
fps_counter = False
bh_color = "white"

# FOR SAVE
graphics = True
points = 0
blackhole_power = 60 #60
max_blackhole_power = 60

# SAVER / LOADER

dir = "blackholedir.txt"
try:
    file = open(dir, 'r', encoding='utf-8')
    data = file.read()
    points = int(data.split(",")[0])
    blackhole_power = int(data.split(",")[1])
    max_blackhole_power = int(data.split(",")[2])
    if str(data.split(",")[3]).replace(' ','') == "False":
        graphics = False
    else:
        graphics = True
    if str(data.split(",")[4]).replace(' ','') == "False":
        bg_toggle = False
    else:
        bg_toggle = True
    if str(data.split(",")[5]).replace(' ','') == "False":
        fps_counter = False
    else:
        fps_counter = True
except:
    file = open(dir, 'w', encoding='utf-8')
    file.write("0, 60, 60, True, True")
    file.close
    file = open(dir, 'r', encoding='utf-8')
    data = file.read()
    points = int(data.split(",")[0])
    blackhole_power = int(data.split(",")[1]) 
    max_blackhole_power = int(data.split(",")[2])
    pass

play = True

def menu_snow_generate() -> None:
    """Generates particles in main menu"""
    global objects
    global menu_generated
    global bg_objects
    if menu_generated == False:
        objects = []
        bg_objects = []
        menu_size_limit = size_limit - 2
        count = 100
        for i in range(count): #fg
            x, y = randint(0, WIDTH), randint(0, HEIGHT)
            size = randint(size_min, menu_size_limit)
            color = (200, 200, 200)
            objects.append([x, y, size, color])
        if bg_toggle:
            for i in range(bg_objects_count): #bg
                x, y = randint(0, WIDTH), randint(0, HEIGHT)
                size = randint(80,250)
                color = (15, 15, 15)
                bg_objects.append([x, y, size, color])
        menu_generated = True

def snow_effect_bg() -> None:
    """Views bg in game"""
    global bg_objects
    for obj in bg_objects:
        x, y = obj[0], obj[1]
        size = obj[2]
        color = obj[3]
        if graphics == False:
            if space_pressed == 0:
                pygame.draw.circle(window, color, (x, y), size)
            else:
                pygame.draw.circle(window, (int(255-obj[3][0]), int(255-obj[3][1]), int(255-obj[3][1])), (x, y), size)
        elif graphics == True:
            if space_pressed == 0:
                pygame.gfxdraw.aacircle(window, int(x), int(y), int(size), color)
                pygame.gfxdraw.filled_circle(window, int(x), int(y), int(size), color)
            else:
                pygame.gfxdraw.aacircle(window, int(x), int(y), int(size), (int(255-obj[3][0]), int(255-obj[3][1]), int(255-obj[3][1])))
                pygame.gfxdraw.filled_circle(window, int(x), int(y), int(size), (int(255-obj[3][0]), int(255-obj[3][1]), int(255-obj[3][1])))
        obj[1] += ((obj[2])/160) + y_step/2
        obj[0] += x_step/2
        if obj[1] > HEIGHT+200:
            obj[0] = randint(0, WIDTH)
            obj[1] = randint(-200, 0)
            continue
        if obj[1] < -200:
            obj[0] = randint(0, WIDTH)
            obj[1] = randint(int(HEIGHT+200), HEIGHT)
            continue
        if obj[0] < -200:
            obj[0] = randint(int(WIDTH), WIDTH+200)
            obj[1] = randint(0, HEIGHT)
            continue
        if obj[0] > WIDTH+200:
            obj[0] = randint(-200, 0)
            obj[1] = randint(0, HEIGHT)
            continue   
def menu_snow_effect() -> None:
    """Views particles in main menu"""
    global objects
    x_step = 1
    for obj in objects:
        col1 = int(obj[3][0]/size_limit)*obj[2]
        if col1 > 255:
            col1 = 255
        col2 = int(obj[3][1]/size_limit)*obj[2]
        if col2 > 255:
            col2 = 255
        col3 = int((obj[3][2]/size_limit)*obj[2]*1.2)
        if col3 > 255:
            col3 = 255
        x, y = obj[0], obj[1]
        size = obj[2]
        color = (col1, col2, col3)
        if graphics == False:
            pygame.draw.circle(window, color, (x, y), size)
        elif graphics == True:
            create_light(x, y, (255, 255, 255), 5, int(size*4))
            pygame.gfxdraw.aacircle(window, int(x), int(y), int(size), color)
            pygame.gfxdraw.filled_circle(window, int(x), int(y), int(size), color)
        if y_step == 0:
            obj[1] += ((obj[2]/6))
        else:
            obj[1] += ((obj[2]/6) + y_step)
        if x_step != 0:
            obj[0] += x_step
        if obj[1] > HEIGHT+screen_pixel+obj[2]:
            obj[0] = randint(0, WIDTH)
            obj[1] = randint(0, int(HEIGHT/10))
            continue
        if obj[1] < 0:
            obj[0] = randint(0, WIDTH)
            obj[1] = randint(int(HEIGHT - HEIGHT/10), HEIGHT)
            continue
        if obj[0] < 0:
            obj[0] = randint(int(WIDTH - WIDTH/10), WIDTH)
            obj[1] = randint(0, HEIGHT)
            continue
        if obj[0] > WIDTH+screen_pixel+obj[2]:
            obj[0] = randint(0, int(WIDTH/10))
            obj[1] = randint(0, HEIGHT)
            continue

def snow_effect(objects: list, mouse: tuple) -> None:
    """Calculates particles in game"""
    for i in range(len(objects)):
        obj = objects[i]
        if y_step == 0:
            obj[1] += ((obj[2]/6))
        else:
            obj[1] += ((obj[2]/6) + y_step)
        if x_step != 0:
            obj[0] += x_step
        if obj[1] > HEIGHT+screen_pixel+obj[2]:
            obj[0] = randint(0, WIDTH)
            obj[1] = randint(0, int(HEIGHT/10))
            continue
        if obj[1] < 0:
            obj[0] = randint(0, WIDTH)
            obj[1] = randint(int(HEIGHT - HEIGHT/10), HEIGHT)
            continue
        if obj[0] < 0:
            obj[0] = randint(int(WIDTH - WIDTH/10), WIDTH)
            obj[1] = randint(0, HEIGHT)
            continue
        if obj[0] > WIDTH+screen_pixel+obj[2]:
            obj[0] = randint(0, int(WIDTH/10))
            obj[1] = randint(0, HEIGHT)
            continue

def objects_draw() -> None:
    """Views objects"""
    for obj in objects:
        x, y = obj[0], obj[1]
        size = obj[2]
        if space_pressed == 0:
            col1 = int(obj[3][0]/size_limit)*size
            if col1 > 255:
                col1 = 255
            col2 = int(obj[3][1]/size_limit)*size
            if col2 > 255:
                col2 = 255
            col3 = int((obj[3][2]/size_limit)*size*1.2)
            if col3 > 255:
                col3 = 255
        else:
            col1 = 255 - int(obj[3][0]/size_limit)*size
            if col1 < 0:
                col1 = 0
            col2 = 255 - int(obj[3][1]/size_limit)*size
            if col2 < 0:
                col2 = 0
            col3 = 255 - int((obj[3][2]/size_limit)*size*1.2)
            if col3 < 0:
                col3 = 0
        color = (col1, col2, col3)
        x, y = obj[0], obj[1]
        size = obj[2]
            # Треугольник
            #   a
            #   
            #   b       c
        AB = abs(obj[1] - mouse[1])
        BC = abs(obj[0] - mouse[0])
        AC = abs(((AB ** 2) + (BC ** 2)) ** 0.5)
        range_int = AC
        if obj[4] == False:
            if graphics == False:
                pygame.draw.circle(window, color, (x, y), size)
            elif graphics == True:
                if space_pressed == 0:
                    create_light(x, y, (col1, col2, col3), 2, int(size*4))
                else:
                    create_light(x, y, (0, 0, 0), 2, int(size*4))
                pygame.gfxdraw.aacircle(window, int(x), int(y), int(size), color)
                pygame.gfxdraw.filled_circle(window, int(x), int(y), int(size), color)

def blackhole(objects: list, mouse: tuple) -> None:
    """Creates the blackhole"""
    pygame.mouse.set_visible(False)
    global clicked
    for obj in objects:
        x, y = obj[0], obj[1]
        size = obj[2]
        color = ((obj[3][0]/5)*size, (obj[3][1]/5)*size, (obj[3][2]/5)*size)
        # Треугольник
        #   a
        #   
        #   b       c
        AB = abs(obj[1] - mouse[1])
        BC = abs(obj[0] - mouse[0])
        AC = abs(((AB ** 2) + (BC ** 2)) ** 0.5)
        range_int = AC
        search_range = int(blackhole_power/3)
        if search_range < 50:
            search_range = 50
            # obj[0], obj[1] = randint(0, WIDTH), randint(0, HEIGHT) # - удаление объекта
        if clicked == 0:
            obj[4] = False
            if range_int < search_range: #100
                if obj[0] > mouse[0]: # - отдаление объекта
                    obj[0] += 10
                if obj[0] < mouse[0]:
                    obj[0] -= 10
            continue
        if clicked == 1:
            if obj[4] == True:
                obj[0] = mouse[0]
                obj[1] = mouse[1]
            if range_int < int(blackhole_power/4): # if < bh rad
                if obj[4] == False:
                    obj[4] = True
            elif range_int < int(blackhole_power):
                if obj[4] == False:
                    if obj[0] < mouse[0]: # - приближение объекта по X
                        obj[0] += int(blackhole_power/12)
                    if obj[0] > mouse[0]:
                        obj[0] -= int(blackhole_power/12)
                    if obj[1] > mouse[1]: # - приближение объекта по Y
                        obj[1] -= int(blackhole_power/12)
                    if obj[1] < mouse[1]:
                        obj[1] += int(blackhole_power/12)
                    if graphics == True:
                        create_lines_bh()
                        if space_pressed == 0:
                            create_light(mouse[0], mouse[1], (100, 100, 100), 4, int(blackhole_power/3))
                        else:
                            create_light(mouse[0], mouse[1], (150, 150, 150), 4, int(blackhole_power/3))
            continue
    if clicked == 1:
        draw_ellipse(mouse)
    if clicked == 0:
        draw_range()               
   
def explosion(objects: list, mouse: tuple) -> None:
    """Calculates blackhole's explosion"""
    global clicked
    global explosion_time
    for obj in objects:
        AB = abs(obj[1] - mouse[1])
        BC = abs(obj[0] - mouse[0])
        AC = abs(((AB ** 2) + (BC ** 2)) ** 0.5)
        range_int = AC
        if range_int < 50:
            step = int(blackhole_power/3)
            obj[0] -= obj[2]*randint(-step, step)
            obj[1] -= obj[2]*randint(-step, step)
    explosion_time = float(time.time())
    

def explosion_x(mouse: tuple) -> None:
    """Views blackhole's explosion effect"""
    global explosion_time
    # print(offset_time)
    if space_pressed == 0:
        col1 = 255
        col2 = 255
        col3 = 255
    else:
        col1 = 0
        col2 = 0
        col3 = 0
    centerx, centery = int(mouse[0]), int(mouse[1])
    if explosion_time < float(time.time())+1:
        if float(time.time()) > float(int(explosion_time)+0.1-offset_time) and float(time.time()) < float(int(explosion_time)+0.15+offset_time):
            #print("frame1")
            alpha = int(8)
            rad = 120+int(blackhole_power/10)
            rad_quality = 5 #rad step
            for i in range(int((rad-1)/rad_quality)):
                rad_i = i*rad_quality
                draw_circle_alpha(window, (col1, col2, col3, alpha), (centerx, centery), rad_i)
        elif float(time.time()) > float(int(explosion_time)+0.15-offset_time) and float(time.time()) < float(int(explosion_time)+0.2+offset_time):
            #print("frame2")
            alpha = int(7)
            rad = 110+int(blackhole_power/10)
            rad_quality = 5 #rad step
            for i in range(int((rad-1)/rad_quality)):
                rad_i = i*rad_quality
                draw_circle_alpha(window, (col1, col2, col3, alpha), (centerx, centery), rad_i)
        elif float(time.time()) > float(int(explosion_time)+0.2-offset_time) and float(time.time()) < float(int(explosion_time)+0.25+offset_time):
            #print("frame3")
            alpha = int(6)
            rad = 100+int(blackhole_power/10)
            rad_quality = 5 #rad step
            for i in range(int((rad-1)/rad_quality)):
                rad_i = i*rad_quality
                draw_circle_alpha(window, (col1, col2, col3, alpha), (centerx, centery), rad_i)
        elif float(time.time()) > float(int(explosion_time)+0.25-offset_time) and float(time.time()) < float(int(explosion_time)+0.3+offset_time):
            #print("frame4")
            alpha = int(5)
            rad = 90+int(blackhole_power/10)
            rad_quality = 5 #rad step
            for i in range(int((rad-1)/rad_quality)):
                rad_i = i*rad_quality
                draw_circle_alpha(window, (col1, col2, col3, alpha), (centerx, centery), rad_i)
        elif float(time.time()) > float(int(explosion_time)+0.3-offset_time) and float(time.time()) < float(int(explosion_time)+0.35+offset_time):
            #print("frame5")
            alpha = int(4)
            rad = 80+int(blackhole_power/10)
            rad_quality = 5 #rad step
            for i in range(int((rad-1)/rad_quality)):
                rad_i = i*rad_quality
                draw_circle_alpha(window, (col1, col2, col3, alpha), (centerx, centery), rad_i)
        elif float(time.time()) > float(int(explosion_time)+0.35-offset_time) and float(time.time()) < float(int(explosion_time)+0.4+offset_time):
            #print("frame6")
            alpha = int(3)
            rad = 70+int(blackhole_power/10)
            rad_quality = 5 #rad step
            for i in range(int((rad-1)/rad_quality)):
                rad_i = i*rad_quality
                draw_circle_alpha(window, (col1, col2, col3, alpha), (centerx, centery), rad_i)
        elif float(time.time()) > float(int(explosion_time)+0.4-offset_time) and float(time.time()) < float(int(explosion_time)+0.45+offset_time):
            #print("frame7")
            alpha = int(2)
            rad = 60+int(blackhole_power/10)
            rad_quality = 5 #rad step
            for i in range(int((rad-1)/rad_quality)):
                rad_i = i*rad_quality
                draw_circle_alpha(window, (col1, col2, col3, alpha), (centerx, centery), rad_i)
        elif float(time.time()) > float(int(explosion_time)+0.45-offset_time) and float(time.time()) < float(int(explosion_time)+0.5+offset_time):
            #print("frame8")
            alpha = int(1)
            rad = 50+int(blackhole_power/10)
            rad_quality = 5 #rad step
            for i in range(int((rad-1)/rad_quality)):
                rad_i = i*rad_quality
                draw_circle_alpha(window, (col1, col2, col3, alpha), (centerx, centery), rad_i)
 
def draw_range() -> None:
    """Views effect of collide mode"""
    rad_black = int(blackhole_power/4)
    index = 6
    if graphics == True:
        for i in range(10):
            if space_pressed == 0:
                col = randint(0, 255)
            else:
                col = 0
            radx = int(randint(int(blackhole_power/(index)), int(blackhole_power/(index/2))))
            rady = int(randint(int(blackhole_power/(index)), int(blackhole_power/(index/2))))
            pygame.gfxdraw.ellipse(window, mouse[0], mouse[1], int(1.1*radx), int(1.1*rady), (col, col, col))
        if space_pressed == 0:
            pygame.gfxdraw.filled_circle(window, int(mouse[0]), int(mouse[1]), int(rad_black*1.3), (0,0,0)) 
        else:
            pygame.gfxdraw.filled_circle(window, int(mouse[0]), int(mouse[1]), int(rad_black*1.3), (255, 255, 255)) 
    elif graphics == False:
        for i in range(10):
            col = randint(0, 255)
            radx = int(randint(int(blackhole_power/(index)), int(blackhole_power/(index/2))))
            rady = int(randint(int(blackhole_power/(index)), int(blackhole_power/(index/2))))
            pygame.gfxdraw.ellipse(window, mouse[0], mouse[1], int(1.1*radx), int(1.1*rady), (col, col, col))
        pygame.draw.ellipse(window, (col, col, col), (mouse[0]-int(radx), mouse[1]-int(rady), 2*radx, 2*rady), int(blackhole_power/20))
        pygame.draw.circle(window, (0,0,0), (mouse[0], mouse[1]), rad_black*1.3)
   
def draw_ellipse(mouse: tuple) -> None:
    """Views effect of pump mode"""
    er_count = int(blackhole_power/30)
    d_count = int(blackhole_power/7)
    rad_black = int(blackhole_power/6)
    if er_count > 6:
        er_count = 6
    if rad_black > 50:
        rad_black = 50
    if d_count > rad_black:
        d_count = rad_black
    if er_count > 15:
        er_count = 15
    if graphics == True:
        if space_pressed == 0:
            create_light(mouse[0], mouse[1], (255, 255, 255), 2, int(rad_black+12))
        else:
            create_light(mouse[0], mouse[1], (0, 0, 0), 2, int(rad_black+12))
    if bh_color == "white":
        for i in range(er_count):
            rand_col = randint(50, 220) # grey-white
            ecllipse_size = 15*i
            deviation1 = randint(-d_count, d_count)
            deviation2 = randint(-d_count, d_count)
            if space_pressed == 0:
                pygame.draw.ellipse(window, (rand_col, rand_col, rand_col), (mouse[0]-(ecllipse_size/2)+deviation1, mouse[1]-(ecllipse_size/2)+deviation2, ecllipse_size, ecllipse_size), 1) # size - int(blackhole_power/60)
            else:
                pygame.draw.ellipse(window, (255-rand_col,0,0), (mouse[0]-(ecllipse_size/2)+deviation1, mouse[1]-(ecllipse_size/2)+deviation2, ecllipse_size, ecllipse_size), 1) # size - int(blackhole_power/60)
    if bh_color == "red":
        for i in range(er_count):
            rand_col = randint(100, 200) # red-grey
            ecllipse_size = 15*i
            deviation1 = randint(-d_count, d_count)
            deviation2 = randint(-d_count, d_count)
            if space_pressed == 0:
                pygame.draw.ellipse(window, (rand_col, 0, 0), (mouse[0]-(ecllipse_size/2)+deviation1, mouse[1]-(ecllipse_size/2)+deviation2, ecllipse_size, ecllipse_size), 1) # size - int(blackhole_power/60)
            else:
                pygame.draw.ellipse(window, (255-rand_col,0,0), (mouse[0]-(ecllipse_size/2)+deviation1, mouse[1]-(ecllipse_size/2)+deviation2, ecllipse_size, ecllipse_size), 1) # size - int(blackhole_power/60)
        # col = randint(100, 255)
        # range_int = int(int(blackhole_power/er_count)*i*0.65)
        # line_end_pos_x = mouse[0] + randint(-range_int, range_int)
        # line_end_pos_y = mouse[1] + randint(-range_int, range_int)
        # if space_pressed == 0:
        #     pygame.draw.line(window, (col, col, col), (mouse[0], mouse[1]), (line_end_pos_x, line_end_pos_y), 1)
        # else:
        #     pygame.draw.line(window, (0,0,0), (mouse[0], mouse[1]), (line_end_pos_x, line_end_pos_y), 1)
    if space_pressed == 0:
        pygame.draw.circle(window, (0,0,0), (mouse[0], mouse[1]), rad_black)
    else:
        pygame.draw.circle(window, (255,255,255), (mouse[0], mouse[1]), rad_black)

def create_lines_bh() -> None:
    """Views effect of pumping object"""
    er_count = int(blackhole_power/30)
    for i in range(er_count):
        col = randint(100, 255)
        range_int = int(int(blackhole_power/er_count)*i*0.65)
        line_end_pos_x = mouse[0] + randint(-range_int, range_int)
        line_end_pos_y = mouse[1] + randint(-range_int, range_int)
        if space_pressed == 0:
            pygame.draw.line(window, (col, col, col), (mouse[0], mouse[1]), (line_end_pos_x, line_end_pos_y), 1)
        else:
            pygame.draw.line(window, (0,0,0), (mouse[0], mouse[1]), (line_end_pos_x, line_end_pos_y), 1)

def obj_count_func(objects: list) -> int:
    """Object counter"""
    a = 0
    # for obj in objects:
    #     AB = abs(obj[1] - mouse[1])
    #     BC = abs(obj[0] - mouse[0])
    #     AC = abs(((AB ** 2) + (BC ** 2)) ** 0.5)
    #     range_int = AC
    #     counter_range = int(blackhole_power/6)
    #     if counter_range < 49:
    #         counter_range = 49
    #     if range_int < counter_range:
    #         a += 1
    for obj in objects:
        if obj[4] == True:
            a += 1
    return a

def move_forward() -> None:
    """Camera forward moving"""
    global y_step
    y_step = 1.5

def move_back() -> None:
    """Camera back moving"""
    global y_step
    y_step = -1.5

def move_left() -> None:
    """Camera left moving"""
    global x_step
    x_step = 1.5

def move_right() -> None:
    """Camera right moving"""
    global x_step
    x_step = -1.5

def score_update(obj_count: int) -> None:
    """Updates player's score"""
    global points_received
    global points
    font = pygame.font.SysFont('Comic Sans MS', 20)
    text = font.render(f'You got points for compliting, you can restart.', True, (100, 100, 100))
    if obj_count == entered_volume:
        window.blit(text, (WIDTH/2-210,10))
        if points_received == False:
            points += entered_volume
        points_received = True
    pass

def draw_circle_alpha(surface: pygame.surface.Surface, color: tuple, center: tuple, radius: int) -> None:
    """Views transparent circle"""
    target_rect = pygame.Rect(center, (0, 0)).inflate((radius * 2, radius * 2))
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    pygame.draw.circle(shape_surf, color, (radius, radius), radius)
    surface.blit(shape_surf, target_rect)

def create_light(centerx: int, centery: int, color: tuple, alpha: int, rad: int) -> None:
    """Views smooth light as transparent circle"""
    col1 = color[0]
    col2 = color[1]
    col3 = color[2]
    centerx, centery = int(centerx), int(centery)
    alpha = int(alpha)
    rad = int(rad)
    for i in range(rad-1):
        rad_for = rad - (rad-i)
        draw_circle_alpha(window, (col1, col2, col3, alpha), (centerx, centery), rad_for)

# def blick():
#     global map_color
#     num_col = 8
#     while map_color < 100:
#         map_color += num_col
#         window.fill((map_color, map_color, map_color))
#         clock.tick(FPS)
#         pygame.display.update()
#     while map_color > 0:
#         map_color -= num_col
#         if map_color < 0:
#             map_color = 0
#         window.fill((map_color, map_color, map_color))
#         clock.tick(FPS)
#         pygame.display.update()
#     map_color = 0

def color_swap() -> None:
    """Reverse colors"""
    global map_color
    if space_pressed == 1:
        window.fill((255, 255, 255))
    else:
        window.fill((0, 0, 0))

if __name__ == "__main__":
    while play:
        ping1 = float(time.time())
        # отслеживание клиента
        mouse = pygame.mouse.get_pos()
        key = pygame.key.get_pressed()
        for event in pygame.event.get():   # ВКЛЮЧИТЬ ЕСЛИ ВСАСЫВАНИЕ ПО НАЖАТИЮ
                if event.type == pygame.QUIT:
                    play = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and clicked == 1:
                        if start == 1:
                            explosion(objects, mouse)
                        clicked = 0
                    elif clicked == 0:
                        clicked = 1
        map__color = int(map_color)
        
        if start == 1: # игра
            if key[pygame.K_SPACE] and float(time.time()) > start_time+0.5 and float(time.time()) > color_swap_cooldown+0.4:
                    color_swap_cooldown = float(time.time())
                    if space_pressed == 0:
                        space_pressed = 1
                    else:
                        space_pressed = 0
            color_swap()
            # отслеживание клиента
            mouse = pygame.mouse.get_pos()
            key = pygame.key.get_pressed()
            # window.fill(pygame.Color("black"))
            # отрисовка
            if bg_toggle:
                snow_effect_bg()
            obj_count = obj_count_func(objects)
            col = 255-obj_count
            if col < 0:
                col = 0
            font = pygame.font.SysFont('Comic Sans MS', 50)
            if space_pressed == 0:
                text = font.render(f'{obj_count}', True, (255, col, col))
            else:
                text = font.render(f'{obj_count}', True, (0, col, col))
            if obj_count > int(entered_volume/6) and clicked == 1:
                window.blit(text, (WIDTH/2-40,HEIGHT/2-30))
                score_update(obj_count)
            if int(float(time.time())) < start_time+5:
                font = pygame.font.SysFont('Comic Sans MS', 30)
                text = font.render(f'SPACE to color switch', True, (100, 100, 100))
                window.blit(text, (WIDTH/2-140, HEIGHT-50))
            snow_effect(objects, mouse)
            # print(offset_time)
            explosion_x(mouse)
            objects_draw()
            blackhole(objects, mouse)
            if mouse[1] < HEIGHT/5:
                move_forward()
            if mouse[1] > HEIGHT-HEIGHT/5:
                move_back()
            if mouse[0] < WIDTH/6:
                move_left()
            if mouse[0] > WIDTH-WIDTH/6:
                move_right()
            if mouse[1] > HEIGHT/5 and mouse[1] < HEIGHT-HEIGHT/5:
                y_step = 0
            if mouse[0] > WIDTH/6 and mouse[0] < WIDTH-WIDTH/6:
                x_step = 0
            font = pygame.font.SysFont('Comic Sans MS', 30)
            text = font.render(f'ESC to restart', True, (100, 100, 100))
            window.blit(text, (10, 10))
            font = pygame.font.SysFont('Comic Sans MS', 20)
            text = font.render(f'fps {str(current_fps)[:4]}', True, (100, 100, 100))
            if fps_counter == True:
                window.blit(text, (10, 40))
            if key[pygame.K_ESCAPE]:
                esccooldown = float(time.time())
                start = 0
                entered_volume = 0
                points_received = False
                objects = []
                map_color = 0
        elif start == 0: # меню
            window.fill((map__color, map__color, map__color))
            pygame.mouse.set_visible(True)
            if action == "play":
                clicked = 0
                if entered_volume == 0:
                    font = pygame.font.SysFont('Comic Sans MS', 30)
                    text = font.render(f'Enter objects volume:', True, (100, 100, 100))
                    window.blit(text, (WIDTH/2-150,HEIGHT/2-160))
                    pygame.draw.rect(window, (100, 100, 100), (WIDTH/2-90, HEIGHT/2-110, 180, 40))
                    if entered == "0":
                        if key[pygame.K_0] and float(time.time()) > float(cooldown0+sticky):
                            entered = "0"
                            cooldown0 = float(time.time())
                        if key[pygame.K_1] and float(time.time()) > float(cooldown1+sticky):
                            entered = "1"
                            cooldown1 = float(time.time())
                        if key[pygame.K_2] and float(time.time()) > float(cooldown2+sticky):
                            entered = "2"
                            cooldown2 = float(time.time())
                        if key[pygame.K_3] and float(time.time()) > float(cooldown3+sticky):
                            entered = "3"
                            cooldown3 = float(time.time())
                        if key[pygame.K_4] and float(time.time()) > float(cooldown4+sticky):
                            entered = "4"
                            cooldown4 = float(time.time())
                        if key[pygame.K_5] and float(time.time()) > float(cooldown5+sticky):
                            entered = "5"
                            cooldown5 = float(time.time())
                        if key[pygame.K_6] and float(time.time()) > float(cooldown6+sticky):
                            entered = "6"
                            cooldown6 = float(time.time())
                        if key[pygame.K_7] and float(time.time()) > float(cooldown7+sticky):
                            entered = "7"
                            cooldown7 = float(time.time())
                        if key[pygame.K_8] and float(time.time()) > float(cooldown8+sticky):
                            entered = "8"
                            cooldown8 = float(time.time())
                        if key[pygame.K_9] and float(time.time()) > float(cooldown9+sticky):
                            entered = "9"
                            cooldown9 = float(time.time())
                    else:
                        if key[pygame.K_0] and float(time.time()) > float(cooldown0+sticky):
                            entered = entered + "0"
                            cooldown0 = float(time.time())
                        if key[pygame.K_1] and float(time.time()) > float(cooldown1+sticky):
                            entered = entered + "1"
                            cooldown1 = float(time.time())
                        if key[pygame.K_2] and float(time.time()) > float(cooldown2+sticky):
                            entered = entered + "2"
                            cooldown2 = float(time.time())
                        if key[pygame.K_3] and float(time.time()) > float(cooldown3+sticky):
                            entered = entered + "3"
                            cooldown3 = float(time.time())
                        if key[pygame.K_4] and float(time.time()) > float(cooldown4+sticky):
                            entered = entered + "4"
                            cooldown4 = float(time.time())
                        if key[pygame.K_5] and float(time.time()) > float(cooldown5+sticky):
                            entered = entered + "5"
                            cooldown5 = float(time.time())
                        if key[pygame.K_6] and float(time.time()) > float(cooldown6+sticky):
                            entered = entered + "6"
                            cooldown6 = float(time.time())
                        if key[pygame.K_7] and float(time.time()) > float(cooldown7+sticky):
                            entered = entered + "7"
                            cooldown7 = float(time.time())
                        if key[pygame.K_8] and float(time.time()) > float(cooldown8+sticky):
                            entered = entered + "8"
                            cooldown8 = float(time.time())
                        if key[pygame.K_9] and float(time.time()) > float(cooldown9+sticky):
                            entered = entered + "9"
                            cooldown9 = float(time.time())
                        if key[pygame.K_BACKSPACE] and float(time.time()) > float(bcooldown+sticky):
                            entered = entered[:(len(str(entered))-1)]
                            bcooldown = float(time.time())
                    if int(len(str(entered))) > 1:
                        if int(entered) > 10000:
                            entered = "10000"
                        if key[pygame.K_RETURN]:
                            entered_volume = int(entered)
                            entered = "0"
                    if key[pygame.K_ESCAPE] and float(time.time()) > float(esccooldown+0.8):
                        action = "menu"
                        clicked = 0
                        esccooldown = float(time.time())
                    font = pygame.font.SysFont('Comic Sans MS', 30)
                    text = font.render(f'{entered}', True, (0, 0, 0))
                    window.blit(text, (WIDTH/2-60, HEIGHT/2-110))
                    text = font.render(f'ESC to back menu', True, (100, 100, 100))
                    window.blit(text, (10, 10))
                else:
                    count = entered_volume
                    font = pygame.font.SysFont('Comic Sans MS', 30)
                    text = font.render(f'SPACE to start', True, (100, 100, 100))
                    window.blit(text, (WIDTH/2-100,HEIGHT/2-30))
                    if key[pygame.K_SPACE]:
                        for i in range(count):
                            x, y = randint(0, WIDTH), randint(0, HEIGHT)
                            size = int(randint(int(size_min), int(size_limit)))
                            color = (255, 255, 255)
                            in_hole = False
                            objects.append([x, y, size, color, in_hole])
                        bg_objects = []
                        if bg_toggle:
                            for i in range(bg_objects_count): #bg
                                x, y = randint(0, WIDTH), randint(0, HEIGHT)
                                size = randint(80,250)
                                color = (15, 15, 15)
                                bg_objects.append([x, y, size, color])
                        y_step = 0
                        x_step = 0
                        start = 1
                        space_pressed == 0
                        start_time = float(time.time())
                          
            if action == "menu":
                clicked = 0
                space_pressed = 0
                menu_snow_generate()
                if bg_toggle:
                    snow_effect_bg()
                menu_snow_effect()

                if key[pygame.K_ESCAPE] and float(time.time()) > float(esccooldown+1.2):
                    try:
                        file = open(dir, 'w', encoding='utf-8')
                        file.write(f"{points}, {blackhole_power}, {max_blackhole_power}, {graphics}, {bg_toggle}, {fps_counter}")
                    except:
                        pass
                    pygame.quit()
                font = pygame.font.SysFont('Comic Sans MS', 30)
                text = font.render(f'ESC to exit', True, (100, 100, 100))
                window.blit(text, (10, 10))
                font = pygame.font.SysFont('Comic Sans MS', 18)
                text = font.render(f'By RyzerAfter', True, (100, 100, 100))
                window.blit(text, (10,HEIGHT-20))
                if mouse[1] < HEIGHT/2 and mouse[1] > HEIGHT/2-40:
                    font = pygame.font.SysFont('Comic Sans MS', 30)
                    text = font.render(f'Play', True, (255, 255, 255))
                    window.blit(text, (WIDTH/2-30,HEIGHT/2-40))
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        action = "play"
                        entered = "0"
                        clicked = 0
                        objects = []
                        menu_generated = False
                else:
                    font = pygame.font.SysFont('Comic Sans MS', 30)
                    text = font.render(f'Play', True, (100, 100, 100))
                    window.blit(text, (WIDTH/2-30,HEIGHT/2-40))
                if mouse[1] > HEIGHT/2 and mouse[1] < HEIGHT/2+40:
                    font = pygame.font.SysFont('Comic Sans MS', 30)
                    text = font.render(f'Upgrade', True, (255, 255, 255))
                    window.blit(text, (WIDTH/2-55,HEIGHT/2))
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        action = "upgrade"
                        clicked = 0
                        objects = []
                        menu_generated = False
                        entered = "0"
                else:
                    font = pygame.font.SysFont('Comic Sans MS', 30)
                    text = font.render(f'Upgrade', True, (100, 100, 100))
                    window.blit(text, (WIDTH/2-55,HEIGHT/2))
                if mouse[1] > HEIGHT/2+40 and mouse[1] < HEIGHT/2+80:
                    font = pygame.font.SysFont('Comic Sans MS', 30)
                    text = font.render(f'Settings', True, (255, 255, 255))
                    window.blit(text, (WIDTH/2-55,HEIGHT/2+40))
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        action = "settings"
                        clicked = 0
                        objects = []
                        menu_generated = False
                else:
                    font = pygame.font.SysFont('Comic Sans MS', 30)
                    text = font.render(f'Settings', True, (100, 100, 100))
                    window.blit(text, (WIDTH/2-55,HEIGHT/2+40))
                create_light(mouse[0], mouse[1], (100, 100, 100), 4, int(50))
            if action == "upgrade":
                clicked = 0
                font = pygame.font.SysFont('Comic Sans MS', 30)
                text = font.render(f'ESC to back menu', True, (100, 100, 100))
                window.blit(text, (10, 10))
                if key[pygame.K_ESCAPE] and float(time.time()) > float(esccooldown+sticky):
                        action = "menu"
                        entered = "0"
                        esccooldown = float(time.time())
                font = pygame.font.SysFont('Comic Sans MS', 30)
                text = font.render(f'Your points: {points}', True, (100, 100, 100))
                window.blit(text, (WIDTH/2-100, HEIGHT/2-120))
                if mouse[1] > HEIGHT/2-60 and mouse[1] < HEIGHT/2-20:
                    font = pygame.font.SysFont('Comic Sans MS', 25)
                    text = font.render(f'Upgrade blackhole power - 1000', True, (255, 255, 255))
                    window.blit(text, (WIDTH/2-180, HEIGHT/2-60))
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if points >= 1000 and float(time.time()) > float(buy_cooldown+sticky) and blackhole_power < 200:
                            points -= 1000
                            blackhole_power += 5
                            max_blackhole_power += 5
                            buy_cooldown = float(time.time())
                            clicked = 0
                else:
                    font = pygame.font.SysFont('Comic Sans MS', 25)
                    text = font.render(f'Upgrade blackhole power - 1000', True, (100, 100, 100))
                    window.blit(text, (WIDTH/2-180, HEIGHT/2-60))
                font = pygame.font.SysFont('Comic Sans MS', 30)
                text = font.render(f'Blackhole power: {blackhole_power}/{max_blackhole_power}', True, (100, 100, 100))
                window.blit(text, (WIDTH/2-170, HEIGHT/2-160))
                font = pygame.font.SysFont('Comic Sans MS', 30)
                text = font.render(f'Power settings', True, (100, 100, 100))
                window.blit(text, (WIDTH/2-100, HEIGHT/2+10))
                pygame.draw.rect(window, (50, 50, 50), (WIDTH/2-110, HEIGHT/2+60, 220, 30))
                if entered == "0":
                        if key[pygame.K_0] and float(time.time()) > float(cooldown0+sticky):
                            entered = "0"
                            cooldown0 = float(time.time())
                        if key[pygame.K_1] and float(time.time()) > float(cooldown1+sticky):
                            entered = "1"
                            cooldown1 = float(time.time())
                        if key[pygame.K_2] and float(time.time()) > float(cooldown2+sticky):
                            entered = "2"
                            cooldown2 = float(time.time())
                        if key[pygame.K_3] and float(time.time()) > float(cooldown3+sticky):
                            entered = "3"
                            cooldown3 = float(time.time())
                        if key[pygame.K_4] and float(time.time()) > float(cooldown4+sticky):
                            entered = "4"
                            cooldown4 = float(time.time())
                        if key[pygame.K_5] and float(time.time()) > float(cooldown5+sticky):
                            entered = "5"
                            cooldown5 = float(time.time())
                        if key[pygame.K_6] and float(time.time()) > float(cooldown6+sticky):
                            entered = "6"
                            cooldown6 = float(time.time())
                        if key[pygame.K_7] and float(time.time()) > float(cooldown7+sticky):
                            entered = "7"
                            cooldown7 = float(time.time())
                        if key[pygame.K_8] and float(time.time()) > float(cooldown8+sticky):
                            entered = "8"
                            cooldown8 = float(time.time())
                        if key[pygame.K_9] and float(time.time()) > float(cooldown9+sticky):
                            entered = "9"
                            cooldown9 = float(time.time())
                else:
                        if key[pygame.K_0] and float(time.time()) > float(cooldown0+sticky):
                            entered = entered + "0"
                            cooldown0 = float(time.time())
                        if key[pygame.K_1] and float(time.time()) > float(cooldown1+sticky):
                            entered = entered + "1"
                            cooldown1 = float(time.time())
                        if key[pygame.K_2] and float(time.time()) > float(cooldown2+sticky):
                            entered = entered + "2"
                            cooldown2 = float(time.time())
                        if key[pygame.K_3] and float(time.time()) > float(cooldown3+sticky):
                            entered = entered + "3"
                            cooldown3 = float(time.time())
                        if key[pygame.K_4] and float(time.time()) > float(cooldown4+sticky):
                            entered = entered + "4"
                            cooldown4 = float(time.time())
                        if key[pygame.K_5] and float(time.time()) > float(cooldown5+sticky):
                            entered = entered + "5"
                            cooldown5 = float(time.time())
                        if key[pygame.K_6] and float(time.time()) > float(cooldown6+sticky):
                            entered = entered + "6"
                            cooldown6 = float(time.time())
                        if key[pygame.K_7] and float(time.time()) > float(cooldown7+sticky):
                            entered = entered + "7"
                            cooldown7 = float(time.time())
                        if key[pygame.K_8] and float(time.time()) > float(cooldown8+sticky):
                            entered = entered + "8"
                            cooldown8 = float(time.time())
                        if key[pygame.K_9] and float(time.time()) > float(cooldown9+sticky):
                            entered = entered + "9"
                            cooldown9 = float(time.time())
                        if key[pygame.K_BACKSPACE] and float(time.time()) > float(bcooldown+sticky):
                            entered = entered[:(len(str(entered))-1)]
                            bcooldown = float(time.time())
                if int(len(str(entered))) > 1:
                    if key[pygame.K_RETURN]:
                        if int(entered) > max_blackhole_power:
                            entered = str(max_blackhole_power)
                        if int(entered) < 60:
                            entered = "60"
                        blackhole_power = int(entered)
                font = pygame.font.SysFont('Comic Sans MS', 30)
                text = font.render(f'{entered}', True, (0, 0, 0))
                window.blit(text, (WIDTH/2-30, HEIGHT/2+50))
                create_light(mouse[0], mouse[1], (100, 100, 100), 4, int(50))
            if action == "settings":
                clicked = 0
                font = pygame.font.SysFont('Comic Sans MS', 30)
                text = font.render(f'ESC to back menu', True, (100, 100, 100))
                window.blit(text, (10, 10))
                if key[pygame.K_ESCAPE] and float(time.time()) > float(esccooldown+0.5):
                        action = "menu"
                        esccooldown = float(time.time())
                font = pygame.font.SysFont('Comic Sans MS', 30)
                graphics_switch = "On"
                if graphics:
                    graphics_switch = "On"
                else:
                    graphics_switch = "Off"
                if bg_toggle:
                    bg_toggle_text = "On"
                else:
                    bg_toggle_text = "Off"
                if fps_counter:
                    fps_counter_text = "On"
                else:
                    fps_counter_text = "Off"
                if mouse[1] > HEIGHT/2-10 and mouse[1] < HEIGHT/2+20:
                    font = pygame.font.SysFont('Comic Sans MS', 25)
                    text = font.render(f'Glowing: {graphics_switch}', True, (255, 255, 255))
                    window.blit(text, (WIDTH/2-50, HEIGHT/2-15))
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if float(time.time()) > float(int(graphics_switch_cooldown)+0.7):
                            # print("clicked")
                            if graphics:
                                graphics = False
                            else:
                                graphics = True
                            graphics_switch_cooldown = float(time.time())
                            clicked = 0
                else:
                    font = pygame.font.SysFont('Comic Sans MS', 25)
                    text = font.render(f'Glowing: {graphics_switch}', True, (100, 100, 100))
                    window.blit(text, (WIDTH/2-50, HEIGHT/2-15))
                if mouse[1] > HEIGHT/2+20 and mouse[1] < HEIGHT/2+45:
                    font = pygame.font.SysFont('Comic Sans MS', 25)
                    text = font.render(f'Background: {bg_toggle_text}', True, (255, 255, 255))
                    window.blit(text, (WIDTH/2-70, HEIGHT/2+15))
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if float(time.time()) > float(int(graphics_switch_cooldown)+0.7):
                            # print("clicked")
                            if bg_toggle:
                                bg_toggle = False
                            else:
                                bg_toggle = True
                            graphics_switch_cooldown = float(time.time())
                            clicked = 0
                else:
                    font = pygame.font.SysFont('Comic Sans MS', 25)
                    text = font.render(f'Background: {bg_toggle_text}', True, (100, 100, 100))
                    window.blit(text, (WIDTH/2-70, HEIGHT/2+15))
                if mouse[1] > HEIGHT/2+50 and mouse[1] < HEIGHT/2+70:
                    font = pygame.font.SysFont('Comic Sans MS', 25)
                    text = font.render(f'FPS counter: {fps_counter_text}', True, (255, 255, 255))
                    window.blit(text, (WIDTH/2-70, HEIGHT/2+45))
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if float(time.time()) > float(int(fps_counter_switch_cooldown)+0.7):
                            # print("clicked")
                            if fps_counter:
                                fps_counter = False
                            else:
                                fps_counter = True
                            fps_counter_switch_cooldown = float(time.time())
                            clicked = 0
                else:
                    font = pygame.font.SysFont('Comic Sans MS', 25)
                    text = font.render(f'FPS counter: {fps_counter_text}', True, (100, 100, 100))
                    window.blit(text, (WIDTH/2-70, HEIGHT/2+45))
                font = pygame.font.SysFont('Comic Sans MS', 25)
                text = font.render(f'Settings', True, (100, 100, 100))
                window.blit(text, (WIDTH/2-35, HEIGHT/2-65))
                create_light(mouse[0], mouse[1], (100, 100, 100), 4, int(50))
        
        pygame.display.update()
        ping2 = float(time.time())
        offset_time = ping2 - ping1
        pygame.event.pump()
        current_fps = clock.get_fps()
        clock.tick(FPS) 

    pygame.quit()