import random
from colorama import init


def printMaze(maze):
    for i in range(0, height):
        for j in range(0, width):

            maze[height // 2][width // 2] = 'F'
            maze[0][width - 1] = maze[0][0] = maze[height - 1][0] = maze[height - 1][width - 1] = 'B'

            if (maze[i][j] == '2'):
                print(str(maze[i][j]), end="")
            elif (maze[i][j] == '#'):
                print(str(maze[i][j]), end="")
            else:
                print(str(maze[i][j]), end="")

        print('\n')
    maze[height // 2][width // 2] = 'F'
    maze[0][width - 1] = maze[0][0] = maze[height - 1][0] = maze[height - 1][width - 1] = ''


def surroundingCells(rand_wall):
    s_cells = 0
    if (maze[rand_wall[0] - 1][rand_wall[1]] == '.'):
        s_cells += 1
    if (maze[rand_wall[0] + 1][rand_wall[1]] == '.'):
        s_cells += 1
    if (maze[rand_wall[0]][rand_wall[1] - 1] == '.'):
        s_cells += 1
    if (maze[rand_wall[0]][rand_wall[1] + 1] == '.'):
        s_cells += 1

    return s_cells


wall = '#'
cell = '.'
unvisited = '2'
height = 100
width = 100
maze = []

init()

for i in range(0, height):
    line = []
    for j in range(0, width):
        line.append(unvisited)
    maze.append(line)

starting_height = int(random.random() * height)
starting_width = int(random.random() * width)
if (starting_height == 0):
    starting_height += 1
if (starting_height == height - 1):
    starting_height -= 1
if (starting_width == 0):
    starting_width += 1
if (starting_width == width - 1):
    starting_width -= 1

maze[starting_height][starting_width] = cell
walls = []
walls.append([starting_height - 1, starting_width])
walls.append([starting_height, starting_width - 1])
walls.append([starting_height, starting_width + 1])
walls.append([starting_height + 1, starting_width])

maze[starting_height - 1][starting_width] = '#'
maze[starting_height][starting_width - 1] = '#'
maze[starting_height][starting_width + 1] = '#'
maze[starting_height + 1][starting_width] = '#'

while (walls):

    rand_wall = walls[int(random.random() * len(walls)) - 1]

    if (rand_wall[1] != 0):
        if (maze[rand_wall[0]][rand_wall[1] - 1] == '2' and maze[rand_wall[0]][rand_wall[1] + 1] == '.'):

            s_cells = surroundingCells(rand_wall)

            if (s_cells < 2):
                maze[rand_wall[0]][rand_wall[1]] = '.'

                if (rand_wall[0] != 0):
                    if (maze[rand_wall[0] - 1][rand_wall[1]] != '.'):
                        maze[rand_wall[0] - 1][rand_wall[1]] = '#'
                    if ([rand_wall[0] - 1, rand_wall[1]] not in walls):
                        walls.append([rand_wall[0] - 1, rand_wall[1]])

                if (rand_wall[0] != height - 1):
                    if (maze[rand_wall[0] + 1][rand_wall[1]] != '.'):
                        maze[rand_wall[0] + 1][rand_wall[1]] = '#'
                    if ([rand_wall[0] + 1, rand_wall[1]] not in walls):
                        walls.append([rand_wall[0] + 1, rand_wall[1]])

                if (rand_wall[1] != 0):
                    if (maze[rand_wall[0]][rand_wall[1] - 1] != '.'):
                        maze[rand_wall[0]][rand_wall[1] - 1] = '#'
                    if ([rand_wall[0], rand_wall[1] - 1] not in walls):
                        walls.append([rand_wall[0], rand_wall[1] - 1])

            for wall in walls:
                if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
                    walls.remove(wall)

            continue

    if (rand_wall[0] != 0):
        if (maze[rand_wall[0] - 1][rand_wall[1]] == '2' and maze[rand_wall[0] + 1][rand_wall[1]] == '.'):

            s_cells = surroundingCells(rand_wall)
            if (s_cells < 2):
                maze[rand_wall[0]][rand_wall[1]] = '.'

                if (rand_wall[0] != 0):
                    if (maze[rand_wall[0] - 1][rand_wall[1]] != '.'):
                        maze[rand_wall[0] - 1][rand_wall[1]] = '#'
                    if ([rand_wall[0] - 1, rand_wall[1]] not in walls):
                        walls.append([rand_wall[0] - 1, rand_wall[1]])

                if (rand_wall[1] != 0):
                    if (maze[rand_wall[0]][rand_wall[1] - 1] != '.'):
                        maze[rand_wall[0]][rand_wall[1] - 1] = '#'
                    if ([rand_wall[0], rand_wall[1] - 1] not in walls):
                        walls.append([rand_wall[0], rand_wall[1] - 1])

                if (rand_wall[1] != width - 1):
                    if (maze[rand_wall[0]][rand_wall[1] + 1] != '.'):
                        maze[rand_wall[0]][rand_wall[1] + 1] = '#'
                    if ([rand_wall[0], rand_wall[1] + 1] not in walls):
                        walls.append([rand_wall[0], rand_wall[1] + 1])

            for wall in walls:
                if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
                    walls.remove(wall)

            continue

    if (rand_wall[0] != height - 1):
        if (maze[rand_wall[0] + 1][rand_wall[1]] == '2' and maze[rand_wall[0] - 1][rand_wall[1]] == '.'):

            s_cells = surroundingCells(rand_wall)
            if (s_cells < 2):
                maze[rand_wall[0]][rand_wall[1]] = '.'

                if (rand_wall[0] != height - 1):
                    if (maze[rand_wall[0] + 1][rand_wall[1]] != '.'):
                        maze[rand_wall[0] + 1][rand_wall[1]] = '#'
                    if ([rand_wall[0] + 1, rand_wall[1]] not in walls):
                        walls.append([rand_wall[0] + 1, rand_wall[1]])
                if (rand_wall[1] != 0):
                    if (maze[rand_wall[0]][rand_wall[1] - 1] != '.'):
                        maze[rand_wall[0]][rand_wall[1] - 1] = '#'
                    if ([rand_wall[0], rand_wall[1] - 1] not in walls):
                        walls.append([rand_wall[0], rand_wall[1] - 1])
                if (rand_wall[1] != width - 1):
                    if (maze[rand_wall[0]][rand_wall[1] + 1] != '.'):
                        maze[rand_wall[0]][rand_wall[1] + 1] = '#'
                    if ([rand_wall[0], rand_wall[1] + 1] not in walls):
                        walls.append([rand_wall[0], rand_wall[1] + 1])

            for wall in walls:
                if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
                    walls.remove(wall)

            continue

    if (rand_wall[1] != width - 1):
        if (maze[rand_wall[0]][rand_wall[1] + 1] == '2' and maze[rand_wall[0]][rand_wall[1] - 1] == '.'):

            s_cells = surroundingCells(rand_wall)
            if (s_cells < 2):
                maze[rand_wall[0]][rand_wall[1]] = '.'

                if (rand_wall[1] != width - 1):
                    if (maze[rand_wall[0]][rand_wall[1] + 1] != '.'):
                        maze[rand_wall[0]][rand_wall[1] + 1] = '#'
                    if ([rand_wall[0], rand_wall[1] + 1] not in walls):
                        walls.append([rand_wall[0], rand_wall[1] + 1])
                if (rand_wall[0] != height - 1):
                    if (maze[rand_wall[0] + 1][rand_wall[1]] != '.'):
                        maze[rand_wall[0] + 1][rand_wall[1]] = '#'
                    if ([rand_wall[0] + 1, rand_wall[1]] not in walls):
                        walls.append([rand_wall[0] + 1, rand_wall[1]])
                if (rand_wall[0] != 0):
                    if (maze[rand_wall[0] - 1][rand_wall[1]] != '.'):
                        maze[rand_wall[0] - 1][rand_wall[1]] = '#'
                    if ([rand_wall[0] - 1, rand_wall[1]] not in walls):
                        walls.append([rand_wall[0] - 1, rand_wall[1]])

            for wall in walls:
                if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
                    walls.remove(wall)

            continue

    for wall in walls:
        if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
            walls.remove(wall)

for i in range(0, height):
    for j in range(0, width):
        if (maze[i][j] == '2'):
            maze[i][j] = '#'

for i in range(0, width):
    if (maze[1][i] == '#'):
        maze[0][i] = '.'
        break

for i in range(width - 1, 0, -1):
    if (maze[height - 2][i] == '.'):
        maze[height - 1][i] = '.'
        break

printMaze(maze)