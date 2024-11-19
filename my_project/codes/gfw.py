from pico2d import *

StartScene = True
IngameScene = False
canvas_width = 1100
canvas_height = 675
open_canvas(canvas_width, canvas_height)
center_x = canvas_width // 2
center_y = canvas_height // 2

start_bg = load_image('codes\\res\\StartImage.png')
ingame_bg = load_image('codes\\res\\IngameImage.bmp')
player1_w = load_image('codes\\res\\walking.png')
player1_rw = load_image('codes\\res\\reverse_walking.png')
player1_j = load_image('codes\\res\\p1_jump.png')
player1_s = load_image('codes\\res\\slide.png')
player1_rs = load_image('codes\\res\\reverse_slide.png')

player2_w = load_image('codes\\res\\reverse_walking.png')  # 플레이어2의 걷는 이미지
player2_rw = load_image('codes\\res\\walking.png')
player2_j = load_image('codes\\res\\p2_jump.png')
player2_s = load_image('codes\\res\\reverse_slide.png')
player2_rs = load_image('codes\\res\\slide.png')

# StartScene 루프
StartScene = True
while StartScene:
    start_bg.draw_now(center_x, center_y)
    update_canvas()  # StartScene 화면을 계속 갱신
    for event in get_events():
        if event.type == SDL_QUIT:
            StartScene = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_RETURN:
            StartScene = False  # StartScene 종료
            IngameScene = True   # IngameScene 시작

# IngameScene 루프
IngameScene = True
frame1 = 0  # 플레이어1 프레임
frame2 = 0  # 플레이어2 프레임
key_state1 = {SDLK_a: False, SDLK_d: False, SDLK_w: False, SDLK_s: False}  # 플레이어1 키 상태
key_state2 = {SDLK_j: False, SDLK_l: False, SDLK_i: False, SDLK_k: False}  # 플레이어2 키 상태
draw_reverse1 = False
draw_reverse2 = False

# 플레이어1 초기 위치
p1_x_location = 200
p1_y_location = 0
p1_jump = 0
p1_slide = 0

# 플레이어2 초기 위치
p2_x_location = 800
p2_y_location = 0
p2_jump = 0
p2_slide = 0

def Check_Wall_RCollision(x):
    if x + 64 > 1100: 
        return True
    elif x + 64 > 525 and x + 64 < 575:
        return True
    else:
        return False
        
def Check_Wall_LCollision(x):
    if x - 64 < 0:
        return True
    elif x - 64 > 525 and x - 64 < 575:
        return True
    else:
        return False

while IngameScene:
    clear_canvas()  # 이전 화면을 지움
    ingame_bg.draw_now(center_x, center_y)  # 배경 그리기

    # 플레이어1 점프 및 슬라이드
    if p1_jump != 0:
        player1_j.clip_draw((frame1 // 2) * 64, 0, 64, 63, p1_x_location, p1_y_location + 110 + p1_jump, 128, 126)
        p1_y_location = p1_y_location + p1_jump
        frame1 += 1
        if frame1 == 10:
            frame1 = 9
        if p1_y_location >= 150:
            p1_jump = -p1_jump
        elif p1_y_location == 0:
            p1_jump = 0
            frame1 = 0
    elif p1_slide > 0:
        if(Check_Wall_RCollision(p1_x_location + p1_slide)):
            p1_x_location += p1_slide
            p1_slide = 0
            frame1 = 0
        else:
            player1_s.clip_draw(frame1 // 2 * 64, 0, 64, 63, p1_x_location + p1_slide, p1_y_location + 110 + p1_jump, 128, 126)
            p1_slide = p1_slide + 20
            frame1 += 1
            if p1_slide > 120:
                p1_x_location += p1_slide
                p1_slide = 0
                frame1 = 0
    elif p1_slide < 0:
        if(Check_Wall_LCollision(p1_x_location + p1_slide)):
            p1_x_location += p1_slide
            p1_slide = 0
            frame1 = 0
        else :   
            player1_rs.clip_draw(frame1 // 2 * 64, 0, 64, 63, p1_x_location + p1_slide, p1_y_location + 110 + p1_jump, 128, 126)
            p1_slide = p1_slide - 20
            frame1 += 1
            if p1_slide < -120:
                p1_x_location += p1_slide
                p1_slide = 0
                frame1 = 0
    elif draw_reverse1:
        player1_rw.clip_draw(frame1 * 64, 0, 64, 63, p1_x_location, p1_y_location + 110, 128, 126)
    else:
        player1_w.clip_draw(frame1 * 64, 0, 64, 63, p1_x_location, p1_y_location + 110, 128, 126)

    # 플레이어2 점프 및 슬라이드
    if p2_jump != 0:
        player2_j.clip_draw(frame2 // 2 * 64, 0, 64, 63, p2_x_location, p2_y_location + 110 + p2_jump, 128, 126)
        p2_y_location = p2_y_location + p2_jump
        frame2 += 1
        if frame2 == 10:
            frame2 = 9
        if p2_y_location >= 150:
            p2_jump = -p2_jump
        elif p2_y_location == 0:
            p2_jump = 0
            frame2 = 0
    elif p2_slide > 0:
        if Check_Wall_RCollision(p2_x_location + p2_slide):
            p2_x_location += p2_slide
            p2_slide = 0
            frame2 = 0
        else:
            player2_rs.clip_draw(frame2 // 2 * 64, 0, 64, 63, p2_x_location + p2_slide, p2_y_location + 110 + p2_jump, 128, 126)
            p2_slide = p2_slide + 20
            frame2 += 1
            if p2_slide > 120:
                p2_x_location += p2_slide
                p2_slide = 0
                frame2 = 0
    elif p2_slide < 0:
        if Check_Wall_LCollision(p2_x_location + p2_slide):
            p2_x_location += p2_slide
            p2_slide = 0
            frame2 = 0
        else:
            player2_s.clip_draw(frame2 // 2 * 64, 0, 64, 63, p2_x_location + p2_slide, p2_y_location + 110 + p2_jump, 128, 126)
            p2_slide = p2_slide - 20
            frame2 += 1
            if p2_slide < -120:
                p2_x_location += p2_slide
                p2_slide = 0
                frame2 = 0
    elif draw_reverse2:
        player2_rw.clip_draw(frame2 * 64, 0, 64, 63, p2_x_location, p2_y_location + 110, 128, 126)
    else:
        player2_w.clip_draw(frame2 * 64, 0, 64, 63, p2_x_location, p2_y_location + 110, 128, 126)

    update_canvas()

    # 이벤트 처리
    for event in get_events():
        if event.type == SDL_QUIT:
            IngameScene = False
        elif event.type == SDL_KEYDOWN:
            # 플레이어1 키 입력
            if event.key == SDLK_a and p1_y_location == 0:
                draw_reverse1 = True
                key_state1[SDLK_a] = True
            elif event.key == SDLK_d and p1_y_location == 0:
                draw_reverse1 = False
                key_state1[SDLK_d] = True
            elif event.key == SDLK_w and p1_y_location == 0:
                p1_slide = 0
                p1_jump = 25
            elif event.key == SDLK_s and p1_y_location == 0 and Check_Wall_RCollision(p1_x_location + p1_slide) == False and Check_Wall_LCollision(p1_x_location + p1_slide) == False:
                key_state1[SDLK_a] = False
                key_state1[SDLK_d] = False
                p1_x_location += p1_slide
                p1_slide = -20 if draw_reverse1 else 20

            # 플레이어2 키 입력
            if event.key == SDLK_j and p2_y_location == 0:
                draw_reverse2 = False
                key_state2[SDLK_j] = True
            elif event.key == SDLK_l and p2_y_location == 0:
                draw_reverse2 = True
                key_state2[SDLK_l] = True
            elif event.key == SDLK_i and p2_y_location == 0:
                p2_slide = 0
                p2_jump = 25
            elif event.key == SDLK_k and p2_y_location == 0 and Check_Wall_RCollision(p2_x_location + p2_slide) == False and Check_Wall_LCollision(p2_x_location + p2_slide) == False:
                key_state2[SDLK_l] = False
                key_state2[SDLK_j] = False
                p2_x_location += p2_slide
                p2_slide = 20 if draw_reverse2 else -20

        elif event.type == SDL_KEYUP:
            # 플레이어1 키 해제
            if event.key == SDLK_a:
                key_state1[SDLK_a] = False
            elif event.key == SDLK_d:
                key_state1[SDLK_d] = False

            # 플레이어2 키 해제
            if event.key == SDLK_j:
                key_state2[SDLK_j] = False
            elif event.key == SDLK_l:
                key_state2[SDLK_l] = False

    # 키 상태에 따른 이동
    if key_state1[SDLK_a]:
        if(Check_Wall_LCollision(p1_x_location) == False):
            p1_x_location -= 10
            frame1 = (frame1 + 1) % 5
    elif key_state1[SDLK_d]:
        if(Check_Wall_RCollision(p1_x_location) == False):
            p1_x_location += 10
            frame1 = (frame1 + 1) % 5
    else:
        frame1 = 0

    if key_state2[SDLK_j]:
        if(Check_Wall_LCollision(p2_x_location) == False):
            p2_x_location -= 10
            frame2 = (frame2 + 1) % 5
    elif key_state2[SDLK_l]:
        if(Check_Wall_RCollision(p2_x_location) == False):
            p2_x_location += 10
            frame2 = (frame2 + 1) % 5
    else:
        frame2 = 0
    delay(0.05)

close_canvas()
