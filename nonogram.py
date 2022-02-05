"""
Code for Solving Nonograms by Derek Hofland
Written on 2021/10/16; Last updated on 2022/02/05

Nonograms are picture logic puzzles in which cells in a grid must be
colored or left blank according to numbers at the side of the grid to
reveal a hidden picture (definition from Wikipedia).
"""

#puzzle information
ROWS = [[5], [11], [8, 2], [11, 1], [13], #1-5
        [7, 6], [3, 2, 7], [3, 1, 2, 7], [3, 2, 7], [8, 8], #6-10
        [8, 8], [4, 3, 7], [2, 4, 6, 1], [2, 2, 1, 4, 2], [1, 2, 2, 1, 3], #11-15
        [4, 2, 7], [4, 3, 4], [8, 4], [6, 4], [4, 4]] #16-20
COLS = [[1], [1, 1], [3, 3], [4, 4], [5, 6], #1-5
        [7, 2, 4], [7, 1, 3], [4, 2, 1, 4], [4, 1, 4, 5], [5, 5, 4], #6-10
        [13], [8, 1], [5, 4, 1], [5, 8, 1], [14, 1], #11-15
        [13, 1], [1, 11, 5], [1, 10, 6], [2, 8, 7], [3, 6, 8]] #16-20
ROW_LENGTH = len(COLS)
COL_LENGTH = len(ROWS)

#grid fillers
UNKNOWN = '·'
EMPTY = 'X'
FILLED = 'O'

def main():
    #create grid filled with unknown markers
    grid = []
    for i in range(COL_LENGTH):
        grid.append([UNKNOWN] * ROW_LENGTH)
    #find all possible fill arrangements for each row
    rowPossibilities = []
    for i in range(COL_LENGTH):
        blanks = ROW_LENGTH - sum(ROWS[i])
        rowPossibilities.append(set(permuteRow(ROWS[i], blanks)))
    #find all possible fill arrangements for each column
    colPossibilities = []
    for i in range(ROW_LENGTH):
        blanks = COL_LENGTH - sum(COLS[i])
        colPossibilities.append(set(permuteRow(COLS[i], blanks)))
    #determine known values in the grid until the grid is complete
    while not puzzleCompleted(grid):
        findRowDefinites(grid, rowPossibilities)
        findColDefinites(grid, colPossibilities)
        printGrid(grid) #display the intermediate steps of the process
    #display the final picture
    printPicture(grid)

#determine all possible arrangments of a row or column using recursion
def permuteRow(fillList, blanks):
    #base case for rows with no fill
    if (len(fillList) == 0):
        return [EMPTY * blanks]
    returnList = []
    #base case for rows with one section left to fill
    if (len(fillList) == 1):
        for i in range(blanks + 1):
            returnList.append(EMPTY*i + FILLED*fillList[0] + EMPTY*(blanks - i))
        return returnList
    #recursive step for building possibilities
    for i in range(blanks - len(fillList) + 2):
        beginning = EMPTY*i + FILLED*fillList[0] + EMPTY
        endOptions = permuteRow(fillList[1:], blanks - i - 1)
        for ending in endOptions:
            returnList.append(beginning + ending)
    return returnList

#check to see if the puzzle is finished
def puzzleCompleted(grid):
    for i in range(COL_LENGTH):
        for j in range(ROW_LENGTH):
            if (grid[i][j] == UNKNOWN):
                return False
    return True

#description
def findRowDefinites(grid, rowPossibilities):
    for i in range(COL_LENGTH):
        #determine if any positions in the row have already been found
        alreadyFound = {}
        for j in range(ROW_LENGTH):
            if (grid[i][j] != UNKNOWN):
                alreadyFound[j] = grid[i][j]
        #find all row possibilities that contradict the already known information
        removable = set()
        for item in rowPossibilities[i]:
            for position in alreadyFound:
                if (alreadyFound[position] != item[position]):
                    removable.add(item)
                    break
        #remove all row possibilities that were just found to be removable
        for item in removable:
            rowPossibilities[i].remove(item)
        #determine which positions are identical in all remaining possibilities
        definites = {}
        for item in rowPossibilities[i]:
            for position in range(ROW_LENGTH):
                definites[position] = item[position]
            break
        for item in rowPossibilities[i]:
            poppable = set()
            for position in definites:
                if (definites[position] != item[position]):
                    poppable.add(position)
            for position in poppable:
                definites.pop(position)
            if (len(definites) == 0):
                break
        #update the grid to indicate positions that are definite
        for position in definites:
            grid[i][position] = definites[position]

#description
def findColDefinites(grid, colPossibilities):
    for j in range(ROW_LENGTH):
        #determine if any positions in the row have already been found
        alreadyFound = {}
        for i in range(COL_LENGTH):
            if (grid[i][j] != UNKNOWN):
                alreadyFound[i] = grid[i][j]
        #find all row possibilities that contradict the already known information
        removable = set()
        for item in colPossibilities[j]:
            for position in alreadyFound:
                if (alreadyFound[position] != item[position]):
                    removable.add(item)
                    break
        #remove all row possibilities that were just found to be removable
        for item in removable:
            colPossibilities[j].remove(item)
        #determine which positions are identical in all remaining possibilities
        definites = {}
        for item in colPossibilities[j]:
            for position in range(COL_LENGTH):
                definites[position] = item[position]
            break
        for item in colPossibilities[j]:
            poppable = set()
            for position in definites:
                if (definites[position] != item[position]):
                    poppable.add(position)
            for position in poppable:
                definites.pop(position)
            if (len(definites) == 0):
                break
        #update the grid to indicate positions that are definite
        for position in definites:
            grid[position][j] = definites[position]

#display the grid in its current state
def printGrid(grid):
    for i in range(COL_LENGTH):
        nextLine = ''
        for j in range(ROW_LENGTH):
            nextLine += (grid[i][j] + ' ')
        print(nextLine)
    print()

#display the completed grid as a picture
def printPicture(grid):
    for i in range(COL_LENGTH):
        nextLine = ''
        for j in range(ROW_LENGTH):
            if (grid[i][j] == EMPTY):
                nextLine += "⬜"
            else:
                nextLine += "⬛"
        print(nextLine)
    print()

if __name__ == "__main__":
    main()
