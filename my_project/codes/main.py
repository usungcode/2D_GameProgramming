from pico2d import *

class Player:
    def __init__(self, x, y, resources):
        self.x = x
        self.y = y
        self.jump = 0
        self.slide = 0
        self.frame = 0
        self.draw_reverse = False
        self.key_state = {SDLK_LEFT: False, SDLK_RIGHT: False, SDLK_UP: False, SDLK_DOWN: False}
        
        # 리소스 로드
        self.img_w, self.img_rw, self.img_j, self.img_s, self.img_rs = resources

    def update(self):
        # 점프 처리
        if self.jump != 0:
            self.y += self.jump
            self.frame = (self.frame + 1) % 10
            if self.y >= 150:
                self.jump = -self.jump
            elif self.y <= 0:
                self.y = 0
                self.jump = 0
                self.frame = 0

        # 슬라이드 처리
        elif self.slide != 0:
            slide_distance = 10  # 슬라이드 이동 거리
            max_slide_distance = 60  # 최대 슬라이드 거리
            if abs(self.slide) <= max_slide_distance and (CheckCollision.Check_Wall_LCollision(self.x + self.slide) == False and CheckCollision.Check_Wall_RCollision(self.x + self.slide) == False):
                self.x += self.slide
                self.slide += slide_distance if self.slide > 0 else -slide_distance
                self.frame = (self.frame + 1) % 5
            else:
                self.slide = 0
                self.frame = 0

        # 키 상태에 따른 이동
        elif self.key_state[SDLK_LEFT] and CheckCollision.Check_Wall_LCollision(self.x + self.slide) == False:
            self.x -= 10
            self.draw_reverse = True
            self.frame = (self.frame + 1) % 5
        elif self.key_state[SDLK_RIGHT] and CheckCollision.Check_Wall_RCollision(self.x + self.slide) == False:
            self.x += 10
            self.draw_reverse = False
            self.frame = (self.frame + 1) % 5
        else:
            self.frame = 0

    def draw_p1(self):
        # 애니메이션 그리기
        if self.jump != 0:
            self.img_j.clip_draw((self.frame // 2) * 64, 0, 64, 63, self.x, self.y + 110 + self.jump, 128, 126)
        elif self.slide > 0:
            self.img_s.clip_draw((self.frame // 2) * 64, 0, 64, 63, self.x + self.slide, self.y + 110, 128, 126)
        elif self.slide < 0:
            self.img_rs.clip_draw((self.frame // 2) * 64, 0, 64, 63, self.x + self.slide, self.y + 110, 128, 126)
        elif self.draw_reverse:
            self.img_rw.clip_draw(self.frame * 64, 0, 64, 63, self.x, self.y + 110, 128, 126)
        else:
            self.img_w.clip_draw(self.frame * 64, 0, 64, 63, self.x, self.y + 110, 128, 126)

    def draw_p2(self):
        # 애니메이션 그리기
        if self.jump != 0:
            self.img_j.clip_draw((self.frame // 2) * 64, 0, 64, 63, self.x, self.y + 110 + self.jump, 128, 126)
        elif self.slide > 0:
            self.img_rs.clip_draw((self.frame // 2) * 64, 0, 64, 63, self.x + self.slide, self.y + 110, 128, 126)
        elif self.slide < 0:
            self.img_s.clip_draw((self.frame // 2) * 64, 0, 64, 63, self.x + self.slide, self.y + 110, 128, 126)
        elif self.draw_reverse:
            self.img_w.clip_draw(self.frame * 64, 0, 64, 63, self.x, self.y + 110, 128, 126)
        else:
            self.img_rw.clip_draw(self.frame * 64, 0, 64, 63, self.x, self.y + 110, 128, 126)

class GameScene:
    def __init__(self):
        self.canvas_width = 1100
        self.canvas_height = 675
        self.center_x = self.canvas_width // 2
        self.center_y = self.canvas_height // 2
        
        # 캔버스 초기화
        open_canvas(self.canvas_width, self.canvas_height)

        # 리소스 로드
        self.start_bg = load_image('my_project\\codes\\res\\StartImage.png')
        self.ingame_bg = load_image('my_project\\codes\\res\\IngameImage.bmp')

        # 플레이어 생성
        self.player1 = Player(200, 0, [
            load_image('my_project\\codes\\res\\p1_walking.png'),
            load_image('my_project\\codes\\res\\p1_reverse_walking.png'),
            load_image('my_project\\codes\\res\\p1_jump.png'),
            load_image('my_project\\codes\\res\\p1_slide.png'),
            load_image('my_project\\codes\\res\\p1_reverse_slide.png')
        ])
        self.player2 = Player(800, 0, [
            load_image('my_project\\codes\\res\\p2_walking.png'),
            load_image('my_project\\codes\\res\\p2_reverse_walkin.png'),
            load_image('my_project\\codes\\res\\p2_jump.png'),
            load_image('my_project\\codes\\res\\p2_slide.png'),
            load_image('my_project\\codes\\res\\p2_reverse_slide.png')
        ])

    def start_scene(self):
        start_scene = True
        while start_scene:
            self.start_bg.draw_now(self.center_x, self.center_y)
            update_canvas()
            for event in get_events():
                if event.type == SDL_QUIT:
                    start_scene = False
                elif event.type == SDL_KEYDOWN and event.key == SDLK_RETURN:
                    start_scene = False

    def ingame_scene(self):
        ingame_scene = True
        while ingame_scene:
            clear_canvas()
            self.ingame_bg.draw_now(self.center_x, self.center_y)

        # 플레이어 업데이트 및 그리기
            self.player1.update()
            self.player2.update()
            self.player1.draw_p1()
            self.player2.draw_p2()

            update_canvas()
            for event in get_events():
                if event.type == SDL_QUIT:
                    ingame_scene = False
                elif event.type == SDL_KEYDOWN:
                # 플레이어1 이벤트
                    if event.key == SDLK_a:
                        self.player1.key_state[SDLK_LEFT] = True
                    elif event.key == SDLK_d:
                        self.player1.key_state[SDLK_RIGHT] = True
                    elif event.key == SDLK_w and self.player1.jump == 0:  # 점프 중복 방지
                        self.player1.jump = 25
                    elif event.key == SDLK_s and self.player1.slide == 0:  # 슬라이드 중복 방지
                        self.player1.slide = -20 if self.player1.draw_reverse else 20

                # 플레이어2 이벤트
                    if event.key == SDLK_j:
                        self.player2.key_state[SDLK_LEFT] = True
                    elif event.key == SDLK_l :
                        self.player2.key_state[SDLK_RIGHT] = True
                    elif event.key == SDLK_i and self.player2.jump == 0:  # 점프 중복 방지
                        self.player2.jump = 25
                    elif event.key == SDLK_k and self.player2.slide == 0:  # 슬라이드 중복 방지
                        self.player2.slide = -20 if self.player2.draw_reverse else 20

                elif event.type == SDL_KEYUP:
                # 플레이어1 키 해제
                    if event.key == SDLK_a:
                        self.player1.key_state[SDLK_LEFT] = False
                    elif event.key == SDLK_d:
                        self.player1.key_state[SDLK_RIGHT] = False

                # 플레이어2 키 해제
                    if event.key == SDLK_j:
                        self.player2.key_state[SDLK_LEFT] = False
                    elif event.key == SDLK_l:
                        self.player2.key_state[SDLK_RIGHT] = False
            delay(0.05)

    def run(self):
        self.start_scene()
        self.ingame_scene()
        close_canvas()

class CheckCollision:
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
        



if __name__ == '__main__':
    game = GameScene()
    game.run()
