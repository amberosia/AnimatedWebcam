import pygame
import pyautogui
import os

WIDTH, HEIGHT = 1100, 720
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Webcam")

WHITE = (255, 255, 255)
FPS = 60
SCREEN_SIZE = pyautogui.size()

WRIST_MOUSE_COORD = (273, 494)
SHOULDER_COORD_M = (434, 322)
SHOULDER_POS_M = pygame.math.Vector2(SHOULDER_COORD_M)
MOUSE_POS_ORIGIN = pygame.math.Vector2(WRIST_MOUSE_COORD)
SHOULDER_MOUSE_ORIGIN = SHOULDER_POS_M - MOUSE_POS_ORIGIN

WRIST_KEYBOARD_COORD = (450, 600)
SHOULDER_COORD_K = (602, 349)
SHOULDER_POS_K = pygame.math.Vector2(SHOULDER_COORD_K)
KEY_POS_ORIGIN = pygame.math.Vector2(WRIST_KEYBOARD_COORD)
SHOULDER_KEY_ORIGIN = SHOULDER_POS_K - KEY_POS_ORIGIN

KEYS = [[pygame.K_ESCAPE, pygame.K_BACKQUOTE, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6,
    pygame.K_7, pygame.K_8, pygame.K_9, pygame.K_0, pygame.K_MINUS, pygame.K_EQUALS, pygame.K_BACKSPACE],
    [pygame.K_TAB, pygame.K_q, pygame.K_w, pygame.K_e, pygame.K_r, pygame.K_t, pygame.K_y, pygame.K_u, pygame.K_i,
    pygame.K_o, pygame.K_p, pygame.K_LEFTBRACKET, pygame.K_RIGHTBRACKET, pygame.K_BACKSLASH],
    [pygame.K_CAPSLOCK, pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_f, pygame.K_g, pygame.K_h, pygame.K_j, pygame.K_k,
    pygame.K_l, pygame.K_SEMICOLON, pygame.K_QUOTE, pygame.K_RETURN],
    [pygame.K_LSHIFT, pygame.K_z, pygame.K_x, pygame.K_c, pygame.K_v, pygame.K_b, pygame.K_n, pygame.K_m,
    pygame.K_COMMA, pygame.K_PERIOD, pygame.K_SLASH, pygame.K_RSHIFT],
    [pygame.K_LCTRL, pygame.K_LSUPER, pygame.K_LALT, pygame.K_SPACE, pygame.K_RALT, pygame.K_RCTRL, pygame.K_LEFT,
    pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT]]

# each keyboard row's starting key coordinates and index of first and second key spacing range
KEYBOARD_INFO = [[571, 722, 4, 9], [575, 693, 4, 8], [592, 672, 4, 7], [603, 650, 3, 8], [621, 629, 2, 4]]

key_dist_x, key_dist_y = 24, 13

button_x = 981
button_h_y, button_s_y, button_a_y = 58, 205, 351
button_length = 97

# loads all images into a list
load_images = []
for file_num in range(len(os.listdir("assets"))):
    load_images.append(pygame.image.load(os.path.join("assets", str(file_num + 1) + ".png")))

# assigns variables for every index in load_images list
BG, HEAD_BEHIND, arm_mouse, mouse_none, mouse_left, mouse_right, BODY, arm_keyboard_rest, eyes, face_happy, face_sad, \
    face_angry, HAIR, BG_COVER, SIDEBAR, button_h, button_h_hover, button_h_down, button_h_down_hover, button_s, \
    button_s_hover, button_s_down, button_s_down_hover, button_a, button_a_hover, button_a_down, button_a_down_hover, \
    mouse_both, eyes_shine, arm_keyboard_press = load_images


def draw(mouse_x, mouse_y, mouse, arm_mouse_x, arm_mouse_y, arm_mouse_rotated, eyes_x, eyes_y, arm_keyboard_x,
        arm_keyboard_y, arm_keyboard_rotated, button_happy, button_sad, button_angry, face):

    WIN.fill(WHITE)

    WIN.blit(BG, (0, 0))
    WIN.blit(HEAD_BEHIND, (0, 0))
    WIN.blit(arm_mouse_rotated, (arm_mouse_x - (arm_mouse_rotated.get_width() / 2), arm_mouse_y -
                                 (arm_mouse_rotated.get_height() / 2)))
    WIN.blit(mouse, (mouse_x, mouse_y))
    WIN.blit(BODY, (0, 0))
    WIN.blit(arm_keyboard_rotated, (arm_keyboard_x - (arm_keyboard_rotated.get_width() / 2), arm_keyboard_y -
                                 (arm_keyboard_rotated.get_height() / 2)))
    WIN.blit(eyes, (eyes_x, eyes_y))
    WIN.blit(eyes_shine, (0, -5))
    WIN.blit(face, (0, 0))
    WIN.blit(HAIR, (0, 0))
    WIN.blit(BG_COVER, (0, 0))

    WIN.blit(SIDEBAR, (0, 0))
    WIN.blit(button_happy.draw(button_sad, button_angry), (0, 0))
    WIN.blit(button_sad.draw(button_happy, button_angry), (0, 0))
    WIN.blit(button_angry.draw(button_happy, button_sad), (0, 0))

    pygame.display.update()


def mouse_button_changes():
    if pygame.mouse.get_pressed(3)[0] and pygame.mouse.get_pressed(3)[2]:
        mouse = mouse_both
    elif pygame.mouse.get_pressed(3)[0]:
        mouse = mouse_left
    elif pygame.mouse.get_pressed(3)[2]:
        mouse = mouse_right
    else:
        mouse = mouse_none

    return mouse


def mouse_movement(cursor_x, cursor_y):
    # multiplies the cursor position by ratio of mouse pad to screen
    mouse_x = -cursor_x * (70 / SCREEN_SIZE[0])
    mouse_y = -cursor_x * (62 / SCREEN_SIZE[0])
    mouse_x = mouse_x - cursor_y * (-68 / SCREEN_SIZE[1])
    mouse_y = mouse_y - cursor_y * (22 / SCREEN_SIZE[1])

    return mouse_x, mouse_y


def arm_rotation(arm, shoulder_pos, arm_end, shoulder_origin):
    shoulder_to_arm_end = shoulder_pos - arm_end
    arm_angle = pygame.math.Vector2.angle_to(shoulder_to_arm_end, shoulder_origin)
    arm_rotated = pygame.transform.rotate(arm, arm_angle)

    return arm_rotated, arm_angle


def arm_movement(shoulder_arm_origin, arm_angle, base_angle, shoulder_pos, shoulder_coord, arm_end, wrist_coord):
    # finds wrist coordinate
    wrist_coords_shoulder = pygame.math.Vector2(wrist_coord[0], wrist_coord[1])
    wrist_coords_shoulder.from_polar(
        ((pygame.math.Vector2.length(shoulder_arm_origin)), -arm_angle + base_angle)
        )
    wrist_rotated_x, wrist_rotated_y = shoulder_pos + wrist_coords_shoulder

    # moves wrist to hand
    arm_x, arm_y = shoulder_coord[0] - (wrist_rotated_x - (arm_end[0])), shoulder_coord[1] - (wrist_rotated_y -
        (arm_end[1]))

    return arm_x, arm_y


def eye_movement(cursor_x):
    eyes_x = -cursor_x * (17 / SCREEN_SIZE[0])
    eyes_y = -cursor_x * (4 / SCREEN_SIZE[0])
    eyes_timer = 0

    return eyes_x, eyes_y, eyes_timer


def find_key_pos(event):
    key_x, key_y = 0, 0

    for row in range(len(KEYS)):
        if event.key in KEYS[row]:
            key_index = KEYS[row].index(event.key)
            row_start_x, row_start_y = KEYBOARD_INFO[row][0], KEYBOARD_INFO[row][1]
            range1, range2 = KEYBOARD_INFO[row][2], KEYBOARD_INFO[row][3]

            if row < 4:
                if key_index >= 0: # left section of keyboard
                    key_x = key_x + key_index * key_dist_x
                    key_y = key_y + key_index * key_dist_y

                if key_index >= range1: # middle section of keyboard
                    key_x = key_x - (key_index - range1) * 5
                    key_y = key_y - (key_index - range1) * 3

                if key_index >= range2: # right section of keyboard
                    key_x = key_x - (key_index - range2) * 5
                    key_y = key_y - (key_index - range2)

            else: # to accommodate for irregular keys on 5th row
                if 5 >= key_index >= 0:
                    key_x = key_x + key_index * key_dist_x
                    key_y = key_y + key_index * key_dist_y

                if 5 >= key_index > range1:
                    key_x = key_x + 45
                    key_y = key_y + 20

                if 5 >= key_index >= range2:
                    key_x = key_x - (key_index - range2) * 5 + 20
                    key_y = key_y - (key_index - range2)

                if key_index == 6 or key_index == 7 or key_index == 9:
                    key_x, key_y = 223, 115
                elif key_index == 8:
                    key_x, key_y = 219, 120

            key_pos = pygame.math.Vector2(row_start_x - key_x, row_start_y - key_y)
            break

        else:
            key_pos = pygame.math.Vector2(WRIST_KEYBOARD_COORD)

    return key_pos


def arm_keyboard_changes(arm_keyboard_angle):
    if True in pygame.key.get_pressed():
        arm_keyboard = arm_keyboard_press
        arm_keyboard_angle = arm_keyboard_angle
    else:
        arm_keyboard = arm_keyboard_rest
        arm_keyboard_angle = arm_keyboard_angle - 2

    arm_rotated = pygame.transform.rotate(arm_keyboard, arm_keyboard_angle)

    return arm_rotated


class Button:
    def __init__(self, button, button_hover, button_down, button_down_hover, button_x, button_y, button_dim,
        button_toggle, hotkey):
        self.button = button
        self.button_hover = button_hover
        self.button_down = button_down
        self.button_down_hover = button_down_hover
        self.rect = pygame.Rect((button_x, button_y), (button_dim, button_dim))
        self.button_toggle = button_toggle
        self.hotkey = hotkey

    def draw(self, toggle1, toggle2):
        win_cursor_x, win_cursor_y = pygame.mouse.get_pos()
        if self.button_toggle:
            displayed_button = self.button_down
            if self.rect.collidepoint(win_cursor_x, win_cursor_y):
                displayed_button = self.button_down_hover

        else:
            displayed_button = self.button
            if self.rect.collidepoint(win_cursor_x, win_cursor_y):
                displayed_button = self.button_hover
                if pygame.mouse.get_pressed(3)[0]:
                    self.button_toggle = True
                    toggle1.toggle_off()
                    toggle2.toggle_off()

            if pygame.key.get_pressed()[self.hotkey]:
                self.button_toggle = True
                toggle1.toggle_off()
                toggle2.toggle_off()

        return displayed_button

    def toggle_off(self):
        self.button_toggle = False


def face_changes(button_happy, button_sad):
    if button_happy.button_toggle:
        face = face_happy
    elif button_sad.button_toggle:
        face = face_sad
    else:
        face = face_angry

    return face


def main():
    arm_keyboard = arm_keyboard_rest
    key_pos = pygame.math.Vector2(WRIST_KEYBOARD_COORD)
    eyes_timer = 300

    button_happy = Button(button_h, button_h_hover, button_h_down, button_h_down_hover, button_x, button_h_y,
        button_length, True, pygame.K_F1)
    button_sad = Button(button_s, button_s_hover, button_s_down, button_s_down_hover, button_x, button_s_y,
        button_length, False, pygame.K_F2)
    button_angry = Button(button_a, button_a_hover, button_a_down, button_a_down_hover, button_x, button_a_y,
        button_length, False, pygame.K_F3)

    clock = pygame.time.Clock()
    run = True
    while run:
        dt = clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                key_pos = find_key_pos(event)

        arm_keyboard_rotated, arm_keyboard_angle = arm_rotation(arm_keyboard, SHOULDER_POS_K, key_pos,
            SHOULDER_KEY_ORIGIN)

        arm_keyboard_x, arm_keyboard_y = arm_movement(SHOULDER_KEY_ORIGIN, arm_keyboard_angle, 121.2, SHOULDER_POS_K,
            SHOULDER_COORD_K, key_pos, WRIST_KEYBOARD_COORD)

        arm_keyboard_rotated = arm_keyboard_changes(arm_keyboard_angle)

        mouse = mouse_button_changes()

        cursor_x, cursor_y = pyautogui.position()
        mouse_x, mouse_y = mouse_movement(cursor_x, cursor_y)

        mouse_pos = pygame.math.Vector2(mouse_x + WRIST_MOUSE_COORD[0], mouse_y + WRIST_MOUSE_COORD[1])
        arm_mouse_rotated, arm_mouse_angle = arm_rotation(arm_mouse, SHOULDER_POS_M, mouse_pos, SHOULDER_MOUSE_ORIGIN)

        arm_mouse_x, arm_mouse_y = arm_movement(SHOULDER_MOUSE_ORIGIN, arm_mouse_angle, 133.11, SHOULDER_POS_M,
            SHOULDER_COORD_M, mouse_pos, WRIST_MOUSE_COORD)

        eyes_timer += dt
        if eyes_timer >= 300:
            eyes_x, eyes_y, eyes_timer = eye_movement(cursor_x)

        face = face_changes(button_happy, button_sad)

        draw(mouse_x, mouse_y, mouse, arm_mouse_x, arm_mouse_y, arm_mouse_rotated, eyes_x, eyes_y, arm_keyboard_x,
            arm_keyboard_y, arm_keyboard_rotated, button_happy, button_sad, button_angry, face)
    pygame.quit()


if __name__ == "__main__":
    main()
