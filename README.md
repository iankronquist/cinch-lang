Cinch
=====
[![Build Status](https://travis-ci.org/iankronquist/cinch-lang.svg)](https://travis-ci.org/iankronquist/cinch-lang)

A stupid-simple language.
In this project I have attempted a coding style which is explicit,
straightforward and easily understandable to any programmer at the expense of
being properly idiomatic in python.

Hacking
-------

Set up for the python implementation is simple. Optionally create and activate
a virtualenv and then just run:
```
$ pip install -r requirements.txt
```

When the python implementation is ready, just run:
```
$ ./cinch/cinch [interpret|dump|vm|compile] file.cinch
```

To run tests with coverage:
```
$ nosetests ./cinch/tests/ --with-coverage --cover-html-dir coverage --cover-html --cover-package=cinch
```


Features
--------

All tokens are separated by whitespace to make tokenizing a breeze.

```javascript

# comments !

# while loops
while ( expression ) {
	statement_list
}

# if statements
if ( expression ) {
	statement_list
}

# function definitions
function identifier ( identifier_list ) {

}

# function calls
identifier ( identifier_list )

# expressions
identifier operator expression
```
