import os
import random
import argparse
import unicodedata
from PIL import Image, ImageDraw, ImageFont
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

# Argument Parsing
parser = argparse.ArgumentParser(description='Generate random ASCII art pattern with multiple bishops.')
parser.add_argument('--min-bishops', type=int, default=2, help='Minimum number of bishops')
parser.add_argument('--max-bishops', type=int, default=10, help='Maximum number of bishops')
parser.add_argument('--different-alphabets', action='store_true', help='Use different alphabets for different bishops')

args = parser.parse_args()

RoomWidth = 100
RoomHeight = 80
DefaultAlphabet = " .o+=*BOX@%&#/^"
UnknownChar = '!'
StartCode = 1000
EndCode = 2000
StartChar = 'S'
EndChar = 'E'

# Adding multiple alphabets to choose from
ALPHABETS = [
    " .o+=*BOX@%&#/^",
    " 1234567890<>",
    " !?@#$%^&*()-=_",
    " abcdefghijklmn",
    " ↑↗→↘↓↙←↖",
    " ▁▂▃▄▅▆▇█",
    " ○◔◑◕●"
]



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
    bishop_tracker = [[0 for _ in range(RoomWidth)] for _ in range(RoomHeight)]  # New array to track bishops
    
    bishop_positions = [[random.randint(0, RoomHeight - 1), random.randint(0, RoomWidth - 1)] for _ in range(num_bishops)]
    bishop_alphabets = [random.choice(ALPHABETS) for _ in range(num_bishops)] if args.different_alphabets else [DefaultAlphabet for _ in range(num_bishops)]
    
    for byte in input_bytes:
        bits = format(byte, '08b')
        bitpairs = [bits[i:i+2] for i in range(0, 8, 2)]
        
        for i, pos in enumerate(bishop_positions):
            for bitpair in bitpairs:
                direction = list(DIRECTIONS.keys())[int(bitpair, 2) % 8]
                dY, dX = DIRECTIONS[direction]
                pos[0] += dY
                pos[1] += dX
                pos[0] = max(0, min(RoomHeight - 1, pos[0]))
                pos[1] = max(0, min(RoomWidth - 1, pos[1]))
                
                room[pos[0]][pos[1]] += 1
                bishop_tracker[pos[0]][pos[1]] = i  # Update tracker with the current bishop index
    
    return room, bishop_alphabets, bishop_tracker

# Adding the function to get the string width
def get_str_width(s):
    return sum(2 if unicodedata.east_asian_width(c) in ['F', 'W'] else 1 for c in s)

# Modified room_to_string function
def room_to_string(room, bishop_alphabets, bishop_tracker):
    output = "+" + "-" * RoomWidth + "+\n"
    for row_idx, row in enumerate(room):
        line = []
        for col_idx, col in enumerate(row):
            bishop_index = bishop_tracker[row_idx][col_idx]
            
            if col == StartCode:
                char = StartChar
            elif col == EndCode:
                char = EndChar
            elif col < len(bishop_alphabets[bishop_index]):
                char = bishop_alphabets[bishop_index][col]
            else:
                char = UnknownChar

            line.append(char)

        # Calculate the line width and adjust the frame accordingly
        lineWidth = get_str_width("".join(line))
        adjustment = RoomWidth - lineWidth
        output += "|" + "".join(line) + " " * adjustment + "|\n"
    output += "+" + "-" * RoomWidth + "+"
    return output

def generate_image(room, bishop_alphabets, bishop_tracker, filename):
    img_width, img_height = 512, 768  # Desired output dimensions
    aspect_ratio = RoomWidth / RoomHeight
    # Calculate cell dimensions based on aspect ratio
    cell_height = img_height // RoomHeight
    cell_width = int(cell_height * aspect_ratio)
    
    # Adjust image dimensions based on cell dimensions
    img_width = RoomWidth * cell_width
    img_height = RoomHeight * cell_height
    
    img = Image.new('RGB', (img_width, img_height), color='white')
    draw = ImageDraw.Draw(img)

    for row_idx, row in enumerate(room):
        for col_idx, col in enumerate(row):
            bishop_index = bishop_tracker[row_idx][col_idx]
            max_val = len(bishop_alphabets[bishop_index])
            # Map the cell value to a pastel color
            ratio = col / max_val
            R = int(255 * (1 - ratio))
            G = int(255 * ratio)
            B = int(255 * (1 - abs(ratio - 0.5) * 2))

            color = (R, G, B)
            draw.rectangle(
                [col_idx * cell_width, row_idx * cell_height,
                 (col_idx + 1) * cell_width, (row_idx + 1) * cell_height],
                fill=color
            )

    img = img.rotate(90, expand=1)
    img.save(f"{filename}.png")

def write_to_file(room_string):
    folder_name = "random_patterns"
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)

    i = 1
    while os.path.exists(f"{folder_name}/random_{i}.txt"):
        i += 1

    filename = f"{folder_name}/random_{i}"
    with open(f"{filename}.txt", "w") as f:
        f.write(room_string)
    
    return filename  # Return filename without extension


num_bishops = random.randint(args.min_bishops, args.max_bishops)
random_bytes = [random.randint(0, 255) for _ in range(200)]
room, bishop_alphabets, bishop_tracker = from_bytes(random_bytes, num_bishops)
room_string = room_to_string(room, bishop_alphabets, bishop_tracker)
filename_without_extension = write_to_file(room_string)
generate_image(room, bishop_alphabets, bishop_tracker, filename_without_extension)
