from random import *
import os

#Given a coordinate, returns the list of adjacent cells.
def getAdjCells(board, x, y):
    result = []
    for xc, yc in [(x+i,y+j) for i in (-1,0,1) for j in (-1,0,1) if (i != 0 or j != 0) and (i == 0 or j == 0)]:
        if xc in range(len(board)) and yc in range(len(board[xc])):
            result.append((xc,yc))
    return result

#Generates the start coordinates of a ship.
def genStart(board):
    while(True):
        pos = (randint(0, 9), randint(0, 9))
        if board[pos[0]][pos[1]] == "-":
            return(pos)

#Generates the end coordinates of a ship.  
def genEnd(board, start, length):

    #Randomly determine the orientation of the ship
    x = randint(0, 1); y = 1 if x == 0 else 0; plusMinus = 1 if random() < 0.5 else -1; end = start
    end = (start[0] + (length*plusMinus + 1 * (-plusMinus))*x, start[1] + (length*plusMinus + 1*(-plusMinus))*y)
     
    #Positioning would be out of bounds case check
    if end[0] < 0 or end[0] > 9 or end[1] < 0 or end[1] > 9:
        return (False, end)
    
    #Check if position conflicts with existing pieces or spawns adjacent to another ship
    toCover = []; temp = end
    for i in range(length):
        adjCells = getAdjCells(board, temp[0], temp[1])
        for cell in adjCells:
            if board[cell[0]][cell[1]] == "#":
                return(False, end)
        if board[temp[0]][temp[1]] == "#":
            return(False, end)
        else:
            toCover.append(temp)
        temp = (temp[0] - plusMinus * x, temp[1] - plusMinus * y)
    
    #Confirm placement of the ship
    for i in range(len(toCover)):
        board[toCover[i][0]][toCover[i][1]] = "#"
    return (True, end)
    
#Randomly generates ship placement (subs always together) 
def placeShips():
    
    #Setting up board
    board = [[],[],[],[],[],[],[],[],[],[]]
    for i in range(10):
        for j in range(10):
            board[i].append("-")
    
    #Storing Ship coordinates
    subs = []; des = []; cru = []; bat = []; car = []
    boats = [subs, des, cru, bat, car]
    
    #Special place subs beside each other to prevent advantage
    subs.append(genStart(board))
    board[subs[0][0]][subs[0][1]] = "#"
    adjCells = getAdjCells(board, subs[0][0], subs[0][1])
    for cell in adjCells:
        if board[cell[0]][cell[1]] == "-":
            subs.append(cell)
            board[subs[1][0]][subs[1][1]] = "#"
    
    #Placing Destroyers
    for i in range(2):
        while(True):
            start = genStart(board)
            (valid,end) = genEnd(board, start, 2)
            if valid:
                des.append(start)
                des.append(end)
                break
   
    #Placing Crusier, Battleship and Carrier
    validCrusier = False; validBattleship = False; validCarrier = False
    while(True):
        if not validCrusier:
            startCrusier = genStart(board)
            (validCrusier,endCrusier) = genEnd(board, startCrusier, 3)
        if not validBattleship:
            startBattleship = genStart(board)
            (validBattleship,endBattleship) = genEnd(board, startBattleship, 4)
        if not validCarrier:
            startCarrier = genStart(board)
            (validCarrier,endCarrier) = genEnd(board, startCarrier, 5)
        if validCrusier and validBattleship and validCarrier:
            cru.append(startCrusier); cru.append(endCrusier)
            bat.append(startBattleship); bat.append(endBattleship)
            car.append(startCarrier); car.append(endCarrier)
            break
            
    #Printing initial position setup
    print(boats[0][0][0], boats[0][0][1]);print(boats[0][1][0], boats[0][1][1]);print(boats[1][0][0], str(boats[1][0][1]) + ":" + str(boats[1][1][0]), boats[1][1][1]);print(boats[1][2][0], str(boats[1][2][1]) + ":" + str(boats[1][3][0]), boats[1][3][1]);print(boats[2][0][0], str(boats[2][0][1]) + ":" + str(boats[2][1][0]), boats[2][1][1]);print(boats[3][0][0], str(boats[3][0][1]) + ":" + str(boats[3][1][0]), boats[3][1][1]);print(boats[4][0][0], str(boats[4][0][1]) + ":" + str(boats[4][1][0]), boats[4][1][1])

#Possible combinations of a ship to exist on a given cell in the board for all cells
def probabilty(board, length):
    grid = [[0]*10 for i in range(10)]
    for i in range(len(board)):
        for j in range(len(board)):
            count = 0
            yr = length - 1; yl = 0
            xr = length - 1; xl = 0
            for k in range(length):
                impossibleX = False; impossibleY = False
                startY = i - yl; endY = i + yr
                startX = j - xl; endX = j + xr
                if startY >= 0 and endY <= 9:
                    for l in range(startY, endY+1):
                        if board[l][j] != "-":
                            impossibleY = True
                    if not impossibleY:    
                        count += 1
                if startX >= 0 and endX <= 9:
                    for m in range(startX, endX+1):
                        if board[i][m] != "-":
                            impossibleX = True
                    if not impossibleX:  
                        count += 1
                yl += 1; yr -= 1
                xl += 1; xr -= 1
            grid[i][j] = count
    #Finding greatest value
    maxValues = []
    currentMax = 0
    for i in range(len(grid)):
        for j in range(len(grid)):
            if grid[i][j] == currentMax:
                maxValues.append((i, j))
            if grid[i][j] > currentMax:
                maxValues = maxValues[0:0]
                currentMax = grid[i][j]
                maxValues.append((i, j))
    shuffle(maxValues)
    return((maxValues[0][0], maxValues[0][1]))

#Checks most likely spot for greatest ship still alive, if just subs, random attack
def hunt(board, shipsKilled):
    
    for i in reversed(range(len(shipsKilled))):
        #Carrier, Battleship and Crusier
        if shipsKilled[i] == 0 and (i != 0 or i != 1):
            highest = probabilty(board, i+1)
            print(highest[0], highest[1])
            return 
        #Destroyer
        if i == 1:
            if shipsKilled[i] < 2:
                highest = probabilty(board, i+1)
                print(highest[0], highest[1])
                return  
    #Subs only left
    while(True):
        attackCord = (randint(0, 9), randint(0, 9))
        if board[attackCord[0]][attackCord[1]] == "-":
            print(attackCord[0],attackCord[1])
            break
                
#Finish off injuried boat
def kill(board, indices):
    index = indices[0]
    #Proper finish if two or more hits
    if len(indices) > 1:
        for i in [0,len(indices) - 1]:
            fix = 1 if i == 0 else -1
            diffX = indices[i][0] - indices[i+(1*fix)][0]; diffY = indices[i][1] - indices[i+(1*fix)][1]
            newX = indices[i][0] + diffX; newY = indices[i][1] + diffY
            if newX >= 0 and newX <= 9 and newY >= 0 and newY <= 9:
                if board[newX][newY] == "-":
                    print(newX,newY)
                    return(True)
        #Ends not working, just pick adjacent to hits
        for i in range(len(indices)):
            adjCells = getAdjCells(board, indices[i][0], indices[i][1])
            for cell in adjCells:
                if board[cell[0]][cell[1]] == "-":
                    print(cell[0],cell[1])
                    return(True)    
    #Else, just pick a random adjacent cell
    else:
        adjCells = getAdjCells(board,index[0],index[1] )
        for cell in adjCells:
            if board[cell[0]][cell[1]] == "-":
                print(cell[0],cell[1])
                return(True)    
    return(False)

#Main
if __name__ == "__main__":
    board = []; killing = False; m = input()
    shipsKilled = [0,0,0,0,0]
    #Placing Ships
    if m == "INIT":
        placeShips()
        
    #Battling
    else:

        #Take new board input
        for i in range(10):
            board.append(list(input()))
        
        #Reading ships killed
        if os.path.exists('ships.out'):
            f = open('ships.out','r')
            shipsKilled = [0,0,0,0,0]
            for i in range(len(shipsKilled)):
                shipsKilled[i] = f.readline().rstrip()
            f.close()
            shipsKilled = list(map(int,shipsKilled))
            
        #Read old board, detect what ship killed
        if os.path.exists('board.out'):
            f = open('board.out','r')
            oldBoard = [[],[],[],[],[],[],[],[],[],[]]
            for i in range(10):
                for j in range(10):
                    cell = f.readline().rstrip()
                    oldBoard[i].append(cell)
            f.close()
            oldSum = 0; newSum = 0
            for i in range(10):
                oldD = oldBoard[i].count('d'); oldSum += oldD
                newD = board[i].count('d'); newSum += newD
            if newSum - oldSum > 0:
                shipsKilled[newSum - oldSum - 1] += 1

        #Determine if we should hunt for a ship or kill a damaged ship
        indices = [(i, j) for i, row in enumerate(board) for j, v in enumerate(row) if v=="h"]
        if len(indices) > 0:
            killing = kill(board, indices)
        if not killing:
            hunt(board, shipsKilled)
            
        #Save board state
        f = open('board.out', 'w')
        for i in range(len(board)):
            for j in range(len(board)):
                f.write(str(board[i][j]) + "\n")
        f.close()
        
        #Save ships killed
        f = open('ships.out', 'w')
        for i in range(len(shipsKilled)):
            f.write(str(shipsKilled[i]) + "\n")
        f.close()
