# GenPasswd

[![PyPI](https://img.shields.io/pypi/v/genpasswd)](https://pypi.python.org/pypi/genpasswd)
[![PyPI - License](https://img.shields.io/pypi/l/genpasswd)](https://github.com/Gowthaman1401/GenPasswd/blob/main/LICENSE)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/genpasswd?color=red)](https://pypi.python.org/pypi/genpasswd)

To generate random and strong passwords.

## Installation

`pip install -U genpasswd`

## Usage

```
Usage : genpasswd [options]

Options:
  --version                                     show program's version number and exit
  -h,                 --help                    show this help message and exit
  -l LENGTH,          --length=LENGTH           To set Length to the password
  -r REPEAT,          --repeat                  To repeat the characters in the password
  -n IGNORE,          --no=IGNORE               To ignore unwanted characters to the password
  -o ONLY,            --only=ONLY               To create password only using wanted characters
  -i INCLUDE,         --include=INCLUDE         To include characters to the password
  -s SEPARATOR,       --separator=SEPARATOR     The separator character
  -c SEPARATORLENGTH, --seplen=SEPARATORLENGTH  The length of characters between separator
  --separation                                  To separate password characters using separator
```

###
To generate a random password and print it on the screen.
```
> genpasswd
kj(ot--4mJ1aeJ
```
###

To set the password length, Default password length is `8-16`.

```
> genpasswd -l 10
Q3m/vro|uR
```
###

Whether the characters in passwords repeat or not,
Default value of `repeat` is `False`.
```
> genpasswd -r
96Ndl;1D>jQu4Z2
```
###

You can include, ignore or using only `'alphabets'`, `'numbers'`, `'uppercase'`, `'lowercase'`, `symbols` and some `random characters` in generating password.
###

To ignore `numbers` in passwords. 

```
> genpasswd -n numbers
uyMXP‘$!ZSCYqzj
```
###
To ignore characters `a,b,c,d,e`
```
> genpasswd -n abcde
~}t"R‘jF'ksG8~E
```
###
To create a password only using `special characters`.

```
> genpasswd -o symbols -l 15
?)".=-_^[_‘~{.)
```
###
To include `a,b,c,d,e` characters in a password.
```
> genpasswd -o numbers -i abcde -l 15
78713d1e3d926a3
```
###
To separate characters in a password using separator.
```
> genpasswd -o numbers -i abcde -l 15 --separation
7871-3d1e-3d92-6a3
```
###
To separate characters in a password using separator `_` with `5` characters between each separator.
```
> genpasswd -o numbers -i abcde -l 15 -s _ -c 5 
78713_d1e3d_926a3
```
