from pico2d import *

canvas_width = 1100
canvas_height = 675
open_canvas(canvas_width,canvas_height)
center_x = canvas_width // 2
center_y = canvas_height // 2

start_bg = load_image('codes\\res\\StartImage.png')
start_bg.draw_now(center_x,center_y)

running = True
while running:
    for event in get_events():
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_RETURN:  # enter 키를 누르면 시작화면을 종료
                running = False

ingame_bg = load_image('codes\\res\\IngameImage.bmp')
ingame_bg.draw_now(center_x,center_y)

running = True
while running:
    for event in get_events():
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:  # ESC 키를 누르면 인게임 화면을 종료
                running = False

close_canvas()