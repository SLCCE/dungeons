# loading into the player's state:
from characters import Character, Player, BadGuy, Paint, Gate, Egg
from board import Board
from pathlib import Path

import turtle

TILE_SIZE = 75

def initalizePlayer(boardWidth, boardHeight):
    t = turtle.Turtle()

    project_root = Path(__file__).resolve().parent
    invPath = (project_root / "maps/map1/inventory1.txt").resolve()
    eqPath = (project_root / "maps/map1/equipment1.txt").resolve()
    playerPath = (project_root / "maps/map1/good.txt").resolve()

    inputInventory = []
    with open(invPath, "r") as fin:
        for line in fin.readlines():
            name, offense = line.split()
            inputInventory.append((name, offense))

    inputEquipment = []
    with open(eqPath, "r") as fin:
        for line in fin.readlines():
            name, defense, armorType = line.split()
            inputEquipment.append((name, defense, armorType))

    with open(playerPath, "r") as fin:
        for line in fin.readlines():
            curHealth, maxHealth, startY, startX = map(int, line.split())
    p = Player(curHealth, maxHealth, startY, startX, inputInventory, inputEquipment, t, (boardWidth, boardHeight), TILE_SIZE)
    print(p.inventory, p.equipment)
    return p

def initializeEntities(levelNumber, boardWidth, boardHeight, board: Board.Board):
    project_root = Path(__file__).resolve().parent
    pathString = "maps/map" + str(levelNumber) + "/entity" + str(levelNumber) + ".txt"

    entityPath = (project_root / pathString).resolve()
    with open(entityPath, "r") as fin:
        for line in fin.readlines():
            lineContent = line.split()
            entity = lineContent[0]
            t = turtle.Turtle()
            if entity == 'bad':
                if len(lineContent) == 5:
                    curHp, maxHp, x, y = lineContent[1], lineContent[2], lineContent[3], lineContent[4]
                    x, y = int(x), int(y)
                    badGuy = BadGuy(int(curHp), int(maxHp), int(x), int(y), [], [], t, (boardWidth, boardHeight), TILE_SIZE)
                else:
                    curHp, maxHp, x, y, size = lineContent[1], lineContent[2], lineContent[3], lineContent[4], lineContent[5]
                    x, y, size = int(x), int(y), int(size)
                    badGuy = BadGuy(int(curHp), int(maxHp), int(x), int(y), [], [], t, (boardWidth, boardHeight), TILE_SIZE, size)
                board.get_tile(x, y).setEntity(badGuy)
            # entityList.append((entity, int(curHp), int(maxHp), int(x), int(y)))     
            elif entity == 'paint':
                color, x, y = lineContent[1], lineContent[2], lineContent[3]
                x, y = int(x), int(y)
                paintEntity = Paint.Paint(color, x, y, TILE_SIZE, t, (boardWidth, boardHeight))
                board.get_tile(x, y).setEntity(paintEntity)
            elif entity == 'gate':
                color, x, y = lineContent[1], lineContent[2], lineContent[3]
                x, y = int(x), int(y)
                gateEntity = Gate.Gate(color, x, y, TILE_SIZE, t, (boardWidth, boardHeight))
                board.get_tile(x, y).setEntity(gateEntity)
            elif entity == 'egg':
                x, y = lineContent[1], lineContent[2]
                x, y = int(x), int(y)
                eggEntity = Egg.Egg(x, y, TILE_SIZE, t, (boardWidth, boardHeight))
                board.get_tile(x, y).setEntity(eggEntity)

def loadPlayerPosition(levelNumber):
    project_root = Path(__file__).resolve().parent
    pathString = "maps/map" + str(levelNumber) + "/good.txt"

    entityPath = (project_root / pathString).resolve()
    with open(entityPath, "r") as fin:
        for line in fin.readlines():
            startX, startY = map(int, line.split())
            return startX, startY
