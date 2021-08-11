import random


def map_generator(height, width):
    def fak_generation(maze):
        next = []
        for i in range(height):
            for j in range(width):
                if (maze[i][j] == '.'):
                    next.append([i, j])

        for i in range(4):
            f = random.randint(0, len(next) - 1)
            i1 = next[f][0]
            i2 = next[f][1]
            maze[i1][i2] = 'H'
            next.remove([i1, i2])

        for i in range(4):
            f = random.randint(0, len(next) - 1)
            i1 = next[f][0]
            i2 = next[f][1]
            maze[i1][i2] = 'A'
            next.remove([i1, i2])

    def creatMaze(maze):
        maze[height // 2][width // 2] = 'F'
        for i in range(height):
            for j in range(width):
                if (i == 0 or j == 0 or i == height - 1 or j == width - 1):
                    maze[i][j] = '#'
        maze[1][width - 2] = maze[1][1] = maze[height - 2][1] = maze[height - 2][width - 2] = 'B'

    def printMaze(maze):
        for i in range(height):
            for j in range(width):
                print(maze[i][j], end=" ")
            print("\n")

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
        if maze[1][i] == '#':
            maze[0][i] = '.'
            break

    for i in range(width - 1, 0, -1):
        if (maze[height - 2][i] == '.'):
            maze[height - 1][i] = '.'
            break

    fak_generation(maze)
    creatMaze(maze)

    return maze
