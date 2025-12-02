# loggy-run
this is a tool to capture the terminal outputs of a command and save them on persistent storage while also showing the terminal output.
it creates a ./logs folder at the current directory and makes a new txt file for each run. the files get updated in real time
- all output is captured without modifications including errors
- uses utf9 by default in order to prevent the non utf8 error
- has editable default command so that it can run even with no args
- works with any languages and any command

## requirements
python installed

## installation
just download the run.py file
## usage
`python3 run.py [any type of command with args]`
### examples
- ```python run.py python main.py```
- ```python run.py npm run dev```
- ```python run.py```

