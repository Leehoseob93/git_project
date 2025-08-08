import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtCore import Qt, QTimer

class Background:
    def __init__(self):
        self.bg = QPixmap("background.png")
        self.offset = 0

    def max_scroll(self,screen_width):
        return self.bg.width() - screen_width

    def scroll_left(self,speed,screen_width):
        self.offset = max(0,self.offset - speed)

    def scroll_right(self,speed,screen_width):
        max_scroll = self.bg.width() - screen_width
        self.offset = min(self.max_scroll(screen_width),self.offset + speed)

    def draw(self, painter, screen_width, screen_height):
        painter.drawPixmap(0,0, self.bg.copy(self.offset, 0, screen_width, screen_height))
    
    def height(self):
        return self.bg.height()
    
    def width(self):
        return self.bg.width()
    
class Character:
    def __init__(self, x, background:Background):
        self.char = QPixmap("character.png")
        self.x = x
        self.ground_y = background.height() - self.char.height()
        self.y = self.ground_y
        self.speed = 5
        
        self.is_jumping = False
        self.jump_power = 15
        self.jump_velocity = 0
        self.gravity = 1

    def move_left(self):
        self.x -= self.speed
    
    def move_right(self):
        self.x += self.speed

    def start_jump(self):
        if self.is_jumping == False:
            self.is_jumping = True
            self.jump_velocity = self.jump_power

    def update_jump(self):
        if self.is_jumping == True:
            self.y -= self.jump_velocity
            self.jump_velocity -= self.gravity

            if self.y >= self.ground_y:
                self.y = self.ground_y
                self.is_jumping = False


    def draw(self,painter):
        painter.drawPixmap(self.x, self.y, self.char)

    def width(self):
        return self.char.width()
    
    def height(self):
        return self.char.height()
    
class CharacterManager:
    def __init__(self, character:Character):
        self.character = character
        self.move_left = False
        self.move_right = False

    def key_press(self,key):
        if key == Qt.Key_Left:
            self.move_left = True
        elif key == Qt.Key_Right:
            self.move_right = True

    def key_release(self,key):
        if key == Qt.Key_Left:
            self.move_left = False
        if key == Qt.Key_Right:
            self.move_right = False

class GameWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('2D 횡스크롤 게임')
        self.setFixedSize(800,480)

        self.background = Background()
        self.character = Character(100, self.background)
        self.controller = CharacterManager(self.character)

        self.timer = QTimer()
        self.timer.timeout.connect(self.game_loop)
        self.timer.start(16)

    def keyPressEvent(self, event):
        self.controller.key_press(event.key())
        if event.key() == Qt.Key_Space:
            self.character.start_jump()

    def keyReleaseEvent(self, event):
        self.controller.key_release(event.key())

    def game_loop(self):
        speed = self.character.speed
        max_scroll = self.background.max_scroll(self.width())

        if self.controller.move_right:
            if self.character.x < self.width() // 2:
                self.character.move_right()
            elif self.background.offset < max_scroll:
                self.background.scroll_right(speed,self.width())
            else:
                if self.character.x < self.width() - self.character.width():
                    self.character.move_right()

        if self.controller.move_left:
            if self.character.x > self.width() // 2:
                self.character.move_left()
            elif self.background.offset > 0:
                self.background.scroll_left(speed,self.width())
            else:
                if self.character.x > 0:
                    self.character.move_left()

        self.character.update_jump()

        self.update()


    def paintEvent(self, event):
        painter = QPainter(self)
        self.background.draw(painter, self.width(), self.height())
        self.character.draw(painter)


def main():
    app = QApplication(sys.argv)
    game = GameWidget()
    game.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

