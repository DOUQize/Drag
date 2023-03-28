import arcade
from random import randint

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
TITLE = "DRAG"
TURNING_SPEED = 0.1
ROATATION_SPEED = 0.5
CAR_SPEED = 10
COMPLEXITY = 3  # от 1 до 10 (сложность)

if COMPLEXITY <= 0 or COMPLEXITY > 10:
    print("Выбрана слишком низкая или высокая сложность")
    exit()

class Game(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE, center_window=True)
        self.scene = None
        self.score = 0

    def setup(self):
        self.scene = arcade.Scene()
        self.road = Road()
        self.scene.add_sprite("Road", self.road)
        self.road1 = Road()
        self.road.center_y = SCREEN_HEIGHT + 400
        self.scene.add_sprite("Road1", self.road1)
        self.car_palyer = Car()
        self.scene.add_sprite("Car_player", self.car_palyer)
        self.carAI = CarAI(1)
        self.scene.add_sprite("CarAI", self.carAI)
        self.carAI1 = CarAI(2)
        self.carAI1.polosa = 2
        self.carAI1.center_y = 900
        self.scene.add_sprite("CarAI1", self.carAI1)
        self.carAI2 = CarAI(3)
        self.carAI2.center_y = 1300
        self.scene.add_sprite("CarAI2", self.carAI2)

    def on_draw(self):
        self.clear()
        self.scene.draw()
        arcade.draw_text(f"Health: {self.car_palyer.damage//10}", 3, SCREEN_HEIGHT - 20, [255, 255, 255], 14)
        arcade.draw_text(f"Score: {self.score//10}", 3, SCREEN_HEIGHT - 40, [255, 255, 255], 14)

    def update(self, delta_time: float):
        self.car_palyer.update()
        self.road.update()
        self.road1.update()
        self.carAI.update()
        self.carAI2.update()
        self.carAI1.update()
        if arcade.check_for_collision(self.carAI, self.carAI1):
            self.carAI.center_y = self.carAI.center_y + 100
        if arcade.check_for_collision(self.carAI, self.carAI2):
            self.carAI.center_y = self.carAI.center_y + 100
        if arcade.check_for_collision(self.carAI1, self.carAI2):
            self.carAI1.center_y = self.carAI1.center_y + 100
        if arcade.check_for_collision(self.car_palyer, self.carAI):
            dead()
        if arcade.check_for_collision(self.car_palyer, self.carAI1):
            dead()
        if arcade.check_for_collision(self.car_palyer, self.carAI2):
            dead()
        if self.car_palyer.damage <= 0:
            dead()
        if self.score >= COMPLEXITY * 1000:
            print("You win!")
            arcade.close_window()
        self.score += 1

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.A:
            self.car_palyer.rotation_a = True
        if symbol == arcade.key.D:
            self.car_palyer.rotation_d = True
        if symbol == arcade.key.W:
            if self.car_palyer.car_a_road:
                self.car_palyer.change_y = 2
        if symbol == arcade.key.S:
            if self.car_palyer.car_a_road:
                self.car_palyer.change_y = -2
            if not self.car_palyer.car_a_road:
                self.car_palyer.change_y = -3
            self.car_palyer.car_stop = True

    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == arcade.key.A:
            self.car_palyer.rotation_a = False
        if symbol == arcade.key.D:
            self.car_palyer.rotation_d = False
        if symbol == arcade.key.W:
            if self.car_palyer.car_a_road:
                self.car_palyer.change_y = 0
        if symbol == arcade.key.S:
            if self.car_palyer.car_a_road:
                self.car_palyer.change_y = 0
            self.car_palyer.car_stop = False


class Car(arcade.Sprite):
    def __init__(self):
        super().__init__("CarPlayer.png", 0.7)
        self.center_x = 300
        self.center_y = 300
        self.change_y = 0
        self.change_x = 0
        self.rotation_a = False
        self.rotation_d = False
        self.car_a_road = True
        self.car_stop = False
        self.damage = 1000

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y
        if self.angle < 15:
            if self.rotation_a:
                self.change_x -= TURNING_SPEED
                self.angle += ROATATION_SPEED
        if self.angle > -15:
            if self.rotation_d:
                self.change_x += TURNING_SPEED
                self.angle -= ROATATION_SPEED
        if self.center_x <= 200 or self.center_x >= 400:
            self.damage -= 1
            if not self.car_stop:
                self.change_y = -1
            self.car_a_road = False
        if 400 > self.center_x > 200:
            if not self.car_a_road:
                self.change_y = 0
            self.car_a_road = True
        if self.center_y <= 70:
            self.center_y = 70
        if self.center_y >= SCREEN_HEIGHT - 70:
            self.center_y = SCREEN_HEIGHT - 70
        if self.center_x <= 35:
            self.center_x = 35
        if self.center_x >= SCREEN_WIDTH - 35:
            self.center_x = SCREEN_WIDTH - 35


class CarAI(arcade.Sprite):
    def __init__(self, number):
        super().__init__(f"Car{number}.png", 0.7)
        self.center_x = 235
        self.center_y = 600
        self.polosa = 1

    def update(self):
        self.center_y -= COMPLEXITY
        if self.center_y <= -100:
            self.center_y = SCREEN_HEIGHT + randint(50, 1000)
            self.polosa = randint(1, 2)
        if self.polosa == 1:
            self.center_x = 235
        if self.polosa == 2:
            self.center_x = 365


class Road(arcade.Sprite):
    def __init__(self):
        super().__init__("Road.jpg", 1, angle=90)
        self.center_x = SCREEN_WIDTH / 2
        self.center_y = SCREEN_HEIGHT / 2
        self.change_y = -CAR_SPEED
        self.change_x = 0

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y
        if self.center_y <= -400:
            self.center_y = SCREEN_HEIGHT + 400


def dead():
    print("You lose!")
    arcade.close_window()

window = Game()
window.setup()
arcade.run()