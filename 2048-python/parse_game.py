from game import *

""" Parses a hexadecimal character into an Obj2048 """
def parse_char(ch):
    # Char is a 0
    if ch == '0':
        return Obj2048(0)
    for i in range(ord('1'), ord('9') + 1):
        # Char is a number, between 2 and 512
        if ord(ch) == i:
            return Obj2048(2**(i - ord('1') + 1))
    for i in range(ord('a'), ord('f') + 1):
        # Char is a hexadecimal number
        if ord(ch) == i:
            return Obj2048(2**(i - ord('a') + 10))
    raise ValueError("ERROR: Character " + ch + " is an invalid hexadecimal number.")
    
""" Parses a nxn string matrix into a Board2048; assumes n = num_rc """
def parse_nbyn(s):
    # Initialize grid
    grid = np.full((num_rc, num_rc), Obj2048(0), dtype=Obj2048)
    count = 0
    for i in range(num_rc):
        for j in range(num_rc):
            grid[i][j] = Obj2048(parse_char(s[count]))
            count += 1
        # skip newline
        count += 1
    return Board2048(grid)
    
""" Parses a move string with ... move chosen <MOVE> ... to the move number """
def parse_move(s):
    # find where the move is
    pos = s.find("move chosen ") + 12
    sub_s = ""
    # continue until we find the comma at the end of the move
    while s[pos] != ',':
        sub_s += s[pos]
        pos += 1
    if sub_s == "right":
        return 0
    elif sub_s == "up":
        return 1
    elif sub_s == "left":
        return 2
    elif sub_s == "down":
        return 3
    raise ValueError("ERROR: Invalid move")
    
""" Loads datafile into an array of tuples of Board2048's and moves

    Each tuple corresponds to a Board2048, together with the move
    the heuristic AI is about to make
"""
def load_datafile(filename):
    with open(filename, 'r') as file:
        data = file.readlines()
        tuple_arr = []
        num_lines = len(data)
        # Don't want last matrix, since game is over
        curr_matrix = ""
        curr_board = None
        for i in range(num_lines - 7):
            if (i % 8 in range(4)):
                curr_matrix += data[i]
            elif (curr_matrix != ""):
                curr_board = Board2048(parse_nbyn(curr_matrix))
                curr_matrix = ""
            if (i % 8 == 7):
                tuple_arr.append((curr_board, parse_move(data[i])))
        return tuple_arr