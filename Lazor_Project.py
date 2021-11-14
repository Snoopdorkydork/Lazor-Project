# This is this initial commit to GitHub for the Lazor Project
# file location (mahin): OneDrive/Documents/GitHub/Lazor-Project

class Lazor():
    '''
    This Class creates objects which represent the board
    There are varyious boards with increasing difficulty
    and have different no. and types of blocks
    '''

    def __init__(self, board, reflected_blocks, opaque_blocks, refracted_blocks, lazors, points):
        '''
        Initialises the object of the Class Grid
        *** Parameters ***
        self - variable that holds all the data regarding the class object
        board - n*m matrix consisting of some or all of o, x, A, B and C
        reflected_blocks - number of reflect blocks in the board
        opaque_blocks - number of absorb blocks in the board
        redracted_blocks -  number of refract blocks in the board
        lazors - list of lists of all lazors consisting of orgins and direction
        eg. [[(1,3),(-1,-1)],[(2,4), (1,-1)]] - 2 lazors
        L1 - origin (1,3), direction (-1,-1)
        L2 - origin (2,4), direction (1, -1)
        points- list of hole points that the lazor has to intersect
        *** Returns ***
        Nothing!
        '''
        self.board = board
        self.reflected = reflected_blocks
        self.opaque = opaque_blocks
        self.refracted = refracted_blocks
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
