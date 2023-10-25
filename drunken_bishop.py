import os
import random

RoomWidth = 100
RoomHeight = 80
Alphabet = " .o+=*BOX@%&#/^"
UnknownChar = '!'
StartY = RoomHeight // 2
StartX = RoomWidth // 2
StartCode = 1000
EndCode = 2000
StartChar = 'S'
EndChar = 'E'

# Now with eight directions, including N, E, S, W
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

def from_bytes(input_bytes):
    room = [[0 for _ in range(RoomWidth)] for _ in range(RoomHeight)]
    pos = [StartY, StartX]
    
    for byte in input_bytes:
        bits = format(byte, '08b')
        bitpairs = [bits[i:i+2] for i in range(0, 8, 2)]
        for bitpair in bitpairs:
            direction = list(DIRECTIONS.keys())[int(bitpair, 2) % 8]
            dY, dX = DIRECTIONS[direction]
            pos[0] += dY
            pos[1] += dX
            pos[0] = max(0, min(RoomHeight - 1, pos[0]))
            pos[1] = max(0, min(RoomWidth - 1, pos[1]))
            room[pos[0]][pos[1]] += 1

    room[StartY][StartX] = StartCode
    room[pos[0]][pos[1]] = EndCode
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
    # Create folder if it doesn't exist
    folder_name = "random_patterns"
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)

    # Find the next available file name
    i = 1
    while os.path.exists(f"{folder_name}/random_{i}.txt"):
        i += 1

    # Write to the file
    with open(f"{folder_name}/random_{i}.txt", "w") as f:
        f.write(room_string)

# Test the code
random_bytes = [random.randint(0, 255) for _ in range(200)]
room = from_bytes(random_bytes)
room_string = room_to_string(room)
write_to_file(room_string)