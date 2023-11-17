![Banner](banner.png)

# Random ASCII Art Pattern Generator

## Description

This Python script generates random ASCII art patterns using multiple bishops with various customization options. It produces both text and PDF outputs with the ASCII patterns. The core algorithm of this project is based on the "drunken-bishop" algorithm for visualizing SSH key fingerprints in OpenSSH. 

While this project was inspired by and includes modified code from Manfred Touron's implementation of the "drunken-bishop" algorithm, the original concept of the algorithm is attributed to Alexander von Gernler.

## Features

- Customizable number of bishops
- Optional use of different alphabets for different bishops
- Output in `.txt` and `.pdf` formats

## About the Drunken Bishop Algorithm

The "drunken-bishop" algorithm, initially devised for visualizing SSH key fingerprints in OpenSSH, represents a sophisticated approach to rendering complex data into an accessible, visual format. This algorithm emerged not merely as a whimsical method, but as a robust means to depict the inherent randomness and uniqueness of SSH keys.

In this context, the Random ASCII Art Pattern Generator repurposes the "drunken-bishop" algorithm.
Here, the algorithm is no longer a tool for security visualization, but an instrument for generating distinctive ASCII patterns. The core principle of the algorithm is its stochastic movement, reminiscent of a bishop's diagonal strides in chess. This movement, dictated by the input data, ensures that each execution yields a unique, non-repetitive pattern.

The algorithm's elegance is in its fusion of simplicity and complexity, order and chaos. It demonstrates how algorithmic processes can transcend their original utilitarian purposes to inspire creative expression.

## Cloning the Repository

Before setting up the virtual environment, you first need to clone the repository to your local machine. Here's how to do it:

1. **Open Terminal or Command Prompt**: Navigate to the directory where you want to clone the repository.

2. **Clone the Repository**: Use the following command to clone the repository:

   ```bash
   git clone https://github.com/roadmaus/drunken_bishop.git
   ```

   This command will create a copy of the `drunken_bishop` repository in your current directory.

3. **Navigate to the Repository Directory**: After cloning, move into the repository directory:

   ```bash
   cd drunken_bishop
   ```

With the repository successfully cloned, you're ready to set up the virtual environment as described in the next section.


## Installation with Virtual Environment

To ensure a clean and isolated environment for running the script, it's recommended to use a virtual environment. Here's how you can set it up:

1. **Create a Virtual Environment:**

   Depending on your operating system, the command to create a virtual environment might differ slightly:

   - On **macOS and Linux**:

     ```bash
     python3 -m venv venv
     ```

     This command creates a new virtual environment named `venv` in your current directory using Python 3.

   - On **Windows**:

     ```bash
     python -m venv venv
     ```

     If you have both Python 2 and Python 3 installed, replace `python` with `python3` to ensure that Python 3 is used.


2. **Activate the Virtual Environment:**
   
   - On Windows:
     
     ```bash
     .\venv\Scripts\activate
     ```
   
   - On macOS and Linux:
     
     ```bash
     source venv/bin/activate
     ```
     
     This step activates the virtual environment. You'll notice `(venv)` appears before your command prompt when it's active.

3. **Install Dependencies:**
   While the virtual environment is active, install the required packages:
   
   ```bash
   pip install -r requirements.txt
   ```
   
   This ensures all dependencies are installed within the `venv` and not globally.

4. **Running the Script:**
   You can now run the script as mentioned in the Usage section.

5. **Deactivating the Virtual Environment:**
   Once you're done, you can deactivate the virtual environment by typing:
   
   ```bash
   deactivate
   ```

## Usage

### Basic Usage

To run the script with default settings:

```bash
python drunken_bishop.py
```

## Example output

#### drunken:

![Example_drunk](example.png)

#### sober:

![Example_sober](example_sober.png)

#### text output:

[Click here to view the example](https://raw.githubusercontent.com/roadmaus/drunken_bishop/main/examples/random_112.txt)


### Advanced Usage

To customize the number of bishops, different alphabets, and other settings:

```bash
python drunken_bishop.py --min-bishops 4 --max-bishops 20 --different-alphabets --num-outputs 12 --rand-col --sober --landscape 
```

### Interactive Mode and Settings

#### Interactive Mode

To use the program interactively, enabling easy customization of various settings like the number of bishops, alphabets, and color schemes, use the `--I` flag:

```bash
python drunken_bishop.py --I
```

This initiates an interactive session with a series of questions, allowing you to tailor the ASCII art generation according to your preferences. Options include:

- Minimum and maximum number of bishops
- Choice of using different alphabets for different bishops
- Output aesthetics like color schemes and format

#### Settings File

The program supports saving and loading settings from a file for consistent usage across sessions. 

- **Save Settings**: Use the `--settings` flag to save your current settings to a file.
  
  ```bash
  python drunken_bishop.py --settings
  ```

- **Load Settings**: Use the `--s` flag to load settings from an existing file.
  
  ```bash
  python drunken_bishop.py --s
  ```

This feature is particularly useful for maintaining consistent preferences and quickly reproducing favorite configurations.

### Help Menu

To view all the possible uses and flags:

```bash
python drunken_bishop.py -h
```

## Output

The script generates a text file and a PDF file in the `random_patterns` directory.

## Contributing

Feel free to fork the repository and submit pull requests. For any bugs or feature requests, please open an issue.

## License

This project incorporates elements of Manfred Touron's "drunken-bishop" algorithm (https://github.com/moul/drunken-bishop). This work is licensed under the MIT License. See the LICENSE file for more details.
