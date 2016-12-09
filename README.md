# Lake Forest College CSCI 489 Mini Lang Interpreter

## Completed phases: `1` `2` `3` `4` `FINISHED`

### This program is able to execute all requirements put forth for the mini-lang. All grammars provided have been implemented.

## How to execute:

### Simplest way to execute the program is by running it in the top level directory of the project, it will automatically look for python3 if you have it installed:
`src/interpreter.py file_name`

## Parts of the program:

### Interpreter `src/interpreter.py`

##### Purpose: Ties all parts of the mini-lang execution process into a single program which you can run to handle the source code. It will call the scanner, and then parse the scanned program to the parser which will then return a postfix list. This postfix list is then executed by the interpreter (this file).
---

### Parser `src/parser/parser.py`

##### Purpose: Parser the code stream output from the scanner and confirms that it complies with the grammar laid out for the language (can be found in grammar.ebnf or grammar.bnf). Additionally will eventually write the byte stream into reverse polish which will be executable.
----

### Scanner `src/scanner/scanner.py`

##### Purpose: Scans the 489 lang source code into a code stream based on the `src/scanner/grammar.py` file. Very few errors are thrown at this stage since the scanner is 'dumb' per-se. It simply maps valid tokens to codes, recognizes when a variable is being declared, and recognizes constants.
----

* NOTE: file_name is relative to your current working directory, and the above
snippet assumes that you are currently in the csci489 folder. You can run programs out side of this folder by providing their absolute or relative path.

* NOTE 2: Grammar and vocabulary can be found in src/scanner/grammar.py, this is useful to figure out what the output of a program means.

* NOTE 3: The two sample programs showing off the language's features have been provided in the programs folder and can be executed with the commands:

* NOTE 4: The language's BNF and Extended BNF grammar sheets can be found within the grammar folder.

`src/interpreter.py programs/fibonacci.489`

AND

`src/interpreter.py programs/collatz.489`
