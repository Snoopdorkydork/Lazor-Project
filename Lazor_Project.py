'''
***** Lazor Project 2021 - Software Carpentry *****
Contributors - Mahin Gadkari , Rashi Sultania
Aim:- The code written should generate solution for placing the blocks
in a given board such that the  lazors after interacting with the blocks intersect all holes.
Method or Idea :- Lazors or holes are present on the middle point of the edges
of the blocks, thus we designed a grid for a given board, so each block in the
board is a middle point on the block in a grid (like a block surrounded by x's)
x x x
x o x
x x x - this is one block of the grid portraying one block of the board
So now it's easy to mathematically have a coordinate system for the grid with
  ----- > x
 |
 |
 |
 V
 y
 x,y- As the directions for the coordinate system.
 And just like solving a maze, here we increment each of the lazors one step
 at a time, and as it intersects the holes we remove that hole from the list
 For Placement of Blocks in the grid at the right ( or even wrong) position
 We first found all the permutations of o's , A's, B's, C's ( movable blocks)
 and then generated or created grids and checked each of them with the lazor
 solver that checks if in that case for that placement of blocks, if the lazors
 hit all the sinks/ holes or not. As soon as it comes across the right grid,
 the simulation stops and it prnts out the correct grid or
 the Solution for the lazor game.
 Lastly as an additional challenge we generated a GUI image for the solution
 with light grey blocks/ background as - non movable blocks (x)
 dark grey blocks as - empty positions (o's)
 white blocks as - reflect blocks (A's)
 black blocks as - opaque blocks (B's)
 grey blocks as - refract blocks (C's)
 orange points - Points of intersection
 green points - Lazer starting point
'''

import time
import copy
from sympy.utilities.iterables import multiset_permutations
from PIL import Image, ImageDraw


x = 0  # Positions not allowed to place the block
o = 1  # Positions open to place the block
A = 2  # Reflect Block
B = 3  # Absorb Block
C = 4  # Refract Block
# Colors for the Board and Solution Board Image
COLORS = {
    'x': (160, 160, 160),
    'A': (255, 255, 255),
    'B': (0, 0, 0),
    'C': (161, 161, 161),
    'o': (100, 100, 100),
    }

def set_color(img, x0, y0, dim, color):
    '''
    This function sets a colour for the pixels in that block
    of the board
    *** Parameters ***
    img : CLass Object - Image class object
    x0 : Integer - starting x coordinate
    y0 : Integer -starting y coordinate
    dim : Integer - dimension of the block
    color : String - Color to set the block to
    *** Returns ***
    An image with all the pixels assigned with specific colour.
    '''
    for x in range(dim):
        for y in range(dim):
            img.putpixel(
                (dim * x0 + x, dim * y0 + y), color)

def Image_sol(original_board, solution_board, boardname,
              lazors_origin, points, stack_lazors, blockSize=100):
    '''
    This function is to generate the given and solution board as an image
    Once you run this code the images are saved as
    "file_name_originalboard.png" and "file_name_solution.png"
    The idea of the code is extracted from the maze generation challenge
    given in the software carpentry class.
    *** Parameters ***
    original_board : List of Lists - That hold the board given in .bff file
    solution_board : List of Lists - Solution board so generated
    boardname: String - .bff filename
    lazors_origin : List of tuples - Consisting of all origins and directions
                                  of the lazors
    points : List - consisiting of the hole points
    stack_lazors - List of Lists - consisting of the lazor path
                                   for each lazor
    blocksize - Integer - Size of the block of the board
    *** Returns ***
    Nothing as it saves the boards as images
    '''
    name = boardname.split('.')
    file_name = name[0]
    w_blocks = len(solution_board[0])
    h_blocks = len(solution_board)
    SIZE = (w_blocks * blockSize, h_blocks * blockSize)
#    Creates a new image with all blocks filled with black.
    img = Image.new("RGB", SIZE, color=COLORS['x'])

    for y, row in enumerate(original_board):
        for x, block_ID in enumerate(row):
            set_color(img, x, y, blockSize, COLORS[block_ID])
#   Calls Imagedraw function from PIL to draw shapes on the image.

    draw = ImageDraw.Draw(img)
#   The below code is to generate the image for the original board.
    # For Horizontal Boundaries
    for x in range(100, SIZE[0] + 100, 100):
        x1 = x
        x2 = x
        y1 = 0
        y2 = SIZE[1]
        draw.line([x1, y1, x2, y2], fill=(255, 255, 255))
    # For Vertical Boundaries
    for y in range(100, SIZE[1] + 100, 100):
        y1 = y
        y2 = y
        x1 = 0
        x2 = SIZE[0]
        draw.line([x1, y1, x2, y2], fill=(255, 255, 255))
    # For points
    for i in points:
        x1 = i[0]
        y1 = i[1]
        a = x1 * 50
        b = y1 * 50
        draw.ellipse([a - 10, b - 10, a + 10, b + 10], fill=(255, 165, 0))
    # For Lazor Origin
    for j in lazors_origin:
        ori = j[0]
        x1 = ori[0]
        y1 = ori[1]
        a = x1 * 50
        b = y1 * 50
        draw.ellipse([a - 5, b - 5, a + 5, b + 5], fill=(0, 255, 0))
        draw.ellipse([a - 8, b - 8, a + 8, b + 8], outline=0, width=2)
    # Saving it as an original board
    img.save("%s_original_board.png" % (file_name))

#   The below code is for generating the solved grid image.

    for y, row in enumerate(solution_board):
        for x, block_ID in enumerate(row):
            set_color(img, x, y, blockSize, COLORS[block_ID])
    # For Horizontal Boundaries
    draw = ImageDraw.Draw(img)
    for x in range(100, SIZE[0] + 100, 100):
        x1 = x
        x2 = x
        y1 = 0
        y2 = SIZE[1]
        draw.line([x1, y1, x2, y2], fill=(255, 255, 255))
    # For Vertical Boundaries
    for y in range(100, SIZE[1] + 100, 100):
        y1 = y
        y2 = y
        x1 = 0
        x2 = SIZE[0]
        draw.line([x1, y1, x2, y2], fill=(255, 255, 255))
    # For Points
    for i in points:
        x1 = i[0]
        y1 = i[1]
        a = x1 * 50
        b = y1 * 50
        draw.ellipse([a - 10, b - 10, a + 10, b + 10], fill=(255, 165, 0))
    # For Lazor Origins
    for j in lazors_origin:
        ori = j[0]
        x1 = ori[0]
        y1 = ori[1]
        a = x1 * 50
        b = y1 * 50
        draw.ellipse([a - 5, b - 5, a + 5, b + 5], fill=(0, 255, 0))
        draw.ellipse([a - 8, b - 8, a + 8, b + 8], outline=0, width=2)
    # For Lazor Path
    final_points = []
    for i in range(len(stack_lazors)):
        final_points.append([])
        for j in range(len(stack_lazors[i])):
            if stack_lazors[i][j][0] != stack_lazors[i][j - 1][0]:
                stack_lazors[i][j][0] = [element * 50 for element in stack_lazors[i][j][0]]
                final_points[i].append(tuple(stack_lazors[i][j][0]))
    for i in final_points:
        draw.line(i, fill=(255, 0, 0), width=2)
    # Saving the solution boards
    img.save("%s_solution.png" % (file_name))

class Board():
    '''
    This class creates objects which represent
    the Lazor game board needed to be solved.
    '''

    def __init__(
            self, board, reflect_blocks, opaque_blocks,
            refract_blocks, lazors, points):
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

    def Solver(self, filename):
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
                print("\nThe board is Solved!!!\n")
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
                Image_sol(self.board, solution,
                          filename, self.L, self.P, lazor_stack)
                sol_txt = filename.split(".")[0]
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
                print("\nThe solution is also saved as a text file and image!")
                break
        print("\nIterations taken to solve the board: ", ITER)


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
            if strip_lazor[-2:] not in [
                ["-1", "-1"], ["1", "1"],
                    ["-1", "1"], ["1", "-1"]]:
                raise Exception("Your direction for a lazor is not right")

            for j in range(1, len(strip_lazor), 2):
                lazor_origin.append(
                    [int(strip_lazor[j]), int(strip_lazor[j + 1])])

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
    return(
        new_board, reflect_blocks, opaque_blocks,
        refract_blocks, lazors, points)


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


def unit_test():
    # Dark_1.bff
    lazors = [[(3, 0), (-1, 1)], [(1, 6), (1, -1)],
              [(3, 6), (-1, -1)], [(4, 3), (1, -1)]]
    hole = [[0, 3], [6, 1]]
    solved_grid = [['x', 'x', 'x', 'x', 'x', 'x', 'x'],
                   ['x', 'x', 'x', 'o', 'x', 'o', 'x'],
                   ['x', 'x', 'x', 'x', 'x', 'x', 'x'],
                   ['x', 'o', 'x', 'B', 'x', 'o', 'x'],
                   ['x', 'x', 'x', 'x', 'x', 'x', 'x'],
                   ['x', 'B', 'x', 'B', 'x', 'x', 'x'],
                   ['x', 'x', 'x', 'x', 'x', 'x', 'x']]
    assert lazor_path(solved_grid, lazors, hole)[0] == True
    # Mad_1.bff
    lazors = [[(2, 7), (1, -1)]]
    hole = [[3, 0], [4, 3], [2, 5], [4, 7]]
    solved_grid = [['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                   ['x', 'o', 'x', 'o', 'x', 'c', 'x', 'o', 'x'],
                   ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                   ['x', 'o', 'x', 'o', 'x', 'o', 'x', 'A', 'x'],
                   ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                   ['x', 'A', 'x', 'o', 'x', 'o', 'x', 'o', 'x'],
                   ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                   ['x', 'o', 'x', 'o', 'x', 'o', 'x', 'o', 'x'],
                   ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x']]
    assert lazor_path(solved_grid, lazors, hole)[0] == True
    # Mad_4.bff
    lazors = [[(7, 2), (-1, 1)]]
    hole = [[3, 4], [7, 4], [5, 8]]
    solved_grid = [['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                   ['x', 'o', 'x', 'o', 'x', 'o', 'x', 'o', 'x'],
                   ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                   ['x', 'o', 'x', 'A', 'x', 'o', 'x', 'o', 'x'],
                   ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                   ['x', 'A', 'x', 'o', 'x', 'o', 'x', 'o', 'x'],
                   ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                   ['x', 'o', 'x', 'A', 'x', 'o', 'x', 'A', 'x'],
                   ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                   ['x', 'o', 'x', 'o', 'x', 'A', 'x', 'o', 'x'],
                   ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x']]
    assert lazor_path(solved_grid, lazors, hole)[0] == True
    # Mad_7.bff
    lazors = [[(2, 1), (1, 1)], [(9, 4), (-1, 1)]]
    hole = [[6, 3], [6, 5], [6, 7], [2, 9], [9, 6]]
    solved_grid = [['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                   ['x', 'o', 'x', 'o', 'x', 'A', 'x', 'o', 'x', 'o', 'x'],
                   ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                   ['x', 'o', 'x', 'o', 'x', 'o', 'x', 'A', 'x', 'o', 'x'],
                   ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                   ['x', 'A', 'x', 'o', 'x', 'A', 'x', 'o', 'x', 'x', 'x'],
                   ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                   ['x', 'o', 'x', 'o', 'x', 'o', 'x', 'A', 'x', 'o', 'x'],
                   ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                   ['x', 'o', 'x', 'o', 'x', 'A', 'x', 'o', 'x', 'o', 'x'],
                   ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x']]
    assert lazor_path(solved_grid, lazors, hole)[0] == True
    # Numbered_6.bff
    lazors = [[(4, 9), (-1, -1)], [(6, 9), (-1, -1)]]
    hole = [[2, 5], [5, 0]]
    solved_grid = [['x', 'x', 'x', 'x', 'x', 'x', 'x'],
                   ['x', 'B', 'x', 'o', 'x', 'o', 'x'],
                   ['x', 'x', 'x', 'x', 'x', 'x', 'x'],
                   ['x', 'A', 'x', 'x', 'x', 'x', 'x'],
                   ['x', 'x', 'x', 'x', 'x', 'x', 'x'],
                   ['x', 'B', 'x', 'o', 'x', 'A', 'x'],
                   ['x', 'x', 'x', 'x', 'x', 'x', 'x'],
                   ['x', 'A', 'x', 'x', 'x', 'o', 'x'],
                   ['x', 'x', 'x', 'x', 'x', 'x', 'x'],
                   ['x', 'B', 'x', 'o', 'x', 'o', 'x']]
    assert lazor_path(solved_grid, lazors, hole)[0] == True
    # Showstopper_4.bff
    lazors = [[(3, 6), (-1, -1)]]
    hole = [[2, 3]]
    solved_grid = [['x', 'x', 'x', 'x', 'x', 'x', 'x'],
                   ['x', 'B', 'x', 'A', 'x', 'B', 'x'],
                   ['x', 'x', 'x', 'x', 'x', 'x', 'x'],
                   ['x', 'B', 'x', 'o', 'x', 'A', 'x'],
                   ['x', 'x', 'x', 'x', 'x', 'x', 'x'],
                   ['x', 'A', 'x', 'o', 'x', 'B', 'x'],
                   ['x', 'x', 'x', 'x', 'x', 'x', 'x']]
    assert lazor_path(solved_grid, lazors, hole)[0] == True
    # Tiny_5.bff
    lazors = [[(4, 5), (-1, -1)]]
    hole = [[1, 2], [6, 3]]
    solved_grid = [['x', 'x', 'x', 'x', 'x', 'x', 'x'],
                   ['x', 'A', 'x', 'B', 'x', 'A', 'x'],
                   ['x', 'x', 'x', 'x', 'x', 'x', 'x'],
                   ['x', 'o', 'x', 'o', 'x', 'o', 'x'],
                   ['x', 'x', 'x', 'x', 'x', 'x', 'x'],
                   ['x', 'A', 'x', 'C', 'x', 'o', 'x'],
                   ['x', 'x', 'x', 'x', 'x', 'x', 'x']]
    assert lazor_path(solved_grid, lazors, hole)[0] == True
    # Yarn_5.bff
    lazors = [[(4, 1), (1, 1)]]
    hole = [[6, 9], [9, 2]]
    solved_grid = [['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                   ['x', 'o', 'x', 'B', 'x', 'x', 'x', 'o', 'x', 'o', 'x'],
                   ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                   ['x', 'o', 'x', 'A', 'x', 'o', 'x', 'o', 'x', 'o', 'x'],
                   ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                   ['x', 'A', 'x', 'x', 'x', 'o', 'x', 'o', 'x', 'A', 'x'],
                   ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                   ['x', 'o', 'x', 'x', 'x', 'A', 'x', 'o', 'x', 'x', 'x'],
                   ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                   ['x', 'A', 'x', 'o', 'x', 'x', 'x', 'x', 'x', 'A', 'x'],
                   ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                   ['x', 'B', 'x', 'A', 'x', 'x', 'x', 'A', 'x', 'o', 'x'],
                   ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x']]
    assert lazor_path(solved_grid, lazors, hole)[0] == True


if __name__ == "__main__":
    filename = "dark_1.bff"
    (board_given, reflect_blocks, opaque_blocks,
        refract_blocks, lazors, points) = read_board(filename)
    print("Welcome to the No Stress Lazor Solver ")
    print("Given Board :\n ")
    for y in board_given:
        for x in y:
            print(x, end=' ')
        print()
    print("\nType of Blocks given:")
    print("Reflective blocks - %d" % (reflect_blocks))
    print("Opaque blocks - %d" % opaque_blocks)
    print("Refractive blocks - %d" % refract_blocks)
    unit_test()
    time_start = time.time()
    Board = Board(
        board_given, reflect_blocks, opaque_blocks,
        refract_blocks, lazors, points)
    Board.Solver(filename)
    time_end = time.time()
    print('\nRun time: %f seconds' % (time_end - time_start))
