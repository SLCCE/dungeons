import turtle

from board import Board
import characters
import items
from Loader import initalizePlayer, initializeEntities, loadPlayerPosition
from enum import Enum
from board import Tile

LEVEL = 1
# MAP_1_PATH = "maps/map1/map1.txt"
PLAYER_COLOR = 'green'
enemy = None

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
        for badGuy in badGuys:
            badGuy.die()
        disableMovement()
        # print("going next level")
    for badGuy in badGuys:
        print(badGuy.position[0], badGuy.position[1])
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
            loadLevel(LEVEL)
            status = Status.MOVE
            enableMovement()
        else:
            disableMovement()
            # FUTURE TASK: REDIRECT TO "YOU WIN" SCREEN
            print("You win!")

    for badGuy in badGuys:
        if badGuy.get_position() == player.get_position():
            # Enter combat
            status = Status.COMBAT
            enemy = badGuy
            # Disable movement
            disableMovement()
            # Enable attack
            screen.onkey(attack, 'space')
            print("In Combat")
    
    
####################################
# COMBAT
####################################
def attack():
    global status
    if status == Status.DEAD:
        return
    print('Attacking')
    enemy_new_hp = max(0, enemy.get_hp() - player.get_strength())
    enemy.set_hp(enemy_new_hp)
    if (enemy.get_hp() == 0):
        enemy.die()
        print("Enemy Defeated")
        status = Status.MOVE
        enemyIndex = badGuys.index(enemy)
        badGuys.pop(enemyIndex)
        state_checks()
        return
    player_new_hp = max(0, player.get_hp() - enemy.strength)
    player.set_hp(player_new_hp)
    if (player.get_hp() == 0):
        player.die()
        print("Player Died")
        status = Status.DEAD






####################################
# MOVEMENT
####################################
def move (direction):
    playerPos = player.get_position()
    if (direction == 'up'):
        goalPos = board.get_tile(playerPos[0] + 1, playerPos[1])
        if (goalPos.getStatus() != Board.Tile.TileStatus.WALL.value):
            # solution:
            # player.move_up()
            pass
            print(f'Moving {direction} to {player.get_position()}')
        else:
            print(f'Goal Position is of type: {goalPos.getStatus()}')
    elif (direction == 'down'):
        goalPos = board.get_tile(playerPos[0] - 1, playerPos[1])
        if (goalPos.getStatus() != Board.Tile.TileStatus.WALL.value):
            player.move_down()
            print(f'Moving {direction} to {player.get_position()}')
        else:
            print(f'Goal Position is of type: {goalPos.getStatus()}')
    elif (direction == 'right'):
        goalPos = board.get_tile(playerPos[0], playerPos[1] + 1)
        if (goalPos.getStatus() != Board.Tile.TileStatus.WALL.value):
            player.move_right()
            print(f'Moving {direction} to {player.get_position()}')
        else:
            print(f'Goal Position is of type: {goalPos.getStatus()}')
    elif (direction == 'left'):
        goalPos = board.get_tile(playerPos[0], playerPos[1] - 1)
        if (goalPos.getStatus() != Board.Tile.TileStatus.WALL.value):
            player.move_left()
            print(f'Moving {direction} to {player.get_position()}')
        else:
            print(f'Goal Position is of type: {goalPos.getStatus()}')
            
    player._draw_self(PLAYER_COLOR)
    state_checks()
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

# initialize to dummy values
board, player, badGuys, loot, entities = -1, -1, -1, -1, -1
def loadLevel(levelNumber):
    global board, player, badGuys, loot, entities
    # "maps/map1/map1.txt"
    mapPath = "maps/map" + str(levelNumber) + "/map" + str(levelNumber) + ".txt"
    print(mapPath)
    board = Board.Board(mapPath)

    badGuys = []
    loot = []
    entities = initializeEntities(levelNumber, board.board_width // 2, board.board_height // 2)
    print(entities)
    for entity in entities:
        if (isinstance(entity, characters.BadGuy)):
            badGuys.append(entity)
        elif (isinstance(entity, items)):
            loot.append(entity)
    # draw the board first, then load the player in
    board.draw_board()
    if levelNumber == 1:
        player = initalizePlayer(board.board_width // 2, board.board_height // 2)
    else:
        newX, newY = loadPlayerPosition(LEVEL)
        # print(newX, newY)
        player.set_position(newX, newY)
        player.set_offset((board.board_width // 2, board.board_height // 2))
        player._draw_self(PLAYER_COLOR)
    screen.update()

loadLevel(LEVEL)
# these may be needed?
screen.listen()

enableMovement()
screen.onkey(doNothing, 'space')



screen.mainloop()
