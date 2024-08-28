import pygame
import sys
import random
import socket
import json
from datetime import datetime, timedelta
import statistics
import time
import webbrowser
import os

# List of files we need if you are using Pycharm IDE
# rocket_image = "rocket2.png"
# america = "america.png"
# banana = 'banana.png'
# discover = 'discovery.png'
# laser_ship = 'laser_ship.png'
# pipe_load_image = 'pipe.png'
# background_5_img = 'background5.png'
# main_menu_image = 'space_background.png'
# game_music_1 = 'Game music.mp3'
# game_music_2 = "Game over music.mp3"
# game_music_3 = 'Game main menu music.mp3'
# ability_sfx = 'Destroy Pipe Ability.mp3'
# crash_sfx = 'Death.mp3'
# shield_break_sfx = 'Shield Break.mp3'
# money_sfx = 'ka-ching.mp3'
# shield_on_sfx = 'Shield.mp3'
# logo = 'Logo.png'
# america_shield = 'america_shield.png'
# banana_shield = 'banana_shield.png'
# rocket_shield = 'rocket_shield.png'
# laser_ship_shield = 'laser_ship_shield.png'
# discovery_shield = 'discovery_shield.png'
# pvnet_logo = 'pvnet_logo.png'
# openbci_logo = 'openbci_logo.png'
# shield_image = 'shield.png'
# LEADERBOARD_FILE = "leaderboard.txt"

# List of image files we need if you are using VSCode IDE
rocket_image = "EEG_Game/rocket2.png"
america = "EEG_Game/america.png"
banana = 'EEG_Game/banana.png'
discover = 'EEG_Game/discovery.png'
laser_ship = 'EEG_Game/laser_ship.png'
pipe_load_image = 'EEG_Game/pipe.png'
background_5_img = 'EEG_Game/background5.png'
main_menu_image = 'EEG_Game/space_background.png'
game_music_1 = 'EEG_Game/Game music.mp3'
game_music_2 = "EEG_Game/Game over music.mp3"
game_music_3 = 'EEG_Game/Game main menu music.mp3'
ability_sfx = 'EEG_Game/Destroy Pipe Ability.mp3'
crash_sfx = 'EEG_Game/Death.mp3'
shield_break_sfx = 'EEG_Game/Shield Break.mp3'
money_sfx = 'EEG_Game/ka-ching.mp3'
shield_on_sfx = 'EEG_Game/Shield.mp3'
logo = 'EEG_Game/Logo.png'
america_shield = 'EEG_Game/america_shield.png'
banana_shield = 'EEG_Game/banana_shield.png'
rocket_shield = 'EEG_Game/rocket_shield.png'
laser_ship_shield = 'EEG_Game/laser_ship_shield.png'
discovery_shield = 'EEG_Game/discovery_shield.png'
pvnet_logo = 'EEG_Game/pvnet_logo.png'
openbci_logo = 'EEG_Game/openbci_logo.png'
shield_image = 'EEG_Game/shield.png'
LEADERBOARD_FILE = "EEG_Game/leaderboard.txt"


pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
# Store the Dimention of the screen
SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()

# Constants
last_score_update_time = datetime.min
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PIPE_COLOR = (0, 255, 0)
GRAVITY = (SCREEN_HEIGHT * 0.0004166666667)
SHIP_JUMP = -(SCREEN_HEIGHT * 0.0097222222)
PIPE_WIDTH = 80
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
ABILITY_COST = 0
PIPE_GAP_MODIFIER = 1.0
CURRENT_ABILITY = "explode"
SHIELD_ACTIVE = False
CRASH_TYPE = "none"
INVINCIBILITY_SECONDS = timedelta(seconds=1.5)
TIME_SINCE_CRASH = datetime.min
CURRENT_MODE = "medium"
TIME_SINCE_SCORE_UPDATE = datetime.min
UPDATE_COOLDOWN = timedelta(seconds=0.08)
HARD_BLINK_COOLDOWN = timedelta(seconds=1.0)

BACKGROUND_LENGTH = int(SCREEN_WIDTH * 5.43125)
FONT_SIZE = int(SCREEN_WIDTH // 31.5)
PIPE_SPEED = SCREEN_WIDTH // 189
BACKGROUND_SPEED = PIPE_SPEED // 2

PIPE_GAP = int(SCREEN_HEIGHT/ 2.57 * PIPE_GAP_MODIFIER)
# print(SCREEN_WIDTH, SCREEN_HEIGHT)

pygame.display.set_caption('Cosmic Crashout')


#Load in all the images with correct setting
logo_img = pygame.image.load(logo).convert_alpha()
logo_img = pygame.transform.scale(logo_img, (SCREEN_WIDTH // 1.89, SCREEN_HEIGHT // 1.964))

pvnet_img = pygame.image.load(pvnet_logo).convert()
pvnet_img = pygame.transform.scale(pvnet_img, (SCREEN_WIDTH // 5.688, SCREEN_HEIGHT // 3.2))
openbci_img = pygame.image.load(openbci_logo).convert()
openbci_img = pygame.transform.scale(openbci_img, (pvnet_img.get_width(), pvnet_img.get_height()))

ship_img = rocket_image
ship = pygame.image.load(ship_img).convert_alpha()
ship = pygame.transform.scale(ship, (int(SCREEN_WIDTH / 16.16), int(SCREEN_HEIGHT / 20)))
pipe_image = pygame.image.load(pipe_load_image).convert_alpha()
pipe_image = pygame.transform.scale(pipe_image, (PIPE_WIDTH, SCREEN_HEIGHT))

background = pygame.image.load(background_5_img).convert()
background = pygame.transform.scale(background, (BACKGROUND_LENGTH, SCREEN_HEIGHT))

background2 = pygame.image.load(background_5_img).convert()
background2 = pygame.transform.scale(background, (int(SCREEN_WIDTH * 1.90625), SCREEN_HEIGHT))

main_menu_background = pygame.image.load(main_menu_image).convert()
main_menu_background = pygame.transform.scale(main_menu_background, (SCREEN_WIDTH, SCREEN_HEIGHT))

original_width, original_height = ship.get_size()
aspect_ratio = original_width / original_height
new_width = 75
new_height = int(new_width / aspect_ratio)
# ship = pygame.transform.scale(ship, (new_width, new_height))
ship = pygame.transform.scale(ship, (int(SCREEN_WIDTH / 16.16), int(SCREEN_HEIGHT / 20)))

max_upward_angle = 45
max_downward_angle = -45
recovery_speed = 2

ship_x = SCREEN_WIDTH // 14
ship_y = SCREEN_HEIGHT // 2
ship_velocity = 0
ship_rotation = 0

pipe_list = []
pipe_timer = 0
score = 0
score_updated = False  # Flag to check if the score was already updated for a pipe set

font = pygame.font.Font(None, FONT_SIZE)

ability_last_used = datetime.min
cooldown = 20
ability_cooldown = timedelta(seconds=cooldown)


def save_score(name, score):
    """Save the player's name, score, and timestamp to the leaderboard file."""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    with open(LEADERBOARD_FILE, 'a') as file:
        file.write(f"{name},{score},{timestamp}\n")


def get_top_5_scores(leaderboard_file):
    """Retrieve the top 5 scores from the leaderboard file."""
    if not os.path.exists(leaderboard_file):
        return []

    leaderboard = []
    with open(leaderboard_file, 'r') as file:
        for line in file:
            name, score, timestamp = line.strip().split(',')
            leaderboard.append((name, int(score)))

    # Sort the leaderboard by score in descending order
    leaderboard.sort(key=lambda x: x[1], reverse=True)

    # Return the top 5 scores
    return leaderboard[:5]


def create_pipe():
    ## This function defines a top and bottom pipe of random lengths
    # Generate random pipe length between the threshold
    min_top_height = 100
    max_top_height = SCREEN_HEIGHT - PIPE_GAP - min_top_height
    top_height = random.randint(min_top_height, max_top_height)

    # Define the top and bottom pipe
    top_pipe = pygame.Rect(SCREEN_WIDTH, -int(SCREEN_HEIGHT / 23.07), PIPE_WIDTH, top_height)
    bottom_pipe = pygame.Rect(SCREEN_WIDTH, (top_height + PIPE_GAP) + int(SCREEN_HEIGHT / 30), PIPE_WIDTH, SCREEN_HEIGHT - (top_height + PIPE_GAP))

    return top_pipe, bottom_pipe


def draw_pipes():
    ## This function generates various pipe using pipe_list
    for top_pipe, bottom_pipe in pipe_list:
        # Draw top and bottom pipe
        screen.blit(pipe_image, top_pipe.topleft, (0, 0, PIPE_WIDTH, top_pipe.height))
        screen.blit(pipe_image, bottom_pipe.topleft, (0, SCREEN_HEIGHT - bottom_pipe.height, PIPE_WIDTH, bottom_pipe.height))

def draw_ship():
    ## This function draws the ship on the screen
    rotated_ship = pygame.transform.rotate(ship, ship_rotation)
    ship_rect = rotated_ship.get_rect(center=(ship_x, ship_y))
    screen.blit(rotated_ship, ship_rect.topleft)
    ship_mask = pygame.mask.from_surface(rotated_ship)
    outline = ship_mask.outline()


def move_pipes():
    global score, score_updated, ship_x, last_score_update_time
    cooldown_period = timedelta(seconds=0.5) 

    # Calculate the back end of the ship's x position
    ship_back_end_x = ship_x - (ship.get_width() // 2)

    current_time = datetime.now()

    for pipe_pair in pipe_list:
        top_pipe, bottom_pipe = pipe_pair
        top_pipe.x -= PIPE_SPEED
        bottom_pipe.x -= PIPE_SPEED

        # Check if the back end of the ship has passed the right edge of the pipe
        if ship_back_end_x > top_pipe.x + PIPE_WIDTH:
            if current_time - last_score_update_time >= cooldown_period :
                score += 1
                last_score_update_time = current_time
                score_updated = True

    # Reset the score_updated flag after a pipe has been fully passed
    if len(pipe_list) > 0 and ship_back_end_x > pipe_list[0][0].x + PIPE_WIDTH:
        score_updated = False

    # Remove pipes that have gone off the screen
    if len(pipe_list) > 0 and pipe_list[0][0].x < -PIPE_WIDTH:
        pipe_list.pop(0)


def check_collision():
    global CRASH_TYPE
    rotated_ship = pygame.transform.rotate(ship, ship_rotation)
    ship_rect = rotated_ship.get_rect(center=(ship_x, ship_y))
    ship_mask = pygame.mask.from_surface(rotated_ship)

    for top_pipe, bottom_pipe in pipe_list:
        top_pipe_mask = pygame.mask.from_surface(pipe_image.subsurface((0, 0, PIPE_WIDTH, top_pipe.height)))
        bottom_pipe_mask = pygame.mask.from_surface(pipe_image.subsurface((0, SCREEN_HEIGHT - bottom_pipe.height, PIPE_WIDTH, bottom_pipe.height)))

        top_pipe_offset = (top_pipe.x - ship_rect.x, top_pipe.y - ship_rect.y)
        bottom_pipe_offset = (bottom_pipe.x - ship_rect.x, bottom_pipe.y - ship_rect.y)

        if ship_mask.overlap(top_pipe_mask, top_pipe_offset) or ship_mask.overlap(bottom_pipe_mask, bottom_pipe_offset):
            CRASH_TYPE = "pipe"
            return True
    if ship_y > SCREEN_HEIGHT or ship_y < 0:
        CRASH_TYPE = "screen"
        return True
    return False


def draw_score():
    ## Keep track of score and show the result at the game screen
    global score
    score_surface = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_surface, (10, 10))
    return score


def draw_cooldown_timer():
    ## Keep track of the ability and show the timer at the game scren
    global ability_last_used
    current_time = datetime.now()
    time_since_last_use = current_time - ability_last_used
    if time_since_last_use < ability_cooldown:
        remaining_time = ability_cooldown - time_since_last_use
        remaining_seconds = remaining_time.total_seconds()
        timer_text = f"Ability ready in: {int(remaining_seconds)}s"
    elif score < ABILITY_COST:
        timer_text = "       Score too low"
    else:
        timer_text = "       Ability ready!"
    timer_surface = font.render(timer_text, True, WHITE)
    screen.blit(timer_surface, (SCREEN_WIDTH - int(SCREEN_WIDTH / 4.5), 10))  # Position the timer on the screen


# Define the IP address and port number for the UDP server from OPENBCI GUI
UDP_IP = "127.0.0.1"
UDP_PORT = 12345

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print(f"Listening for UDP packets on {UDP_IP}:{UDP_PORT}")



def filter_unconsious_blink(list):
    ### Return True if amplitude is all below True. We will consider this as unconsious blinkning
    threshold = 8
    for i in list:
        if i >= threshold:
            return False
    return True


def filter_hard_blink(channel_1, channel_2):
    global threshold_1, threshold_2
    # return True if list_1 goes above threshold1 and list_2 goes above threshold2 which is hard blink
    current_time = time.time()
    try:
        threshold_1
    except NameError:
        threshold_1 = None
    try:
        threshold_2
    except NameError:
        threshold_2 = None

    if threshold_1 is None:
        threshold_1 = 30
    if threshold_2 is None:
        threshold_2 = 1
    list_1_pass = False
    list_2_pass = False
    if channel_1 > threshold_1:
        list_1_pass = True
    if channel_2 > threshold_2:
        list_2_pass = True

    if list_1_pass and list_2_pass:
        return True
    return False


# Function to process live data
def process_data(data):
    # Returns two numbers, aggregated result from first channel and result from third channel
    try:
        # Decode the data and parse it to json
        data_str = data.decode('utf-8')
        parsed_data = json.loads(data_str)

        if parsed_data.get('type') == 'fft' and 'data' in parsed_data:
            fft_data = parsed_data['data']

            # We are only interested in first and third channel data
            first_channel_amplitude = fft_data[0]
            third_channel_amplitude = fft_data[2]

            frequencies = [(i * 200 / len(first_channel_amplitude)) for i in range(len(first_channel_amplitude))]

            # Extract Amplitude where Frequency from 4.8 to 17.6
            amplitude_interest_second = first_channel_amplitude[3:12]
            amplitude_interest_third = third_channel_amplitude[3:12]
            frequencies_interest = frequencies[3:12]

            if filter_unconsious_blink(amplitude_interest_second):
                # Unconcious blink will be ignored as 0, 0
                return 0, 0
            else:
                # Either blink of hard blink is detected, we will return the average amplitude from both channels
                return statistics.mean(amplitude_interest_second), statistics.mean(amplitude_interest_third)
        else:
            print("Invalid data format received.")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")


def udp_listener():
    global play_game, calibration_on, threshold_1, threshold_2, calibration_now
    avr_amplitude_front_1 = 0
    avr_amplitude_back_1 = 0
    blink_count = 0
    blink_count_2 = 0
    blink_count_3 = 0
    calibration_count = 0
    while True:
        data, addr = sock.recvfrom(8196)
        avr_amplitude_front_2, avr_amplitude_back_2 = process_data(data)

        if calibration_on:
            if calibration_now:
                if (avr_amplitude_back_1 == avr_amplitude_back_2) and (avr_amplitude_back_2 == 0):
                    # The user is not blinking, so reset the variable
                    avr_amplitude_front_1 = 0
                    avr_amplitude_back_1 = 0
                    continue
                elif avr_amplitude_back_1 < avr_amplitude_back_2:
                    # This means that blinks are detected
                    avr_amplitude_front_1 = avr_amplitude_front_2
                    avr_amplitude_back_1 = avr_amplitude_back_2
                elif (avr_amplitude_back_1 > avr_amplitude_back_2):
                    # print("Calibration done!")
                    if calibration_count == 0:
                        ##We will look at the peak of the bell curve to see for hard blink
                        threshold_1 = (avr_amplitude_front_1 * 4) / 5
                        threshold_2 = (avr_amplitude_back_1 * 3) / 5
                        print(threshold_1, threshold_2)
                        calibration_count += 1
                    avr_amplitude_front_1 = avr_amplitude_front_2
                    avr_amplitude_back_1 = avr_amplitude_back_2
        elif play_game:
            # IF we are playing the game, we use blink as jump and hard blink as ultimate
            if (avr_amplitude_front_1 == avr_amplitude_front_2) and (avr_amplitude_front_2 == 0):
                # The user is not blinking, so reset the variable
                avr_amplitude_front_1 = 0
                avr_amplitude_back_2 = 0
                blink_count = 0
                blink_count_2 = 0
                continue
            elif avr_amplitude_front_1 < avr_amplitude_front_2:
                # This means that blinks are detected
                if blink_count == 0:
                    print("Blinking DETECTED!!!")
                    blink_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)
                    pygame.event.post(blink_event)
                    blink_count += 1
                    avr_amplitude_front_1 = avr_amplitude_front_2
                else:
                    avr_amplitude_front_1 = avr_amplitude_front_2
            elif (avr_amplitude_front_1 > avr_amplitude_front_2):
                ##We will look at the peak of the bell curve to see for hard blink
                if blink_count_2 == 0:
                    if filter_hard_blink(avr_amplitude_front_2, avr_amplitude_back_2):
                        print("HARD BLINK TOO")
                        blink_hard_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_x)
                        pygame.event.post(blink_hard_event)
                        blink_count_2 += 1
                avr_amplitude_front_1 = avr_amplitude_front_2
                blink_count = 0
        else:
            # The game is not being played, so use blink for next and hard blink for select
            if (avr_amplitude_front_1 == avr_amplitude_front_2) and (avr_amplitude_front_2 == 0):
                # The user is not blinking, so reset the variable
                avr_amplitude_front_1 = 0
                avr_amplitude_back_2 = 0
                blink_count_3 = 0
                continue
            elif avr_amplitude_front_1 < avr_amplitude_front_2:
                # This means that blinks are starting to be detected
                avr_amplitude_front_1 = avr_amplitude_front_2
                blink_count_3 = 0
            elif (avr_amplitude_front_1 > avr_amplitude_front_2):
                if blink_count_3 == 0:
                    if filter_hard_blink(avr_amplitude_front_2, avr_amplitude_back_2):
                        print("HARD BLINK")
                        blink_hard_select = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)
                        pygame.event.post(blink_hard_select)
                        blink_count_3 += 1
                    else:
                        print("Next_option")
                        blink_next = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_LSHIFT)
                        pygame.event.post(blink_next)
                        blink_count_3 += 1
                avr_amplitude_front_1 = avr_amplitude_front_2


# Start the UDP listener in a separate thread
import threading

udp_thread = threading.Thread(target=udp_listener)
udp_thread.daemon = True
udp_thread.start()


def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()


def calibration():
    global play_game, audio_exists, calibration_on, calibration_now
    menu_active = True
    calibration_on = True
    calibration_now = False
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(shield_on_sfx)
        audio_exists = True
    except pygame.error as e:
        audio_exists = False

    # Get the starting time
    start_time = pygame.time.get_ticks()

    while menu_active:
        handle_events()
        # Calculate the elapsed time in seconds
        elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
        countdown = 10 - elapsed_time

        if countdown <= 0:
            countdown = "Now"
            calibration_now = True
            menu_active = False  # End the loop after displaying "Now"

        screen.fill(BLACK)
        calibration_text = font.render("Calibration Setup", True, WHITE)
        screen.blit(calibration_text, (SCREEN_WIDTH // 2 - calibration_text.get_width() // 2, SCREEN_HEIGHT // 9))

        instruction_text_1 = font.render("Instruction: Do a single HARD BLINK when", True, WHITE)
        screen.blit(instruction_text_1, (SCREEN_WIDTH // 2 - instruction_text_1.get_width() // 2, SCREEN_HEIGHT // 6))
        instruction_text_2 = font.render('the screen says "now"', True, WHITE)
        screen.blit(instruction_text_2, (SCREEN_WIDTH // 2 - instruction_text_2.get_width() // 2, SCREEN_HEIGHT // 5))

        warning_text_1 = font.render("Note: Restart the program if calibration fails!!", True, WHITE)
        screen.blit(warning_text_1, (SCREEN_WIDTH // 2 - warning_text_1.get_width() // 2, SCREEN_HEIGHT // 1.3))
        warning_text_2 = font.render("Make sure that the uV in the FFT plot is less than 10 for both channels before continuing", True, WHITE)
        screen.blit(warning_text_2, (SCREEN_WIDTH // 2 - warning_text_2.get_width() // 2, SCREEN_HEIGHT // 1.2))

        # Render the countdown or "Now"
        countdown_text = font.render(str(countdown), True, WHITE)
        screen.blit(countdown_text, (SCREEN_WIDTH // 2 - countdown_text.get_width() // 2, SCREEN_HEIGHT // 2))

        # Update the display
        pygame.display.flip()

        # Handle events to prevent the window from freezing
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_active = False

        # Limit the loop to 60 frames per second
        pygame.time.Clock().tick(60)

    # Pause for a moment after showing "Now"
    pygame.time.wait(2000)  # 1000 milliseconds = 1 second
    time.sleep(2)
    main_menu()


def main_menu():
    global play_game, audio_exists, calibration_on
    play_game = False
    menu_active = True
    selected_option = 0
    calibration_on = False
    time_since_start = datetime.now()
    options = ["Start", "Settings","Credits", "Quit"]
    # Get top scores and render the leaderboard
    top_scores = get_top_5_scores(LEADERBOARD_FILE)
    leaderboard_texts = []

    # Start playing music when the game starts
    if (audio_exists):
        pygame.mixer.init()
        pygame.mixer.music.load(game_music_3)
        pygame.mixer.music.play(-1)

    for i, (name, score) in enumerate(top_scores, start=1):
        leaderboard_text = font.render(f"{i}. {name}: {score}", True, pygame.Color('white'))
        leaderboard_texts.append(leaderboard_text)

    while menu_active:
        screen.blit(main_menu_background, (0, 0))
        screen.blit(logo_img, (SCREEN_WIDTH // 2 - logo_img.get_width() // 2, SCREEN_HEIGHT // 50))

        # Draw menu options that users can select
        for i, option in enumerate(options):
            color = (0, 255, 255) if i == selected_option else WHITE
            option_text = font.render(option, True, color)
            screen.blit(option_text, (SCREEN_WIDTH // 2 - option_text.get_width() // 2,
                                      SCREEN_HEIGHT // 2.45 + i * SCREEN_HEIGHT // 16.3666666667))

        # Draw the leaderboard
        leaderboard_text = font.render("LEADERBOARD", True, WHITE)
        screen.blit(leaderboard_text, (SCREEN_WIDTH // 2 - leaderboard_text.get_width() // 2, SCREEN_HEIGHT // 1.5))
        leaderboard_start_y = SCREEN_HEIGHT // 1.5 + SCREEN_HEIGHT // 19.64
        for i, leaderboard_text in enumerate(leaderboard_texts):
            screen.blit(leaderboard_text,
                        (SCREEN_WIDTH // 2 - leaderboard_text.get_width() // 2,
                         leaderboard_start_y + i * (SCREEN_HEIGHT // 19.64)))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:  # Next Options
                    selected_option = (selected_option + 1) % len(options)
                elif event.key == pygame.K_RETURN and datetime.now() - time_since_start >= HARD_BLINK_COOLDOWN:
                    if (audio_exists):
                        pygame.mixer.music.stop()
                    if selected_option == 0:  # Start
                        menu_active = False
                        main_game()
                    elif selected_option == 1:  # Settings
                        menu_active = False
                        settings()
                    elif selected_option == 2:  # Credits
                        menu_active = False
                        credits()
                    elif selected_option == 3:  # Quit
                        pygame.quit()
                        sys.exit()


def game_over_menu():
    global play_game, score, audio_exists
    menu_active = True
    time.sleep(0.5)
    selected_option = 0
    options = ["Restart", "Main Menu", "Record Score"]
    play_game = False
    handle_events()
    time_since_start = datetime.now()
    score_reviewed = score

    # Start playing music when the game starts
    if (audio_exists):
        pygame.mixer.init()
        pygame.mixer.music.load(game_music_2)
        pygame.mixer.music.play(-1)

        # Draw the leaderboard
    top_scores = get_top_5_scores(LEADERBOARD_FILE)
    leaderboard_texts = []
    for i, (name, score) in enumerate(top_scores, start=1):
        leaderboard_text = font.render(f"{i}. {name}: {score}", True, pygame.Color('white'))
        leaderboard_texts.append(leaderboard_text)

    while menu_active:
        screen.fill(BLACK)

        game_over_text = font.render("Game Over", True, WHITE)
        score_text = font.render(f"Score: {int(score_reviewed)}", True, WHITE)

        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 5))
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 4))

        for i, option in enumerate(options):
            color = (0, 255, 255) if i == selected_option else WHITE
            option_text = font.render(option, True, color)
            screen.blit(option_text, (SCREEN_WIDTH // 2 - option_text.get_width() // 2,
                                      SCREEN_HEIGHT // 2.5 + i * (SCREEN_HEIGHT // 16.3666666667)))

        leaderboard_text = font.render("LEADERBOARD", True, WHITE)
        screen.blit(leaderboard_text, (SCREEN_WIDTH // 2 - leaderboard_text.get_width() // 2, SCREEN_HEIGHT // 1.5))
        leaderboard_start_y = SCREEN_HEIGHT // 1.5 + SCREEN_HEIGHT // 19.64
        for i, leaderboard_text in enumerate(leaderboard_texts):
            screen.blit(leaderboard_text,
                        (SCREEN_WIDTH // 2 - leaderboard_text.get_width() // 2,
                         leaderboard_start_y + i * (SCREEN_HEIGHT // 19.64)))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:  # Next option
                    selected_option = (selected_option + 1) % len(options)
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_RETURN and datetime.now() - time_since_start >= HARD_BLINK_COOLDOWN:
                    if (audio_exists):
                        pygame.mixer.music.stop()
                    if selected_option == 0:  # Restart
                        menu_active = False
                        return "restart"
                    elif selected_option == 1:  # Main Menu
                        menu_active = False
                        return "main_menu"
                    elif selected_option == 2:  # Inputting scores
                        return "input_score"


def credits():
    font = pygame.font.Font(None, FONT_SIZE)
    menu_active = True
    time_since_start = datetime.now()
    selected_option = 0
    options = ["Team Members", "Direct to Abstract", "Link to Website", "Exit"]
    play_game = False

    while menu_active:
        screen.blit(main_menu_background, (0, 0)) 
        title_text = font.render("Credits", True, WHITE)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 15))

        techcentor_text = font.render("PVNet Advanced Technology Center", True, (144, 238, 144))
        screen.blit(techcentor_text, (SCREEN_WIDTH // 2 - techcentor_text.get_width() // 2, SCREEN_HEIGHT // 6.5))
        team_text = font.render("Research and Development Team", True, (144, 238, 144))
        screen.blit(team_text, (SCREEN_WIDTH // 2 - team_text.get_width() // 2, SCREEN_HEIGHT // 5))

        screen.blit(pvnet_img,
                    (SCREEN_WIDTH // 2 - pvnet_img.get_width() // 2 - SCREEN_WIDTH // 5, SCREEN_HEIGHT // 4.025))
        screen.blit(openbci_img,
                    (SCREEN_WIDTH // 2 - openbci_img.get_width() // 2 + SCREEN_WIDTH // 5, SCREEN_HEIGHT // 4.025))

        for i, option in enumerate(options):
            color = (0, 255, 255) if i == selected_option else WHITE
            option_text = font.render(option, True, color)
            screen.blit(option_text, (SCREEN_WIDTH // 2 - option_text.get_width() // 2,
                                      SCREEN_HEIGHT // 3.35 + i * SCREEN_HEIGHT // 16.3666666667))

        acknoledgement_text_1 = font.render("Acknowledgement to OpenBCI for pioneering technology that", True, WHITE)
        screen.blit(acknoledgement_text_1,
                    (SCREEN_WIDTH // 2 - acknoledgement_text_1.get_width() // 2, SCREEN_HEIGHT // 1.75))
        acknoledgement_text_2 = font.render("empowers real scientific research and enriches educational opportunities.",
                                            True, WHITE)
        screen.blit(acknoledgement_text_2,
                    (SCREEN_WIDTH // 2 - acknoledgement_text_2.get_width() // 2, SCREEN_HEIGHT // 1.65))

        special_thanks_1 = font.render("Special Thanks to:", True, WHITE)
        screen.blit(special_thanks_1, (SCREEN_WIDTH // 2 - special_thanks_1.get_width() // 2, SCREEN_HEIGHT // 1.51))
        special_thanks_2 = font.render("Richard Hakims for EEG consulting and advice", True, WHITE)
        screen.blit(special_thanks_2, (SCREEN_WIDTH // 2 - special_thanks_2.get_width() // 2, SCREEN_HEIGHT // 1.4))
        special_thanks_3 = font.render("Richard Hoffman for Game Development ideas", True, WHITE)
        screen.blit(special_thanks_3, (SCREEN_WIDTH // 2 - special_thanks_3.get_width() // 2, SCREEN_HEIGHT // 1.3))
        special_thanks_4 = font.render("Lem Wang - PVNet research Sponsor", True, WHITE)
        screen.blit(special_thanks_4, (SCREEN_WIDTH // 2 - special_thanks_4.get_width() // 2, SCREEN_HEIGHT // 1.22))
        special_thanks_5 = font.render("Promenade PV mall for supporting education", True, WHITE)
        screen.blit(special_thanks_5, (SCREEN_WIDTH // 2 - special_thanks_5.get_width() // 2, SCREEN_HEIGHT // 1.15))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:  #Next option
                    selected_option = (selected_option + 1) % len(options)
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_RETURN and datetime.now() - time_since_start >= HARD_BLINK_COOLDOWN:
                    if selected_option == 0: #Team Member
                        menu_active = False
                        team_member()
                    elif selected_option == 1:  # Dirct you to abstract
                        menu_active = False
                        webbrowser.open('https://www.google.com')
                        credits()
                    elif selected_option == 2:  # Direct you to pvnet
                        menu_active = False
                        webbrowser.open('https://www.pvnet.com')
                        credits()
                    elif selected_option == 3:  # Direct you to main menu
                        menu_active = False
                        main_menu()


def team_member():
    font = pygame.font.Font(None, FONT_SIZE)
    menu_active = True
    time_since_start = datetime.now()
    selected_option = 0
    options = ["Exit"]
    play_game = False
    luna_role = ["EEG Data Analysis Lead", "Open BCI Integration Development Lead",
                 "Leaderboard Management Integration"]
    pat_role = ["UI & Game strategy Development Lead", "BCI Interface Integration & Accessibility Development",
                "Open BCI Integration Development"]
    joe_role = ["BCI Interface Integration & Accessibility Development Lead", "UI & Game strategy Development",
                "Quality Assurance Tester"]
    tommy_role = ["EEG Headset Electronic Integration", "Visual & Asset Development", "Quality Assurance Tester"]

    while menu_active:
        screen.blit(main_menu_background, (0, 0))
        title_text = font.render("Team Members", True, WHITE)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 15))

        ted_text = font.render("Ted Vegvari - ", True, WHITE)
        screen.blit(ted_text, (SCREEN_WIDTH // 2 - ted_text.get_width() - (SCREEN_WIDTH // 5), SCREEN_HEIGHT // 9))
        ted_text = font.render("Director of Research Development", True, WHITE)
        screen.blit(ted_text, (SCREEN_WIDTH // 2 - (SCREEN_WIDTH // 5), SCREEN_HEIGHT // 9))

        Luna_text = font.render("Jill Luna Nomura - ", True, WHITE)
        screen.blit(Luna_text, (SCREEN_WIDTH // 2 - Luna_text.get_width() - (SCREEN_WIDTH // 5), SCREEN_HEIGHT // 6.3))
        luna_role_1 = font.render(luna_role[0], True, WHITE)
        screen.blit(luna_role_1, (SCREEN_WIDTH // 2 - (SCREEN_WIDTH // 5), SCREEN_HEIGHT // 6.3))
        luna_role_2 = font.render(luna_role[1], True, WHITE)
        screen.blit(luna_role_2, (SCREEN_WIDTH // 2 - (SCREEN_WIDTH // 5), SCREEN_HEIGHT // 6.3 + font.get_height()))
        luna_role_3 = font.render(luna_role[2], True, WHITE)
        screen.blit(luna_role_3,
                    (SCREEN_WIDTH // 2 - (SCREEN_WIDTH // 5), SCREEN_HEIGHT // 6.3 + (font.get_height() * 2)))

        pat_text = font.render("Patrick Mc Grath - ", True, WHITE)
        screen.blit(pat_text, (SCREEN_WIDTH // 2 - pat_text.get_width() - (SCREEN_WIDTH // 5), SCREEN_HEIGHT // 3.5))
        pat_role_1 = font.render(pat_role[0], True, WHITE)
        screen.blit(pat_role_1, (SCREEN_WIDTH // 2 - (SCREEN_WIDTH // 5), SCREEN_HEIGHT // 3.5))
        pat_role_2 = font.render(pat_role[1], True, WHITE)
        screen.blit(pat_role_2, (SCREEN_WIDTH // 2 - (SCREEN_WIDTH // 5), SCREEN_HEIGHT // 3.5 + font.get_height()))
        pat_role_3 = font.render(pat_role[2], True, WHITE)
        screen.blit(pat_role_3,
                    (SCREEN_WIDTH // 2 - (SCREEN_WIDTH // 5), SCREEN_HEIGHT // 3.5 + (font.get_height() * 2)))

        Joe_text = font.render("Joe Huber - ", True, WHITE)
        screen.blit(Joe_text, (SCREEN_WIDTH // 2 - Joe_text.get_width() - (SCREEN_WIDTH // 5), SCREEN_HEIGHT // 2.4))
        joe_role_1 = font.render(joe_role[0], True, WHITE)
        screen.blit(joe_role_1, (SCREEN_WIDTH // 2 - (SCREEN_WIDTH // 5), SCREEN_HEIGHT // 2.4))
        joe_role_2 = font.render(joe_role[1], True, WHITE)
        screen.blit(joe_role_2, (SCREEN_WIDTH // 2 - (SCREEN_WIDTH // 5), SCREEN_HEIGHT // 2.4 + font.get_height()))
        joe_role_3 = font.render(joe_role[2], True, WHITE)
        screen.blit(joe_role_3,
                    (SCREEN_WIDTH // 2 - (SCREEN_WIDTH // 5), SCREEN_HEIGHT // 2.4 + (font.get_height() * 2)))

        Tommy_text = font.render("Tommy Nguyen - ", True, WHITE)
        screen.blit(Tommy_text,
                    (SCREEN_WIDTH // 2 - Tommy_text.get_width() - (SCREEN_WIDTH // 5), SCREEN_HEIGHT // 1.85))
        tommy_role_1 = font.render(tommy_role[0], True, WHITE)
        screen.blit(tommy_role_1, (SCREEN_WIDTH // 2 - (SCREEN_WIDTH // 5), SCREEN_HEIGHT // 1.85))
        tommy_role_2 = font.render(tommy_role[1], True, WHITE)
        screen.blit(tommy_role_2, (SCREEN_WIDTH // 2 - (SCREEN_WIDTH // 5), SCREEN_HEIGHT // 1.85 + font.get_height()))
        tommy_role_3 = font.render(tommy_role[2], True, WHITE)
        screen.blit(tommy_role_3,
                    (SCREEN_WIDTH // 2 - (SCREEN_WIDTH // 5), SCREEN_HEIGHT // 1.85 + (font.get_height() * 2)))

        Josh_text = font.render("Joshua Nwabuzor - ", True, WHITE)
        screen.blit(Josh_text, (SCREEN_WIDTH // 2 - Josh_text.get_width() - (SCREEN_WIDTH // 5), SCREEN_HEIGHT // 1.5))
        Josh_text_3 = font.render("Visual & Asset Development", True, WHITE)
        screen.blit(Josh_text_3, (SCREEN_WIDTH // 2 - (SCREEN_WIDTH // 5), SCREEN_HEIGHT // 1.5))
        Josh_text_2 = font.render("BCI Interface Integration & Accessibility Development", True, WHITE)
        screen.blit(Josh_text_2, (SCREEN_WIDTH // 2 - (SCREEN_WIDTH // 5), SCREEN_HEIGHT // 1.5 + font.get_height()))
        Mark_text_1 = font.render("Mark Segal - ", True, WHITE)
        screen.blit(Mark_text_1,
                    (SCREEN_WIDTH // 2 - Mark_text_1.get_width() - (SCREEN_WIDTH // 5), SCREEN_HEIGHT // 1.32))
        Mark_text_2 = font.render("UI & Game strategy Development", True, WHITE)
        screen.blit(Mark_text_2, (SCREEN_WIDTH // 2 - (SCREEN_WIDTH // 5), SCREEN_HEIGHT // 1.32))
        mag_text_1 = font.render("Mathias Gutierrez - ", True, WHITE)
        screen.blit(mag_text_1,
                    (SCREEN_WIDTH // 2 - mag_text_1.get_width() - (SCREEN_WIDTH // 5), SCREEN_HEIGHT // 1.25))
        mag_text_2 = font.render("Sound Design", True, WHITE)
        screen.blit(mag_text_2, (SCREEN_WIDTH // 2 - (SCREEN_WIDTH // 5), SCREEN_HEIGHT // 1.25))
        Daniel_text_1 = font.render("Daniel Belonio - ", True, WHITE)
        screen.blit(Daniel_text_1,
                    (SCREEN_WIDTH // 2 - Daniel_text_1.get_width() - (SCREEN_WIDTH // 5), SCREEN_HEIGHT // 1.18))
        Daniel_text_2 = font.render("UI & Game strategy Development", True, WHITE)
        screen.blit(Daniel_text_2, (SCREEN_WIDTH // 2 - (SCREEN_WIDTH // 5), SCREEN_HEIGHT // 1.18))

        for i, option in enumerate(options):
            color = (0, 255, 255) if i == selected_option else WHITE
            option_text = font.render(option, True, color)
            screen.blit(option_text, (SCREEN_WIDTH // 2 - option_text.get_width() // 2, SCREEN_HEIGHT // 1.1 + i * 60))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT: #Next option
                    selected_option = (selected_option + 1) % len(options)
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_RETURN and datetime.now() - time_since_start >= HARD_BLINK_COOLDOWN:
                    if selected_option == 0:  #Main menu
                        menu_active = False
                        main_menu()


def settings():
    font = pygame.font.Font(None, FONT_SIZE)
    menu_active = True
    time_since_start = datetime.now()
    selected_option = 0
    options = ["Styles", "Ability", "Difficulty", "Main Menu"]
    play_game = False

    while menu_active:
        screen.blit(main_menu_background, (0, 0))
        title_text = font.render("Settings", True, WHITE)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 5))

        for i, option in enumerate(options):
            color = (0, 255, 255) if i == selected_option else WHITE
            option_text = font.render(option, True, color)
            screen.blit(option_text, (SCREEN_WIDTH // 2 - option_text.get_width() // 2, SCREEN_HEIGHT // 2.5 + i * 60))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:  #Next Option
                    selected_option = (selected_option + 1) % len(options)
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_RETURN and datetime.now() - time_since_start >= HARD_BLINK_COOLDOWN:
                    if selected_option == 0:  #Style
                        menu_active = False
                        styles()
                    elif selected_option == 1:  # Ability
                        menu_active = False
                        abilities()
                    elif selected_option == 2:  # Difficulty
                        menu_active = False
                        difficulty()
                    elif selected_option == 3:  # Main Menu
                        menu_active = False
                        main_menu()


def styles():
    global ship, ship_img

    font = pygame.font.Font(None, FONT_SIZE)
    menu_active = True
    time_since_start = datetime.now()
    selected_option = 0
    options = ["Default", "Discovery Shuttle", "Laser Ship", "AMERICA!!!", "banaannana", "Settings"]
    play_game = False

    while menu_active:
        screen.blit(main_menu_background, (0, 0))
        title_text = font.render("Styles", True, WHITE)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 5))

        for i, option in enumerate(options):
            color = (0, 255, 255) if i == selected_option else (240, 240, 240)
            option_text = font.render(option, True, color)
            screen.blit(option_text, (SCREEN_WIDTH // 2 - option_text.get_width() // 2, SCREEN_HEIGHT // 2.5 + i * 60))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:  # Next Option
                    selected_option = (selected_option + 1) % len(options)
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_RETURN and datetime.now() - time_since_start >= HARD_BLINK_COOLDOWN:
                    if selected_option == 0:  #Default
                        ship_img = rocket_image
                    elif selected_option == 1:  # Discovery
                        ship_img = discover
                    elif selected_option == 2:  # Laser
                        ship_img = laser_ship
                    elif selected_option == 3:  # america
                        ship_img = america
                    elif selected_option == 4:  # banana
                        ship_img = banana
                    elif selected_option == 5:  # Settings
                        menu_active = False
                        settings()
                    ship = pygame.image.load(ship_img).convert_alpha()
                    ship = pygame.transform.scale(ship, (int(SCREEN_WIDTH / 16.16), int(SCREEN_HEIGHT / 20)))
                    menu_active = False
                    settings()


def difficulty():
   global PIPE_GAP, PIPE_GAP_MODIFIER, CURRENT_MODE, PIPE_SPEED, GRAVITY

   font = pygame.font.Font(None, FONT_SIZE)
   menu_active = True
   time_since_start = datetime.now()
   selected_option = 0
   options = ["Easy", "Medium", "Hard", "Settings"]


   while menu_active:
       screen.blit(main_menu_background, (0, 0)) 
       title_text = font.render("Difficulty", True, WHITE)
       screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 5))
       for i, option in enumerate(options):
        color = (0, 255, 255) if i == selected_option else (240, 240, 240)
        option_text = font.render(option, True, color)
        screen.blit(option_text, (SCREEN_WIDTH // 2 - option_text.get_width() // 2, SCREEN_HEIGHT // 2.5 + i * 60))
            
        pygame.display.flip()


       for event in pygame.event.get():
           if event.type == pygame.QUIT:
               pygame.quit()
               sys.exit()
           elif event.type == pygame.KEYDOWN:
               if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:  # Next Option
                   selected_option = (selected_option + 1) % len(options)
               elif event.key == pygame.K_ESCAPE:
                   pygame.quit()
                   sys.exit()
               elif event.key == pygame.K_RETURN and datetime.now() - time_since_start >= HARD_BLINK_COOLDOWN:
                   if selected_option == 0:  #Easy
                       PIPE_GAP = int(SCREEN_HEIGHT / 1.8 * PIPE_GAP_MODIFIER)
                       PIPE_SPEED = SCREEN_WIDTH // 189
                       menu_active = False
                       CURRENT_MODE = "easy"
                       GRAVITY = (SCREEN_HEIGHT * 0.0004166666667) // 2
                       settings()
                   elif selected_option == 1:  # Medium
                       PIPE_GAP = int(SCREEN_HEIGHT / 2.57 * PIPE_GAP_MODIFIER)
                       PIPE_SPEED = SCREEN_WIDTH // 189
                       menu_active = False
                       CURRENT_MODE = "medium"
                       GRAVITY = (SCREEN_HEIGHT * 0.0004166666667)
                       settings()
                   elif selected_option == 2:  # Hard
                       PIPE_GAP = int(SCREEN_HEIGHT / 3 * PIPE_GAP_MODIFIER)
                       PIPE_SPEED = SCREEN_WIDTH // 189 * 2.75
                       menu_active = False
                       CURRENT_MODE = "hard"
                       GRAVITY = (SCREEN_HEIGHT * 0.0004166666667) * 1.6666666
                       settings()
                   elif selected_option == 3:  # Settings
                       menu_active = False
                       settings()
def abilities():
    global ABILITY_COST, CURRENT_ABILITY, PIPE_GAP, PIPE_GAP_MODIFIER, ability_cooldown

    font = pygame.font.Font(None, FONT_SIZE)
    menu_active = True
    time_since_start = datetime.now()
    selected_option = 0
    options = ["Explode Pipes", "Shield", "Bonus Score", "Larger Gaps", "Settings"]

    while menu_active:
        screen.blit(main_menu_background, (0, 0))
        title_text = font.render("Abilities", True, WHITE)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 5))

        for i, option in enumerate(options):
            color = (0, 255, 255) if i == selected_option else (240, 240, 240)
            option_text = font.render(option, True, color)
            screen.blit(option_text, (SCREEN_WIDTH // 2 - option_text.get_width() // 2, SCREEN_HEIGHT // 2.5 + i * 60))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:  # Next Option
                    selected_option = (selected_option + 1) % len(options)
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_RETURN and datetime.now() - time_since_start >= HARD_BLINK_COOLDOWN:
                    if selected_option == 0:  # Explode
                        CURRENT_ABILITY = "explode"
                        ABILITY_COST = 0
                        ability_cooldown = timedelta(seconds=20)
                        menu_active = False
                        settings()
                    elif selected_option == 1:  # Shield
                        CURRENT_ABILITY = "shield"
                        ABILITY_COST = 10
                        ability_cooldown = timedelta(seconds=30)
                        menu_active = False
                        settings()
                    elif selected_option == 2:  # Bonus Score
                        CURRENT_ABILITY = "bonus score"
                        ABILITY_COST = 0
                        ability_cooldown = timedelta(seconds=25)
                        menu_active = False
                        settings()
                    elif selected_option == 3:  # Larger Gaps
                        ABILITY_COST = 0
                        CURRENT_ABILITY = "larger gaps"
                        PIPE_GAP_MODIFIER = 1.15
                        menu_active = False
                        settings()
                    elif selected_option == 4:  # Settings
                        menu_active = False
                        settings()


def input_name(score):
    font = pygame.font.Font(None, FONT_SIZE)
    input_box = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 50)
    color = pygame.Color('dodgerblue2')
    character_options = [chr(i) for i in range(ord('A'), ord('Z') + 1)] + [' ']
    max_length = 3
    name = []
    current_char_index = 0
    done = False
    time_since_start = datetime.now()

    score_recieved = score

    while not done:
        screen.fill((30, 30, 30))

        score_text = font.render(f"Score: {int(score_recieved)}", True, WHITE)
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 4))

        instruction_text = font.render(f"Enter your Initials", True, WHITE)
        screen.blit(instruction_text, (SCREEN_WIDTH // 2 - instruction_text.get_width() // 2, SCREEN_HEIGHT // 2.5))

        current_char = character_options[current_char_index]
        text_surface = font.render(''.join(name) + current_char, True, color)
        screen.blit(text_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, color, input_box, 2)
        pygame.display.flip()

        current_time = datetime.now()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                    # Cycle through character options with Shift
                    current_char_index = (current_char_index + 1) % len(character_options)
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_RETURN and current_time - time_since_start >= HARD_BLINK_COOLDOWN:
                    # Confirm the character and move to the next
                    time_since_start = datetime.now()
                    if len(name) < max_length:
                        name.append(character_options[current_char_index])
                        current_char_index = 0
                    # Check if the name is complete
                    if len(name) == max_length:
                        done = True

    name_final = ''.join(name)
    # print(name_final)
    # Add users score to the leaderboard
    save_score(name_final, score)

    main_menu()
    main_game()


def shield_crash():
    global SHIELD_ACTIVE, CRASH_TYPE, ship_y, TIME_SINCE_CRASH, ship_velocity, ship
    SHIELD_ACTIVE = False
    TIME_SINCE_CRASH = datetime.now()
    if (CRASH_TYPE == "screen"):
        ship_y = SCREEN_HEIGHT // 2
        ship_velocity = 0
    ship = pygame.image.load(ship_img).convert_alpha()
    ship = pygame.transform.scale(ship, (int(SCREEN_WIDTH / 16.16), int(SCREEN_HEIGHT / 20)))


def draw_shield():
    shield = pygame.image.load(shield_image).convert_alpha()
    shield = pygame.transform.scale(shield, (int(SCREEN_WIDTH / 11.5), int(SCREEN_HEIGHT / 13)))

    rotated_shield = pygame.transform.rotate(shield, ship_rotation)
    ship_rect = rotated_shield.get_rect(center=(ship_x, ship_y))

    shield_rect = rotated_shield.get_rect(center=(ship_x, ship_y))
    screen.blit(rotated_shield, shield_rect.topleft)


def main_game():
    time.sleep(0.5)
    global background, ship_velocity, ship_rotation, ship_y, pipe_timer, pipe_list, score, score_updated, ability_last_used, play_game, SHIELD_ACTIVE, INVINCIBILITY_SECONDS, TIME_SINCE_CRASH, PIPE_SPEED, SCREEN_WIDTH, audio_exists
    ship_y = SCREEN_HEIGHT // 2
    ship_velocity = 0
    ship_rotation = 0
    pipe_list = []
    pipe_timer = 0
    score = 0
    score_updated = False
    clock = pygame.time.Clock()
    running = True
    play_game = True
    ability_last_used = datetime.min
    time_since_start = datetime.now()

    # Start playing music when the game starts
    if (audio_exists):
        pygame.mixer.init()
        pygame.mixer.music.load(game_music_1)
        pygame.mixer.music.play(-1)
        ability_sound = pygame.mixer.Sound(ability_sfx)
        money_sound = pygame.mixer.Sound(money_sfx)
        shield_sound = pygame.mixer.Sound(shield_on_sfx)

    background_x = 1
    while running:
        screen.blit(background, (background_x, 0))
        screen.blit(background, (background_x + BACKGROUND_LENGTH, 0))
        if (background_x / BACKGROUND_LENGTH <= -1):
            background_x = 1

        background_x -= BACKGROUND_SPEED
        current_time = datetime.now()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    ship_velocity = SHIP_JUMP
                elif event.key == pygame.K_x and current_time - time_since_start >= HARD_BLINK_COOLDOWN:
                    current_time = datetime.now()
                    if current_time - ability_last_used >= ability_cooldown and score >= ABILITY_COST and CURRENT_ABILITY == "explode":
                        score -= ABILITY_COST
                        pipe_list.clear()
                        ability_last_used = current_time
                        if audio_exists:
                            ability_sound.play(0, 2000, 0)
                    elif current_time - ability_last_used >= ability_cooldown and score >= ABILITY_COST and CURRENT_ABILITY == "shield" and not SHIELD_ACTIVE:
                        draw_shield()
                        SHIELD_ACTIVE = True
                        score -= ABILITY_COST
                        ability_last_used = current_time
                        if audio_exists:
                            shield_sound.play(0, 2000, 0)
                    elif current_time - ability_last_used >= ability_cooldown and score >= ABILITY_COST and CURRENT_ABILITY == "bonus score":
                        score -= ABILITY_COST
                        ability_last_used = current_time
                        score += 5
                        if audio_exists:
                            money_sound.play(0, 2000, 0)

        # Ship movement and rotation
        ship_velocity += GRAVITY
        ship_y += ship_velocity

        if ship_velocity < 0:
            ship_rotation += 2
        else:
            ship_rotation -= 2

        if ship_rotation > max_upward_angle:
            ship_rotation -= 2
        elif ship_rotation < max_downward_angle:
            ship_rotation += 2

        # Pipe management
        pipe_timer += 1
        # Adjust the pipe generation rate here (lower value means more frequent pipes)
        if pipe_timer >= 90:
            pipe_list.append(create_pipe())
            pipe_timer = 0

        move_pipes()

        # Check for collisions
        current_time = datetime.now()
        if check_collision() and current_time - TIME_SINCE_CRASH > INVINCIBILITY_SECONDS:
            print("Collision detected!")
            if (SHIELD_ACTIVE):
                shield_crash()
                if (audio_exists):
                    shield_break_sound = pygame.mixer.Sound(shield_break_sfx)
                    shield_break_sound.play(0, 2000, 0)
            else:
                if (audio_exists):
                    crash_sound = pygame.mixer.Sound(crash_sfx)
                    crash_sound.play(0, 2000, 0)
                running = False

        draw_ship()
        if SHIELD_ACTIVE:
            draw_shield()
        draw_pipes()
        result_score = draw_score()
        draw_cooldown_timer()
        pygame.display.flip()
        # Adjusting framerate
        clock.tick(30)

        # Stop music when the game ends
    if (audio_exists):
        pygame.mixer.music.stop()

    result = game_over_menu()
    if result == "restart":
        ship_y = SCREEN_HEIGHT // 2
        ship_velocity = 0
        ship_rotation = 0
        pipe_list = []
        pipe_timer = 0
        score = 0
        score_updated = False
        main_game()
    elif result == "main_menu":
        main_menu()
        main_game()
    elif result == "input_score":
        input_name(result_score)
    elif result == "settings":
        settings()


if __name__ == "__main__":
    calibration()
