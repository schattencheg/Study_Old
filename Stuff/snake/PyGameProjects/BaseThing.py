import math

class BaseThing:
    '''
    direction = 0 => right, 1 => top, 2 => left, 3 => bottom
    '''
    def __init__(self, x = 5, y = 5, direction = 0, speed = 1.0, allwprnt = True):
        self._x = x
        self._prevX = x
        self._y = y
        self._prevY = y
        self._direction = direction
        self._speed = 20.0 # frames per one shift
        self._allowTextOutput = allwprnt
        
        self._mult = math.pi / 2.0
        self._framesPerMove = 500.0
        
        self._currentFrame = 0.0
        self._angleToChange = 0
        self._score = 0.0
        self._lifetimeFrames = 0
        self._minimalSpeed = 20.0
        self._maximalSpeed = 500.0

        self.SetFieldSize(10, 10)

    def SetFieldSize(self, x, y):
        self._width = x
        self._height = y

    def Update(self, angle):
        self._lifetimeFrames += 1
        self._currentFrame += 1.0
        if angle != 0:
            self._angleToChange = angle
        if self._currentFrame >= self._framesPerMove / self._speed:
            self._currentFrame = 0.0
            self._direction = (self._direction + self._angleToChange) % 4
            self._angleToChange = 0.0
            self.Move()
    
    def SpeedUp(self, amount = 1):
        self._speed = min(self._maximalSpeed, self._speed + amount)

    def SlowDown(self, amount = 1):
        self._speed -= amount
        if (self._speed <= 0):
            self._speed = self._minimalSpeed

    def Move(self):
        xShift = math.cos(self._mult * self._direction)
        yShift = math.sin(self._mult * self._direction)
        self._x += xShift
        self._y -= yShift
        self.PrintPos()
        if self.CheckIfDead():
            self.print("GAME OVER!!")
            self.AnnounceResults()
            self.Destruct()

    def Eaten(self, score, name = "sweet"):
        self._score += score
        self._speed += abs(score)
        self.print("Eaten", name, score)

    def CheckIfDead(self):
        if "_width" in dir(self):
            if self._x > self._width or self._x < 0 or self._y > self._height or self._y < 0:
                return True
        return False

    def AnnounceResults(self):
        self.print("Total score:", self._score)
        self.print("Total frames alive", self._lifetimeFrames)

    def PrintPos(self):
        if self._prevX != self._x or self._prevY != self._y:
            self.print(self._x, self._y, "[", self._speed, "]")
            self._prevX = self._x
            self._prevY = self._y

    def print(self, *args):
        if self._allowTextOutput:
            print(args)
