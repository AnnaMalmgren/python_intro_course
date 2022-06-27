"""
Module: main.py
Runs the Cannon Game application using the
graphical UI
"""
# Imports everything from both model and graphics
import gamemodel as model
import gamegraphics as graphic


# Here is a nice little method you get for free
# It fires a shot for the current player and animates it until it stops
def graphicFire(game, graphics, angle, vel):
    player = game.getCurrentPlayer()
    # create a shot and track until it hits ground or leaves window
    proj = player.fire(angle, vel)
    while proj.isMoving():
        proj.update(1 / 50)
        graphics.sync()  # This deals with all graphics-related issues
        graphic.update(50)  # Waits short amount of time before next iteration
    return proj


def graphicPlay():
    """
    Runs the graphic version of Cannon Game
    """
    FIRE = 'Fire!'
    game = model.Game(10, 3)
    graphics = graphic.GameGraphics(game)

    while True:
        dialog = graphic.InputDialog(*game.getCurrentPlayer().getAim(),
                                     game.getCurrentWind())
        wantsToPlay = dialog.interact() == FIRE
        dialog.close()

        if not wantsToPlay:
            break

        playTurn(game, graphics, *dialog.getValues())


def playTurn(game, grx, angle, vel):
    """
    Fires a projectile, calculates a result, if it is a
    hit starts a new round and then syncs the graphics.
    """
    HIT = 0.0
    proj = graphicFire(game, grx, angle, vel)
    result = game.getOtherPlayer().projectileDistance(proj)

    if result == HIT:
        game.getCurrentPlayer().increaseScore()
        game.newRound()

    game.nextPlayer()
    grx.sync()


# Run the game with graphical interface
if __name__ == '__main__':
    graphicPlay()
