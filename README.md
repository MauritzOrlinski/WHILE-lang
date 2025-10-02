# A very smalls WHILE-Interpreter

This small project is my attempt at writing a compact and small interpreter for the programming language WHILE
It lead me to an overuse of regex and a probably bug-prone WHILE-Interpreter. Please don't orientate your own interpreters on that mess I created. Take a look at some of my other projects for a clean approach to building languages.

## WHILE

The WHILE programming language is Turing complete programming language.
As there is no typical specification, I used this grammar:

```
P ::= P ; P
  | X = N
  | X = X OP X
  | while X != 0 do P end
  | if X == 0 then P else P end
  | >X<
```

`X` represents variable names and `N` represents integer string representations.
The `>X<` lets you print out the value of the integer to the Terminal.
This grammar is quite easy to work with, as you can just split it up on the
semicolons and then pattern match on the structure of the text.
Therefore I wanted to interpret it without major lexical and syntactical analysis.

## Examples

I wrote a few example programs in WHILE. If you want to add a example program, feel free to do so!

## Contributing

You are welcome to contribute.
You can do so by writing Issues, or adding features.
For code changes just fork the Project and set up a PR with the changes.
