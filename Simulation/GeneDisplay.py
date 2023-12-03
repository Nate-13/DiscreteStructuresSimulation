from turtle import Turtle

X_SIDE = -725


def getCreatureColor(creature):
    return int(creature.color()[1][0]), int(creature.color()[1][1]), int(creature.color()[1][2])


def drawGene(t, sense):
    HEIGHT = 64
    t.pensize(1)
    t.penup()
    t.fillcolor("light sky blue")
    t.begin_fill()
    t.circle(HEIGHT / 2)
    t.end_fill()
    t.setheading(0)
    t.goto(t.xcor(), t.ycor() + 2 * HEIGHT / 2)
    t.write(sense.func.__name__.replace("sense", "") + f" ({sense.weight})<{sense.sensitivity}>", align="center", font=("Ariel", 12, "bold"))
    t.goto(t.xcor() + HEIGHT / 2, t.ycor() - HEIGHT / 2)
    t.pendown()
    t.forward(100)
    t.seth(135)
    t.forward(15)
    t.forward(-15)
    t.seth(225)
    t.forward(15)
    t.forward(-15)
    t.penup()
    t.goto(t.xcor(), t.ycor() + HEIGHT / 2)
    t.seth(0)
    t.fillcolor("salmon")
    t.begin_fill()
    for i in range(4):
        t.forward(HEIGHT)
        t.right(90)
    t.goto(t.xcor() + HEIGHT / 2, t.ycor())
    t.write(sense.pointsTo.func.__name__.replace("action", "") + f" ({sense.pointsTo.weight})", align="center",
            font=("Ariel", 12, "bold"))
    t.end_fill()


class GeneDisplay(Turtle):
    def __init__(self):
        super().__init__()
        self.penup()
        self.goto(X_SIDE, 400)
        self.currentCreature = None
        self.onclick(self.draw)
        self.hideturtle()

    def put(self, x, y, creature):
        if self.currentCreature is not None:
            self.currentCreature.pencolor("black")
        self.currentCreature = creature
        creature.pencolor("white")
        return self

    def draw(self, x, y, allCreatures):
        if self.currentCreature is None: return
        self.goto(X_SIDE, 300)
        self.clear()
        self.pencolor("black")
        currentGene = self.currentCreature.gene

        for sense in currentGene.senses:
            drawGene(self, sense)
            self.goto(X_SIDE, self.ycor() - 175)
            if sense.func.__name__ == "senseFood":
                x, y = self.pos()
                self.goto(self.currentCreature.xcor(), self.currentCreature.ycor() - abs(sense.weight) * 200)
                self.pendown()
                self.circle(abs(sense.weight) * 200)
                self.penup()
                self.goto(x, y)

            # circle highlighted creature
            if self.currentCreature.energy > 0:
                self.pencolor("green")
                x, y = self.pos()
                self.goto(self.currentCreature.xcor(), self.currentCreature.ycor() - 30)
                self.pendown()
                self.circle(30)
                self.penup()
                self.goto(x, y)
                self.pencolor("black")

        self.goto(-800, -300)
        self.write(
            f"Energy: {self.currentCreature.energy}  \nTotal Lifespan: {self.currentCreature.aliveTicks}",
            font=("Ariel", 18, "normal")
        )
        self.goto(-400, 400)
        self.write(f"Total Population: {len(allCreatures)}", font=("Ariel", 18, "normal"))

        # family tree
        def drawTree(creature, x, y, d):
            if d == 4: return

            self.goto(x, y)
            self.shape("turtle")
            self.color(getCreatureColor(creature))
            self.pencolor("black")
            if creature.energy == 0: self.pencolor("red")
            self.showturtle()
            self.stamp()
            xl, yl = x - 50/(d), y - 40
            xr, yr, = x + 50/(d), y - 40
            if len(creature.children) == 0: return
            if len(creature.children) == 1:
                drawTree(creature.children[0], xl, yl, d + 1)
            else:
                drawTree(creature.children[0], xl, yl, d + 1)
                drawTree(creature.children[1], xr, yr, d + 1)

        # draw parent
        if self.currentCreature.parent is not None:
            self.goto(650, 400)
            self.shape("turtle")
            self.color(getCreatureColor(self.currentCreature.parent))
            self.pencolor("black")
            if self.currentCreature.parent.energy == 0: self.pencolor("red")
            self.showturtle()
            self.stamp()
        drawTree(self.currentCreature, 650, 360, 1)

