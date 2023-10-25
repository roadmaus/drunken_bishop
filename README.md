
# Random ASCII Art Pattern Generator

## Description

This Python script generates random ASCII art patterns using multiple bishops with various customization options. It produces both text and PDF outputs with the ASCII patterns.

## Features

- Customizable number of bishops
- Optional use of different alphabets for different bishops
- Output in `.txt` and `.pdf` formats

## Dependencies

- `os`
- `random`
- `argparse`
- `unicodedata`
- `PIL`
- `pandas`
- `reportlab`

You can install the required third-party packages using pip:

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

To run the script with default settings:

```bash
python script_name.py
```

### Advanced Usage

To customize the number of bishops, different alphabets, and other settings:

```bash
python script_name.py --min-bishops 4 --max-bishops 20 --different-alphabets
```

### Help Menu

To view all the possible uses and flags:

```bash
python script_name.py -h
```

## Output

The script generates a text file and a PDF file in the `random_patterns` directory.

## Contributing

Feel free to fork the repository and submit pull requests. For any bugs or feature requests, please open an issue.

## License

This project is open-source and available under the MIT License.
