import pygame
import random
import time
import RPi.GPIO as GPIO
from mpu6050 import is_shaken
from animation import load_frames_from_folder
from constants import *
from aim import *
from buzzer import dice_roll_sound, win_sound, hit_enemy, lose_sound, beep



# start pygame
pygame.init()



# roll the dice between 1 to 6
def roll_dice():
    return random.randint(1, 6)
    
    
#download animation from the folder
idle_frames = load_frames_from_folder('images/MiniPrinceMan_idle2')
idle_frames_bt = load_frames_from_folder('images/MiniPrinceMan_idle2_bt')
walk_frames = load_frames_from_folder('images/MiniPrinceMan_walk2')
enemy_idle_frames = load_frames_from_folder('images/MiniZombieMan_idle2')
boss_idle_frames = load_frames_from_folder('images/Boss_idle')
#download attack animation
attack_frames = load_frames_from_folder('images/MiniPrinceMan_attack') 

dice_animation_1= load_frames_from_folder('images/dice_animation/dice_1')
dice_animation_2= load_frames_from_folder('images/dice_animation/dice_2') 
dice_animation_3= load_frames_from_folder('images/dice_animation/dice_3') 
dice_animation_4= load_frames_from_folder('images/dice_animation/dice_4') 
dice_animation_5= load_frames_from_folder('images/dice_animation/dice_5') 
dice_animation_6= load_frames_from_folder('images/dice_animation/dice_6')   
dice_faces = [dice_animation_1, dice_animation_2, dice_animation_3, dice_animation_4, dice_animation_5, dice_animation_6]

# variable for attacking
attacking = False
attack_frame_counter = 0
background_image = pygame.image.load('mapp.png').convert()
bg_dice = pygame.image.load('bg_dice.png').convert()

dice_roll_sound = pygame.mixer.Sound('sound/sound_dice.mp3')
battle_screen_sound = pygame.mixer.Sound('sound/sound_battle.mp3')
rolling_dice = False

# initialize general animation
current_animation = 'idle'
current_frames = idle_frames
current_frame = 0
animation_speed = 10  
frame_counter = 0

#initialize enemy animation
enemy_frame_counter = 0
enemy_current_frame = 0
enemy_animation_speed = 10  

boss_position = 13
boss_hp = 10



#variable for dice value
dice_value = 0
steps_remaining = 0
current_tile = 0  #set the start tile
rolled_dice_value = 0
dice_rolling_start_time = 0

game_state = "map" 
encountered_enemy_pos = None  # keep the position that found enemy

#variable to keep power of player and enemy
player_power = 0  
enemy_power = 0   
power_increase = 5  
enemy_power_increase_rate = 0.05 
#Download target image and aim
target_image = pygame.image.load('images/target.png').convert_alpha() 
boss_target_image = pygame.image.load('images/boss_target.png').convert_alpha() 
aim_image = pygame.image.load('images/aim.png').convert_alpha() 
ready_image = pygame.image.load('images/ready_to_battle.png').convert_alpha()  
ready_image_rect = ready_image.get_rect(center=(1280 // 2, 720 // 2))  # set the image to center


target_width, target_height = target_image.get_size()
aim_width, aim_height = aim_image.get_size()

#position of target and aim
target_x = random.randint(target_width // 2, 800 - target_width // 2)
target_y = 300  
aim_x, aim_y = 800 // 2, 600 // 2

screen_width, screen_height = 1280, 720
screen = pygame.display.set_mode((screen_width, screen_height))
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# set width and height to according to screen_width and screen_height
width, height = screen_width, screen_height
target_radius = 20
target_position = (random.randint(target_radius, screen_width - target_radius),
                   random.randint(target_radius, screen_height - target_radius))
aim_x, aim_y = 1280 // 2, 720 // 2
time_on_target = 0
target_locked_time =  80  # 3 วินาทีที่ต้องเล็งตรงกับเป้าหมายเพื่อทำคะแนน
target_x = random.randint(target_radius, width - target_radius)  #randomize the target position in x axis
target_y = aim_y  # กำหนดให้เป้าหมายอยู่ในแนวเดียวกับจุดเล็ง

player_lives = 3

button_pin = 23
GPIO.setmode(GPIO.BCM)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# เริ่มต้น GPIO สำหรับการควบคุม LED
led_pins = [17, 27, 22]  # GPIO ที่ใช้ควบคุม LED (สมมติว่าคุณใช้ GPIO 17, 27, 22 สำหรับ LED 3 ดวง)
GPIO.setmode(GPIO.BCM)
for pin in led_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

# ฟังก์ชันสำหรับอัปเดต LED ตามจำนวนชีวิตที่เหลืออยู่ของผู้เล่น
def update_lives_led(lives_remaining):
    print(lives_remaining)
    for i in range(3):
        if i < lives_remaining:
            GPIO.output(led_pins[i], GPIO.LOW)  # เปิด LED ถ้าชีวิตยังเหลือ
            print(led_pins[i])
        else:
            GPIO.output(led_pins[i], GPIO.HIGH)   # ปิด LED ถ้าชีวิตหมด
    

            
def wait_for_button_press():
    print("Waiting for button press to start battle...")
    # แสดงภาพพร้อมข้อความให้ผู้เล่นทราบว่าต้องกดปุ่ม
    waiting = True
    while waiting:
        screen.blit(ready_image, ready_image_rect)  # แสดงภาพเตรียมพร้อมเข้าสู่การต่อสู้
        pygame.display.flip()  # อัพเดตหน้าจอแสดงผล
        if GPIO.input(button_pin) == GPIO.HIGH:  # ตรวจสอบว่าปุ่มถูกกดหรือไม่
            waiting = False
            print("Button pressed! Starting battle.")
        time.sleep(0.1)

def start_button():
    print("Waiting for button press to start battle...")

    waiting = True
    while waiting:
        # ล้างหน้าจอและทำให้เป็นสีดำ
        screen.fill((0, 0, 0))  # สีดำเต็มหน้าจอ

        # แสดงภาพเตรียมพร้อม (ready image)
        screen.blit(ready_image, ready_image_rect)

        # เพิ่มข้อความแนะนำให้กดปุ่มเพื่อเริ่มเกม
        instruction_font = pygame.font.Font(None, 36)
        instruction_text = instruction_font.render("Press the button to start", True, (255, 255, 255))  # ข้อความสีขาว
        instruction_rect = instruction_text.get_rect(center=(screen_width // 2, screen_height // 2 + 100))
        screen.blit(instruction_text, instruction_rect)

        # อัพเดตหน้าจอ
        pygame.display.flip()

        # ตรวจสอบการกดปุ่ม
        if GPIO.input(button_pin) == GPIO.HIGH:
            waiting = False
            print("Button pressed! Starting the game.")

        time.sleep(0.1)  # เพิ่ม delay เล็กน้อยเพื่อไม่ให้ลูปทำงานหนักเกินไป
        
def roll_dice_animation():
    animation_duration = 3000  # ระยะเวลาการแสดงผลแอนิเมชันทั้งหมด (เช่น 4 วินาที)
    frame_delay = animation_duration // 3  # เวลาที่แต่ละเฟรมแสดงผล (แบ่งเท่าๆ กัน)
    start_time = pygame.time.get_ticks()

    current_frame = 0

    # ขนาดของลูกเต๋า (สมมติว่าภาพลูกเต๋าแต่ละหน้ามีขนาดเท่ากัน)
    dice_width, dice_height = dice_faces[0][0].get_size()

    # คำนวณตำแหน่งให้อยู่ตรงกลางบน
    dice_x = (screen_width - dice_width) // 2
    dice_y = (screen_height - dice_height) //2

    # แสดงแอนิเมชันของลูกเต๋าจนกว่าจะครบ 4 เฟรม
    for i in range(3):  # แสดงทั้งหมด 4 เฟรม
        # เคลียร์หน้าจอก่อนที่จะวาดภาพใหม่
        screen.blit(bg_dice, (0, 0))  # สมมติว่า background_image คือภาพพื้นหลังที่คุณใช้

        current_animation = dice_animation_1
        screen.blit(current_animation[current_frame], (dice_x, dice_y))
        pygame.display.flip()

        # รอเป็นเวลา frame_delay เพื่อให้แอนิเมชันดูช้าและชัดเจน
        pygame.time.delay(frame_delay)
        current_frame += 1

        # จัดการเหตุการณ์เพื่อไม่ให้หน้าจอค้าง
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    # ทอยลูกเต๋าเพื่อหาผลลัพธ์จริง
    dice_value = random.randint(1, 6)

    # แสดงเฟรมสุดท้ายที่ตรงกับผลลัพธ์
    screen.blit(bg_dice, (0, 0))  # เคลียร์หน้าจอก่อนที่จะวาดภาพใหม่
    final_animation = dice_faces[dice_value - 1]
    screen.blit(final_animation[-1], (dice_x, dice_y))
    pygame.display.flip()
    pygame.time.delay(2000)  # แสดงผลลูกเต๋าสุดท้ายเป็นเวลา 1 วินาที

    return dice_value



# ฟังก์ชันวาดหลอดพลังบนหน้าจอ
def draw_power_bars():
    # วาดหลอดพลังของศัตรู (ให้เต็มภายใน 100 คะแนน)
    enemy_bar_width = min(enemy_power * 2, 200)  # จำกัดหลอดพลังศัตรูที่ 200 (เท่ากับผู้เล่น)
    pygame.draw.rect(screen, BLUE, (screen_width // 4 * 3 - 150, screen_height // 2 + 50, enemy_bar_width, 20))
    pygame.draw.rect(screen, BLACK, (screen_width // 4 * 3 - 150, screen_height // 2 + 50, 200, 20), 2)

# ฟอนต์สำหรับแสดงผลลัพธ์
font = pygame.font.Font(None, 36)

# ฟังก์ชันตรวจสอบว่ามีศัตรูในระยะการเคลื่อนที่หรือไม่
def find_enemy_in_path(player_pos, dice_value, enemy_positions):
    global boss_position
    new_pos = player_pos + dice_value
    for enemy_pos in enemy_positions:
        if player_pos < enemy_pos <= new_pos:  # ศัตรูอยู่ในระหว่างที่ผู้เล่นเดินผ่าน
            return enemy_pos
        elif player_pos < boss_position <= new_pos:
            return enemy_pos
    return None


# ฟังก์ชันวาดลูกกลมเป้าหมายในโหมดการต่อสู้
def draw_target_circle():
    pygame.draw.circle(screen, BLUE, target_position, target_radius)

# ฟังก์ชันคำนวณมุมจากข้อมูล accelerometer
def calculate_roll(acc_data):
    ax = acc_data['x']
    ay = acc_data['y']
    az = acc_data['z']
    roll = math.atan2(ay, az) * (180 / math.pi)  # คำนวณ roll จากแกน Y และ Z
    return roll
    
# ฟังก์ชันวาดจุดเล็งของผู้เล่น
idle_frame_counter = 0  # เพิ่มตัวนับเฟรมสำหรับ idle frames

def draw_aiming_point(surface, roll):
    global aim_x, attack_frame_counter, attack_frames, attacking, idle_frames, idle_frame_counter

    # ปรับการเคลื่อนที่เฉพาะทิศทางซ้าย-ขวา
    x_offset = int(roll * sensitivity)

    # อัปเดตตำแหน่งของจุดเล็ง
    aim_x += x_offset

    # ทำให้จุดเล็งอยู่ภายในขอบเขตของหน้าจอ
    aim_x = max(0, min(1280 - aim_width, aim_x))

    if attacking:
        # แสดงแอนิเมชันการโจมตี
        if attack_frame_counter < len(attack_frames):
            character_image = attack_frames[attack_frame_counter]
            surface.blit(character_image, (aim_x, aim_y - aim_height // 2))
            attack_frame_counter += 1
        else:
            attack_frame_counter = 0  # เริ่มแอนิเมชันใหม่หากยังโจมตีอยู่ในรัศมี
    else:
        # แสดงแอนิเมชัน Idle
        if idle_frame_counter < len(idle_frames_bt):
            character_image = idle_frames_bt[idle_frame_counter]
            surface.blit(character_image, (aim_x, aim_y - aim_height // 2))
            idle_frame_counter += 1
        else:
            idle_frame_counter = 0  # รีเซ็ตแอนิเมชัน Idle


# ฟังก์ชันแสดงผลการต่อสู้ (แก้ไขสำหรับบอส)
def battle_screen():
    global player_power, enemy_power, target_x, target_y, aim_x, aim_y, time_on_target, game_state, encountered_enemy_pos
    global enemy_positions, player_lives, player_previous_pos, steps_remaining, player_pos, attack_frame_counter, attack_frames, attacking, boss_hp, boss_position

    if game_state == "battle" and encountered_enemy_pos is not None:
        player_previous_pos = player_pos - 1

    print(player_previous_pos)
    print(player_pos)

    screen.fill(BLACK)
    battle_text = font.render("BATTLE MODE", True, WHITE)
    screen.blit(battle_text, (width // 2 - 100, height // 2 - 100))

    # วาดเป้าหมาย
    
    if encountered_enemy_pos == boss_position:
        screen.blit(boss_target_image, (target_x - target_width // 2, target_y - target_height // 2))
    else:
        screen.blit(target_image, (target_x - target_width // 2, target_y - target_height // 2))

    # อ่านข้อมูลจาก MPU6050
    accel_data = sensor.get_accel_data()
    roll = calculate_roll(accel_data)

    # วาดจุดเล็งของผู้เล่น
    draw_aiming_point(screen, roll)

    # ตรวจสอบการเล็งเป้าหมาย
    distance = math.sqrt((aim_x + aim_width // 2 - target_x) ** 2 + (aim_y - target_y) ** 2)
    if distance <= target_radius + 10:
        time_on_target += 1
        print(time_on_target)

        # เริ่มต้นแอนิเมชันการโจมตี
        if not attacking:
            attacking = True
    else:
        time_on_target = 0
        attacking = False  # หยุดแอนิเมชันโจมตีเมื่อออกจากรัศมี

    # วาดหลอดเวลาที่เล็งเป้าหมาย
    progress_percentage = min(time_on_target / target_locked_time, 1.0)  # จำกัดค่าสูงสุดที่ 1.0 (100%)
    bar_width = int(progress_percentage * 200)  # ความกว้างของหลอดจะเป็นไปตามเปอร์เซ็นต์ที่เล็งได้
    pygame.draw.rect(screen, GREEN, (width // 2 - 100, height // 2 + 100, bar_width, 20))
    pygame.draw.rect(screen, WHITE, (width // 2 - 100, height // 2 + 100, 200, 20), 2)

    # เมื่อเล็งตรงกับเป้าหมายครบ 3 วินาที
    if time_on_target >= target_locked_time:
        player_power += 1
        hit_enemy()
        print(f"Player power: {player_power}")
        time_on_target = 0
        # สุ่มตำแหน่งใหม่ของเป้าหมาย
        target_x = random.randint(target_width // 2, 800 - target_width // 2)

    # แสดงคะแนนของผู้เล่นบนหน้าจอ
    score_text = font.render(f"Score: {player_power}", True, WHITE)
    screen.blit(score_text, (10, 10))  # แสดงที่มุมซ้ายบนของหน้าจอ

    # วาดหลอดพลังของศัตรูในฟังก์ชัน battle_screen
    enemy_power_bar_width = min(enemy_power, 200)  # จำกัดความกว้างสูงสุดที่ 200 หน่วย
    pygame.draw.rect(screen, RED, (width // 2 - 100, height // 2 + 150, enemy_power_bar_width * 2, 20))
    pygame.draw.rect(screen, WHITE, (width // 2 - 100, height // 2 + 150, 200, 20), 2)

    # เพิ่มพลังของศัตรูอัตโนมัติ
    enemy_power += enemy_power_increase_rate
    if enemy_power >= 100:  # ศัตรูชนะ
        print("Enemy wins!")
        # รีเซ็ตพลังของผู้เล่นและศัตรูหลังจากศัตรูชนะ
        player_power = 0
        enemy_power = 0
        game_state = "map"  # กลับไปโหมดแผนที่
        player_lives -= 1  # ลดจำนวนชีวิตของผู้เล่น
        print(f"Player lost a life! Lives remaining: {player_lives}")
        lose_sound()
        update_lives_led(player_lives)  # อัปเดต LED แสดงชีวิตที่เหลืออยู่
        live_text = font.render(f"{player_lives}", True, WHITE)
        screen.blit(live_text, (20, 30))
        steps_remaining = 0
        player_pos = player_previous_pos
        print(player_previous_pos)
        print(player_pos)

    # ตรวจสอบว่าผู้เล่นชนะหรือไม่
    if player_power >= (5 if encountered_enemy_pos == boss_position else 3):
        if encountered_enemy_pos == boss_position:
            print("Player defeated the boss!")
        else:
            print("Player wins!")

        win_sound()
        # รีเซ็ตค่าพลังและสถานะเกม
        player_power = 0
        game_state = "map"
        battle_screen_sound.stop()
        if encountered_enemy_pos != boss_position:
            enemy_positions.pop(0)  # ลบศัตรูที่ไม่ใช่บอสออกจากแผนที่
        else:
            boss_hp = 10  # รีเซ็ตพลังชีวิตบอส
        return  # ออกจากฟังก์ชันเพื่อหยุดการวาด battle screen

    pygame.display.flip()
    battle_screen_sound.play()

# วนลูปเกม
running = True
start_button()

while running:
    # screen.fill(WHITE)
    update_lives_led(player_lives)
    screen.blit(background_image, (0, 0))
    live_text = font.render(f"x {player_lives}", True, WHITE)
    screen.blit(live_text, (70, 25))
    
    # วาดข้อความลูกเต๋าหากทอยเสร็จแล้ว
    if not rolling_dice:
        dice_text = font.render(f"{rolled_dice_value}", True, WHITE)
        screen.blit(dice_text, (670, 28))

    # ตรวจสอบสถานะเกม
    if game_state == "map":
        # วาดช่องสี่เหลี่ยมบนแผนที่
        #for tile in map_tiles:
            #pygame.draw.rect(screen, BLACK, (tile[0], tile[1], tile_size, tile_size), 2)

        # วาดศัตรูในช่องที่กำหนด
        enemy_frame_counter += 1
        if enemy_frame_counter >= enemy_animation_speed:
            if len(enemy_idle_frames) > 0:
                enemy_current_frame = (enemy_current_frame + 1) % len(enemy_idle_frames)
            enemy_frame_counter = 0

        for enemy_pos in enemy_positions:
            if len(enemy_idle_frames) > 0 and 0 <= enemy_current_frame < len(enemy_idle_frames):
                enemy_image = enemy_idle_frames[enemy_current_frame]
                enemy_rect = enemy_image.get_rect(center=(map_tiles[enemy_pos][0] + tile_size // 2, map_tiles[enemy_pos][1] + tile_size // 2))
                screen.blit(enemy_image, enemy_rect)
        
        if enemy_frame_counter >= enemy_animation_speed:
            if len(boss_idle_frames) > 0:
                enemy_current_frame = (enemy_current_frame + 1) % len(boss_idle_frames)
            enemy_frame_counter = 0

        # วาดบอสที่ตำแหน่งบอส
        if len(boss_idle_frames) > 0 and 0 <= enemy_current_frame < len(boss_idle_frames):
            boss_image = boss_idle_frames[enemy_current_frame]
            boss_rect = boss_image.get_rect(center=(map_tiles[boss_position][0] + tile_size // 2, map_tiles[boss_position][1] + tile_size // 2))
            screen.blit(boss_image, boss_rect)

        # วาดไอเทมฟื้นฟู HP ในช่องที่กำหนด
        for item_pos in item_positions:
            pygame.draw.rect(screen, GREEN, (map_tiles[item_pos][0], map_tiles[item_pos][1], tile_size, tile_size))

        # เคลื่อนที่ผู้เล่นถ้ามีการทอยลูกเต๋าแล้ว
        if steps_remaining > 0:
            current_animation = 'walk'
            current_frames = walk_frames

            current_time = pygame.time.get_ticks()
            if current_time - last_step_time >= 1000:  # ถ้าเวลาผ่านไปมากกว่า 1 วินาที
                player_pos += 1
                steps_remaining -= 1
                last_step_time = current_time

                if player_pos >= num_tiles:
                    player_pos = num_tiles - 1

                current_tile = player_pos  # อัปเดต current_tile ให้เป็นตำแหน่งปัจจุบันของตัวละคร

                # ตรวจสอบว่าผู้เล่นเดินไปถึงตำแหน่งศัตรูแล้วหรือยัง
                if encountered_enemy_pos is not None and player_pos == encountered_enemy_pos:
                    # เมื่อเดินถึงศัตรูแล้ว ให้เข้าสู่โหมดต่อสู้
                    player_previous_pos = 0
                    player_previous_pos = player_pos - 1
                    player_dice_value = 0  # กำหนดค่าเริ่มต้น
                    enemy_dice_value = 0  # กำหนดค่าเริ่มต้น
                    player_power = 0  # รีเซ็ตพลังผู้เล่น
                    enemy_power = 0  # รีเซ็ตพลังศัตรู
                    game_state = "battle"
                    current_enemy_hp = boss_hp if encountered_enemy_pos == boss_position else 5  # พลังชีวิตของศัตรูหรือบอส
                    encountered_enemy_pos = None
                    wait_for_button_press()

        if steps_remaining == 0:
                current_animation = 'idle'
                current_frames = idle_frames

        # อัปเดตเฟรมแอนิเมชัน
        frame_counter += 1
        if frame_counter >= animation_speed:
            # ตรวจสอบว่า current_frames มีเฟรมก่อนที่จะอัปเดต current_frame
            if len(current_frames) > 0:
                current_frame = (current_frame + 1) % len(current_frames)
            frame_counter = 0

        # วาดตัวละครที่เป็นแอนิเมชัน
        if len(current_frames) > 0 and 0 <= current_frame < len(current_frames):
            character_image = current_frames[current_frame]
            character_rect = character_image.get_rect(center=(map_tiles[player_pos][0] + tile_size // 2, map_tiles[player_pos][1] + tile_size // 2))
            screen.blit(character_image, character_rect)

    elif game_state == "battle":
        
        battle_screen()  # แสดงผลหน้าจอการต่อสู้

        #if player_power >= 200:  # ผู้เล่นชนะ
            #print("Player wins!")
            #enemy_positions.pop(0)  # ลบศัตรูออกจากแผนที่
            #player_power = 0  # รีเซ็ตค่าพลังของผู้เล่น
            #enemy_power = 0  # รีเซ็ตค่าพลังของศัตรู
            #game_state = "map"  # กลับไปโหมดแผนที่
            #battle_screen_sound.stop()

    # ตรวจสอบเหตุการณ์ต่างๆ
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # ตรวจสอบการเขย่า MPU6050 เพื่อทอยลูกเต๋า
    if game_state == "map" and not rolling_dice:
        if is_shaken():
            # เขย่าเพื่อทอยลูกเต๋า
            dice_value = roll_dice_animation()
            #beep(1200, 0.1)  # ความถี่ 1200 Hz
            #time.sleep(0.05)  # หยุดสั้น ๆ เพื่อทำให้เหมือนเสียงหมุน
            #beep(1400, 0.1)  # ความถี่ 1400 Hz
            #time.sleep(0.05)  # หยุดสั้น ๆ
            rolled_dice_value = dice_value
            dice_roll_sound.play()
            rolling_dice = True  # ตั้งสถานะการทอยลูกเต๋า
            dice_rolling_start_time = pygame.time.get_ticks()  # เก็บเวลาที่เริ่มทอยลูกเต๋า
            print(f"Dice: {dice_value}")

            # ตรวจสอบว่ามีศัตรูในเส้นทางที่จะเดินหรือไม่
            enemy_in_path = find_enemy_in_path(player_pos, dice_value, enemy_positions)
            
            if enemy_in_path is not None:
                print(f"Encountered an enemy in path at position {enemy_in_path}!")
                encountered_enemy_pos = enemy_in_path  # เก็บตำแหน่งศัตรูที่พบเจอ

    # ใน loop หลักของเกม (while running:)
    current_time = pygame.time.get_ticks()
    if rolling_dice and current_time - dice_rolling_start_time > 500:  # ถ้าผ่านไปมากกว่า 2 วินาที
        rolling_dice = False  # เสียงทอยลูกเต๋าเล่นจบแล้ว
        steps_remaining = dice_value  # เริ่มการเดิน
        last_step_time = pygame.time.get_ticks()  # ตั้งเวลาของการเดิน

    # อัพเดตหน้าจอ
    pygame.display.flip()

# ออกจาก pygame  
pygame.quit()
GPIO.cleanup() 