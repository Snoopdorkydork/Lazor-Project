# This is this initial commit to GitHub for the Lazor Project
# file location (mahin): OneDrive/Documents/GitHub/Lazor-Project

import time
import copy
from sympy.utilities.iterables import multiset_permutations


class Board():
    '''
    This class creates objects which represent
    the Lazor game board needed to be solved.
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
        eg. [[(4,3),(-1,-1)],[(2,5), (1,-1)]] - 2 lazors
        Lazor 1 - origin (4,3), direction (-1,-1)
        Lazor 2 - origin (2,5), direction (1, -1)
        points- list of hole points that the lazor has to intersect
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
        Based on the data read from the .bff file this function
        first creats all possible permutations of the blocks on
        the board then checks if the simulated board is the solution.
        When the solution is found it displays the solution on the console
        and stores the solution as a text file.
        *** Parameters ***
        self - all the data from the .bff file.
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
                print("Board is Solved!!!")
                solution = []
                length = int((len(possible_sol) - 1) / 2)
                width = int((len(possible_sol[0]) - 1) / 2)
                print("Solution grid: \n")
                for i in range(length):
                    solution.append([])
                    for j in range(width):
                        solution[i].append(
                            possible_sol[2 * i + 1][2 * j + 1])
                        print(possible_sol[2 * i + 1][2 * j + 1], end=' ')
                    print()
                GUI_board(self.board, solution,
                          self.filename, self.L, self.P, lazor_stack)
                sol_txt = self.filename.split(".")[0]
                sol_txt = sol_txt + "_solution.txt"
                sol = open(sol_txt, "w+")
                sol.write("The solution to your board is: \n")
                for i in range(length):
                    for j in range(width):
                        sol.write(possible_sol[2 * i + 1][2 * j + 1])
                        sol.write(" ")
                    sol.write("\n")
                sol.write("A represents the reflect block, ")
                sol.write("B represents the absorb block ")
                sol.write("and C represents the reflect block.\n")
                sol.write("The o should be empty.\n")
                sol.write("Try not to cheat next time :P")
                sol.close()
                print("The solution is also saved as a text file and image!")
                break
        print("Iterations taken to solve the board: ", ITER)


def create_grid(grid, permut):
    '''
    This function converts the permutaion of open game pieces
    into a list of lists which can represent board.
    eg,
    Board -   o A
              B o
    for the above permut would be = ['o','A', 'B', 'o']
    the grid generated by the function is shown below.
    Grid so generated - x x x x x
                        x o x A x
                        x x x x x
                        x B x o x
                        x x x x x
    *** Parameters ***
    grid - List of lists representing the board provided in the
           .bff file.
    permut - List of game pieces.
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
    grid - List of Lists representing the board
    pos - array : Current position of the lazor
    direc - array : Current direction of the lazor
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
    This function determines the next step the lazor will take
    depending on the type o fblock it intersects.
    *** Parameters ***
    grid - List of lists representing the board
    pos - array : Current position of the lazor
    direc - array : Current direction of the lazor
    *** Returns ***
    new_dir = new direction the lazor is taking depending on the type
    of the block it interacts with and its orginal direction
    (-1, -1)             (1, -1)
                 @
    (-1, 1)               (1, 1)
    @ - is the current location of the lazor
    and the 4 coordinates are it are the 4 directions possible
    for the movement of lazor
    '''
    x = pos[0]
    y = pos[1]
    if y % 2 == 0:
        '''
        Based on how we have represented the board as a grid,
        if y is even then block lies above or below
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
        Based on how we have represented the board as a grid,
        if y is odd the block is left or right
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
    This function creats a stack of the path followed by the lazor
    it also checks to see if all the sinks are intersected.
    *** Parameters ***
    grid - List of lists: consisting of the board on which the lazor moves
    lazaors - array : consisting of origin and direction of each lazor
    points - array : consists of all the hole/sink points
    ***Returns***
    lazor_stack - list of lists: The path followed by the lazor.
    True or False - depending on wether all the sinks are intersected or not.
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
