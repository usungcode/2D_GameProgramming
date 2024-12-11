from pico2d import *

class Player:
    def __init__(self, x, y, resources):
        self.x = x
        self.y = y
        self.jump = 0
        self.slide = 0
        self.frame = 0
        self.draw_reverse = False
        self.spike = True
        self.skill = True
        self.net_stop = 0
        self.spike_cooltime = 0
        self.skill_cooltime = 0
        self.key_state = {SDLK_LEFT: False, SDLK_RIGHT: False, SDLK_UP: False, SDLK_DOWN: False}
        
        # 리소스 로드
        self.img_w, self.img_rw, self.img_j, self.img_s, self.img_rs, self.img_net = resources

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
            max_slide_distance = 40  # 최대 슬라이드 거리
            if abs(self.slide) <= max_slide_distance and (CheckCollision.Check_Wall_LCollision(self.x + self.slide) == False and CheckCollision.Check_Wall_RCollision(self.x + self.slide) == False):
                self.x += self.slide
                self.slide += slide_distance if self.slide > 0 else -slide_distance
                self.frame = (self.frame + 1) % 5
            else:
                self.slide = 0
                self.frame = 0

        # 키 상태에 따른 이동
        elif self.key_state[SDLK_LEFT] and CheckCollision.Check_Wall_LCollision(self.x + self.slide) == False:
            self.x -= 5
            self.draw_reverse = True
            self.frame = (self.frame + 1) % 5
        elif self.key_state[SDLK_RIGHT] and CheckCollision.Check_Wall_RCollision(self.x + self.slide) == False:
            self.x += 5
            self.draw_reverse = False
            self.frame = (self.frame + 1) % 5
        else:
            self.frame = 0

    def draw_p1(self):
        # 애니메이션 그리기
        if self.jump != 0:
            self.img_j.clip_draw((self.frame // 2) * 64, 0, 64, 63, self.x, self.y + 110 + self.jump, 128, 126)
        elif self.slide > 0:
            self.img_s.clip_draw((self.frame // 4) * 64, 0, 64, 63, self.x + self.slide, self.y + 110, 128, 126)
        elif self.slide < 0:
            self.img_rs.clip_draw((self.frame // 2) * 64, 0, 64, 63, self.x + self.slide, self.y + 110, 128, 126)
        elif self.draw_reverse:
            self.img_rw.clip_draw(self.frame * 64, 0, 64, 63, self.x, self.y + 110, 128, 126)
        else:
            self.img_w.clip_draw(self.frame * 64, 0, 64, 63, self.x, self.y + 110, 128, 126)
        if self.net_stop > 0:
            self.img_net.clip_draw(0, 0, 100, 100, self.x + 20, self.y + 110 + self.jump, 120, 100)

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
        if self.net_stop > 0:
            self.img_net.clip_draw(0, 0, 100, 100, self.x + 20, self.y + 110 + self.jump, 120, 100)

            
class Ball:
    def __init__(self, x, y, resources, player1, player2):
        self.x = x
        self.y = y
        self.x_speed = 0
        self.y_speed = 20
        self.gravity = 0.1
        self.ball_img = resources
        self.player1 = player1
        self.player2 = player2
        self.start =  False
        self.ballSound = load_wav('my_project\\codes\\res\\ballSound.wav')
        self.ballSound.set_volume(20)
        self.CheckSound = False

    def update(self):
        collision_p1 = CheckCollision.Check_BallChar_Collision(self.player1.x, self.player1.y, self.x, self.y)
        collision_p2 = CheckCollision.Check_BallChar_Collision(self.player2.x, self.player2.y, self.x, self.y)
        collision_wall = CheckCollision.Check_BallWall_Collision(self.x, self.y)

        if not self.start:
            self.y -= 15  # 공 초기 상태: 떨어지는 애니메이션
            if self.y <= self.player1.y + 110:  # 캐릭터와 충돌하면 게임 시작
                self.start = True
        else :
        # 공의 기본 이동
            self.x += self.x_speed
            self.y += self.y_speed
            self.y_speed += self.gravity  # 중력 적용

        # 캐릭터와 충돌
        if collision_p1:
            self.x_speed = 20
            self.y_speed = 20
            if self.CheckSound == False:
                self.ballSound.play(1)
                self.CheckSound = True
            self.start = True

        elif collision_p2:
            self.x_speed = -20
            self.y_speed = 20
            if self.CheckSound == False:
                self.ballSound.play(1)
                self.CheckSound = True
            self.start = True
            
        # 벽과 충돌
        if collision_wall == 1:  # 왼쪽 벽
            self.x_speed = abs(self.x_speed)  # 오른쪽으로 반사
        elif collision_wall == 2:  # 오른쪽 벽
            self.x_speed = -abs(self.x_speed)  # 왼쪽으로 반사
        elif collision_wall == 5:  # 천장 충돌
            self.y_speed = -abs(self.y_speed)  # 아래로 반사
            self.CheckSound = False
        elif collision_wall == 6:
            self.x -= self.x_speed
            self.x_speed = -self.x_speed

    def draw_ball(self):
        self.ball_img.clip_draw(0, 0, 100, 100, self.x, self. y, 100, 100)

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
        self.BaseBGM = load_wav('my_project\\codes\\res\\BaseBGM.wav')

        # 플레이어 생성
        self.player1 = Player(200, 0, [
            load_image('my_project\\codes\\res\\p1_walking.png'),
            load_image('my_project\\codes\\res\\p1_reverse_walking.png'),
            load_image('my_project\\codes\\res\\p1_jump.png'),
            load_image('my_project\\codes\\res\\p1_slide.png'),
            load_image('my_project\\codes\\res\\p1_reverse_slide.png'),
            load_image('my_project\\codes\\res\\net.png')

        ])
        self.player2 = Player(800, 0, [
            load_image('my_project\\codes\\res\\p2_walking.png'),
            load_image('my_project\\codes\\res\\p2_reverse_walkin.png'),
            load_image('my_project\\codes\\res\\p2_jump.png'),
            load_image('my_project\\codes\\res\\p2_slide.png'),
            load_image('my_project\\codes\\res\\p2_reverse_slide.png'),
            load_image('my_project\\codes\\res\\net.png')

        ])

        self.score_p1 = Rule(0, [
            load_image('my_project\\codes\\res\\0.png'),
            load_image('my_project\\codes\\res\\1.png'),
            load_image('my_project\\codes\\res\\2.png'),
            load_image('my_project\\codes\\res\\3.png'),
            load_image('my_project\\codes\\res\\4.png'),
            load_image('my_project\\codes\\res\\5.png'),
            load_image('my_project\\codes\\res\\winner.png')
        ])

        self.score_p2 = Rule(0, [
            load_image('my_project\\codes\\res\\0.png'),
            load_image('my_project\\codes\\res\\1.png'),
            load_image('my_project\\codes\\res\\2.png'),
            load_image('my_project\\codes\\res\\3.png'),
            load_image('my_project\\codes\\res\\4.png'),
            load_image('my_project\\codes\\res\\5.png'),
            load_image('my_project\\codes\\res\\winner.png')
        ])

        # 공 생성
        self.ball = Ball(300, 600, load_image('my_project\\codes\\res\\ball.png'), self.player1, self.player2)

    def start_scene(self):
        start_scene = True
        self.BaseBGM.repeat_play()
        self.BaseBGM.set_volume(60)
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
            self.ingame_bg.draw(self.center_x, self.center_y)

        # 플레이어 업데이트 및 그리기
            self.player1.update()
            self.player2.update()
            self.ball.update()
            self.player1.draw_p1()
            self.player2.draw_p2()
            self.ball.draw_ball()
            
            collision_wall = CheckCollision.Check_BallWall_Collision(self.ball.x, self.ball.y)
            if collision_wall == 3:  # 바닥 충돌
                self.score_p2.score += 1
                self.ball.x = 300
                self.ball.y = 600
                self.ball.start = False
                self.player1.spike = True
                self.player2.spike = True
            elif collision_wall == 4:  # 바닥 충돌
                self.score_p1.score += 1
                self.ball.x = 800
                self.ball.y = 600
                self.ball.start = False
                self.player1.spike = True
                self.player2.spike = True

            if self.score_p1.score == 5 or self.score_p2.score == 5:
                self.ball.x = 550
                self.ball.y = 600
                self.ball.start = False
                self.ball.x_speed = 0
                self.ball.y_speed = 0

            
            self.score_p1.draw_score_p1()
            self.score_p2.draw_score_p2()
            
            update_canvas()
            for event in get_events():
                if event.type == SDL_QUIT:
                    ingame_scene = False
                elif event.type == SDL_KEYDOWN:
                    if event.key == SDLK_ESCAPE:
                        ingame_scene = False
                # 플레이어1 이벤트
                    elif event.key == SDLK_a and self.player1.net_stop == 0:
                        self.player1.key_state[SDLK_LEFT] = True
                    elif event.key == SDLK_d and self.player1.net_stop == 0:
                        self.player1.key_state[SDLK_RIGHT] = True
                    elif event.key == SDLK_w and self.player1.jump == 0:  # 점프 중복 방지
                        self.player1.jump = 25
                    elif event.key == SDLK_s and self.player1.slide == 0 and self.player1.net_stop == 0:  # 슬라이드 중복 방지
                        self.player1.slide = -20 if self.player1.draw_reverse else 20
                    elif event.key == SDLK_r and self.player1.spike == True:
                        self.ball.x_speed *= 2
                        self.ball.y_speed *= 2
                        self.player1.spike = False
                    elif event.key == SDLK_e and self.player1.skill == True:
                        self.player2.net_stop = 60
                        self.player1.skill = False

                # 플레이어2 이벤트
                    if event.key == SDLK_j and self.player2.net_stop == 0:
                        self.player2.key_state[SDLK_LEFT] = True
                    elif event.key == SDLK_l and self.player2.net_stop == 0:
                        self.player2.key_state[SDLK_RIGHT] = True
                    elif event.key == SDLK_i and self.player2.jump == 0:  # 점프 중복 방지
                        self.player2.jump = 25
                    elif event.key == SDLK_k and self.player2.slide == 0 and self.player2.net_stop == 0:  # 슬라이드 중복 방지
                        self.player2.slide = -20 if self.player2.draw_reverse else 20
                    elif event.key == SDLK_p and self.player2.spike == True:
                        self.ball.x_speed *= 2
                        self.ball.y_speed *= 2
                        self.player2.spike = False
                    elif event.key == SDLK_o and self.player2.skill == True:
                        self.player1.net_stop = 60
                        self.player2.skill = False

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

            if self.player1.spike == False:
                self.player1.spike_cooltime += 1
                if self.player1.spike_cooltime >= 150:
                    self.player1.spike = True
                    self.player1.spike_cooltime = 0

            if self.player1.skill == False:
                self.player1.skill_cooltime += 1
                if self.player1.skill_cooltime >= 200:
                    self.player1.skill = True
                    self.player1.skill_cooltime = 0

            if self.player1.net_stop > 0:
                self.player1.net_stop -= 1

            if self.player2.spike == False:
                self.player2.spike_cooltime += 1
                if self.player2.spike_cooltime >= 150:
                    self.player2.spike = True
                    self.player2.spike_cooltime = 0

            if self.player2.skill == False:
                self.player2.skill_cooltime += 1
                if self.player2.skill_cooltime >= 200:
                    self.player2.skill = True
                    self.player2.skill_cooltime = 0
            
            if self.player2.net_stop > 0:
                self.player2.net_stop -= 1
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

    def Check_BallChar_Collision(px, py, bx, by):
        if (px - 64 < bx + 50 and px + 64 > bx - 50 and py + 110 < by + 100 and py + 220 > by):
            return True
        else:
            return False

    def Check_BallWall_Collision(bx, by):
        if (bx - 50 <= 0):
            return 1
        elif (bx + 50 >= 1100):
            return 2
        elif (by <= 110 and bx < 550):
            return 3
        elif (by <= 110 and bx > 550):
            return 4
        elif (by >= 600):
            return 5
        elif by <= 335 and (bx + 50 >= 550) and bx - 50 <= 550: 
            return 6
        else:
            return 7

class Rule:
    def __init__(self, score, resources):
        self.score = 0        
        self.zero, self.one, self.two, self.three, self.four, self.five, self.winner = resources

    def draw_score_p1(self):
        if(self.score == 0):
            self.zero.clip_draw(0,0,100,100,150,600,100,100)
        elif(self.score == 1):
            self.one.clip_draw(0,0,100,100,150,600,100,100)
        elif(self.score == 2):
            self.two.clip_draw(0,0,100,100,150,600,100,100)       
        elif(self.score == 3):
            self.three.clip_draw(0,0,100,100,150,600,100,100)          
        elif(self.score == 4):
            self.four.clip_draw(0,0,100,100,150,600,100,100)        
        elif(self.score == 5):
            self.five.clip_draw(0,0,100,100,150,600,100,100)
            self.winner.clip_draw(0, 0, 300 , 100 , 250, 300, 300, 100)
    
    def draw_score_p2(self):
        if(self.score == 0):
            self.zero.clip_draw(0,0,100,100,950,600,100,100)
        elif(self.score == 1):
            self.one.clip_draw(0,0,100,100,950,600,100,100)
        elif(self.score == 2):
            self.two.clip_draw(0,0,100,100,950,600,100,100)       
        elif(self.score == 3):
            self.three.clip_draw(0,0,100,100,950,600,100,100)          
        elif(self.score == 4):
            self.four.clip_draw(0,0,100,100,950,600,100,100)        
        elif(self.score == 5):
            self.five.clip_draw(0,0,100,100,950,600,100,100)
            self.winner.clip_draw(0, 0, 300 , 100 , 850, 300, 300, 100)

        

if __name__ == '__main__':
    game = GameScene()
    game.run()
