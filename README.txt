Date: November 2019
License: GNU GPL v3

Usage:
$ game.py

What's interesting is that I fetch a pacman-like maze from
shaunlebron's website and parse it to a graph, so that the maze
is different each game!

Currently there's only one ghost (red one), but new ones with
custom ai might be added very easily

Note: it's pretty god damn hard, because the ghost can turn on
a straight way; it's not limited to only turn on crossroads

Dependencies: pygame, selenium, webdriver_manager, Pillow

Screenshots:
https://imgur.com/a/Iecee7t

Credits:
https://shaunlebron.github.io/
for creating an impressive pacman-like maze generator in js
I use it in this repo
