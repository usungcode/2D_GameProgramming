from pico2d import *
from scene import StartScene, IngameScene

canvas_width = 1100
canvas_height = 675
open_canvas(canvas_width, canvas_height)
center_x = canvas_width // 2
center_y = canvas_height // 2

start_bg = load_image('codes\\res\\StartImage.png')
ingame_bg = load_image('codes\\res\\IngameImage.bmp')
player1_w = load_image('codes\\res\\walking.png')
player1_rw = load_image('codes\\res\\reverse_walking.png')


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
frame = 0  # frame은 한 번만 초기화하고 계속 사용
key_state = {SDLK_a: False, SDLK_d: False}  # 키 상태를 추적하기 위한 딕셔너리
draw_reverse = False

x = 200
while IngameScene:
    clear_canvas()  # 이전 화면을 지움
    ingame_bg.draw_now(center_x, center_y)  # 배경 그리기
    if (draw_reverse == True) : 
        player1_rw.clip_draw(frame * 64, 0, 64, 63, x, 110, 128, 126)  # 플레이어 그리기
    else : 
        player1_w.clip_draw(frame * 64, 0, 64, 63, x, 110, 128, 126)  # 플레이어 그리기
    update_canvas()  # 화면에 반영


    # 이벤트 처리
    for event in get_events():
        if event.type == SDL_QUIT:
            IngameScene = False  # 종료 조건
        elif event.type == SDL_KEYDOWN:
            # a 키 눌렀을 때
            if event.key == SDLK_a:
                draw_reverse = True
                key_state[SDLK_a] = True  # a 키 눌림
            # d 키 눌렀을 때
            elif event.key == SDLK_d:
                draw_reverse = False
                key_state[SDLK_d] = True  # d 키 눌림
        elif event.type == SDL_KEYUP:
            # a 키 뗐을 때
            if event.key == SDLK_a:
                key_state[SDLK_a] = False  # a 키 뗌
            # d 키 뗐을 때
            elif event.key == SDLK_d:
                key_state[SDLK_d] = False  # d 키 뗌

    # 키 상태에 따라 프레임 변경
    if key_state[SDLK_a]:
        x -= 10
        frame = (frame - 1) % 5  # a 키를 계속 눌렀을 때 frame을 감소시킴
    if key_state[SDLK_d]:
        x += 10
        frame = (frame + 1) % 5  # d 키를 계속 눌렀을 때 frame을 증가시킴

    delay(0.05)  # 딜레이로 애니메이션 속도 조절

close_canvas()  # 게임 종료 후 캔버스 닫기
