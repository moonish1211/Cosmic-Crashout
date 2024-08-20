import pygame
import sys
import random
import socket
import json
from datetime import datetime, timedelta
import statistics
import time

# List of files we need
rocket_image = "EEG_Game/rocket2.png"
pipe_load_image = 'EEG_Game/pipe.png'
background_5_img = 'EEG_Game/background5.png'
main_menu_imgage = 'EEG_Game/img.png'
leaderboard_txt = 'EEG_Game/leaderboard.txt'
game_music_1 = 'EEG_Game/Game music.mp3'


# Initialize Pygame
pygame.init()

# Constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PIPE_COLOR = (0, 255, 0)
GRAVITY = 0.3
BIRD_JUMP = -7
PIPE_WIDTH = 80
PIPE_GAP = 350
PIPE_SPEED = 8
WIDTH_BIRD = 50
HEIGHT_BIRD = 50
FONT_SIZE = 36
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
ABILITY_COST = 0 * 8  # The first number is the ability cost, the * 8 is to match the scoring system

# Set up display
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # Set full-screen mode
SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()  # Update screen dimensions

PIPE_GAP = int(SCREEN_HEIGHT/ 2.57)
print(SCREEN_WIDTH, SCREEN_HEIGHT)

pygame.display.set_caption('Flappy Bird')

# Load assets
bird = pygame.image.load(rocket_image).convert_alpha()  # Load and convert the bird image
bird = pygame.transform.scale(bird, (66, 30))  # Scale the image if needed
pipe_image = pygame.image.load(pipe_load_image).convert_alpha()  # Load the pipe image
pipe_image = pygame.transform.scale(pipe_image, (PIPE_WIDTH, SCREEN_HEIGHT))  # Scale the pipe image

# Load background images
background = pygame.image.load(background_5_img).convert()
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Scale to match screen size

main_menu_background = pygame.image.load(main_menu_imgage).convert()
main_menu_background = pygame.transform.scale(main_menu_background, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Scale to match screen size

original_width, original_height = bird.get_size()
aspect_ratio = original_width / original_height
new_width = 75
new_height = int(new_width / aspect_ratio)
bird = pygame.transform.scale(bird, (new_width, new_height))
max_upward_angle = 45
max_downward_angle = -45
recovery_speed = 2

# Bird settings
bird_x = 50
bird_y = SCREEN_HEIGHT // 2
bird_velocity = 0
bird_rotation = 0  # Rotation angle in degrees

# Pipe settings
pipe_list = []
pipe_timer = 0
score = 0
score_updated = False  # Flag to check if the score was already updated for a pipe set

# Set up font
font = pygame.font.Font(None, FONT_SIZE)

# Ability settings
ability_last_used = datetime.min  # Initialize the last used time to the earliest possible date
ability_cooldown = timedelta(seconds=20)  # Set the cooldown time to 20 seconds

def store_score(name, score):
    print("store_score function called")
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(f"{name},{score},{current_time}")
    with open(leaderboard_txt, 'a') as f:
        f.write(f"{name},{score},{current_time}\n")

def get_top_scores():
    scores = []
    with open(leaderboard_txt, 'r') as f:
        for line in f:
            name, score_leaderboard, current_time = line.strip().split(',')
            scores.append((name, int(float(score_leaderboard)), current_time))
    # Sort the scores in descending order
    scores.sort(key=lambda x: x[1], reverse=True)
    # Return the top 5
    return scores[:5]

def create_pipe():
    # Define minimum and maximum heights for the top pipe
    min_top_height = 100
    max_top_height = SCREEN_HEIGHT - PIPE_GAP - min_top_height

    # Random height for the top pipe
    top_height = random.randint(min_top_height, max_top_height)

    # Define the top and bottom pipe rectangles
    top_pipe = pygame.Rect(SCREEN_WIDTH, 0, PIPE_WIDTH, top_height)
    bottom_pipe = pygame.Rect(SCREEN_WIDTH, top_height + PIPE_GAP, PIPE_WIDTH, SCREEN_HEIGHT - (top_height + PIPE_GAP))

    return top_pipe, bottom_pipe

def draw_pipes():
    for top_pipe, bottom_pipe in pipe_list:
        # Draw top pipe
        screen.blit(pipe_image, top_pipe.topleft, (0, 0, PIPE_WIDTH, top_pipe.height))
        # Draw bottom pipe
        screen.blit(pipe_image, bottom_pipe.topleft, (0, SCREEN_HEIGHT - bottom_pipe.height, PIPE_WIDTH, bottom_pipe.height))
        # pygame.draw.rect(screen, BLACK, top_pipe, 2)  # Draw the collision box (outline) for the top pipe
        # pygame.draw.rect(screen, BLACK, bottom_pipe, 2)  # Draw the collision box (outline) for the bottom pipe

def draw_bird():
    rotated_bird = pygame.transform.rotate(bird, bird_rotation)
    bird_rect = rotated_bird.get_rect(center=(bird_x, bird_y))
    screen.blit(rotated_bird, bird_rect.topleft)
    bird_mask = pygame.mask.from_surface(rotated_bird)
    outline = bird_mask.outline()
    # pygame.draw.polygon(screen, BLACK, [(bird_rect.left + p[0], bird_rect.top + p[1]) for p in outline], 2)

def move_pipes():
    global score, score_updated
    for pipe_pair in pipe_list:
        top_pipe, bottom_pipe = pipe_pair
        top_pipe.x -= PIPE_SPEED
        bottom_pipe.x -= PIPE_SPEED

        # Check if the bird passed the pipes to increment the score
        if top_pipe.x + PIPE_WIDTH < bird_x and not score_updated:
            score += 1
            score_updated = True

    # Reset the score_updated flag when the bird has passed the pipes
    if len(pipe_list) > 0 and pipe_list[0][0].x + PIPE_WIDTH < bird_x:
        score_updated = False

    # Remove pipes that have gone off the screen
    if len(pipe_list) > 0 and pipe_list[0][0].x < -PIPE_WIDTH:
        pipe_list.pop(0)

def check_collision():
    rotated_bird = pygame.transform.rotate(bird, bird_rotation)
    bird_rect = rotated_bird.get_rect(center=(bird_x, bird_y))
    bird_mask = pygame.mask.from_surface(rotated_bird)

    for top_pipe, bottom_pipe in pipe_list:
        top_pipe_mask = pygame.mask.from_surface(pipe_image.subsurface((0, 0, PIPE_WIDTH, top_pipe.height)))
        bottom_pipe_mask = pygame.mask.from_surface(pipe_image.subsurface((0, SCREEN_HEIGHT - bottom_pipe.height, PIPE_WIDTH, bottom_pipe.height)))

        top_pipe_offset = (top_pipe.x - bird_rect.x, top_pipe.y - bird_rect.y)
        bottom_pipe_offset = (bottom_pipe.x - bird_rect.x, bottom_pipe.y - bird_rect.y)

        if bird_mask.overlap(top_pipe_mask, top_pipe_offset) or bird_mask.overlap(bottom_pipe_mask, bottom_pipe_offset):
            return True

    if bird_y > SCREEN_HEIGHT or bird_y < 0:
        return True

    return False

def draw_score():
    global score
    score_surface = font.render(f"Score: {score // 8}", True, WHITE)
    screen.blit(score_surface, (10, 10))  # Draw the score at the top left corner
    return score // 8


def draw_cooldown_timer():
    global ability_last_used
    # Function to draw the cooldown timer
    current_time = datetime.now()
    time_since_last_use = current_time - ability_last_used
    if time_since_last_use < ability_cooldown:
        remaining_time = ability_cooldown - time_since_last_use
        remaining_seconds = remaining_time.total_seconds()
        timer_text = f"Ability ready in: {int(remaining_seconds)}s"
    else:
        timer_text = "Ability ready!"
    timer_surface = font.render(timer_text, True, WHITE)
    screen.blit(timer_surface, (SCREEN_WIDTH - 300, 10))  # Position the timer on the screen


# Define the IP address and port number for the UDP server
UDP_IP = "127.0.0.1"  # The IP address configured in the OpenBCI GUI
UDP_PORT = 12345  # The port number configured in the OpenBCI GUI

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
    #return True if list_1 goes above threshold1 and list_2 goes above threshold2
    # print(channel_1, channel_2)
    theshold_1 = 20
    threshold_2 = 5

    list_1_pass = False
    list_2_pass = False
    if channel_1 > theshold_1:
        list_1_pass = True
    if channel_2 >threshold_2:
        list_2_pass = True

    if list_1_pass and list_2_pass:
        return True
    return False

# Function to process received data
def process_data(data):
    try:
        # Decode the received data
        data_str = data.decode('utf-8')
        # Parse JSON data
        parsed_data = json.loads(data_str)
        # print(parsed_data)

        if parsed_data.get('type') == 'fft' and 'data' in parsed_data:
            fft_data = parsed_data['data']
            # print(datetime.now())

            second_channel_amplitude = fft_data[0]
            third_channel_amplitude = fft_data[2]

            frequencies = [(i * 200 / len(second_channel_amplitude)) for i in range(len(second_channel_amplitude))]

            # Frequency from 4.8 to 17.6
            amplitude_interest_second = second_channel_amplitude[3:12]
            amplitude_interest_third = third_channel_amplitude[3:12]
            frequencies_interest = frequencies[3:12]

            if filter_unconsious_blink(amplitude_interest_second):
                # print('unconcious_blink')
                return 0, 0
            # elif max(amplitude_interest) > 30:
            #     print("THAT WAS A HARD BLINK")
            #     print(max(amplitude_interest))
            else:
                # print("BLINK DETECTED")
                # print(max(amplitude_interest))
                return statistics.mean(amplitude_interest_second), statistics.mean(amplitude_interest_third)

                # Further processing can be done here
        else:
            print("Invalid data format received.")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")

def udp_listener():
    global play_game
    avr_amplitude_front_1 = 0
    avr_amplitude_back_1 = 0
    blink_count = 0
    blink_count_2 = 0
    blink_count_3 = 0
    while True:
        data, addr = sock.recvfrom(8196)  # Buffer size is 1024 bytes
        avr_amplitude_front_2, avr_amplitude_back_2 = process_data(data)

        if play_game:
            if (avr_amplitude_front_1 == avr_amplitude_front_2) and (avr_amplitude_front_2 == 0):
                #The user is not blinking, skip
                avr_amplitude_front_1 = 0
                avr_amplitude_back_2 = 0
                blink_count = 0
                blink_count_2 = 0
                continue
            elif avr_amplitude_front_1 < avr_amplitude_front_2:
                # This means that blinks are starting to be detected
                if blink_count == 0:
                    print("Blinking DETECTED!!!")
                    blink_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)
                    pygame.event.post(blink_event)
                    blink_count += 1
                    avr_amplitude_front_1 = avr_amplitude_front_2
                else:
                    avr_amplitude_front_1 = avr_amplitude_front_2
                    # print("Consecutive Blink Detected!!!")
                    # blink_count += 1
                    # if blink_count >= 4:
                    #     print("Four Consecutive Blinks Detected!!!")
                    #     blink_event = pygame.event.Event(pygame.QUIT)
                    #     pygame.event.post(blink_event)
                    # avr_amplitude = 0
            elif (avr_amplitude_front_1 > avr_amplitude_front_2):
                if blink_count_2 == 0:
                    if filter_hard_blink(avr_amplitude_front_2, avr_amplitude_back_2):
                        print("HARD BLINK TOO")
                        blink_hard_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_x)
                        pygame.event.post(blink_hard_event)
                        blink_count_2 += 1
                avr_amplitude_front_1 = avr_amplitude_front_2
                blink_count = 0
        else:
            if (avr_amplitude_front_1 == avr_amplitude_front_2) and (avr_amplitude_front_2 == 0):
                #The user is not blinking, skip
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


def main_menu():
    global play_game
    play_game = False
    menu_active = True
    selected_option = 0
    options = ["Start", "Quit"]
    # Get top scores and render the leaderboard
    top_scores = get_top_scores()
    leaderboard_texts = []
    for idx, (name, score_leaderboard, date_time) in enumerate(top_scores):
        leaderboard_text = font.render(f"{idx + 1}. {name}: {score_leaderboard}", True, pygame.Color('white'))
        leaderboard_texts.append(leaderboard_text)

    while menu_active:
        screen.blit(main_menu_background, (0, 0))  # Draw the main menu background image

        title_text = font.render("Flappy Bird", True, WHITE)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 4))

        # Draw menu options
        for i, option in enumerate(options):
            color = (145, 38, 63) if i == selected_option else WHITE # Highlight selected option
            option_text = font.render(option, True, color)
            screen.blit(option_text, (SCREEN_WIDTH // 2 - option_text.get_width() // 2, SCREEN_HEIGHT // 2.7 + i * 60))

        leaderboard_text = font.render("LEADERBOARD", True, WHITE)
        screen.blit(leaderboard_text, (SCREEN_WIDTH // 2 - leaderboard_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
        # Draw leaderboard below the play/exit options (adjusted position)
        leaderboard_start_y = SCREEN_HEIGHT // 2 + 100  # Adjusted to be lower on the screen
        for i, leaderboard_text in enumerate(leaderboard_texts):
            screen.blit(leaderboard_text,
                        (SCREEN_WIDTH // 2 - leaderboard_text.get_width() // 2, leaderboard_start_y + i * 30))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:  # Cycle through options
                    selected_option = (selected_option + 1) % len(options)
                elif event.key == pygame.K_RETURN:  # Select option
                    if selected_option == 0:  # Start
                        menu_active = False
                    elif selected_option == 1:  # Quit
                        pygame.quit()
                        sys.exit()


def game_over_menu():
    global play_game, score
    menu_active = True
    selected_option = 0
    options = ["Restart", "Main Menu", "Record Score"]
    play_game = False
    score_reviewed = score
    # Get top scores and render the leaderboard
    top_scores = get_top_scores()
    leaderboard_texts = []
    for idx, (name, score_leaderboard, date_time) in enumerate(top_scores):
        leaderboard_text = font.render(f"{idx + 1}. {name}: {score_leaderboard}", True, pygame.Color('white'))
        leaderboard_texts.append(leaderboard_text)

    while menu_active:
        screen.fill(BLACK)

        game_over_text = font.render("Game Over", True, WHITE)
        score_text = font.render(f"Score: {int(score // 8)}", True, WHITE)

        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 5))
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 4))

        # Draw menu options
        for i, option in enumerate(options):
            color = (145, 38, 63) if i == selected_option else WHITE  # Highlight selected option
            option_text = font.render(option, True, color)
            screen.blit(option_text, (SCREEN_WIDTH // 2 - option_text.get_width() // 2, SCREEN_HEIGHT // 2.5 + i * 60))

        leaderboard_text = font.render("LEADERBOARD", True, WHITE)
        screen.blit(leaderboard_text, (SCREEN_WIDTH // 2 - leaderboard_text.get_width() // 2, SCREEN_HEIGHT // 2 + 140))
        # Draw leaderboard below the play/exit options (adjusted position)
        leaderboard_start_y = SCREEN_HEIGHT // 2 + 200  # Adjusted to be lower on the screen
        for i, leaderboard_text in enumerate(leaderboard_texts):
            screen.blit(leaderboard_text,
                        (SCREEN_WIDTH // 2 - leaderboard_text.get_width() // 2, leaderboard_start_y + i * 30))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:  # Cycle through options
                    selected_option = (selected_option + 1) % len(options)
                elif event.key == pygame.K_RETURN:  # Select option
                    if selected_option == 0:  # Restart
                        menu_active = False
                        return "restart"
                    elif selected_option == 1:  # Main Menu
                        menu_active = False
                        return "main_menu"
                    elif selected_option == 2:
                        return "input_score"

def input_name(score):
    font = pygame.font.Font(None, FONT_SIZE)
    input_box = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 50)
    color = pygame.Color('dodgerblue2')
    character_options =[chr(i) for i in range(ord('a'), ord('z') + 1)] + [' ']# [' ', 'a', 'b', ..., 'z']
    max_length = 3
    name = []
    current_char_index = 0
    done = False

    score_recieved = score

    while not done:
        screen.fill((30, 30, 30))

        score_text = font.render(f"Score: {int(score_recieved // 8)}", True, WHITE)
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 4))

        instruction_text = font.render(f"Enter your Initials", True, WHITE)
        screen.blit(instruction_text, (SCREEN_WIDTH // 2 - instruction_text.get_width() // 2, SCREEN_HEIGHT // 2.5))

        # Update display
        current_char = character_options[current_char_index]
        text_surface = font.render(''.join(name) + current_char, True, color)
        screen.blit(text_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, color, input_box, 2)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                    # Cycle through character options with Shift
                    current_char_index = (current_char_index + 1) % len(character_options)
                elif event.key == pygame.K_RETURN:
                    # Confirm the character and move to the next
                    if len(name) < max_length:
                        name.append(character_options[current_char_index])
                        current_char_index = 0
                    # Check if the name is complete
                    if len(name) == max_length:
                        done = True


    name_final =  ''.join(name)
    print(name_final)
    store_score(name_final, score)

    main_menu()
    main_game()

# Load and set up music
try:
    pygame.mixer.init()
    pygame.mixer.music.load(game_music_1)  # Replace with your actual music file
    #print('audio sucsess')\
    audio_exists = True
except pygame.error as e:
    audio_exists = False
    #print('no audio detected')



def main_game():
    global bird_velocity, bird_rotation, bird_y, pipe_timer, pipe_list, score, score_updated, ability_last_used, play_game
    bird_y = SCREEN_HEIGHT // 2
    bird_velocity = 0
    bird_rotation = 0
    pipe_list = []
    pipe_timer = 0
    score = 0
    score_updated = False
    clock = pygame.time.Clock()
    running = True
    play_game = True

    # Start playing music when the game starts
    if (audio_exists):
        pygame.mixer.music.play(-1)  # -1 means the music will loop indefinitely

    while running:
        screen.blit(background, (0, 0))  # Draw the background image

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird_velocity = BIRD_JUMP
                elif event.key == pygame.K_x:
                    current_time = datetime.now()
                    if current_time - ability_last_used >= ability_cooldown and score >= ABILITY_COST:
                        score -= ABILITY_COST
                        pipe_list.clear()
                        ability_last_used = current_time
                        print("Ability used: All pipes destroyed")

        # Bird movement and rotation
        bird_velocity += GRAVITY
        bird_y += bird_velocity

        if bird_velocity < 0:
            bird_rotation += 2
        else:
            bird_rotation -= 2

        if bird_rotation > max_upward_angle:
            bird_rotation -= 2
        elif bird_rotation < max_downward_angle:
            bird_rotation += 2

        # Pipe management
        pipe_timer += 1
        if pipe_timer >= 90:  # Adjust the pipe generation rate here (lower value means more frequent pipes)
            pipe_list.append(create_pipe())
            pipe_timer = 0

        move_pipes()

        # Check for collisions
        if check_collision():
            print("Collision detected!")
            running = False

        # Draw everything
        draw_bird()
        draw_pipes()
        result_score = draw_score()
        draw_cooldown_timer()
        pygame.display.flip()
        clock.tick(30)  # Adjust the frame rate here (30 frames per second)

    # Stop music when the game ends
    if (audio_exists):
        pygame.mixer.music.stop()

    result = game_over_menu()
    if result == "restart":
        bird_y = SCREEN_HEIGHT // 2
        bird_velocity = 0
        bird_rotation = 0
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


if __name__ == "__main__":
    main_menu()
    main_game()



