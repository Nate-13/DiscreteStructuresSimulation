from turtle import Turtle
from random import randint

X_BOUND = 400
Y_BOUND = 400


class Food(Turtle):
    def __init__(self):
        super().__init__()
        self.penup()
        self.shape("circle")
        self.color("gold")
        self.turtlesize(1)
        self.goto(randint(-X_BOUND, X_BOUND), randint(-Y_BOUND, Y_BOUND))

    def eat(self):
        self.goto(2000,2000)

    def spawn(self):
        self.goto(randint(-X_BOUND, X_BOUND), randint(-Y_BOUND, Y_BOUND))
