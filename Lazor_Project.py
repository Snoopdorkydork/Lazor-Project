# This is this initial commit to GitHub for the Lazor Project
# file location (mahin): OneDrive/Documents/GitHub/Lazor-Project

import time
import copy
from sympy.utilities.iterables import multiset_permutations


class Board():
    '''
    This Class creates objects which represent the board
    There are varyious boards with increasing difficulty
    and have different no. and types of blocks
    '''

    def __init__(
            self, board, reflect_blocks, opaque_blocks,
            refract_blocks, lazors, points, filename):
        '''
        Initialises the object of the Class Board
        *** Parameters ***
        self - variable that holds all the data regarding the class object
        board - n*m matrix consisting of some or all of o, x, A, B and C
        reflect_blocks - number of reflect blocks in the board
        opaque_blocks - number of absorb blocks in the board
        redract_blocks -  number of refract blocks in the board
        lazors - list of lists of all lazors consisting of orgins and direction
        eg. [[(1,3),(-1,-1)],[(2,4), (1,-1)]] - 2 lazors
        L1 - origin (1,3), direction (-1,-1)
        L2 - origin (2,4), direction (1, -1)
        points- list of hole points that the lazor has to intersect
        *** Returns ***
        Nothing!
        '''
        self.board = board
        self.reflect = reflect_blocks
        self.opaque = opaque_blocks
        self.refract = refract_blocks
        self.L = lazors
        self.P = points
        length = 2 * len(self.board) + 1
        width = 2 * len(self.board[0]) + 1
        grid = []
        for i in range(length):
            grid.append([])
            for j in range(width):
                grid[i].append('x')
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                grid[2 * i + 1][2 * j + 1] = self.board[i][j]
        self.grid = grid
        self.file = filename

    def Solver(self):
        '''

        '''
        # Maing a list of all open game pieces.
        game_pieces = []
        for i in self.board:
            for j in i:
                if j == 'o':
                    game_pieces.append(j)
        for i in range(self.reflect):
            game_pieces[i] = 'A'
        for i in range(self.reflect, (self.reflect + self.opaque)):
            game_pieces[i] = 'B'
        for i in range(
            (self.reflect + self.opaque),
                (self.reflect + self.opaque + self.refract)):
            game_pieces[i] = 'C'
        # Generating possible permutations of the board
        permutations = list(multiset_permutations(game_pieces))
        ITER = 0
        for permut in permutations:
            points = copy.deepcopy(self.P)
            actual_board = copy.deepcopy(self.grid)
            possible_sol = create_grid(actual_board, permut)
            ITER += 1
            Result, lazor_stack = lazor_path(possible_sol, self.L, points)
            if Result:
                print("Congratulations!! Board Solved")
                solution = []
                length = int((len(possible_sol) - 1) / 2)
                width = int((len(possible_sol[0]) - 1) / 2)
                for i in range(length):
                    solution.append([])
                    for j in range(width):
                        solution[i].append(
                            possible_sol[2 * i + 1][2 * j + 1])
                        print(possible_sol[2 * i + 1][2 * j + 1], end=' ')
                    print()
                print("This is the solution grid!")
                print("OR just check the text file or image so created!")
                GUI_board(self.board, solution,
                          filename, self.L, self.P, lazor_stack)
                fname1 = self.filename.split(".")[0]
                fname = fname1 + "_solution_textfile.txt"
                f = open(fname, "w+")
                f.write("The solution to your board is: \n")
                for i in range(length):
                    for j in range(width):
                        f.write(possible_sol[2 * i + 1][2 * j + 1])
                        f.write(" ")
                    f.write("\n")
                f.write("A is the reflect block, B is the absorb ")
                f.write("block and  C is the reflect block.\nThe o should ")
                f.write("be empty.\nTry not to cheat next time :)")
                f.close()
                break
        print("Iteration took to solve: ", ITER)


def create_grid(grid, permut):
    '''
        Creates a grid as explained in the top section for the given board
        for eg. if board is 2 x 2 matrix
        Board - o A
                B o
        Grid so generated - x x x x x
                            x o x A x
                            x x x x x
                            x B x o x
                            x x x x x
        *** Parameters ***
        self - consists of all data (board, A_blocks, B_blocks, C_blocks .. )
        *** Returns ***
        a (2n + 1) x (2m +1) matrix (grid) if board size is n x m
    '''
    value = 0
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 'o':
                grid[i][j] = permut[value]
                value += 1
    return grid


def boundary_check(grid, position, direc):
    '''
    This function just checks if the current lazor position and the next
    possible position is within the boundary of the grid or not
    If it is then we can continue with the lazor or else the lazor is dead
    as it crosses the boundary of the board/grid
    ** Parameters **
    grid - List of Lists : consisting of the board on which the lazor moves
    pos - Array : Current position of the lazor
    direc - Array : Current direction of the lazor
    ** Returns **
    True or False - depending upon if the point is in or out of the boundary
    '''
    x = position[0]
    y = position[1]
    y_max = len(grid) - 1
    x_max = len(grid[0]) - 1
    if x < 0 or x > x_max or y < 0 or y > y_max or (x + direc[0]) < 0 or (
        x + direc[0]) > x_max or (y + direc[1]) < 0 or (
            y + direc[1]) > y_max:
        return False
    else:
        return True


def next_step(grid, pos, direc):
    '''
    This function is to calculate the next step the lazor will take
    depending on the type of the block it intersects, and its position
    *** Parameters ***
    grid - List of lists : consisting of the board on which the lazor moves
    pos - array : current position of the lazor
    direc - array : current direction of the lazor
    *** Returns ***
    new_dir = new direction the lazor is taking depending on the type
    of the block it interacts with and its orginal direction
    (-1, -1)             (1, -1)
                 *
    (-1, 1)               (1, 1)
    * - is the current location of the lazor
    and the 4 coordinates are it are the 4 directions possible
    for the movement of lazor
    '''
    x = pos[0]
    y = pos[1]
    if y % 2 == 0:
        '''
        If y is even then block lies above or below
        '''
        if grid[y + direc[1]][x].lower() == 'o' or (
                grid[y + direc[1]][x].lower() == 'x'):
            new_dir = direc
        elif grid[y + direc[1]][x].lower() == 'a':
            new_dir = [direc[0], -1 * direc[1]]
        elif grid[y + direc[1]][x].lower() == 'b':
            new_dir = []
        elif grid[y + direc[1]][x].lower() == 'c':
            direc_1 = direc
            direc_2 = [direc[0], -1 * direc[1]]
            new_dir = [direc_1[0], direc_1[1], direc_2[0], direc_2[1]]
    else:
        '''
        If y is odd the block is left or right
        '''
        if grid[y][x + direc[0]].lower() == 'o' or (
                grid[y][x + direc[0]].lower() == 'x'):
            new_dir = direc
        elif grid[y][x + direc[0]].lower() == 'a':
            new_dir = [-1 * direc[0], direc[1]]
        elif grid[y][x + direc[0]].lower() == 'b':
            new_dir = []
        elif grid[y][x + direc[0]].lower() == 'c':
            direc_1 = direc
            direc_2 = [-1 * direc[0], direc[1]]
            new_dir = [direc_1[0], direc_1[1], direc_2[0], direc_2[1]]
    return new_dir


def lazor_path(grid, lazors, points):
    '''
    This function is the main lazor solver for the given/ generated
    board. The stack of lazors consists of the lazor path for all lazors
    available. It is appending after each step all the lazors take.
    If in their path they intersect the hole, that point is then removed
    from the hole list. As soon as the whole list is empty, the while loop
    breaks and it returns True i.e Solved; else the loop goes on till Maximum
    Iterations are reached.
    *** Parameters ***
    grid - List of lists: consisting of the board on which the lazor moves
    lazaors - Array: Consisting of origin and direction of each lazor
    points - Array : consists of all the hole/sink points
    ***Returns***
    lazor_stack - list of lists: having coordinates the lazor took to
    reach the hole
    '''

    # list of all lazors and and each lazor list has its path
    lazor_stack = []
    for i in range(len(lazors)):
        lazor_stack.append([lazors[i]])
    ITER = 0
    MAX_ITER = 100
    while len(points) != 0 and ITER <= MAX_ITER:
        ITER += 1
        for i in range(len(lazor_stack)):
            lazor_pos = list(lazor_stack[i][-1][0])
            direc = list(lazor_stack[i][-1][1])
            if boundary_check(grid, lazor_pos, direc):
                new_dir = next_step(grid, lazor_pos, direc)
                if len(new_dir) == 0:
                    lazor_stack[i].append([lazor_pos, direc])
                elif len(new_dir) == 2:
                    direc = new_dir
                    lazor_pos = [
                        lazor_pos[0] + direc[0],
                        lazor_pos[1] + direc[1]]
                    lazor_stack[i].append([lazor_pos, direc])
                else:
                    direc = new_dir
                    lazor_pos_1 = [
                        lazor_pos[0] + direc[0],
                        lazor_pos[1] + direc[1]]
                    lazor_pos_2 = [
                        lazor_pos[0] + direc[2],
                        lazor_pos[1] + direc[3]]
                    lazor_stack.append([[lazor_pos_1, [direc[0], direc[1]]]])
                    lazor_stack[i].append([lazor_pos_2, [direc[2], direc[3]]])
                    lazor_pos = lazor_pos_2
            if lazor_pos in points:
                points.remove(lazor_pos)
    if len(points) == 0:
        return (True, lazor_stack)
    else:
        return (False, lazor_stack)
