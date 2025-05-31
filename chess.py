import stt


TILES_SET = []
for alfa in [chr(num) for num in range(65, 73)]:
    for num  in list(range(1, 9)):
        TILES_SET.append(alfa+str(num))



class Piece():
    def __init__(self, name, moving, represent, color):
        self.name = name
        self.moving = moving
        self.represent = represent
        self.color = color


class Tile():
    def __init__(self, pawn):
        self.pawn = pawn
        self.is_bold = False
        self.id = id
    
    def __repr__(self):
        if (self.is_bold == False):
            return f"\033[0m[{' ' if self.pawn == None else self.pawn.represent}]"
        else:
            return f"\033[1m[{' ' if self.pawn == None else self.pawn.represent}]\033[0m"

class Moving():
    def __init__(self, points, invers=False, hits=None):
        self.points = points
        self.hit = points if hits == None else points


W_PAWN = Piece(name="Pawn", moving=Moving(points=[-8], hits=[-7, -8]), represent='♟', color='white')
W_ROOK = Piece(name="Rook", 
              moving=Moving(points=[-8, -8*2, -8*3, -8*4, -8*5, -8*6, -8*7,    # vertical forwad
                                     8,  8*2,  8*3,  8*4,  8*5,  8*6,  8*7,    # vertical backward 
                                     1,    2,    3,    4,    5,    6,    7,    # horizontal right
                                    -1,   -2,   -3,   -4,   -5,   -6,   -7,]), # horizontal left
              represent='♜',
              color='white')
W_BISHOP= Piece(name="Bishop", 
               moving=Moving(points=[-7, -7*2, -7*3, -7*4, -7*5, -7*6, -7*7,
                                      -9, -9*2, -9*3, -9*4, -9*5, -9*6, -9*7,
                                       7,  7*2,  7*3,  7*4,  7*5,  7*6,  7*7,
                                       9,  9*2,  9*3,  9*4,  9*5,  9*6,  9*7,],),
               represent='♝',
               color='white')
W_KNIGHT= Piece(name="Knight"
                , moving=Moving(points=[-8*2+1, -8*2-1, # forwad
                                        8*2+1, 8*2-1,   #backward
                                        -10, -6,        # left
                                        6, 10])         # rigt
                , represent='♞'
                , color='white')

W_KING = Piece(name="King", 
               moving=Moving(points=[-7, -8, -9
                                     -1, +1,
                                     +7, +8, +9]),
               represent="♚",
               color="white")


tiles = [ Tile(pawn=None) for _ in range(8*8) ]
tiles[27].pawn = W_KING


def display_board():
    for i in range(8):
        print(f' {chr(65+i)} ', end='')
    print()

    for row in range(8):
        for column in range(8):
            if ((row + column ) % 2 == 0 ):
                tiles[(row * 8) + column].is_bold = True

            print(tiles[(row * 8) + column], end='')
        print(' ', row + 1)


def find_legal_area(piece:Piece, loc_idx):
    global tiles

    # retriev first
    legal_area = [loc_idx + p for p in piece.moving.points]

    # Normalize, restrict just on board;
    legal_area = [a for a in legal_area if (a >= 0 and a <= 8*8-1)]

    if (piece.name == 'Rook'):
    
        legal_area_left = []
        for area in [a for a in legal_area if (a >= (loc_idx // 8) * 8  and a < loc_idx )] :
            if (tiles[area].pawn != None):
                print(f"found!! {area} is {tiles[area].pawn.name}!")
                legal_area_left.append(area)
                break
            
            legal_area_left.append(area)
        
        legal_area_right = []
        for area in [a for a in legal_area if (a > loc_idx and a <= (loc_idx // 8) * 8 + 8)]  :
            if (tiles[area].pawn != None):
                print(f"found!! {area} is {tiles[area].pawn.name}!")
                legal_area_right.append(area)
                break
            
            legal_area_right.append(area)

        legal_area_up = []
        for area in [loc_idx - b*8 for b in range(1, loc_idx // 8 + 1)]  :
            if (tiles[area].pawn != None):
                print(f"found!! {area} is {tiles[area].pawn.name}!")
                legal_area_up.append(area)
                break
            
            legal_area_up.append(area)


        legal_area_down = []
        for area in [loc_idx+ c*8 for c in range(1, 8 - loc_idx//8)]:
            if (tiles[area].pawn != None):
                print(f"found!! {area} is {tiles[area].pawn.name}!")
                legal_area_down.append(area)
                break
            legal_area_down.append(area)
        

        return legal_area_up + legal_area_down + legal_area_right + legal_area_left
    
    elif (piece.name == "Bishop"):

        right_line = [8 * a - 1 for a in range(1, 9)]
        left_line = [8 * a for a in range(8)]

        legal_area_topleft = []
        for i in [loc_idx - a*9 for a in range(1, loc_idx//8 + 1)]:
            if (i in left_line or tiles[i].pawn != None ):
                legal_area_topleft.append(i)
                break
            legal_area_topleft.append(i)

        legal_area_topright = []
        for i in [loc_idx - a*7 for a in range(1, loc_idx//8 + 1)]:
            if (i in right_line or tiles[i].pawn != None ):
                legal_area_topright.append(i)
                break
            legal_area_topright.append(i)
        

        legal_area_bottomleft = []
        for i in [loc_idx + a*7 for a in range (1, 8 - (loc_idx//8 ))]:
            if (i in left_line or tiles[i].pawn != None ):
                legal_area_bottomleft.append(i)
                break;
            legal_area_bottomleft.append(i)


        legal_area_bottomright = []
        for i in [loc_idx + a*9 for a in range (1, 8 - (loc_idx//8 ))]:
            if (i in right_line or tiles[i].pawn != None ):
                legal_area_bottomright.append(i)
                break
            legal_area_bottomright.append(i)

        return (legal_area_topleft 
                + legal_area_topright 
                + legal_area_bottomleft 
                + legal_area_bottomright)

    # TODO: perbaiki ini
    elif (piece.name == 'Knight'):
        print('piece on:', loc_idx)
        if (loc_idx in range(0, 16)):
            try:
                legal_area.remove(loc_idx - 8*2 + 1)
            except ValueError: pass
            try:
                legal_area.remove(loc_idx - 8*2 - 1)
            except ValueError: pass

        if (loc_idx in range(48, 64)):
            try:
                legal_area.remove(loc_idx + 8*2 + 1)
            except ValueError: pass

            try:
                legal_area.remove(loc_idx + 8*2 - 1)
            except ValueError: pass

        if (loc_idx in list(range(0, 64, 8)) + list(range(1, 65, 8))):
            try:
                legal_area.remove(loc_idx - 10)
            except ValueError: pass

            try:
                legal_area.remove(loc_idx - 6 )
            except ValueError: pass

        if (loc_idx in list(range(22, 54, 8)) + list(range(23, 55, 8))):
            try:
                legal_area.remove(loc_idx + 10)
            except ValueError: pass

            try:
                legal_area.remove(loc_idx + 6 )
            except ValueError: pass

        #     legal_area.remive
        print('polish move', legal_area)
        return legal_area
    
    elif (piece.name == 'King') :
        if (loc_idx in list(range(0, 8))):
            try:
                legal_area.remove(loc_idx - 9)
            except ValueError: pass

            try:
                legal_area.remove(loc_idx - 8)
            except ValueError: pass

            try:
                legal_area.remove(loc_idx - 7)
            except ValueError: pass

        if (loc_idx in list(range(56, 64))):
            try:
                legal_area.remove(loc_idx + 9)
            except ValueError: pass

            try:
                legal_area.remove(loc_idx + 8)
            except ValueError: pass

            try:
                legal_area.remove(loc_idx + 7)
            except ValueError: pass
        
        if (loc_idx in list(range(0, 64, 8))):
            try:
                legal_area.remove(loc_idx - 1)
            except ValueError: pass
        
        if (loc_idx in list(range(7, 71, 8))):
            try:
                legal_area.remove(loc_idx + 1)
            except ValueError: pass
        
        return legal_area



def moving(target, destination):

    if (target == '' or destination == ''):
        print('perintah tidak benar')
        return;

    target_idx = list(target)
    target_idx = (ord(target_idx[0]) - 65) + (8 * (int(target_idx[1]) - 1 ))
    dest_idx = list(destination)
    dest_idx = (ord(dest_idx[0]) - 65) + (8 * (int(dest_idx[1]) - 1 ))

    if tiles[target_idx].pawn == None:
        print('tidak ada piece di sana')
        return

    # store pieces
    pawn = tiles[target_idx].pawn
    
    legal_area = find_legal_area(pawn, target_idx)

    if (dest_idx not in legal_area):
        print("⚠️  illegal move")
    else:
        if tiles[dest_idx].pawn != None:
            print(f"you hit {tiles[dest_idx].pawn.name}")
        tiles[target_idx].pawn = None
        tiles[dest_idx].pawn = pawn
    
        legal_area = find_legal_area(pawn, dest_idx)


def find_movement(text_from_stt):
    text = text_from_stt.split()
    target = ''
    dest = ''

    for t in range(len(text)):
        if text[t] in TILES_SET:
            target = text[t]
            if t !=  len(text) - 1:
                for d in range(t+1, len(text)):
                    if text[d] in TILES_SET:
                        dest = text[d]
                        break
        break;
    return [target, dest]


while (True):
    display_board();
    stt.move_pion()

    text = stt.stt()
    print('perintah terbaca: ',text)
    
    move = find_movement(text);
    moving(move[0], move[1])
    input('--lanjut')