import os
import sys
import json
import random
import colorsys
import inquirer 
import argparse
import unicodedata
import subprocess
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
pdfmetrics.registerFont(TTFont('Mono', 'DejaVuSansMono.ttf'))
pdfmetrics.registerFont(TTFont('UnifrakturMaguntia', 'UnifrakturMaguntia.ttf'))

# Argument Parsing
parser = argparse.ArgumentParser(description='Generate random ASCII art pattern with multiple bishops.')
parser.add_argument('--min-bishops', type=int, default=2, help='Minimum number of bishops')
parser.add_argument('--max-bishops', type=int, default=10, help='Maximum number of bishops')
parser.add_argument('--different-alphabets', action='store_true', help='Use different alphabets for different bishops')
parser.add_argument('--num-outputs', type=int, default=1, help='Number of outputs to generate')
parser.add_argument('--rand-col', action='store_true', help='Use random background color from predefined palette')
parser.add_argument('--rand-pleasing-col', action='store_true', help='Use a random pleasing color')
parser.add_argument('--I', action='store_true', help='Interactive mode')
parser.add_argument('--sober', action='store_true', help='Generate a symmetrical pattern')
parser.add_argument('--landscape', action='store_true', help='Produce output in landscape format')
parser.add_argument('--label', action='store_true', help='Add auto-generated label to the output')
parser.add_argument('--ulabel', type=str, help='Specify a custom label for the output. For special characters (e.g., &, %%), enclose the label in quotes, like "Bishop&Bytes".')
parser.add_argument('--alphabet', type=int, default=0, help='Choose the alphabet')
parser.add_argument('--faces', action='store_true', help='Attract bishops towards the middle of the board, works best in conjunction with the --sober flag')
parser.add_argument('--settings', action='store_true', help='Save settings to a file')
parser.add_argument('--s', action='store_true', help='Load settings from a file')

args = parser.parse_args()

def get_user_choices():
    questions = [
        inquirer.Text('min_bishops', message="Minimum number of bishops [Default: 2]", default='2'),
        inquirer.Text('max_bishops', message="Maximum number of bishops [Default: 10]", default='10'),
        inquirer.List('different_alphabets', message='Use different alphabets for different bishops?', choices=['Yes', 'No'], default='No'),
        inquirer.Text('num_outputs', message="Number of outputs to generate [Default: 1]", default='1'),
        inquirer.List('rand_col', message='Use random background color from predefined palette?', choices=['Yes', 'No'], default='No'),
        inquirer.List('rand_pleasing_col', message='Use a random pleasing color?', choices=['Yes', 'No'], default='No'),        
        inquirer.List('sober', message='use a sober bishop?', choices=['Yes', 'No'], default='No'), 
        inquirer.List('faces', message='Attract bishops towards the middle of the board?', choices=['Yes', 'No'], default='No'),
        inquirer.List('landscape', message='Produce output in landscape format?', choices=['Yes', 'No'], default='No'), 
        inquirer.List('label', message='Add a label to the output?', choices=['No', 'Yes, random', 'Yes, custom'], default='No'),
    ]
    answers = inquirer.prompt(questions)

    if answers['label'] == 'Yes, custom':
        custom_label_question = [
            inquirer.Text('ulabel', message="Enter your custom label", validate=lambda _, x: x != ''),
        ]
        answers.update(inquirer.prompt(custom_label_question))
        
    if not answers['different_alphabets'] == 'Yes':
        alphabet_question = [
            inquirer.List('alphabet', message='Choose the alphabet', choices=ALPHABETS, default=ALPHABETS[0]),
        ]
        answers.update(inquirer.prompt(alphabet_question))

    return answers

# Predefined background colors in HEX
PREDEFINED_COLORS = ["dc6900", "eb8c00", "e0301e", "a32020", "602320"]

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
    " ٥٦٧٨٩ٹٻچ",
    " ₠₡₢₣₥₦₩₪₫",
    " ⋞⋟⋠⋩⋜⋝⋚⋛",
    " ⎛⎞⎠⎝⎡⎤⎨⎬⎫⎧",
    " ↑↗→↘↓↙←↖",
    " ░▒▓",
    " ◜◝◞◟◠◡",
    " ☣☠☢☤☩☫☬☹",
    " ▁▂▃▄▅▆▇█",
    " ○◔◑◕●",
    " 01",
    "01"
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

max_visits = len(ALPHABETS) - 1  # Maximum number of visits to a cell

def load_settings():
    with open('settings.json', 'r') as f:
        return json.load(f)
    
def save_settings(settings):
    with open('settings.json', 'w') as f:
        json.dump(settings, f, indent=4)
        
def generate_pleasing_color():
    hue = random.random()  # Generates a random number between 0 and 1
    saturation = 0.9  # Set saturation to 90%
    lightness = 0.5  # Set lightness to 50%

    # Convert HSL color to RGB
    r, g, b = [int(x * 255) for x in colorsys.hls_to_rgb(hue, lightness, saturation)]
    
    # Convert RGB color to hexadecimal
    hex_color = "{:02x}{:02x}{:02x}".format(r, g, b)
    
    return hex_color

def update_counter(filename, num_bishops, sober, random_bytes):
    counter_file = "counter.json"
    if os.path.exists(counter_file):
        with open(counter_file, "r") as f:
            data = json.load(f)
    else:
        data = {"patterns": []}

    pattern_number = len(data["patterns"]) + 1
    random_bytes_str = "".join(str(b) for b in random_bytes[:7])  # Only take the first 7 bytes
    pattern_name = f"bishops-{num_bishops}_sober-{sober}_bytes-{random_bytes_str}"
    data["patterns"].append({"name": f"{filename}_{pattern_name}", "number": pattern_number})

    with open(counter_file, "w") as f:
        json.dump(data, f, indent=4)

    return pattern_name, pattern_number

def from_bytes(input_bytes, num_bishops, sober=False, faces=False):
    room = [[0 for _ in range(RoomWidth)] for _ in range(RoomHeight)]
    bishop_tracker = [[0 for _ in range(RoomWidth)] for _ in range(RoomHeight)]  # New array to track bishops
    
    bishop_positions = [[random.randint(0, RoomHeight - 1), random.randint(0, RoomWidth - 1)] for _ in range(num_bishops)]
    if args.different_alphabets:
        bishop_alphabets = [random.choice(ALPHABETS) for _ in range(num_bishops)]
    else:
        bishop_alphabets = [ALPHABETS[args.alphabet] for _ in range(num_bishops)]  

    for byte in input_bytes:
        bits = format(byte, '08b')
        bitpairs = [bits[i:i+2] for i in range(0, 8, 2)]
        
        for i, pos in enumerate(bishop_positions):
            for bitpair in bitpairs:
                direction = list(DIRECTIONS.keys())[int(bitpair, 2) % 8]
                
                # Add bias if --faces flag is used
                if faces and random.random() < 0.2:  # 20% chance to apply bias
                    if pos[0] < RoomHeight / 2:  # Bishop is in the upper half of the board
                        if pos[1] < RoomWidth / 2:  # Bishop is in the left half of the board
                            if direction in ['N', 'W', 'NW']:
                                direction = random.choice(['S', 'E', 'SE'])  # Bias towards moving down and right
                        else:  # Bishop is in the right half of the board
                            if direction in ['N', 'E', 'NE']:
                                direction = random.choice(['S', 'W', 'SW'])  # Bias towards moving down and left
                    else:  # Bishop is in the lower half of the board
                        if pos[1] < RoomWidth / 2:  # Bishop is in the left half of the board
                            if direction in ['S', 'W', 'SW']:
                                direction = random.choice(['N', 'E', 'NE'])  # Bias towards moving up and right
                        else:  # Bishop is in the right half of the board
                            if direction in ['S', 'E', 'SE']:
                                direction = random.choice(['N', 'W', 'NW'])  # Bias towards moving up and left

                dY, dX = DIRECTIONS[direction]
                pos[0] += dY
                pos[1] += dX
                pos[0] = max(0, min(RoomHeight - 1, pos[0]))
                pos[1] = max(0, min(RoomWidth - 1, pos[1]))

                # Only increment the count if it's less than max_visits
                if room[pos[0]][pos[1]] < max_visits:
                    room[pos[0]][pos[1]] += 1
                bishop_tracker[pos[0]][pos[1]] = i  # Update tracker with the current bishop index

                # If the sober flag is used, mirror the bishop's movements
                if sober:
                    mirror_pos = [pos[0], RoomWidth - 1 - pos[1]]
                    if room[mirror_pos[0]][mirror_pos[1]] < max_visits:
                        room[mirror_pos[0]][mirror_pos[1]] += 1
                    bishop_tracker[mirror_pos[0]][mirror_pos[1]] = i
    
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

def write_to_file(room_string, banner_text=None):
    folder_name = "random_patterns"
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)

    i = 1
    while os.path.exists(f"{folder_name}/random_{i}.txt"):
        i += 1

    filename = f"{folder_name}/random_{i}"
    with open(f"{filename}.txt", "w") as f:
        f.write(room_string)
        if banner_text:  
            f.write("\n" + banner_text)
    
    return filename  

#def print_directly(output_string):
    # Prepare the string with escape sequences
    #formatted_output = "\033@" + output_string + "\n\n\033@"
    
    # Command to execute
    #command = f"echo -e '{formatted_output}' | lp -d LQ-350"
    
    # Execute the command using subprocess
    #subprocess.run(command, shell=True, check=True)
    
    
def hex_to_rgb(hex_code):
    hex_code = hex_code.lstrip("#")
    return tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))


def rgb_to_reportlab(r, g, b):
    """Converts an RGB color in range 0-255 to a ReportLab Color."""
    return colors.Color(r / 255.0, g / 255.0, b / 255.0)

# For background color (8, 4, 5, 1)
term_bg = rgb_to_reportlab(30, 30, 30)

# For foreground color (251, 251, 251, 1)
term_fg = rgb_to_reportlab(251, 251, 251)

# Parse background color
if args.rand_col:
    bg_color_hex = random.choice(PREDEFINED_COLORS)
else:
    bg_color_hex = "1E1E1E"  # The default color

bg_r, bg_g, bg_b = hex_to_rgb(bg_color_hex)
term_bg = rgb_to_reportlab(bg_r, bg_g, bg_b)

def write_to_pdf(room_string, filename_without_extension, banner_text):
    if args.landscape:
        custom_page_size = (820, 430)  # Width x Height in points for landscape
    else:
        custom_page_size = (515, 680)  # Width x Height in points for portrait

    c = canvas.Canvas(f"{filename_without_extension}.pdf", pagesize=custom_page_size)
    width, height = custom_page_size

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
    
    # Adjust the way text is drawn
    for line in lines:
        c.drawString(x, y, line)
        y -= line_height  # Move down one line

    # Add banner text at the bottom of the PDF
    if banner_text:
        c.setFont("UnifrakturMaguntia", 10)  # Adjust size as needed
        text_width = pdfmetrics.stringWidth(banner_text, "UnifrakturMaguntia", 10)
        text_x = (width - text_width) / 2 - 5  # Adjust position as needed
        text_y = 5  # Adjust position as needed

        c.drawString(text_x, text_y, banner_text)

    c.save()

if __name__ == "__main__":
    args = parser.parse_args()

    if args.s:
        user_choices = load_settings()
        args.min_bishops = int(user_choices['min_bishops'])
        args.max_bishops = int(user_choices['max_bishops'])
        args.different_alphabets = user_choices['different_alphabets'] == 'Yes'
        args.num_outputs = int(user_choices['num_outputs'])
        args.rand_col = user_choices['rand_col'] == 'Yes'
        args.rand_pleasing_col = user_choices['rand_pleasing_col'] == 'Yes'
        args.sober = user_choices['sober'] == 'Yes'
        args.faces = user_choices['faces'] == 'Yes'
        args.landscape = user_choices['landscape'] == 'Yes'
        args.alphabet = ALPHABETS.index(user_choices['alphabet']) if 'alphabet' in user_choices else 0
        args.label = user_choices['label'] in ['Yes, random', 'Yes, custom']
        args.ulabel = user_choices['ulabel'] if 'ulabel' in user_choices else None
    elif args.settings:
        user_choices = get_user_choices()
        save_settings(user_choices)
        print("settings saved. to run this code with your saved settings, use --s flag")
        args.min_bishops = int(user_choices['min_bishops'])
        args.max_bishops = int(user_choices['max_bishops'])
        args.different_alphabets = user_choices['different_alphabets'] == 'Yes'
        args.num_outputs = int(user_choices['num_outputs'])
        args.rand_col = user_choices['rand_col'] == 'Yes'
        args.rand_pleasing_col = user_choices['rand_pleasing_col'] == 'Yes'
        args.sober = user_choices['sober'] == 'Yes'
        args.faces = user_choices['faces'] == 'Yes'
        args.landscape = user_choices['landscape'] == 'Yes'
        args.alphabet = ALPHABETS.index(user_choices['alphabet']) if 'alphabet' in user_choices else 0
        args.label = user_choices['label'] in ['Yes, random', 'Yes, custom']
        args.ulabel = user_choices['ulabel'] if 'ulabel' in user_choices else None
    elif args.I:
        user_choices = get_user_choices()
        args.min_bishops = int(user_choices['min_bishops'])
        args.max_bishops = int(user_choices['max_bishops'])
        args.different_alphabets = user_choices['different_alphabets'] == 'Yes'
        args.num_outputs = int(user_choices['num_outputs'])
        args.rand_col = user_choices['rand_col'] == 'Yes'
        args.rand_pleasing_col = user_choices['rand_pleasing_col'] == 'Yes'
        args.sober = user_choices['sober'] == 'Yes'
        args.faces = user_choices['faces'] == 'Yes'        
        args.landscape = user_choices['landscape'] == 'Yes'
        args.alphabet = ALPHABETS.index(user_choices['alphabet']) if 'alphabet' in user_choices else 0
        args.label = user_choices['label'] in ['Yes, random', 'Yes, custom']
        args.ulabel = user_choices['ulabel'] if 'ulabel' in user_choices else None
    else:
        args.ulabel = args.ulabel if args.ulabel else None
        if args.ulabel:
            args.label = True

    if args.landscape:
        RoomWidth = 120  # Adjusted width for landscape
        RoomHeight = 40  # Adjusted height for landscape
    else:
        RoomWidth = 75   # Adjusted width for portrait
        RoomHeight = 65  # Adjusted height for portrait


    for i in range(args.num_outputs):
        if args.rand_col:
            bg_color_hex = random.choice(PREDEFINED_COLORS)
        elif args.rand_pleasing_col:
            bg_color_hex = generate_pleasing_color()
        else:
            bg_color_hex = "1E1E1E" 

        bg_r, bg_g, bg_b = hex_to_rgb(bg_color_hex)
        term_bg = rgb_to_reportlab(bg_r, bg_g, bg_b)

        num_bishops = random.randint(args.min_bishops, args.max_bishops)
        random_bytes = [random.randint(0, 255) for _ in range(200)]
        room, bishop_alphabets, bishop_tracker = from_bytes(random_bytes, num_bishops, args.sober, args.faces)
        room_string = room_to_string(room, bishop_alphabets, bishop_tracker)
        filename_without_extension = write_to_file(room_string)

        # Print directly
        #print_directly(room_string)
        
        # Update the counter file
        pattern_name, pattern_number = update_counter(filename_without_extension, num_bishops, args.sober, random_bytes)

        # Generate label based on user input or auto-generation
        if args.label:
            if args.ulabel:  # User has provided a custom label
                custom_label = args.ulabel
                banner_text = f"{custom_label} #{pattern_number}"
            else:  # User wants an auto-generated label
                banner_text = f"{pattern_name} #{pattern_number}"
        else:  # No label should be added
            banner_text = ""

        write_to_pdf(room_string, filename_without_extension, banner_text)
        #if i == 0:  # Only print the preview for the first pattern
        print("Preview")
        print(room_string)
        print(f"Generated pattern #{pattern_number}: {filename_without_extension}")
        print(f"Number of bishops: {num_bishops}")
        print(f"Sobriety status: {'Sober' if args.sober else 'Drunk'}")
        print(f"Input bytes (truncated): {random_bytes[:10]}...")      
