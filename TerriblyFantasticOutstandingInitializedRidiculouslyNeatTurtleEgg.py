import turtle
import time
import random

from board import Board
import characters
import items
from Loader import initalizePlayer, initializeEntities, loadPlayerPosition
from enum import Enum
from board import Tile
from items.Equipment import WeaponType

# OTHER EXERCISES
# EXERCISE 2: map2/entity2.txt
# EXERCISE 5: map5/map5.txt

LEVEL = 1
# MAP_1_PATH = "maps/map1/map1.txt"
PLAYER_COLOR = 'green'
enemy = None
# Single turtle to draw any animations. Avoids the creation of many turtles
animationTurtle = turtle.Turtle()
animationTurtle.hideturtle()
turtle.mode("world")
globalX = 0
globalY = 0

class Status(Enum):
    ERROR = -1
    MOVE = 1
    COMBAT = 2
    DEAD = 3
    GOAL = 4

status = Status.ERROR


def state_checks():
    global status, enemy, LEVEL
    # check for goal
    # print(board.boardState[player.get_position()[0]][player.get_position()[1]].getStatus())
    if board.boardState[player.get_position()[0]][player.get_position()[1]].getStatus() == Tile.TileStatus.GOAL.value:
        status = Status.GOAL
        disableMovement()
        # print("going next level")
    if (status == Status.DEAD):
        disableMovement()
    elif (status == Status.COMBAT):
        return
    elif (status == Status.MOVE):
        enableMovement()
        screen.onkey(doNothing, 'space')
    elif (status == Status.GOAL):
        print("reached goal")
        if LEVEL < 5:
            LEVEL += 1            
            board.clear_entities()
            loadLevel(LEVEL)
            status = Status.MOVE
            enableMovement()
        else:
            disableMovement()
            # FUTURE TASK: REDIRECT TO "YOU WIN" SCREEN            
            if not any(isinstance(ent, characters.Egg.Egg) for ent in player.inventory):
                print("You win! But you missed a secret.")                
            else:
                # redirect to level 6: puzzle
                print("To level 6!")
                # return
                LEVEL += 1
                board.clear_entities()
                loadLevel(LEVEL)
                status = Status.MOVE
                enableMovement()

    curEntity = board.boardState[player.get_position()[0]][player.get_position()[1]].getEntity()
    print(player.get_position()[0], player.get_position()[1], curEntity)
    if curEntity:
        if isinstance(curEntity, characters.BadGuy):
            # Enter combat
            status = Status.COMBAT
            enemy = curEntity
            # Disable movement
            disableMovement()
            # Enable attack
            screen.onkey(attack, 'space')
            print("In Combat")
        elif isinstance(curEntity, characters.Paint.Paint):
            # print("WE ARE ON PAINT")
            player.color = curEntity.getColor()
        elif isinstance(curEntity, characters.Egg.Egg):
            print("WE ARE ON EGG")
            # add to inventory
            player.add_to_inventory(curEntity)
            # clear on frontend
            curEntity.clear()
            # clear on backend
            board.boardState[player.get_position()[0]][player.get_position()[1]].setEntity(None)
    
####################################
# COMBAT
####################################
def attack():
    global status
    if status == Status.DEAD:
        return
    # LEVEL 4 EXERCISE
    player.equipment[WeaponType.SWORD] = 1
    print('Attacking')
    playerAttackAnimation()
    enemy_new_hp = max(0, enemy.get_hp() - player.get_strength())
    enemy.set_hp(enemy_new_hp)
    if (enemy.get_hp() == 0):
        enemy.die()
        board.boardState[player.get_position()[0]][player.get_position()[1]].setEntity(None)
        print("Enemy Defeated")
        status = Status.MOVE
        state_checks()
        return
    if LEVEL == 3:
        # LEVEL 3 EXERCISE
        for i in range(100):
            player_new_hp = max(0, player.get_hp() - enemy.strength)
            player.set_hp(player_new_hp)
            print("You're being attacked!")
    else:
        player_new_hp = max(0, player.get_hp() - enemy.strength)
        player.set_hp(player_new_hp)

    if (player.get_hp() == 0):
        player.die()
        print("Player Died")
        status = Status.DEAD

def playerAttackAnimation():
    """
    Draws an hit markers around the player's current position then clears the hit markers after some time. 
    """
    print("Displaying attack animation")
    # Size of the hit mark, with direct relation to the tile_size
    markSize = player.tile_size * 0.15
    # Get position of the player tile position, then get the screen position of the bottom edge of the tile
    xPos = player.position[1] * player.tile_size - player.offset[0] + player.tile_size // 2
    yPos = player.position[0] * player.tile_size - player.offset[1]

    # Setup the turtle to begin drawing the hit marker
    animationTurtle.penup()
    # Make pensize a multiple of marksize so it scales well
    animationTurtle.pensize(markSize * 0.1)
    animationTurtle.pencolor('white')
    # Set fill color to be player color
    animationTurtle.fillcolor(player.color)
    animationTurtle.goto(xPos, yPos)
    animationTurtle.setheading(0)
    # Get a random starting position centered around the player's tile
    animationTurtle.circle(player.tile_size * 0.5, random.random() * 360)
    # Position turtle at 3 points to draw individual hit markers
    for i in range(3):
        animationTurtle.begin_fill()
        animationTurtle.pendown()
        # Draw individual hit marker
        for j in range(4):
            animationTurtle.circle(markSize * 0.75, 180)
            animationTurtle.left(90)
        animationTurtle.end_fill()
        animationTurtle.penup()
        animationTurtle.circle(player.tile_size * 0.5, 120)

    # Display the hit marker
    screen.update()
    # Wait then clear the hit marker
    time.sleep(0.25)
    animationTurtle.clear()
    # Display the cleared hit marker
    screen.update()
        



def checkGate(direction):
    destinationRow, destinationCol = -1, -1
    playerPos = player.get_position()
    if direction == 'up':
        destinationRow, destinationCol = playerPos[0] + 1, playerPos[1]
    elif direction == 'down':
        destinationRow, destinationCol = playerPos[0] - 1, playerPos[1]
    elif direction == 'left':
        destinationRow, destinationCol = playerPos[0], playerPos[1] - 1
    else:
        destinationRow, destinationCol = playerPos[0], playerPos[1] + 1
    ent = board.get_tile(destinationRow, destinationCol).getEntity()
    if isinstance(ent, characters.Gate.Gate):
        if ent.getColor() != player.color: 
            return True; 
    return False

####################################
# MOVEMENT
####################################
def move(direction):
    global globalX, globalY
    playerPos = player.get_position()
    # check if there's a gate
    if checkGate(direction):
        print("Need to be same color as gate to move through")
        return
    # check wall -- can move to function later ex. checkWall()
    if (direction == 'up'):
        # Level 1 exercise
        # goalPos = board.get_tile(playerPos[0] + 1, playerPos[1])
        if (goalPos.getStatus() != Board.Tile.TileStatus.WALL.value):
            player.move_up()
            globalY += board.square_size
            print(f'Moving {direction} to {player.get_position()}')
        else:
            print(f'Goal Position is of type: {goalPos.getStatus()}')
    elif (direction == 'down'):
        goalPos = board.get_tile(playerPos[0] - 1, playerPos[1])
        if (goalPos.getStatus() != Board.Tile.TileStatus.WALL.value):
            player.move_down()
            globalY -= board.square_size
            print(f'Moving {direction} to {player.get_position()}')
        else:
            print(f'Goal Position is of type: {goalPos.getStatus()}')
    elif (direction == 'right'):
        goalPos = board.get_tile(playerPos[0], playerPos[1] + 1)
        if (goalPos.getStatus() != Board.Tile.TileStatus.WALL.value):
            player.move_right()
            globalX += board.square_size
            print(f'Moving {direction} to {player.get_position()}')
        else:
            print(f'Goal Position is of type: {goalPos.getStatus()}')
    elif (direction == 'left'):
        goalPos = board.get_tile(playerPos[0], playerPos[1] - 1)
        if (goalPos.getStatus() != Board.Tile.TileStatus.WALL.value):
            player.move_left()
            globalX -= board.square_size
            print(f'Moving {direction} to {player.get_position()}')
        else:
            print(f'Goal Position is of type: {goalPos.getStatus()}')

    screen.setworldcoordinates(-300 + globalX, -300 + globalY, 300 + globalX, 300 + globalY)
    player._draw_self()
    state_checks()
    player._draw_self()
    screen.update()

def disableMovement():
    screen.onkey(doNothing, 'Up')
    screen.onkey(doNothing, 'Down')
    screen.onkey(doNothing, 'Right')
    screen.onkey(doNothing, 'Left')

def enableMovement():
    # screen.onkey(up, 'Up')
    # screen.onkey(down, 'Down')
    # screen.onkey(right, 'Right')
    # screen.onkey(left, 'Left')
    screen.onkey(lambda: move('up'), 'Up')
    screen.onkey(lambda: move('down'), 'Down')
    screen.onkey(lambda: move('right'), 'Right')
    screen.onkey(lambda: move('left'), 'Left')

def doNothing ():
    pass

####################################
# GAMEPLAY LOOP
####################################
screen = turtle.Screen()
screen.tracer(0)
# default: 600x600 centered at (0, 0)
# screen.setworldcoordinates(-300, -300, 300, 300)
# screen.setworldcoordinates(-280, -300, 320, 300)

# initialize to dummy values
board, player, loot = -1, -1, -1
def loadLevel(levelNumber):
    global board, player, loot, globalX, globalY
    # "maps/map1/map1.txt"
    mapPath = "maps/map" + str(levelNumber) + "/map" + str(levelNumber) + ".txt"
    print(mapPath)
    board = Board.Board(mapPath)

    loot = []
    initializeEntities(levelNumber, board.board_width // 2, board.board_height // 2, board)
    # deal with loot later
    # for entity in entities:
    #     if (isinstance(entity, characters.BadGuy)):
    #         badGuys.append(entity)
    #     elif (isinstance(entity, items)):
    #         loot.append(entity)
    # draw the board first, then load the player in
    board.draw_board()
    if levelNumber == 1:
        player = initalizePlayer(board.board_width // 2, board.board_height // 2)
    else:
        newX, newY = loadPlayerPosition(LEVEL)
        # print(newX, newY)
        player.set_position(newX, newY)
        player.set_offset((board.board_width // 2, board.board_height // 2))
        # reset screen offset
        print("PLAYER COORDS", player.t.xcor(), player.t.ycor())        
        globalX = player.position[1] * player.tile_size - player.offset[0] + player.tile_size // 2
        globalY = player.position[0] * player.tile_size - player.offset[1] + player.tile_size // 4
            
        print("PLAYER OFFSET", player.offset)
        # player.t.pendown() 
        # player.t.color("yellow")
        # player.t.fillcolor("yellow")
        # player.t.dot(50)
        # screen.update()
        # time.sleep(3)
        # player.t.penup()
        screen.setworldcoordinates(-300 + globalX, -300 + globalY, 300 + globalX, 300 + globalY)
        player._draw_self()
    screen.update()

turtle.setup(600, 600)
loadLevel(LEVEL)
# these may be needed?
screen.listen()
# screen.setworldcoordinates(-300, -300, 300, 300)

enableMovement()
screen.onkey(doNothing, 'space')

# time.sleep(3)
# screen.setworldcoordinates(-280, -300, 320, 300)
screen.mainloop()


