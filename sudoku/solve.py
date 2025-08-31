from grid import makeMatrix as makeGrid
from grid import makeCustomMatrix as makeCustomGrid
from grid import printMatrix as printGrid

grid = makeCustomGrid(1)

def isValid(grid, row, col, n):
    if n in grid[row]:
        return False

    if n in [grid[i][col] for i in range(9)]:
        return False

    col0 = (col // 3) * 3
    row0 = (row // 3) * 3
    for i in range(row0, row0 + 3):
        for j in range(col0, col0 + 3):
            if grid[i][j] == n:
                return False

    return True

def fillGrid():
    global grid

    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                for n in range(1,10):
                    if isValid(grid, row, col, n):
                        grid[row][col] = n
                        if fillGrid():
                            return True
                        grid[row][col] = 0
                return False
    printGrid(grid)
    return True

def main():
    if not fillGrid():
        print("No solution found")

if __name__ == "__main__":
    main()
