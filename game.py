import random
import math
WIDTH = 840
HEIGHT = 630
TILE_SIZE = 70
WALL_THICKNESS = TILE_SIZE
HALF_TILE = TILE_SIZE // 2
TILES_X = WIDTH // TILE_SIZE
TILES_Y = HEIGHT // TILE_SIZE
SCENARIO_WIDTH = WIDTH
SCENARIO_HEIGHT = HEIGHT
OFFSET_X = 0
OFFSET_Y = 0
SCENARIO_LEFT = OFFSET_X + WALL_THICKNESS
SCENARIO_RIGHT = OFFSET_X + SCENARIO_WIDTH - WALL_THICKNESS
SCENARIO_TOP = OFFSET_Y + WALL_THICKNESS
SCENARIO_BOTTOM = OFFSET_Y + SCENARIO_HEIGHT - WALL_THICKNESS
COLLISION_LEFT = OFFSET_X
COLLISION_RIGHT = OFFSET_X + SCENARIO_WIDTH
COLLISION_TOP = OFFSET_Y
COLLISION_BOTTOM = OFFSET_Y + SCENARIO_HEIGHT
PLAYER_SCALE = 0.7
ZOMBIE_SCALE = 0.7
SOUNDS_ON_OF = True
GAME_STATE = "MENU"
PLAYER_LIVES = 3
GAME_OVER_ZOMBIE = None
GAME_OVER_FRAME = 0
ZOMBIES_KILLED = 0
ZOMBIES_TO_WIN = 10
GAME_WIN_FRAME = 0
GAME_OVER_SOUND_PLAYED = False
GAME_WIN_SOUND_PLAYED = False
ACTIVE_ZOMBIES = []
MAX_ZOMBIES = 15
ZOMBIE_SPAWN_INTERVAL = 2.0
PLAYER_INPUT = ""
ZOMBIE_WALK_FRAMES = ['zombie_walk1', 'zombie_walk2']
ZOMBIE_WALK_FRAMES_LEFT = ['zombie_walk1_flip', 'zombie_walk2_flip']
ZOMBIE_ACTION_FRAMES = ['zombie_action1', 'zombie_action2']
ZOMBIE_ACTION_FRAMES_LEFT = ['zombie_action1_flip', 'zombie_action2_flip']
ZOMBIE_CHEER_FRAMES = ['zombie_cheer1', 'zombie_cheer2']
ZOMBIE_SPEED = 1
ZOMBIE_ATTACK_RANGE = 60
player_facing_left = False
zombie_facing_left = False
is_moving = False
is_attacking = False
is_hurt = False
PLAYER_CAN_BE_HURT = True
current_frame = 0
flicker_timer = 0.0
WALKING_FRAMES_RIGHT = ['player_walk1', 'player_walk2']
WALKING_FRAMES_LEFT = ['player_walk1_flip', 'player_walk2_flip']
ACTION_FRAMES = ['player_action1', 'player_action2']
ACTION_FRAMES_LEFT = ['player_action1_flip', 'player_action2_flip']
PLAYER_CHEER_FRAMES = ['player_cheer1', 'player_cheer2']
HURT_SPRITE = 'player_hurt'
STAND_FRAMES = ['player_stand', 'player_stand2']


try:
    from pgzero.actor import Actor
    player = Actor('player_stand')
    player.scale = PLAYER_SCALE
    player.x = (SCENARIO_LEFT + SCENARIO_RIGHT) // 2
    player.y = (SCENARIO_TOP + SCENARIO_BOTTOM) // 2
except NameError:
    class MockActor:
        def __init__(self):
            self.x = 0
            self.y = 0
            self.scale = 0
            self.image = ''
            self.right = 0
            self.left = 0
            self.bottom = 0
            self.top = 0
            self.height = 0
        def distance_to(self, other): return 0
        def colliderect(self, other): return False
        def draw(self): pass
        def angle_to(self, other): return 0
    player = MockActor()

SCENARIO = []

def toggle_sound():
    global SOUNDS_ON_OF
    SOUNDS_ON_OF = not SOUNDS_ON_OF
    if SOUNDS_ON_OF == True:
        try:
            sounds.mouse_click.play()
        except NameError:
            pass
            
def start_game():
    global GAME_STATE
    if SOUNDS_ON_OF == True:
        try:
            sounds.mouse_click.play()
        except NameError:
            pass
    restart_game()
    GAME_STATE = "PLAYING"

def show_instructions():
    global GAME_STATE
    if SOUNDS_ON_OF == True:
        try:
            sounds.mouse_click.play()
        except NameError:
            pass
    GAME_STATE = "INSTRUCTIONS"

def exit_game():
    if SOUNDS_ON_OF == True:
        try:
            sounds.mouse_click.play()
        except NameError:
            pass
    print("O jogo foi encerrado.")
    try:
        quit()
    except:
        exit()


def generate_equation():
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    if random.choice([True, False]) and num1 >= num2:
        op = '-'
        result = num1 - num2
    else:
        op = '+'
        result = num1 + num2
    return {'text': f"{num1} {op} {num2}", 'result': result}
    
def spawn_zombie():
    if len(ACTIVE_ZOMBIES) >= MAX_ZOMBIES or GAME_STATE != "PLAYING":
        return
    while True:
        tile_x = random.randrange(SCENARIO_LEFT, SCENARIO_RIGHT, TILE_SIZE)
        tile_y = random.randrange(SCENARIO_TOP, SCENARIO_BOTTOM, TILE_SIZE)
        try:
            temp_zombie = Actor('zombie_stand')
            temp_zombie.x = tile_x + HALF_TILE
            temp_zombie.y = tile_y + HALF_TILE
        except NameError:
            return
            
        if not temp_zombie.colliderect(player):
            break
    try:
        new_zombie = Actor('zombie_stand')
        new_zombie.x = temp_zombie.x
        new_zombie.y = temp_zombie.y
    except NameError:
         return
         
    new_zombie.scale = ZOMBIE_SCALE
    new_zombie.hp = 1
    new_zombie.is_attacking = False
    new_zombie.is_hurt = False
    new_zombie.facing_left = False
    new_zombie.equation = generate_equation()
    new_zombie.attack_cooldown_timer = 0.0
    new_zombie.current_frame = 0
    ACTIVE_ZOMBIES.append(new_zombie)

def restart_game():
    global GAME_STATE, PLAYER_LIVES, ACTIVE_ZOMBIES, PLAYER_INPUT, GAME_OVER_ZOMBIE, flicker_timer, ZOMBIES_KILLED
    global GAME_OVER_SOUND_PLAYED, GAME_WIN_SOUND_PLAYED, is_hurt, PLAYER_CAN_BE_HURT, is_attacking, player_facing_left, zombie_facing_left
    try:
        clock.unschedule(spawn_zombie)
        clock.unschedule(animate_game_over)
        clock.unschedule(animate_game_win)
        clock.unschedule(animate)
        clock.unschedule(reset_player_hurt)
    except NameError:
        pass
    PLAYER_LIVES = 3
    ZOMBIES_KILLED = 0
    GAME_OVER_SOUND_PLAYED = False
    GAME_WIN_SOUND_PLAYED = False
    ACTIVE_ZOMBIES.clear()
    GAME_OVER_ZOMBIE = None
    try:
        player.x = (SCENARIO_LEFT + SCENARIO_RIGHT) // 2
        player.y = (SCENARIO_TOP + SCENARIO_BOTTOM) // 2
    except AttributeError:
        pass
    PLAYER_INPUT = ""
    flicker_timer = 0.0
    is_hurt = False
    PLAYER_CAN_BE_HURT = True
    is_attacking = False
    player_facing_left = False
    zombie_facing_left = False
    try:
        clock.schedule_interval(spawn_zombie, ZOMBIE_SPAWN_INTERVAL)
        clock.schedule_interval(animate, 0.15)
    except NameError:
        pass


def player_win():
    global GAME_STATE, GAME_WIN_FRAME, GAME_WIN_SOUND_PLAYED
    if GAME_STATE == "WIN": return
        
    GAME_STATE = "WIN"
    
    if SOUNDS_ON_OF == True and not GAME_WIN_SOUND_PLAYED:
        try:
            sounds.you_win.play()
            GAME_WIN_SOUND_PLAYED = True
        except NameError:
            pass
    
    try:
        clock.unschedule(spawn_zombie)
        clock.unschedule(animate)
        clock.unschedule(reset_player_hurt)
    except NameError:
        pass
    
    ACTIVE_ZOMBIES.clear()
    
    GAME_WIN_FRAME = 0
    try:
        clock.schedule_interval(animate_game_win, 0.15)
    except NameError:
        pass


def player_die():
    global GAME_STATE, GAME_OVER_ZOMBIE, GAME_OVER_SOUND_PLAYED
    
    if GAME_STATE == "GAME_OVER": return
        
    GAME_STATE = "GAME_OVER"
    
    if SOUNDS_ON_OF == True and not GAME_OVER_SOUND_PLAYED:
        try:
            sounds.you_loose.play()
            GAME_OVER_SOUND_PLAYED = True
        except NameError:
            pass

    try:
        clock.unschedule(spawn_zombie)
        clock.unschedule(reset_player_hurt)
        clock.unschedule(animate)
    except NameError:
        pass
    
    if ACTIVE_ZOMBIES:
        try:
            closest_zombie = min(ACTIVE_ZOMBIES, key=lambda z: player.distance_to(z))
            GAME_OVER_ZOMBIE = closest_zombie
            
            if GAME_OVER_ZOMBIE in ACTIVE_ZOMBIES:
                ACTIVE_ZOMBIES.remove(GAME_OVER_ZOMBIE)
                
            clock.schedule_interval(animate_game_over, 0.15)
        except (NameError, AttributeError, ValueError):
            pass


def reset_player_hurt():
    global is_hurt, PLAYER_CAN_BE_HURT, flicker_timer
    is_hurt = False
    PLAYER_CAN_BE_HURT = True
    flicker_timer = 0.0


def player_hurt():
    global PLAYER_LIVES, is_hurt, GAME_STATE, PLAYER_CAN_BE_HURT, flicker_timer
    if not PLAYER_CAN_BE_HURT or GAME_STATE != "PLAYING": return
    PLAYER_LIVES -= 1
    is_hurt = True
    PLAYER_CAN_BE_HURT = False
    try:
        player.image = HURT_SPRITE
    except AttributeError:
        pass
    flicker_timer = 0.0
    if PLAYER_LIVES <= 0:
        player_die()
    else:
        try:
            clock.schedule_unique(reset_player_hurt, 2.0)
        except NameError:
             pass

def zombie_die(zombie):
    global PLAYER_INPUT, ZOMBIES_KILLED
    zombie.is_hurt = True
    try:
        zombie.image = 'zombie_hurt'
    except AttributeError:
        pass
    PLAYER_INPUT = ""
    if zombie in ACTIVE_ZOMBIES:
        ACTIVE_ZOMBIES.remove(zombie)     
    ZOMBIES_KILLED += 1
    if ZOMBIES_KILLED >= ZOMBIES_TO_WIN:
        player_win()

def reset_player_attack():
    global is_attacking
    is_attacking = False

def on_key_down(key):
    global PLAYER_INPUT, is_attacking, GAME_STATE
    try:
        from pgzero.keyboard import keys
    except ImportError:
        return 
    if GAME_STATE != "PLAYING" or not ACTIVE_ZOMBIES:
        return
    target_zombie = ACTIVE_ZOMBIES[0]
    if key >= keys.K_0 and key <= keys.K_9:
        numeric_char = chr(key)
        if len(PLAYER_INPUT) < 3:
            PLAYER_INPUT += numeric_char
    elif key == keys.BACKSPACE:
        PLAYER_INPUT = PLAYER_INPUT[:-1]
    elif key == keys.RETURN:
        if PLAYER_INPUT:
            try:
                player_answer = int(PLAYER_INPUT)
                
                if player_answer == target_zombie.equation['result']:
                    
                    is_attacking = True
                    try:
                        clock.schedule_unique(reset_player_attack, 0.3)
                    except NameError:
                        pass
                    
                    zombie_die(target_zombie)
                
                PLAYER_INPUT = ""
                
            except ValueError:
                PLAYER_INPUT = ""


def on_mouse_down(pos):
    
    global GAME_STATE

    BUTTON_WIDTH = 250
    BUTTON_HEIGHT = 50
    BUTTON_Y_START = HEIGHT // 2 - 50
    
    try:
        from pgzero.rect import Rect
    except ImportError:
        return

    if GAME_STATE == "MENU":
        start_rect = Rect((WIDTH // 2 - BUTTON_WIDTH // 2, BUTTON_Y_START), (BUTTON_WIDTH, BUTTON_HEIGHT))
        instructions_rect = Rect((WIDTH // 2 - BUTTON_WIDTH // 2, BUTTON_Y_START + 80), (BUTTON_WIDTH, BUTTON_HEIGHT))
        sound_rect = Rect((WIDTH // 2 - BUTTON_WIDTH // 2, BUTTON_Y_START + 160), (BUTTON_WIDTH, BUTTON_HEIGHT))
        exit_rect = Rect((WIDTH // 2 - BUTTON_WIDTH // 2, BUTTON_Y_START + 240), (BUTTON_WIDTH, BUTTON_HEIGHT))
        
        if start_rect.collidepoint(pos):
            start_game()
        elif instructions_rect.collidepoint(pos):
            show_instructions()
        elif sound_rect.collidepoint(pos):
            toggle_sound()
        elif exit_rect.collidepoint(pos):
            exit_game()
            
    elif GAME_STATE == "INSTRUCTIONS":
        back_rect = Rect((WIDTH // 2 - 100, HEIGHT - 70), (200, 50))
        if back_rect.collidepoint(pos):
            if SOUNDS_ON_OF:
                try:
                    sounds.mouse_click.play()
                except NameError:
                    pass
            GAME_STATE = "MENU"
            
    elif GAME_STATE == "GAME_OVER" or GAME_STATE == "WIN":
        button_rect = Rect((WIDTH // 2 - 100, HEIGHT // 2 + 150), (200, 50))
        
        if button_rect.collidepoint(pos):
            if SOUNDS_ON_OF == True:
                try:
                    sounds.mouse_click.play()
                except NameError:
                    pass
            start_game()
try:
    from pgzero.actor import Actor
    for y in range(SCENARIO_TOP, SCENARIO_BOTTOM, TILE_SIZE):
        for x in range(SCENARIO_LEFT, SCENARIO_RIGHT, TILE_SIZE):
            tile = Actor('floor')
            tile.topleft = (x, y)
            SCENARIO.append(tile)

    DOOR_INDEX = (TILES_X - 2) // 2
    DOOR_INDEX_Y = (TILES_Y - 2) // 2

    for i in range(TILES_X):
        if i > 0 and i < TILES_X - 1:
            x_pos = OFFSET_X + i * TILE_SIZE
            tile_up = Actor('floor' if i == DOOR_INDEX else 'wall-up')
            tile_up.topleft = (x_pos, OFFSET_Y)
            SCENARIO.append(tile_up)
            tile_down = Actor('floor' if i == DOOR_INDEX else 'wall-down')
            tile_down.topleft = (x_pos, OFFSET_Y + SCENARIO_HEIGHT - TILE_SIZE)
            SCENARIO.append(tile_down)

    for i in range(TILES_Y):
        if i > 0 and i < TILES_Y - 1:
            y_pos = OFFSET_Y + i * TILE_SIZE
            tile_left = Actor('floor' if i == DOOR_INDEX_Y else 'wall-left')
            tile_left.topleft = (OFFSET_X, y_pos)
            SCENARIO.append(tile_left)
            tile_right = Actor('floor' if i == DOOR_INDEX_Y else 'wall-right')
            tile_right.topleft = (OFFSET_X + SCENARIO_WIDTH - TILE_SIZE, y_pos)
            SCENARIO.append(tile_right)

    SCENARIO.append(Actor('corner-left-up', topleft=(OFFSET_X, OFFSET_Y)))
    SCENARIO.append(Actor('corner-right-up', topleft=(OFFSET_X + SCENARIO_WIDTH - TILE_SIZE, OFFSET_Y)))
    SCENARIO.append(Actor('corner-left-down', topleft=(OFFSET_X, OFFSET_Y + SCENARIO_HEIGHT - TILE_SIZE)))
    SCENARIO.append(Actor('corner-right-down', topleft=(OFFSET_X + SCENARIO_WIDTH - TILE_SIZE, OFFSET_Y + SCENARIO_HEIGHT - TILE_SIZE)))
except NameError:
    pass


def animate_game_over():
    global GAME_OVER_FRAME
    if GAME_STATE != "GAME_OVER" or not GAME_OVER_ZOMBIE: return
    
    GAME_OVER_FRAME = (GAME_OVER_FRAME + 1) % len(ZOMBIE_CHEER_FRAMES)
    z = GAME_OVER_ZOMBIE
    try:
        z.image = ZOMBIE_CHEER_FRAMES[GAME_OVER_FRAME]
    except AttributeError:
        pass


def animate_game_win():
    global GAME_WIN_FRAME
    if GAME_STATE != "WIN": return
    try:
        GAME_WIN_FRAME = (GAME_WIN_FRAME + 1) % len(PLAYER_CHEER_FRAMES)
        player.image = PLAYER_CHEER_FRAMES[GAME_WIN_FRAME]
    except AttributeError:
        pass


def animate():
    global current_frame, GAME_STATE
    
    if GAME_STATE != "PLAYING": return
    
    try:
        if is_hurt:
            player.image = HURT_SPRITE
            if SOUNDS_ON_OF == True:
                try:
                    sounds.zombie_bite.play()
                except NameError:
                    pass

        elif is_attacking:
            if SOUNDS_ON_OF == True:
                try:
                    if current_frame == 0:
                        sounds.player_atack.play()
                except NameError:
                    pass

            attack_set = ACTION_FRAMES
            current_frame = (current_frame + 1) % len(attack_set)
            sprite_name = attack_set[current_frame]
            player.image = sprite_name
            
        elif is_moving:
            if player_facing_left == False:
                walking_set = WALKING_FRAMES_RIGHT
            else:
                walking_set = WALKING_FRAMES_LEFT
            current_frame = (current_frame + 1) % len(walking_set)
            player.image = walking_set[current_frame]
            
        else:
            stand_set = STAND_FRAMES
            current_frame = (current_frame + 1) % len(stand_set)
            player.image = stand_set[current_frame]

    except AttributeError:
        pass
        
    for z in ACTIVE_ZOMBIES:
        z.current_frame = (z.current_frame + 1) % 10
        
        try:
            if z.is_hurt:
                z.image = 'zombie_hurt'
            elif z.is_attacking:
                frame_index = z.current_frame % len(ZOMBIE_ACTION_FRAMES)
                z.image = ZOMBIE_ACTION_FRAMES[frame_index] 
            else:
                if z.attack_cooldown_timer > 0.0:
                    z.image = 'zombie_stand'
                else:
                    if zombie_facing_left == True:
                        frame_index = z.current_frame % len(ZOMBIE_WALK_FRAMES)
                        z.image = ZOMBIE_WALK_FRAMES[frame_index] 
                    else:
                        frame_index = z.current_frame % len(ZOMBIE_WALK_FRAMES_LEFT)
                        z.image = ZOMBIE_WALK_FRAMES_LEFT[frame_index]
        except AttributeError:
            pass


def draw():
    global flicker_timer, GAME_STATE
    
    try:
        screen.clear()
        from pgzero.rect import Rect
    except NameError:
        print("Pygame Zero 'screen' not found, cannot draw.")
        return
        
    for tile in SCENARIO: tile.draw()


    if GAME_STATE == "MENU":
        TITLE_SIZE = 80
        BUTTON_COLOR = (25, 25, 50)
        TEXT_COLOR = "yellow"
        
        BUTTON_WIDTH = 250
        BUTTON_HEIGHT = 50
        BUTTON_Y_START = HEIGHT // 2 - 50 


        screen.draw.text("THE WALKING MATH",
                         center=(WIDTH // 2, HEIGHT // 2 - 150),
                         color="red",
                         fontsize=TITLE_SIZE,
                         owidth=2.0,
                         ocolor="white")


        start_rect = Rect((WIDTH // 2 - BUTTON_WIDTH // 2, BUTTON_Y_START), (BUTTON_WIDTH, BUTTON_HEIGHT))
        screen.draw.filled_rect(start_rect, BUTTON_COLOR)
        screen.draw.text("COMECAR O JOGO",
                         center=start_rect.center,
                         color=TEXT_COLOR,
                         fontsize=30)
            
        instructions_rect = Rect((WIDTH // 2 - BUTTON_WIDTH // 2, BUTTON_Y_START + 80), (BUTTON_WIDTH, BUTTON_HEIGHT))
        screen.draw.filled_rect(instructions_rect, BUTTON_COLOR)
        screen.draw.text("INSTRUCOES",
                         center=instructions_rect.center,
                         color=TEXT_COLOR,
                         fontsize=30)

        sound_status = "LIGADO" if SOUNDS_ON_OF else "DESLIGADO"
        sound_rect = Rect((WIDTH // 2 - BUTTON_WIDTH // 2, BUTTON_Y_START + 160), (BUTTON_WIDTH, BUTTON_HEIGHT))
        screen.draw.filled_rect(sound_rect, BUTTON_COLOR)
        screen.draw.text(f"SOM: {sound_status}",
                         center=sound_rect.center,
                         color=TEXT_COLOR,
                         fontsize=30)
            
        exit_rect = Rect((WIDTH // 2 - BUTTON_WIDTH // 2, BUTTON_Y_START + 240), (BUTTON_WIDTH, BUTTON_HEIGHT))
        screen.draw.filled_rect(exit_rect, BUTTON_COLOR)
        screen.draw.text("SAIR",
                         center=exit_rect.center,
                         color=TEXT_COLOR,
                         fontsize=30)
        
        return
    
    elif GAME_STATE == "INSTRUCTIONS":
        instruction_text = "Nosso heroi ficou de recuperacao e a unica forma de passar e tirando 10 em matematica. Ajude-o a passar usando as setas para fugir dos zombies (questoes) e digite o valor do resultado da conta alvo (questao atual), depois aperte enter para matar o zombie correspondente, bom jogo!"
        
        panel_rect = Rect((WIDTH // 2 - 350, HEIGHT // 2 - 150), (700, 300))
        screen.draw.filled_rect(panel_rect, (0, 0, 0, 200))
        screen.draw.rect(panel_rect, "white")
        
        screen.draw.text("INSTRUCOES",
                             center=(WIDTH // 2, HEIGHT // 2 - 120),
                             color="yellow",
                             fontsize=50)
        screen.draw.text(instruction_text,
                             center=(WIDTH // 2, HEIGHT // 2 + 10),
                             color="white",
                             fontsize=30,
                             width=650)
        
        back_rect = Rect((WIDTH // 2 - 100, HEIGHT - 70), (200, 50))
        screen.draw.filled_rect(back_rect, (50, 50, 50))
        screen.draw.text("VOLTAR",
                             center=back_rect.center,
                             color="yellow",
                             fontsize=30)
        
        return

    is_target = len(ACTIVE_ZOMBIES) > 0
    for z in ACTIVE_ZOMBIES:
        try:
            z.draw()
        except AttributeError:
            pass
            
        if z.is_hurt: continue
        
        eq_text = z.equation['text']
        color = "red" if is_target and z == ACTIVE_ZOMBIES[0] else "white"
        text_pos = (z.x, z.y - z.height/2 - 30)
        screen.draw.text(eq_text,
                         center=text_pos,
                         color=color,
                         fontsize=24)
                         
    try:
        if (GAME_STATE == "PLAYING" and (not is_hurt or int(flicker_timer * 10) % 2 == 0)) or GAME_STATE == "WIN":
            if GAME_STATE == "WIN":
                player.x = WIDTH // 2
                player.y = HEIGHT // 2 - 100
                
            player.draw()
    except AttributeError:
        pass


    if GAME_STATE == "PLAYING":
        screen.draw.text(f"Vidas: {PLAYER_LIVES}", (20, 20), color="red", fontsize=30)
        screen.draw.text(f"Questoes: {ZOMBIES_KILLED}/{ZOMBIES_TO_WIN}", (WIDTH - 250, 20), color="yellow", fontsize=30)
        
        if is_target:
            target_zombie = ACTIVE_ZOMBIES[0]
            cursor = "_" if int(flicker_timer * 10) % 2 == 0 or not is_hurt else ""
            text_to_display = f"ALVO: {target_zombie.equation['text']} = {PLAYER_INPUT}{cursor}"
            screen.draw.text(text_to_display,
                             center=(WIDTH // 2, HEIGHT - 30),
                             color="yellow",
                             fontsize=40)
                             
    if GAME_STATE == "GAME_OVER":
        
        if GAME_OVER_ZOMBIE:
            try:
                GAME_OVER_ZOMBIE.x = WIDTH // 2
                GAME_OVER_ZOMBIE.y = HEIGHT // 2 - 100
                GAME_OVER_ZOMBIE.draw()
            except AttributeError:
                pass
        
        screen.draw.text("GAME OVER",
                             center=(WIDTH // 2, HEIGHT // 2 - 200),
                             color="red",
                             fontsize=100)
                             
        grade = ZOMBIES_KILLED * 10 / ZOMBIES_TO_WIN
        message = f"Nao foi dessa vez, reprovado com nota {grade:.1f}"
        screen.draw.text(message,
                             center=(WIDTH // 2, HEIGHT // 2 + 50),
                             color="yellow",
                             fontsize=35)
                             
        button_rect = Rect((WIDTH // 2 - 100, HEIGHT // 2 + 150), (200, 50))
        screen.draw.filled_rect(button_rect, (50, 50, 50))
        screen.draw.text("TENTAR DE NOVO",
                             center=button_rect.center,
                             color="yellow",
                             fontsize=30)

    if GAME_STATE == "WIN":
        
        screen.draw.text("VITORIA",
                             center=(WIDTH // 2, HEIGHT // 2 - 200),
                             color="green",
                             fontsize=100)


        message = "Parabens, aprovado com nota 10"
        screen.draw.text(message,
                             center=(WIDTH // 2, HEIGHT // 2 + 50),
                             color="yellow",
                             fontsize=35)


        button_rect = Rect((WIDTH // 2 - 100, HEIGHT // 2 + 150), (200, 50))
        screen.draw.filled_rect(button_rect, (50, 50, 50))
        screen.draw.text("Jogar de Novo",
                             center=button_rect.center,
                             color="yellow",
                             fontsize=30)


def update():

    global player_facing_left, is_moving, flicker_timer, GAME_STATE, zombie_facing_left
    
    try:
        from pgzero.keyboard import keyboard
    except ImportError:
        return

    if GAME_STATE != "PLAYING": return

    speed = 2
    is_moving = False

    try:
        if not is_attacking:
            if keyboard.left:
                player.x -= speed
                player_facing_left = True
                is_moving = True
            if keyboard.right:
                player.x += speed
                player_facing_left = False
                is_moving = True
            if keyboard.up:
                player.y -= speed
                is_moving = True
            if keyboard.down:
                player.y += speed
                is_moving = True
                
        if player.right > COLLISION_RIGHT: player.right = COLLISION_RIGHT
        if player.left < COLLISION_LEFT: player.left = COLLISION_LEFT
        if player.bottom > COLLISION_BOTTOM: player.bottom = COLLISION_BOTTOM
        if player.top < COLLISION_TOP: player.top = COLLISION_TOP
    except AttributeError:
        pass 
    
    if is_hurt and flicker_timer < 2.0:
        flicker_timer += 1/60.0

    for z in ACTIVE_ZOMBIES:
        
        if z.is_hurt:
            z.is_attacking = False
            continue
            
        try:
            distance = player.distance_to(z)
        except AttributeError:
            distance = 1000
            
        if z.attack_cooldown_timer > 0.0:
            z.attack_cooldown_timer -= 1/60.0
            z.is_attacking = False
        
        if distance < ZOMBIE_ATTACK_RANGE and z.attack_cooldown_timer <= 0.0:
            
            z.is_attacking = True
            z.attack_cooldown_timer = 1.0
            
            try:
                clock.schedule_unique(lambda z=z: setattr(z, 'is_attacking', False), 0.3)
            except NameError:
                z.is_attacking = False
            
            if PLAYER_CAN_BE_HURT:
                player_hurt()
                
        elif z.attack_cooldown_timer <= 0.0:
            
            try:
                angle_degrees = z.angle_to(player)
                angle_rad = math.radians(angle_degrees)
                
                dx = math.cos(angle_rad) * ZOMBIE_SPEED
                dy = -math.sin(angle_rad) * ZOMBIE_SPEED
                
                z.x += dx
                z.y += dy
                
                z.facing_left = z.x < player.x
                zombie_facing_left = z.facing_left
            except AttributeError:
                pass