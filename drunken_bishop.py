import os
import random
import argparse
import unicodedata
from PIL import Image, ImageDraw, ImageFont
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors

# Register the font (change the path and name accordingly)
pdfmetrics.registerFont(TTFont('Mono', 'Menlo-Regular.ttf'))

# Argument Parsing
parser = argparse.ArgumentParser(description='Generate random ASCII art pattern with multiple bishops.')
parser.add_argument('--min-bishops', type=int, default=2, help='Minimum number of bishops')
parser.add_argument('--max-bishops', type=int, default=10, help='Maximum number of bishops')
parser.add_argument('--different-alphabets', action='store_true', help='Use different alphabets for different bishops')
parser.add_argument('--num-outputs', type=int, default=1, help='Number of outputs to generate')


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

def rgb_to_reportlab(r, g, b):
    """Converts an RGB color in range 0-255 to a ReportLab Color."""
    return colors.Color(r / 255.0, g / 255.0, b / 255.0)

# Step 1: Get the RGB values of your terminal's background and foreground colors.
# For example, if your terminal uses a background color of #282C34 and a foreground color of #ABB2BF:
term_bg = rgb_to_reportlab(40, 44, 52)
term_fg = rgb_to_reportlab(171, 178, 191)

def write_to_pdf(room_string, filename_without_extension):
    custom_page_size = (510, 680)  # Width x Height in points
    c = canvas.Canvas(f"{filename_without_extension}.pdf", pagesize=custom_page_size)
    width, height = custom_page_size
    
    # Step 2: Use your terminal colors
    c.setFillColor(term_bg)
    c.rect(0, 0, width, height, fill=1)
    
    c.setFont("Mono", 8)
    c.setFillColor(term_fg)
    
    lines = room_string.split('\n')
    line_height = 8  # Reduced line height
    x = 5  # Reduced x position
    
    # Margins
    top_margin = 10
    bottom_margin = 10
    
    # Calculate total height of text and adjust starting y position
    total_text_height = len(lines) * line_height
    starting_y = (height - total_text_height - top_margin - bottom_margin) // 2 + total_text_height + bottom_margin

    y = starting_y
    
    for line in lines:
        c.drawString(x, y, line)
        y -= line_height  # Move down one line

    c.save()


for _ in range(args.num_outputs):
    num_bishops = random.randint(args.min_bishops, args.max_bishops)
    random_bytes = [random.randint(0, 255) for _ in range(200)]
    room, bishop_alphabets, bishop_tracker = from_bytes(random_bytes, num_bishops)
    room_string = room_to_string(room, bishop_alphabets, bishop_tracker)
    filename_without_extension = write_to_file(room_string)
    write_to_pdf(room_string, filename_without_extension)

