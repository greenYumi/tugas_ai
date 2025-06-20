import stt
import os


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


class Tile():
    def __init__(self, post:dict):
        self.position = post
        self.occupied:Piece = None

    def __repr__(self):
        p = self.occupied if self.occupied != None else ' '
        return f"[{p}]"

class Piece():
    def __init__(self, name, color, represent):
        self.name = name
        self.color = color
        self.represent = represent
        
        self.position = {}
        self.tile_moves = []

    def __repr__(self):
        return self.represent
    


class Board():
    def __init__(self):
        self.board = []

        for y in range(8):
            y_axis = []
            for x in range(8):
                y_axis.append(Tile(post={'x': x, 'y': y}))
            self.board.append(y_axis)

        self.tiles_occupied = []

    ## FOR DEMO ONLY
    def setPiece(self, x, y, piece:Piece):
        piece.position = {'x': x, 'y': y}
        self.board[y][x].occupied = piece
        self.tiles_occupied.append({'x': x, 'y': y})
        self.updateAllPiece()
    
    def updateAllPiece(self):
        for piece in self.tiles_occupied:
            self.board[piece['y']][piece['x']].occupied.updateMoveTiles(self.board)

    def movePiece(self, by_x, by_y, to_x, to_y):

        piece = self.board[by_y][by_x].occupied

        # checking if the said position have occupied by a piece
        if self.board[by_y][by_x].occupied is None:
            print('tidak ada piece')
            return -1
        
        # checkig if the piece can move to the destionation tiles
        dest = {'x': to_x, 'y': to_y}
        if dest not in piece.tile_moves:
            print('illegal move')
            return -1
        
        # move the piece to the desire tiles
        self.board[by_y][by_x].occupied = None
        self.board[to_y][to_x].occupied = piece

        # update the piece tile move
        piece.position = {'x': to_x, 'y': to_y}

        # update first_move status on spesifik phone
        # all pices name will update
        if piece.name == 'pawn': 
            piece.first_move = True

        # update tiles_occupied and update all movement set for each pice
        self.tiles_occupied.append(dest)
        self.tiles_occupied.remove({'x': by_x, 'y': by_y})
        self.updateAllPiece()

class PAWN(Piece):
    def __init__(self, name, color, represent, inverse=False):
        super().__init__(name, color, represent)

        self.inverse = inverse
        self.first_move = False;
    
    def updateMoveTiles(self, board:Board):
        x = self.position['x']
        y = self.position['y']

        # ASSUME THE PAWN IS FROM BOTTOM OF THE DISPLAY

        # clear tile_moves list
        self.tile_moves.clear()
        
        direction  = 1 if self.inverse else -1
        one_step_y = y + direction

        # add 1 tiles forward move
        if (0 <= one_step_y <= 7 
            and board[one_step_y][x].occupied is None):
                self.tile_moves.append({'x': x, 'y': one_step_y})

        # add 2 tiles forward move for the first move
        two_step_y = y + direction * 2
        if (not self.first_move
        and 0 <= two_step_y <= 7    
        and board[one_step_y][x].occupied is None
        and board[two_step_y][x].occupied is None): 
            self.tile_moves.append({'x': x, 'y': two_step_y})

        # add left diagonal move
        if x - 1 >= 0 and 0 <= one_step_y <= 7:
            left_diag = board[one_step_y][x-1] 
            if (left_diag.occupied is not None
                and left_diag.occupied.color != self.color):
                    self.tile_moves.append({'x': x-1, 'y': one_step_y})
                    print(self.name, self.color, ':',f'see {left_diag.occupied.name} on left')


        # add right diagonal move
        if x + 1 < 7 and 0 <= one_step_y <= 7:
            right_diag = board[one_step_y][x+1]
            if (right_diag.occupied is not None 
                and right_diag.occupied.color != self.color):
                    self.tile_moves.append({'x': x+1, 'y': one_step_y})

        print(self.color, self.tile_moves)

class KNIGHT(Piece):
    def __init__(self, name, color, represent):
        super().__init__(name, color, represent)

    def updateMoveTiles(self, board):
        x = self.position['x']
        y = self.position['y']

        self.tile_moves.clear()

        two_step_forward = y - 2
        two_step_backward = y + 2
        two_step_left = x - 2
        two_step_right = x + 2

        # add two forward and one left
        if (x - 1 >= 0 and two_step_forward >= 0):
            forward_left = board[two_step_forward][x-1] 
            if(forward_left.occupied is None 
               or forward_left.occupied.color != self.color):
                self.tile_moves.append({'x': x-1, 'y': two_step_forward})

        # add two forward and one right
        if (x + 1 <= 7  and two_step_forward >= 0):
            forward_right = board[two_step_forward][x+1] 
            if(forward_right.occupied is None 
               or forward_right.occupied.color != self.color):
                self.tile_moves.append({'x': x+1, 'y': two_step_forward})

        # add two backward and one left
        if (x - 1 >= 0 and two_step_backward <= 7):
            backward_left = board[two_step_backward][x-1] 
            if(backward_left.occupied is None 
               or backward_left.occupied.color != self.color):
                self.tile_moves.append({'x': x-1, 'y': two_step_backward})
        
        # add two backward and one left
        if (x + 1 <= 7 and two_step_backward <= 7):
            backward_right = board[two_step_backward][x+1] 
            if(backward_right.occupied is None 
               or backward_right.occupied.color != self.color):
                self.tile_moves.append({'x': x+1, 'y': two_step_backward})
        
        # add two left and one forward
        if (two_step_left >= 0 and y-1 >= 0):
            left_forward = board[y-1][two_step_left]
            if(left_forward.occupied is None
               or left_forward.occupied.color != self.color):
                self.tile_moves.append({'x': two_step_left, 'y': y-1})
        
        # add two left and one backward
        if (two_step_left >= 0 and y+1 <= 7):
            left_backward = board[y+1][two_step_left]
            if(left_backward.occupied is None
               or left_backward.occupied.color != self.color):
                self.tile_moves.append({'x': two_step_left, 'y': y+1})

        # add two right and one forward
        if (two_step_right <= 7 and y-1 >= 0):
            right_forward = board[y-1][two_step_right]
            if(right_forward.occupied is None
               or right_forward.occupied.color != self.color):
                self.tile_moves.append({'x': two_step_right, 'y': y-1})

        # add two right and one backward
        if (two_step_right <= 7 and y+1 <= 7):
            right_backward = board[y+1][two_step_right]
            if(right_backward.occupied is None
               or right_backward.occupied.color != self.color):
                self.tile_moves.append({'x': two_step_right, 'y': y+1})
        
        print(self.name,':',self.tile_moves)


class ROOK(Piece):
    def __init__(self, name, color, represent):
        super().__init__(name, color, represent)
    
    def updateMoveTiles(self, board):
        x = self.position['x']
        y = self.position['y']

        self.tile_moves.clear()


        # add streight forward move
        i = 1
        while (y - i >= 0):
            if board[y-i][x].occupied is None or board[y-i][x].occupied.color != self.color:
                self.tile_moves.append({'x': x, 'y': y-i})
                i += 1
            else:
                break

        # add streight backward move
        i = 1
        while (y + i <= 7):
            if board[y+i][x].occupied is None or board[y+i][x].occupied.color != self.color:
                self.tile_moves.append({'x': x, 'y': y+i})
                i += 1
            else:
                break
        
        # add streight right move
        i = 1
        while (x + i <= 7):
            if board[y][x+i].occupied is None or board[y][x+i].occupied.color != self.color:
                self.tile_moves.append({'x': x+i, 'y': y})
                i += 1
            else:
                break
        
        # add streight left move
        i = 1
        while (x - i >= 0):
            if board[y][x-i].occupied is None or board[y][x-i].occupied.color != self.color:
                self.tile_moves.append({'x': x-i, 'y': y})
                i += 1
            else:
                break
        print(self.name, self.tile_moves)

class BISHOP(Piece):
    def __init__(self, name, color, represent):
        super().__init__(name, color, represent)
    
    def updateMoveTiles(self, board):
        x = self.position['x']
        y = self.position['y']

        self.tile_moves.clear()

        # left forward diagonal
        i = 1
        while (x-i >= 0 and y-i >=0):
            if (board[y-i][x-i].occupied is None or board[y-i][x-i].occupied.color != self.color):
                self.tile_moves.append({'x': x-i, 'y': y-i})
                i += 1
            else:
                break
        
        # right forward diagonal
        i = 1
        while (x+i <= 7 and y-i >=0):
            if (board[y-i][x+i].occupied is None or board[y-i][x+i].occupied.color != self.color):
                self.tile_moves.append({'x': x+i, 'y': y-i})
                i += 1
            else:
                break
        
        # left backward diagonal
        i = 1
        while (x-i >= 0 and y+i <= 7):
            if (board[y+i][x-i].occupied is None or board[y+i][x-i].occupied.color != self.color):
                self.tile_moves.append({'x': x-i, 'y': y+i})
                i += 1
            else:
                break
        
        # right backward diagonal
        i = 1
        while (x+i <= 7 and y+i <= 7):
            if (board[y+i][x+i].occupied is None or board[y+i][x+i].occupied.color != self.color):
                self.tile_moves.append({'x': x+i, 'y': y+i})
                i += 1
            else:
                break


        # print(self.name, ':', self.tile_moves)


class QUEEN(Piece):
    def __init__(self, name, color, represent):
        super().__init__(name, color, represent)
    
    def updateMoveTiles(self, board):
        x = self.position['x']
        y = self.position['y']

        self.tile_moves.clear()

         # left forward diagonal
        i = 1
        while (x-i >= 0 and y-i >=0):
            if (board[y-i][x-i].occupied is None or board[y-i][x-i].occupied.color != self.color):
                self.tile_moves.append({'x': x-i, 'y': y-i})
                i += 1
            else:
                break
        
        # right forward diagonal
        i = 1
        while (x+i <= 7 and y-i >=0):
            if (board[y-i][x+i].occupied is None or board[y-i][x+i].occupied.color != self.color):
                self.tile_moves.append({'x': x+i, 'y': y-i})
                i += 1
            else:
                break
        
        # left backward diagonal
        i = 1
        while (x-i >= 0 and y+i <= 7):
            if (board[y+i][x-i].occupied is None or board[y+i][x-i].occupied.color != self.color):
                self.tile_moves.append({'x': x-i, 'y': y+i})
                i += 1
            else:
                break
        
        # right backward diagonal
        i = 1
        while (x+i <= 7 and y+i <= 7):
            if (board[y+i][x+i].occupied is None or board[y+i][x+i].occupied.color != self.color):
                self.tile_moves.append({'x': x+i, 'y': y+i})
                i += 1
            else:
                break

        
        # add streight forward move
        i = 1
        while (y - i >= 0):
            if board[y-i][x].occupied is None or board[y-i][x].occupied.color != self.color:
                self.tile_moves.append({'x': x, 'y': y-i})
                print('ok')
                i += 1
            else:
                break

        # add streight backward move
        i = 1
        while (y + i <= 7):
            if board[y+i][x].occupied is None or board[y-i][x].occupied.color != self.color:
                self.tile_moves.append({'x': x, 'y': y+i})
                print('ok')
                i += 1
            else:
                break
        
        # add streight right move
        i = 1
        while (x + i <= 7):
            if board[y][x+i].occupied is None or board[y][x+i].occupied.color != self.color:
                self.tile_moves.append({'x': x+i, 'y': x})
                i += 1
            else:
                break
        
        # add streight left move
        i = 1
        while (x - i >= 0):
            if board[y][x-i].occupied is None or board[y][x-i].occupied.color != self.color:
                self.tile_moves.append({'x': x-i, 'y': x})
                i += 1
            else:
                break
        
        # print(self.name, ':', self.tile_moves)

class KING(Piece):
    def __init__(self, name, color, represent):
        super().__init__(name, color, represent)
    
    def updateMoveTiles(self, board):
        x = self.position['x']
        y = self.position['y']

        self.tile_moves.clear()

        # on step forward
        if (y-1 >= 0) :
            if ((board[y-1][x].occupied is None or board[y-1][x].occupied.color != self.color)):
                self.tile_moves.append({'x': x, 'y':y-1})

        # on step backward
        if (y+1 <= 7) :
            if ((board[y+1][x].occupied is None or board[y+1][x].occupied.color != self.color)):
                self.tile_moves.append({'x': x, 'y':y+1})

        # on step right
        if (x+1 <= 7) :
            if ((board[y][x+1].occupied is None or board[y][x+1].occupied.color != self.color)):
                self.tile_moves.append({'x': x+1, 'y':y})

        # on step left
        if (x-1 >= 0) :
            if ((board[y][x-1].occupied is None or board[y][x-1].occupied.color != self.color)):
                self.tile_moves.append({'x': x-1, 'y':y})

        # on step forward right
        if (y-1 >= 0 and x+1 <= 7) :
            if ((board[y-1][x+1].occupied is None or board[y-1][x+1].occupied.color != self.color)):
                self.tile_moves.append({'x': x+1, 'y':y-1})        

        # one step forward left
        if (y-1 >= 0 and x-1 >= 0) :
            if ((board[y-1][x-1].occupied is None or board[y-1][x-1].occupied.color != self.color)):
                self.tile_moves.append({'x': x-1, 'y':y-1})

        # one step backward left
        if (y+1 <= 7 and x-1 >= 0) :
            if ((board[y+1][x-1].occupied is None or board[y+1][x-1].occupied.color != self.color)):
                self.tile_moves.append({'x': x-1, 'y':y+1})

        # one step bacward right
        if (y+1 <= 7 and x+1 <= 7) :
            if ((board[y+1][x+1].occupied is None or board[y+1][x+1].occupied.color != self.color)):
                self.tile_moves.append({'x': x+1, 'y':y+1})

        # print(self.name, ':' , self.tile_moves)
        
tile_alfa = {
    'a': 0,
    'b': 1,
    'c': 2,
    'd': 3,
    'e': 4,
    'f': 5,
    'g': 6,
    'h': 7,
}
tile_numb = {
    'one': 0,
    'two': 1,
    'three': 2,
    'four': 3,
    'five': 4,
    'six': 5,
    'seven': 6,
    'eight': 7,
}

tile_piece = [
    'pawn',
    'rook',
    'bishop',
    'knight',
    'queen',
    'king',
]


def normalizeText(text:list, board:Board, color):
    print('get text is -> ', text)

    if len(text) == 2:
        if text[0] in tile_alfa and text[1] in tile_numb:
            
            target_tile = {'x':tile_alfa[text[0]], 'y':tile_numb[text[1]]}
            found = []
            to_x=tile_alfa[text[0]]
            to_y=tile_numb[text[1]]

            for piece in board.tiles_occupied:
                for tile in board.board[piece['y']][piece['x']].occupied.tile_moves:
                    if target_tile == tile and board.board[piece['y']][piece['x']].occupied.color == color:
                        found.append( board.board[piece['y']][piece['x']].position)

            if len(found) == 1:
                board.movePiece(by_x=found[0]['x'],
                                by_y=found[0]['y'],
                                to_x=to_x,
                                to_y=to_y)
                return (0)

            elif len(found) > 1:
                found = set(frozenset(d.items()) for d in found)
                found = [dict(d) for d in found]

                print('which one? say the position')
                for position in found:
                    print(board.board[position['y']][position['x']].occupied.name, ':', chr(position['x']+65), position['y']+1)

                text = stt.getText()
                if text[0] in tile_alfa and text[1] in tile_numb: 
                    by_x = tile_alfa[text[0]]
                    by_y = tile_numb[text[1]]

                    if {'x': by_x, 'y' : by_y} in found:
                        board.movePiece(by_x=by_x, by_y=by_y, to_x=to_x, to_y=to_y)
                        displayBoard()
                        return (0)      

                    else:
                        print('command invalid')
                        return (-1)
                print('command invalid')
                displayBoard()
                return (-1)

    elif len(text) == 3:
        if (text[0] in tile_piece and text[1] in tile_alfa and text[2] in tile_numb ):
            piece_name = text[0]
            to_x = tile_alfa[text[1]]
            to_y = tile_numb[text[2]]
            found = []
            for tile in board.tiles_occupied:
                if (board.board[tile['y']][tile['x']].occupied.name == piece_name
                    and {'x': to_x, 'y': to_y} in board.board[tile['y']][tile['x']].occupied.tile_moves
                    and board.board[tile['y']][tile['x']].occupied.color == color):
                    found.append({'x':board.board[tile['y']][tile['x']].occupied.position['x'],
                                  'y':board.board[tile['y']][tile['x']].occupied.position['y']})
            if len(found) == 1:
                board.movePiece(by_x=found[0]['x'],
                                by_y=found[0]['y'],
                                to_x=to_x,
                                to_y=to_y)
                return (0)

            elif len(found) > 1:
                 ## TODO: perbaiki nanti (rio)
                found = set(frozenset(d.items()) for d in found)
                found = [dict(d) for d in found]

                print('which one? say the position')
                for position in found:
                    print(board.board[position['y']][position['x']].occupied.name, ':', chr(position['x']+65), position['y']+1)

                text = stt.getText()
                if text[0] in tile_alfa and text[1] in tile_numb: 
                    by_x = tile_alfa[text[0]]
                    by_y = tile_numb[text[1]]

                    if {'x': by_x, 'y' : by_y} in found:
                        board.movePiece(by_x=by_x, by_y=by_y, to_x=to_x, to_y=to_y)
                        displayBoard()
                        return (0)  
                    else:
                        print('commnand invalid')
                        return(-1)
                print('command invalid')
                return (-1)
                   

    return -1



b_knight = KNIGHT(color='black', name='knight', represent='♘')
b_bishop = BISHOP(color='black', name='bishop', represent='♗')
w_rook = ROOK(color='white', name='rook', represent='♜')
w_bishop = BISHOP(color='white', name='bishop', represent='♝')


board = Board()

def displayBoard():
    for i in range(8):
        print(f' {chr(i+65)} ', end= '')
    print()

    for y in range(8):
        for x in range(8):
            print(board.board[y][x], end='')
        print(y+1, end='')
        print()


board.setPiece(x=0, y=6, piece=w_bishop)
board.setPiece(x=3, y=0, piece=b_bishop)
board.setPiece(x=6, y=3, piece=b_knight)
board.setPiece(x=7, y=6, piece=w_rook)
input()


# while True:
#     normalizeText(stt.getText(), board)

def play():

    color = 'white'
    while True:
        clear_screen()
        displayBoard()
        print(color, "player turn")
        status = normalizeText(stt.getText(), board, color)
        if status == -1:
            input('salah')
            clear_screen()
            continue
        else:
            color = 'black' if color == 'white' else 'white'



play()