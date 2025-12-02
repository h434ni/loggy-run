# loggy-run

this is a tool to capture the terminal outputs of a command and save them on persistent storage while also showing the terminal output.
it creates a ./logs folder at the current directory and makes a new txt file for each run.

- the log files get updated in real time
- all output is captured without modifications including errors
- Auto-detects Python Virtual Environments (venv).
- Forces UTF-8 encoding to prevent Windows Unicode crashes (Charmap errors).
- Has editable default command so that it can run even with no args
- Works with any languages and any command

## requirements

python installed

## installation

just download the run.py file into the current working directory

## usage

`python3 run.py [any type of command with args]`

### examples

- ```python run.py python main.py```
- ```python run.py npm run dev```
- ```python run.py```

### contribution

this is a  small project yet nowhere to be found. i get the result i wanted with the current state but if there was any issues or suggestions, feel welcomed to contribute.