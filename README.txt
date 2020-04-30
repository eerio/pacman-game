Date: November 2019
License: GNU GPL v3

To fetch a maze you're gonna need a chrome webdriver
Just install python's webdriver_manager module and it
should do the trick; this code uses this lib, so you'd
have to change a line or two at the beginning of parse_maze.py
if you can't use it

Currently there's only one ghost (red one), but new ones with
custom ai might be added very easily

Dependencies: pygame, selenium, webdriver_manager, Pillow

Credits:
https://shaunlebron.github.io/
for creating an impressive pacman-like maze generator in js
I use it in this repo
