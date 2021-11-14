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

        def read_board(boardfile):
    '''
    This function is to read  file given in bff format
    This file consists of the board, number of blocks of type A, B, and C,
    lazors ( with their origin and direction), points of intersection
    *** Parameters ***
    boardfile - the name of the bff file
    *** Returns ***
    new_board - list of lists :board given in the bff file
    reflect_blocks - number of reflect blocks in the board
    opaque_blocks - number of absorb blocks in the board
    refract_blocks -  number of refract blocks in the board
    lazors - list of lists of all lazors consisting of orgins and direction
    '''
    split_line = [char for char in boardfile]
    if split_line[-4:] != [".", "b", "f", "f"]:
        raise Exception("File type is not .bff")
    board = []
    reflect_blocks = 0
    opaque_blocks = 0
    refract_blocks = 0
    lazor_origin = []
    points = []
    '''
    If no such file exists with this filename
    '''
    try:
        board_read = open(boardfile, "r").read()
    except UnboundLocalError:
        print("There is no such file")
    file_read = board_read.strip().split("\n")
    start_found = 0
    stop_found = 0
    for i in range(len(file_read)):
        if file_read[i] == "":
            continue
#        Raise an error if board has no START or STOP
        if file_read[i] == "GRID START":
            a = i + 1
            start_found = 1
            while file_read[a] != "GRID STOP":
                board.append(file_read[a])
                a = a + 1
                if file_read[a + 1] == "GRID STOP":
                    stop_found = 1
        if file_read[i][0] == "A" and (
                file_read[i][2] != "x") and file_read[i][2] != "o":
            reflect_temp = []
            if len(file_read[i]) > 3:
                for j in range(2, len(file_read[i])):
                    reflect_temp.append(file_read[i][j])
                num_str_reflect = "".join(reflect_temp)
                reflect_blocks = int(num_str_reflect)
#                print("A",reflect_blocks)
            else:
                reflect_blocks = int(file_read[i][2])
        if file_read[i][0] == "B" and (
                file_read[i][2]) != "x" and file_read[i][2] != "o":
            opaque_temp = []
            if len(file_read[i]) > 3:
                for j in range(2, len(file_read[i])):
                    opaque_temp.append(file_read[i][j])
                num_str_opaque = "".join(opaque_temp)
                opaque_blocks = int(num_str_opaque)
            else:
                opaque_blocks = int(file_read[i][2])
        if file_read[i][0] == "C" and (
                file_read[i][2]) != "x" and file_read[i][2] != "o":
            refract_temp = []
            if len(file_read[i]) > 3:
                for j in range(2, len(file_read[i])):
                    refract_temp.append(file_read[i][j])
                num_str_refract = "".join(refract_temp)
                refract_blocks = int(num_str_refract)
#                print("C",refract_blocks)
            else:
                refract_blocks = int(file_read[i][2])
        if len(file_read[i]) != 0 and file_read[i][0] == "L":
            strip_lazor = file_read[i].split(" ")
            '''
            Check for  wrong lazor input format
            '''
            if len(strip_lazor) != 5:
                raise Exception("Wrong number of lazor origin points")
            if strip_lazor[-2:] not in [["-1", "-1"], ["1", "1"], ["-1", "1"], ["1", "-1"]]:
                raise Exception("Your direction for a lazor is not right")

            for j in range(1, len(strip_lazor), 2):
                lazor_origin.append(
                    (int(strip_lazor[j]), int(strip_lazor[j + 1])))

        if len(file_read[i]) != 0 and file_read[i][0] == "P":
            points.append([int(file_read[i][2]), int(file_read[i][4])])
    new_board = []
    lazors = []

    for i in range(int(len(lazor_origin) / 2)):
        lazors.append([lazor_origin[2 * i], lazor_origin[2 * i + 1]])
    for x in board:
        lists = x.split()
        new_board.append(lists)
    '''
    Check if noo board present in the .bff file
    '''
    if len(new_board) == 0:
        raise Exception("There is no board in your file")
    ocount = 0
    for i in range(len(new_board)):
        for j in range(len(new_board[0])):
            if new_board[i][j] == 'o':
                ocount = ocount + 1

            '''
            If random characters other than the ones mentioned
            '''
            if new_board[i][j].lower() not in ['x', 'o', 'a', 'c', 'b']:
                raise Exception("Board has characters other than x and o")
    # If more blocks than movable spaces
    if (reflect_blocks + opaque_blocks + refract_blocks) > (ocount):
        raise Exception("There are more blocks than there are movable spaces")
    # If no blocks to place
    if reflect_blocks == 0 and opaque_blocks == 0 and refract_blocks == 0:
        raise Exception("Your file has no blocks in it to place")
    # If lazor or points of intersection out of bounds
    for i in range(len(lazors)):
        if lazors[i][0][0] > 2 * len(new_board[0]) or lazors[i][0][0] < 0:
            raise Exception("A lazor is out of the bounds of the boards")
    for i in range(len(lazors)):
        if lazors[i][0][1] > 2 * len(new_board) or lazors[i][0][0] < 0:
            raise Exception("A lazor is out of the bounds of the boards")
    for i in range(len(points)):
        if points[i][0] > 2 * len(new_board[0]) or points[i][0] < 0:
            raise Exception("A point is out of the bounds of the boards")
    for i in range(len(points)):
        if points[i][1] > 2 * len(new_board) or points[i][0] < 0:
            raise Exception("A point is out of the bounds of the boards")
    # If not enough lazors or points and check for that
    if len(lazors) < 1:
        raise Exception("No lasers found")
    if len(points) < 1:
        raise Exception("No point found")
    if start_found == 0:
        raise Exception("Start not found")
    if stop_found == 0:
        raise Exception("Stop not found")
    return(new_board, reflect_blocks, opaque_blocks, refract_blocks, lazors, points)

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
