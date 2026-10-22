<H1>Welcome to Joe's REPL calculator-o-matic 5000!</H1>

## Intro
This is a basic Python calculator created for my IS601 Python course.  

This calculator can do simple math (Addition, Subtraction, Multiplication, Division) along with some more advanced functions like Power, Root, Percent, Modulus, Absolute Difference and Integer Divide.  It features a history of calculations, and has an undo/redo function for those with a fear of commitment.  When you run the calculator there is a 'help' option that explains all of the features and capabilities to the user.

This calculator uses colors (red for errors, green for answers, etc.), but that can be disabled at startup.


## Installation
Requires python 3.10 or newer. Developed and tested on Python 3.14
To check your version of Python:
python3 --version


Navigate to your project folder:
cd <i>your_project_folder</i>


Clone this repository:
git clone git@github.com:jstrong8026/assignment6-7_midterm.git


Start a virtual environment:
python3 -m venv venv
source venv/bin/activate # Mac/Linux
venv\Scripts\activate.bat # Windows


Install required packages:
pip install -r requirements.txt


Start the calculator:
python3 main.py

Start the calculator with colors disabled:
NO_COLOR=1 python3 main.py # Mac/Linux
set NO_COLOR=1 python main.py #Windows


## Configuration
Settings can be found in a '.env' file in the project root.  Format: one 'NAME=value' per line, with no quotes and no spaces around the '=' character. Anything not specifically mentioned will use the default. Invalid values will cause the program to stop at startup with an appropriate warning message.

Variable | Default | Meaning
'CALCULATOR_LOG_DIR' | 'logs' | specify the folder where logs are stored
'CALCULATOR_LOG_FILE' | 'calculator.log' | name of the log file
`CALCULATOR_HISTORY_DIR` | `history` | specify the folder where the history is stored
`CALCULATOR_HISTORY_FILE` | `calculator_history.csv` | name of the history file
`CALCULATOR_MAX_HISTORY_SIZE` | `100` | Maximum entries in the history. When the limit is reached the oldest file is overwritten.
`CALCULATOR_AUTO_SAVE` | `true` | `true` or `false`: save history automatically
`CALCULATOR_PRECISION` | `6` | Decimal places kept in results
`CALCULATOR_MAX_INPUT_VALUE` | `1000000` | Largest number allowed as input (positive or negative) 
`CALCULATOR_DEFAULT_ENCODING` | `utf-8` | Encoding for the log and history files

Set `NO_COLOR=1` in your environment to turn off colored output.


## How to use

Start the calculator: 
python3 main.py

You will be greeted with a prompt asking for your calculation command (Add, Subtract, Multiply, etc.). After you enter it will ask for your two numbers and then deliver the results. 
At any time you can type help to get to the help screen, cancel to stop your current calculation, or exit to quit the calculator program altogether. 


## Valid commands

| Command | Result |
|---|---|
| `add` | a + b |
| `subtract` | a − b |
| `multiply` | a × b |
| `divide` | a ÷ b |
| `power` | a raised to the power b |
| `root` | the b-th root of a |
| `modulus` | remainder of a ÷ b |
| `int_divide` | a ÷ b with the fractional part dropped |
| `percent` | (a ÷ b) × 100 |
| `abs_diff` | the distance between a and b, never negative |

### Other commands

| Command | Action |
|---|---|
| `history` | Show the calculation history |
| `clear` | Clear the history (undo can bring it back) |
| `undo` / `redo` | Step backward or forward through changes |
| `save` / `load` | Write the history to, or read it from, the CSV file |
| `help` | Show all commands |
| `exit` | Quit |

If you want to be cheeky and try commands I haven't set you may get a few snarky responses 


## Testing
Make sure you've installed the requirements.txt file so Pytest will work!

Pytest                                          #runs all tests
pytest --cov=app --cov-report=term-missing      #runs all tests and generates a coverage report, which should show 100% because that's how I roll.

Name                        Stmts   Miss  Cover
-----------------------------------------------
app/__init__.py                 0      0   100%
app/calculation.py             25      0   100%
app/calculator.py              94      0   100%
app/calculator_config.py       72      0   100%
app/calculator_memento.py       3      0   100%
app/calculator_repl.py        112      0   100%
app/colors.py                  14      0   100%
app/exceptions.py               8      0   100%
app/helper_text.py             16      0   100%
app/history.py                 60      0   100%
app/input_validation.py        13      0   100%
app/logger.py                  24      0   100%
app/operations.py              91      0   100%
-----------------------------------------------
TOTAL                         532      0   100%
Required test coverage of 90% reached. Total coverage: 100.00%
======================================= 226 passed in 0.49s ========================================


Thank you for reading and I hope you enjoy the calculator!