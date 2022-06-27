# ------------------------------------------------------
# This module contains all graphics-classes for the cannon game.
# The two primary classes have these responsibilities:
#  * GameGraphics is responsible for the main window
#  * Each PlayerGraphics is responsible for the graphics of a
#    single player (score, cannon, projectile)
# In addition there are two UI-classes that have no
# counterparts in the model:
#  * Button
#  * InputDialog
# ------------------------------------------------------
from graphics import *

# Constants to get correct size and placement for UI components
from gamemodel import (X_LEFT, X_RIGHT, Y_LOWER, Y_UPPER, Y_GROUND, Y_LABLE,
                       WIN_SIZE)


class GameGraphics():
    """ This is the graphics for the game"""

    title = 'Cannon game'

    def __init__(self, game):
        self.gm = game

        # Create GraphWin instance
        self.win = GraphWin(self.title, *WIN_SIZE, autoflush=False)
        self.win.setCoords(X_LEFT, Y_LOWER, X_RIGHT, Y_UPPER)

        # Create two PlayerGraphics instances
        self.players = [PlayerGraphics(self, p) for p in self.gm.getPlayers()]

        # Create Line instance as Ground
        Line(Point(X_LEFT, Y_GROUND),
             Point(X_RIGHT, Y_GROUND)).draw(self.getWindow())

    """Syncronizes the graphics for all player instances in the game"""
    def sync(self):
        for player in self.players:
            player.sync()

    """Returns the GraphWin attribute"""
    def getWindow(self):
        return self.win

    # Added two getters to remove the need to send the whole Game instance to
    # PlayerGraphics (and avoid calling GameGraphic's game attribute directly)
    """Gets the size of the cannon"""
    def getCannonSize(self):
        return self.gm.getCannonSize()

    """Gets the size of the cannon ball"""
    def getBallSize(self):
        return self.gm.getBallSize()


class PlayerGraphics:
    """ This is the graphics for a Player"""

    ball = None
    scoreStr = 'Score: '

    def __init__(self, ggame, player):
        self.player = player
        self.win = ggame.getWindow()
        self.cannonSize = ggame.getCannonSize()
        self.ballSize = ggame.getBallSize()

        # Create player's score lable
        text = self.scoreStr + str(self.player.getScore())
        point = Point(self.player.getX(), Y_LABLE)
        self.lable = Text(point, text).draw(self.win)

        # Create player's cannon
        p1 = Point(self.player.getX() - (self.cannonSize / 2), Y_GROUND)
        p2 = Point(self.player.getX() + (self.cannonSize / 2), self.cannonSize)
        (Rectangle(p1, p2)
            .draw(self.win)
            .setFill(self.player.getColor()))

    """Updates the player's graphics by creating or moving the cannonball
    and updates the score lable"""
    def sync(self):

        proj = self.player.getProjectile()

        if proj:
            if not self.ball:
                center = Point(proj.getX(), proj.getY())
                self.ball = Circle(center, self.ballSize).draw(self.win)
                self.ball.setFill(self.player.getColor())
            else:
                xpos = proj.getX() - self.ball.getCenter().getX()
                ypos = proj.getY() - self.ball.getCenter().getY()
                self.ball.move(xpos, ypos)

            self.lable.setText(self.scoreStr + str(self.player.getScore()))


""" A somewhat specific input dialog class (adapted from the book) """


class InputDialog:
    """ Creates an input dialog with initial values for angle and velocity and
    displaying wind """

    def __init__(self, angle, vel, wind):
        self.win = win = GraphWin('Fire', 200, 300)
        win.setCoords(0, 4.5, 4, .5)
        Text(Point(1, 1), "Angle").draw(win)
        self.angle = Entry(Point(3, 1), 5).draw(win)
        self.angle.setText(str(angle))

        Text(Point(1, 2), "Velocity").draw(win)
        self.vel = Entry(Point(3, 2), 5).draw(win)
        self.vel.setText(str(vel))

        Text(Point(1, 3), "Wind").draw(win)
        self.height = Text(Point(3, 3), 5).draw(win)
        self.height.setText("{0:.2f}".format(wind))

        self.fire = Button(win, Point(1, 4), 1.25, .5, "Fire!")
        self.fire.activate()
        self.quit = Button(win, Point(3, 4), 1.25, .5, "Quit")
        self.quit.activate()

    """ Waits for the player to enter values and click a button """
    def interact(self):
        while True:
            pt = self.win.getMouse()
            if self.quit.clicked(pt):
                return "Quit"
            if self.fire.clicked(pt):
                return "Fire!"

    """ Gets the values entered into this window, typically called after
    interact """
    def getValues(self):
        a = float(self.angle.getText())
        v = float(self.vel.getText())
        return a, v

    """ Closes the input window """
    def close(self):
        self.win.close()


""" A general button class (from the book) """


class Button:

    """A button is a labeled rectangle in a window.
    It is activated or deactivated with the activate()
    and deactivate() methods. The clicked(p) method
    returns true if the button is active and p is inside it."""

    def __init__(self, win, center, width, height, label):
        """ Creates a rectangular button, eg:
        qb = Button(myWin, Point(30,25), 20, 10, 'Quit') """

        w, h = width / 2.0, height / 2.0
        x, y = center.getX(), center.getY()
        self.xmax, self.xmin = x + w, x - w
        self.ymax, self.ymin = y + h, y - h
        p1 = Point(self.xmin, self.ymin)
        p2 = Point(self.xmax, self.ymax)
        self.rect = Rectangle(p1, p2)
        self.rect.setFill('lightgray')
        self.rect.draw(win)
        self.label = Text(center, label)
        self.label.draw(win)
        self.deactivate()

    def clicked(self, p):
        "RETURNS true if button active and p is inside"
        return self.active and \
            self.xmin <= p.getX() <= self.xmax and \
            self.ymin <= p.getY() <= self.ymax

    def getLabel(self):
        "RETURNS the label string of this button."
        return self.label.getText()

    def activate(self):
        "Sets this button to 'active'."
        self.label.setFill('black')
        self.rect.setWidth(2)
        self.active = 1

    def deactivate(self):
        "Sets this button to 'inactive'."
        self.label.setFill('darkgrey')
        self.rect.setWidth(1)
        self.active = 0
