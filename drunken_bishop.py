import os
import random
import argparse

# Argument Parsing
parser = argparse.ArgumentParser(description='Generate random ASCII art pattern with multiple bishops.')
parser.add_argument('--min-bishops', type=int, default=2, help='Minimum number of bishops')
parser.add_argument('--max-bishops', type=int, default=10, help='Maximum number of bishops')

args = parser.parse_args()

RoomWidth = 100
RoomHeight = 80
Alphabet = " .o+=*BOX@%&#/^"
UnknownChar = '!'
StartCode = 1000
EndCode = 2000
StartChar = 'S'
EndChar = 'E'

DIRECTIONS = {
    "NW": [-1, -1],
    "NE": [-1, 1],
    "SW": [1, -1],
    "SE": [1, 1],
    "N": [-1, 0],
    "E": [0, 1],
    "S": [1, 0],
    "W": [0, -1]
}

def from_bytes(input_bytes, num_bishops):
    room = [[0 for _ in range(RoomWidth)] for _ in range(RoomHeight)]

    bishop_positions = [[random.randint(0, RoomHeight - 1), random.randint(0, RoomWidth - 1)] for _ in range(num_bishops)]
    
    for byte in input_bytes:
        bits = format(byte, '08b')
        bitpairs = [bits[i:i+2] for i in range(0, 8, 2)]
        
        for pos in bishop_positions:
            for bitpair in bitpairs:
                direction = list(DIRECTIONS.keys())[int(bitpair, 2) % 8]
                dY, dX = DIRECTIONS[direction]
                pos[0] += dY
                pos[1] += dX
                pos[0] = max(0, min(RoomHeight - 1, pos[0]))
                pos[1] = max(0, min(RoomWidth - 1, pos[1]))
                room[pos[0]][pos[1]] += 1

    for i, pos in enumerate(bishop_positions):
        if i == 0:
            room[pos[0]][pos[1]] = StartCode
        elif i == num_bishops - 1:
            room[pos[0]][pos[1]] = EndCode
        else:
            room[pos[0]][pos[1]] = random.randint(StartCode + 1, EndCode - 1)
    
    return room

def room_to_string(room):
    output = "+" + "-" * RoomWidth + "+\n"
    for row in room:
        line = []
        for col in row:
            if col == StartCode:
                char = StartChar
            elif col == EndCode:
                char = EndChar
            elif col < len(Alphabet):
                char = Alphabet[col]
            else:
                char = UnknownChar
            line.append(char)
        output += "|" + "".join(line) + "|\n"
    output += "+" + "-" * RoomWidth + "+"
    return output

def write_to_file(room_string):
    folder_name = "random_patterns"
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)

    i = 1
    while os.path.exists(f"{folder_name}/random_{i}.txt"):
        i += 1

    with open(f"{folder_name}/random_{i}.txt", "w") as f:
        f.write(room_string)

num_bishops = random.randint(args.min_bishops, args.max_bishops)
random_bytes = [random.randint(0, 255) for _ in range(200)]
room = from_bytes(random_bytes, num_bishops)
room_string = room_to_string(room)
write_to_file(room_string)
