
import pygame
import serial
import time

# Config & Setup
FPS = 60
SCREEN_WIDTH = 780
SCREEN_HEIGHT = 780
background_color = 'black'
background_draw_color = 'white'
indicator_color = 'red'

#you MUST select the right port.
arduino_port = "COM6"



pygame.init()
clock = pygame.time.Clock()
# setup
setup = 0
joysticks = []
arduino = None
# EXPERIMENTAL:
try:
    arduino = serial.Serial(port=arduino_port, baudrate=115200, timeout=0.01)
    time.sleep(.01)

except:
    print("ERROR: Could not connect to Arduino")
    print("Waiting for arduino connection...")
    setup -= 1

if pygame.joystick.get_count() == 0:
    print("ERROR: Joystick not found")
    print("Waiting for joystick connection...")
    setup -= 1

def setup_check():
    global setup, arduino
    if setup < 0:

        if arduino is None:
            try:
                arduino = serial.Serial(port=arduino_port, baudrate=115200, timeout=0.01)
                time.sleep(.01)

            except:
                pass

            else:
                print("Arduino connected")
                setup += 1

        if pygame.joystick.get_count() == 0:
            #for event in pygame.event.get():
            #    if event.type == pygame.JOYDEVICEADDED:
            #        joy = pygame.joystick.Joystick(event.device_index)
            #        joysticks.append(joy)

            if pygame.joystick.get_count() > 0:
                print("Joystick found")
                setup += 1

    else: setup = 1

# screen stuff
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_icon(pygame.image.load('icon.png'))
pygame.display.set_caption('JVS Ground Station')
scr_x = SCREEN_WIDTH / 2
scr_y = SCREEN_HEIGHT / 2
scr_z = 0
scr_slider = 500
stick_pos = pygame.Rect(scr_x, scr_y, 1, 1)

joy_area = 3.5
indicator_width = 2
font_size = 20
font = pygame.font.SysFont('arial', font_size)

def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img, (x, y))

def draw_background():
    screen.fill(pygame.Color(background_color))
    #pygame.draw.rect(screen, pygame.Color(background_draw_color), pygame.Rect(SCREEN_WIDTH / 2 - SCREEN_WIDTH / joy_area, SCREEN_HEIGHT * 0.622 - SCREEN_HEIGHT / joy_area, SCREEN_WIDTH / (joy_area * 0.5), SCREEN_HEIGHT / (joy_area * 1)))
    #pygame.draw.rect(screen, pygame.Color(background_color), pygame.Rect(SCREEN_WIDTH / 2 - SCREEN_WIDTH / joy_area + 3, SCREEN_HEIGHT * 0.622 - SCREEN_HEIGHT / joy_area + 3, SCREEN_WIDTH / (joy_area * 0.5) - 6, SCREEN_HEIGHT / (joy_area * 1) - 6))
    pygame.draw.circle(screen, pygame.Color(background_draw_color), (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), 3, 3)
    pygame.draw.circle(screen, pygame.Color(background_draw_color), (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), SCREEN_WIDTH / joy_area, 3)
    pygame.draw.circle(screen, pygame.Color(background_draw_color), (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), SCREEN_WIDTH / (joy_area * 1.33), 3)
    pygame.draw.circle(screen, pygame.Color(background_draw_color), (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), SCREEN_WIDTH / (joy_area * 2), 3)
    pygame.draw.circle(screen, pygame.Color(background_draw_color), (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), SCREEN_WIDTH / (joy_area * 4), 3)

def draw_info():
    global joystick

    if arduino is None:
        draw_text('ARDUINO NOT FOUND', font, pygame.Color('red'), SCREEN_WIDTH * 0.37, SCREEN_HEIGHT * 0.95)

    if not joysticks:
        draw_text('JOYSTICK NOT FOUND', font, pygame.Color('red'), SCREEN_WIDTH * 0.37, SCREEN_HEIGHT * 0.014)
    else:
        for joystick in joysticks:
            draw_text(str(joystick.get_name()), font, pygame.Color(background_draw_color), 260, 10)
            draw_text("Number of axes: " + str(joystick.get_numaxes()), font, pygame.Color(background_draw_color), 260, 35)
            draw_text("X_Axis: " + str(X_Axis), font, pygame.Color(background_draw_color), 10, 10)
            draw_text("Y_Axis: " + str(Y_Axis), font, pygame.Color(background_draw_color), 10, 35)
            draw_text("Z_Axis: " + str(Z_Axis), font, pygame.Color(background_draw_color), 10, 60)
            draw_text("Slider_Axis: " + str(Slider_Axis), font, pygame.Color(background_draw_color), 10, 85)

            draw_text(str("Hat:"), font, pygame.Color(background_draw_color), 485, 35)
            if joystick.get_hat(0) == (0, 1):
                draw_text(str("up"), font, pygame.Color(background_draw_color), 535, 35)
            if joystick.get_hat(0) == (0, -1):
                draw_text(str("down"), font, pygame.Color(background_draw_color), 535, 35)
            if joystick.get_hat(0) == (-1, 0):
                draw_text(str("left"), font, pygame.Color(background_draw_color), 535, 35)
            if joystick.get_hat(0) == (1, 0):
                draw_text(str("right"), font, pygame.Color(background_draw_color), 535, 35)

            if joystick.get_hat(0) == (1, 1):
                draw_text(str("upright"), font, pygame.Color(background_draw_color), 535, 35)
            if joystick.get_hat(0) == (1, -1):
                draw_text(str("downright"), font, pygame.Color(background_draw_color), 535, 35)
            if joystick.get_hat(0) == (-1, -1):
                draw_text(str("downleft"), font, pygame.Color(background_draw_color), 535, 35)
            if joystick.get_hat(0) == (-1, 1):
                draw_text(str("upleft"), font, pygame.Color(background_draw_color), 535, 35)

            draw_text(str("Btn:"), font, pygame.Color(background_draw_color), 485, 10)
            if joystick.get_button(0):
                draw_text(str("0"), font, pygame.Color(background_draw_color), 535, 10)
            if joystick.get_button(1):
                draw_text(str("1"), font, pygame.Color(background_draw_color), 535, 10)
            if joystick.get_button(2):
                draw_text(str("2"), font, pygame.Color(background_draw_color), 535, 10)
            if joystick.get_button(3):
                draw_text(str("3"), font, pygame.Color(background_draw_color), 535, 10)
            if joystick.get_button(4):
                draw_text(str("4"), font, pygame.Color(background_draw_color), 535, 10)
            if joystick.get_button(5):
                draw_text(str("5"), font, pygame.Color(background_draw_color), 535, 10)
            if joystick.get_button(6):
                draw_text(str("6"), font, pygame.Color(background_draw_color), 535, 10)
            if joystick.get_button(7):
                draw_text(str("7"), font, pygame.Color(background_draw_color), 535, 10)
            if joystick.get_button(8):
                draw_text(str("8"), font, pygame.Color(background_draw_color), 535, 10)
            if joystick.get_button(9):
                draw_text(str("9"), font, pygame.Color(background_draw_color), 535, 10)
            if joystick.get_button(10):
                draw_text(str("10"), font, pygame.Color(background_draw_color), 535, 10)
            if joystick.get_button(11):
                draw_text(str("11"), font, pygame.Color(background_draw_color), 535, 10)
            if joystick.get_button(12):
                draw_text(str("12"), font, pygame.Color(background_draw_color), 535, 10)
            if joystick.get_button(13):
                draw_text(str("13"), font, pygame.Color(background_draw_color), 535, 10)
            if joystick.get_button(14):
                draw_text(str("14"), font, pygame.Color(background_draw_color), 535, 10)
            if joystick.get_button(15):
                draw_text(str("15"), font, pygame.Color(background_draw_color), 535, 10)

def draw_pointer():
    stick_pos.center = (scr_x, scr_y)
    pygame.draw.rect(screen, pygame.Color(indicator_color), pygame.Rect(scr_x - 1, scr_y - indicator_width * 5, indicator_width, indicator_width * 10))
    pygame.draw.rect(screen, pygame.Color(indicator_color), pygame.Rect(scr_x - indicator_width * 5, scr_y - 1, indicator_width * 10, indicator_width))
    pygame.draw.rect(screen, pygame.Color(indicator_color), stick_pos)

def draw_throttle():
    pygame.draw.rect(screen, pygame.Color(background_draw_color), pygame.Rect(SCREEN_WIDTH * 0.86, SCREEN_HEIGHT / 4.66, joy_area * 14.3, SCREEN_HEIGHT / 1.75))
    pygame.draw.rect(screen, pygame.Color(background_color), pygame.Rect(SCREEN_WIDTH * 0.86 + 3, SCREEN_HEIGHT / 4.66 + 3, joy_area * 14.3 - 6, SCREEN_HEIGHT / 1.75 - 6))
    pygame.draw.rect(screen, pygame.Color(indicator_color), pygame.Rect(SCREEN_WIDTH * 0.86 + 9, (SCREEN_HEIGHT / 4.66 + 9) + (SCREEN_HEIGHT / 1.75 - 18) * (1 - scr_slider / 1000), joy_area * 14.3 - 18, (SCREEN_HEIGHT / 1.75 - 18) * (scr_slider / 1000)))

def draw_z_arrow():
    arrow_width = indicator_width * 10
    arrow_height = indicator_width * 20
    scr_z_arrow = pygame.Surface((arrow_width, arrow_height), pygame.SRCALPHA)
    pygame.draw.rect(scr_z_arrow, pygame.Color(indicator_color), pygame.Rect(0, arrow_height // 2 - indicator_width // 2, arrow_width, indicator_width))
    pygame.draw.rect(scr_z_arrow, pygame.Color(indicator_color), pygame.Rect(arrow_width // 2 - indicator_width // 2, 0, indicator_width, arrow_height))
    pygame.draw.rect(scr_z_arrow, pygame.Color(background_color), pygame.Rect(0, arrow_height * 0.75, arrow_width, arrow_height * 0.25))
    scr_z_arrow_rotated = pygame.transform.rotate(scr_z_arrow, scr_z)
    scr_z_arrow_rotated_rect = scr_z_arrow_rotated.get_rect(center=(SCREEN_WIDTH / 10, SCREEN_HEIGHT / 2))
    screen.blit(scr_z_arrow_rotated, scr_z_arrow_rotated_rect.topleft)

# modes
arm = 1100
failsafe = 1200
# = 1300
# = 1400
manual = 1500
auto_trim = 1600
auto_launch = 1700
altitude_hold = 1800
flaperon = 1900

X_Axis = 1500
Y_Axis = 1500
Slider_Axis = 1500
Z_Axis = 1500
Cam_X = 1500
Cam_Y = 1500
AUX = 1500
MODE = 1000
Arduino_LED = 0
def map_val(mapit, inmin, inmax, outmin, outmax):
    return (outmin + (((mapit - inmin) / (inmax - inmin)) * (outmax - outmin))) // 1



startMarker = '<'
endMarker = '\n'
dividingmarker = ','
def Send_Data():

    Sending_Data = str(X_Axis)
    Sending_Data += (dividingmarker)
    Sending_Data += str(Y_Axis)
    Sending_Data += (dividingmarker)
    Sending_Data += str(Slider_Axis)
    Sending_Data += (dividingmarker)
    Sending_Data += str(Z_Axis)
    Sending_Data += (dividingmarker)
    Sending_Data += str(Cam_X)
    Sending_Data += (dividingmarker)
    Sending_Data += str(Cam_Y)
    Sending_Data += (dividingmarker)
    Sending_Data += str(AUX)
    Sending_Data += (dividingmarker)
    Sending_Data += str(MODE)
    Sending_Data += (dividingmarker)
    Sending_Data += str(Arduino_LED)
    Sending_Data += (endMarker)

    Sending_Data_ByteArray = bytearray(Sending_Data, 'ascii')

    if arduino.inWaiting():
        arduino.flush()
        arduino.write(Sending_Data_ByteArray)
        data = arduino.readline()
        print(data)
        arduino.flush()
    else: draw_text('ARDUINO NOT FOUND', font, pygame.Color('red'), SCREEN_WIDTH * 0.37, SCREEN_HEIGHT * 0.95)

#this
setup = 1

running = True
while running:

    #this is experimental, use "setup_check" at your own risk and if you do so, comment the "setup = 1" line above.
    #setup_check()

    clock.tick(FPS)

    draw_background()
    draw_info()
    draw_pointer()
    draw_z_arrow()
    draw_throttle()

    if setup == 1:

        for joystick in joysticks:

            Arduino_LED = 1

            # Axes
            X_Axis = map_val(joystick.get_axis(0), -1, 1, 1000, 2000)
            Y_Axis = map_val(joystick.get_axis(1), -1, 1, 2000, 1000)
            Z_Axis = map_val(joystick.get_axis(2), -1, 1, 1000, 2000)
            Slider_Axis = map_val(joystick.get_axis(3), -1, 1, 2000, 1000)
            if X_Axis > 1995: X_Axis = 2000
            if Z_Axis > 1400 and Z_Axis < 1525: Z_Axis = 1500
            if Z_Axis > 1995: Z_Axis = 2000

            # Mode Selector
            if (joystick.get_button(7) & joystick.get_button(13)): MODE = arm
            if joystick.get_button(2): MODE = manual
            if joystick.get_button(15): MODE = auto_trim
            if joystick.get_button(1): MODE = flaperon
            if joystick.get_button(9): MODE = auto_launch

            # Hat Switch / Camera Control
            Cam_X = 1500
            Cam_Y = 1500
            Cam_Vel = -50 #-500 to 500
            if joystick.get_hat(0) == (1, 0):
                Cam_X = 1500 + Cam_Vel #right
            if joystick.get_hat(0) == (-1, 0):
                Cam_X = 1500 - Cam_Vel #left
            if joystick.get_hat(0) == (0, 1):
                Cam_Y = 1500 + Cam_Vel #up
            if joystick.get_hat(0) == (0, -1):
                Cam_Y = 1500 - Cam_Vel #down

            if joystick.get_hat(0) == (1, -1):
                Cam_X = 1500 + Cam_Vel # right
                Cam_Y = 1500 - Cam_Vel # down
            if joystick.get_hat(0) == (1, 1):
                Cam_X = 1500 + Cam_Vel # right
                Cam_Y = 1500 + Cam_Vel # up
            if joystick.get_hat(0) == (-1, -1):
                Cam_X = 1500 - Cam_Vel  # left
                Cam_Y = 1500 - Cam_Vel  # down
            if joystick.get_hat(0) == (-1, 1):
                Cam_X = 1500 - Cam_Vel # left
                Cam_Y = 1500 + Cam_Vel # up

            # Screen Axes
            scr_x = (SCREEN_WIDTH / 2) + joystick.get_axis(0) * (SCREEN_WIDTH / joy_area)
            scr_y = (SCREEN_HEIGHT / 2) + joystick.get_axis(1) * (SCREEN_HEIGHT / joy_area)
            scr_z = map_val(joystick.get_axis(2), -1, 1, 35, -35)
            scr_slider = map_val(joystick.get_axis(3), -1, 1, 1000, 0)

        Send_Data()

    # event handler
    for event in pygame.event.get():
        if event.type == pygame.JOYDEVICEADDED:
            joy = pygame.joystick.Joystick(event.device_index)
            joysticks.append(joy)
        # quit program
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

pygame.quit()
