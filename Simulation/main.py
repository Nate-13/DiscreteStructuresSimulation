import turtle as trtl
from copy import copy
from random import randint, choice
from turtle import Turtle

from Food import Food
from GeneDisplay import GeneDisplay

'''

Program developed by Nathan Borwick - 11/30/23

How to run:

Run this main.py file and make sure the Food.py and
GeneDisplay.py file are in the same folder.
Import all modules if needed.

I have had problems in the past with the turtle module
working differently on mac vs. pc (I have a macbook)

If the program breaks or the screen size is wrong, I uploaded
a video of the program running on my project report

'''

NUM_CREATURES = 50
GENE_SIZE = 3
ENERGY_START = 1000
NUM_FOOD = 20

X_BOUND = 400
Y_BOUND = 400

wn = trtl.Screen()
wn.tracer(False)
wn.setup(width=1.0, height=1.0)
trtl.colormode(255)

allCreatures = []
allFood = []
geneDisplay = GeneDisplay()


# draw boundary
def drawField():
    drawer = trtl.Turtle()
    drawer.penup()
    drawer.fillcolor("light gray")
    drawer.goto(-X_BOUND, Y_BOUND)
    drawer.begin_fill()
    for i in range(4):
        drawer.forward(800)
        drawer.right(90)
    drawer.end_fill()
    drawer.hideturtle()
    drawer.goto(600, 450)
    drawer.write("Family Tree", align="center", font=("Ariel", 24, "bold"))
    drawer.goto(450, 400)
    drawer.pencolor("grey")
    drawer.pensize(2)
    labels = ["parent", "self", "children", "grandchildren"]
    for i in range(4):
        drawer.write(labels[i], font=("Ariel", 12, "normal"))
        drawer.pendown()
        drawer.seth(0)
        drawer.forward(300)
        drawer.penup()
        drawer.goto(drawer.xcor() - 300, drawer.ycor() - 40)


drawField()


def randWeight():
    return randint(-100, 100) / 100


class Creature(Turtle):
    def __init__(self, gene=None):
        super().__init__()
        self.shape("turtle")
        self.randColor = randint(0, 255), randint(0, 255), randint(0, 255)
        self.color(self.randColor)  # init random color
        self.penup()
        self.energy = ENERGY_START
        self.gene = gene if gene is not None else Gene(self).createRandom(GENE_SIZE, allSenses, allActions)
        self.onclick(lambda x, y: geneDisplay.put(x, y, self).draw(x, y, allCreatures))
        self.pencolor("black")
        self.goto(randint(-X_BOUND, X_BOUND), randint(-Y_BOUND, Y_BOUND))
        self.offspring = []
        self.parent = None
        self.children = []
        self.aliveTicks = 0

    def go(self):
        for sense in self.gene.senses:
            sense.do()
        self.checkBoundary()
        self.energy -= 1
        self.checkEnergy()
        for food in allFood:
            if self.distance(food) <= 10:
                food.eat()
                self.energy += 500
        self.aliveTicks += 1

    def checkEnergy(self):
        if self.energy <= 0:
            self.die()

    def die(self):
        self.hideturtle()
        allCreatures.remove(self)

    def checkBoundary(self):
        x, y = self.pos()
        if x > X_BOUND:
            self.goto(-X_BOUND, y)
        if x < -X_BOUND:
            self.goto(X_BOUND, y)
        if y > Y_BOUND:
            self.goto(x, -Y_BOUND)
        if y < -Y_BOUND:
            self.goto(x, Y_BOUND)

    def display(self, x, y):
        print("----------------------------------")
        for sense in self.gene.senses:
            print(f"{sense.func}   {sense.weight}   {sense.sensitivity}")
            print(f"{sense.pointsTo.func}   {sense.pointsTo.weight}")
        print("----------------------------------")


class Gene:
    def __init__(self, creature):
        self.senses = []
        self.creature = creature

    def setSenses(self, senses):
        self.senses = senses

    def createRandom(self, num, sensesList, actionsList):
        # nodes should be >= than 2
        self.senses = []
        for node in range(num):
            newAction = Action(randWeight(), choice(actionsList), self.creature)
            newSense = Sense(randWeight(), randWeight(), choice(sensesList), self.creature, newAction)
            self.senses.append(newSense)
        return self

    def setChildGene(self, child):
        for sense in self.senses:
            sense.creature = child
            sense.pointsTo.creature = child
        self.creature = child

    def getChildGene(self):
        new_gene = self.__class__(self.creature)
        new_gene.senses = copy(self.senses)
        return new_gene


# -------------------------- Action Functions --------------------------------------
# returns a value between -1 and 1
def actionForwards(creature, num, weight):
    creature.forward(10 * num)


def actionTurn(creature, num, weight):
    creature.right(10 * num)

# ----------------------------------------------------------------------------------

class Action():
    def __init__(self, weight, func, creature):
        # weight should be a value between -1 and 1
        # function performs the action
        self.weight = weight
        self.func = func
        self.creature = creature

    def do(self, num):
        self.func(self.creature, num, self.weight)

    def setRandomValues(self):
        self.weight = randint(-100, 100) / 100

    def package(self):
        return [self.weight, self.func]


# -------------------------- Sensing Functions --------------------------------------
# returns a value between -1 and 1

def senseRandom(creature, weight):
    return randint(-100, 100) / 100


def senseConstant(creature, weight):
    return weight

# ----------------------------------------------------------------------------------

class Sense:
    def __init__(self, weight, sensitivity, func, creature, pointsTo=None):
        # weight should be between -1 and 1
        # sensitivity should be between -1 and 1
        self.weight = weight
        self.sensitivity = sensitivity
        self.creature = creature
        self.func = func
        self.pointsTo = pointsTo

    def do(self):
        if randint(-100, 100) < self.sensitivity * 100:  # probability check
            num = self.func(self.creature, self.weight)

            if self.pointsTo is not None:
                self.pointsTo.do(num)

    def setRandomValues(self):
        self.weight = randint(-100, 100) / 100
        self.sensitivity = randint(-100, 100) / 100

    def package(self):
        return [self.weight, self.sensitivity, self.func, self.pointsTo.package()]


# List of all possible Sense functions:
allSenses = [
    senseRandom,
    senseConstant,
]

# list of all possible Action functions:
allActions = [
    actionForwards,
    actionTurn,
]

for i in range(NUM_CREATURES):
    allCreatures.append(Creature(None))

for i in range(NUM_FOOD):
    allFood.append(Food())


def replenishFood():
    trtl.ontimer(replenishFood, 500 * 50)
    for food in allFood:
        food.spawn()


isPaused = False


def run_loop():
    if not isPaused: trtl.ontimer(run_loop, 25)
    geneDisplay.draw(0, 0, allCreatures)
    for creature in allCreatures:
        creature.go()
        if creature.aliveTicks == 1250 or creature.aliveTicks == 2250:
            child = Creature(None)
            child.randColor = creature.randColor
            child.color(child.randColor)
            child.pencolor("black")
            childSenses = child.gene.senses
            for s in range(len(childSenses)):
                parentSense = creature.gene.senses[s]
                childSenses[s].weight = parentSense.weight
                childSenses[s].sensitivity = parentSense.sensitivity
                childSenses[s].func = parentSense.func
                childSenses[s].pointsTo.weight = parentSense.pointsTo.weight
                childSenses[s].pointsTo.func = parentSense.pointsTo.func
            child.parent = creature
            creature.children.append(child)
            allCreatures.append(child)

    wn.update()


pauseButton = trtl.Turtle()
pauseButton.penup()
pauseButton.goto(0, -430)
pauseButton.turtlesize(2)
pauseButton.shape("square")
pauseButton.color("gray")
pauseButton.pencolor("black")


def pauseUnpause(x, y):
    global isPaused
    if not isPaused:
        isPaused = True
        run_loop()
        pauseButton.shape("triangle")
    else:
        pauseButton.shape("square")
        isPaused = False
        run_loop()
    wn.update()


pauseButton.onclick(pauseUnpause)

stepButton = trtl.Turtle()
stepButton.penup()
stepButton.goto(50, -430)
stepButton.shapesize(2)
stepButton.onclick(lambda x, y: run_loop() if isPaused else None)

def onScreenClick(x, y):
    if x < -X_BOUND or x > X_BOUND or y < -Y_BOUND or y > Y_BOUND: return
    nearest = allCreatures[0]
    for creature in allCreatures:
        if creature.distance((x, y)) < nearest.distance((x, y)):
            nearest = creature
    geneDisplay.put(x, y, nearest)


trtl.onscreenclick(onScreenClick)

run_loop()
replenishFood()

wn.mainloop()
