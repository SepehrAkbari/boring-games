import random
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

def fillGrid(grid):
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                numbers = list(range(1, 10))
                random.shuffle(numbers)
                for num in numbers:
                    if isValid(grid, row, col, num):
                        grid[row][col] = num
                        if fillGrid(grid):
                            return True
                        grid[row][col] = 0
                return False
    return True

def generate(grid, difficulty):
    num_to_remove = 81 - difficulty
    while num_to_remove > 0:
        row, col = random.randint(0, 8), random.randint(0, 8)
        if grid[row][col] != 0:
            grid[row][col] = 0
            num_to_remove -= 1

def main():
    global grid
    while True:
        if fillGrid(grid):
            difficulty = 50
            generate(grid, difficulty)
            printGrid(grid)
            break
        else:
            print("Failed to fill the grid")
            x = input("Whould you like to try again [y/n]? ")
            if (x == 'y' or x == 'yes'):
                pass
            else:
                break

if __name__ == "__main__":
    main()
