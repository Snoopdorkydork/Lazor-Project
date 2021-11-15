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
    'C': (211, 211, 211),
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


def GUI_board(original_board, solution_board, boardname,
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
        draw.ellipse([a - 5, b - 5, a + 5, b + 5], fill=(255, 165, 0))
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
        draw.ellipse([a - 5, b - 5, a + 5, b + 5], fill=(255, 165, 0))
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
