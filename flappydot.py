import tkinter as tk
import random as rn

from gamelib import Sprite, GameApp, Text

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 500

UPDATE_DELAY = 33
GRAVITY = 2.5
STARTING_VELOCITY = -30
JUMP_VELOCITY = -20
PILLAR_SPEED = 10


class PillarPair(Sprite):
    def init_element(self):
        self.y = self.random_height()
        self.vx = PILLAR_SPEED
        self.start_x = self.x

        self.in_frame = True
        self.update()


    def update(self):
        self.x -= self.vx
        if self.x < 0:
            self.stop()

    def is_out_of_screen(self):
        if self.x > CANVAS_WIDTH:
            self.stop()

    def reset_position(self):
        self.x = self.start_x + 60
        self.y = self.random_height()
        self.stop()

    def start(self):
        self.in_frame = True

    def stop(self):
        self.in_frame = False

    def random_height(self):
        return rn.randint(30,470)


class Dot(Sprite):
    def init_element(self):
        self.vy = STARTING_VELOCITY
        self.is_started = False
        self.jump()

    def update(self):
        if self.is_started and self.gameover == False :
            self.y += self.vy
            self.vy += GRAVITY

    def start(self):
        self.is_started = True

    def jump(self):
        if self.gameover == False:
            self.vu = JUMP_VELOCITY
            self.vy =self.vu

    def is_out_of_screen(self):
        if self.y >490:
            self.gameover = True
        if self.y < 0:
            self.gameover = True

    def is_collision(self,pillar):
        x = pillar.x
        y1 = pillar.y - 100
        y2 = pillar.y + 100
        size = 40
        x1, x2 = (x) - size , (x) + size
        # y1, y2 = (y) - size / 2, (y) + size / 2
        tx = self.x
        ty = self.y
        return x1 <= tx <= x2 and ( 0 <= ty <= y1 or y2 <=ty <= 500)


class FlappyGame(GameApp):
    def create_sprites(self):
        self.dot = Dot(self, 'images/dot.png', CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2)
        self.pillar_pair = PillarPair(self, 'images/pillar-pair.png', CANVAS_WIDTH, CANVAS_HEIGHT // 2)

        self.elements.append(self.pillar_pair)
        self.elements.append(self.dot)

    def init_game(self):
        self.create_sprites()
        self.is_started = False

    def pre_update(self):
        pass

    def post_update(self):
        if not self.pillar_pair.in_frame:
            self.pillar_pair.reset_position()
            self.pillar_pair.start()
        self.dot.is_out_of_screen()
        if self.dot.is_collision(self.pillar_pair) :
            self.dot.gameover = True



    def on_key_pressed(self, event):
        self.dot.is_started = True
        self.dot.jump()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Flappy Game")
 
    # do not allow window resizing
    root.resizable(False, False)
    app = FlappyGame(root, CANVAS_WIDTH, CANVAS_HEIGHT, UPDATE_DELAY)
    app.start()
    root.mainloop()
