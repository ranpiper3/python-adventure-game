#!/usr/bin/env python3

"""The main game script."""

import os
import shelve
import sys
if os.name is not "nt":
    import readline

assert sys.version_info >= (3, 6), "You must use at least Python 3.6."

# Change directory to directory that includes play.py
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from src import parser
from src import locations
from src import classes


def main():
    sf_exists = False
    for i in os.listdir():
        if i.startswith('save'):
            sf_exists = True
            break
    if sf_exists:
        save = shelve.open('save')
        player = save['player']
        Locations = save['locations']
        save.close()
        player.locations = Locations
        for i in Locations:
            player.visited_places[i] = False
        player.location.give_info(True, player.has_light)
    else:
        player = classes.Player(classes.location_storage, 
                                locations.start_location())
    previous_noun = ''
    turns = 0
    dark_turn = 0
    
    # Main game loop
    while True:
        try:
            command = parser.parse_command(input('> '))
            if command is not None:
                action = command[0]
                if len(command) >= 2:
                    noun = command[1]
                else:
                    noun = ''
                if action is None and noun != '':
                    action = 'go'
                if previous_noun != '' and noun == 'it':
                    noun = previous_noun
                # Where game executes result.
                # Player stuff happens here
                # Ex: getattr(player, "go")(action, noun) -> player.go(action, noun)
                try:
                    result = getattr(player, action)(action, noun)
                except AttributeError:
                    print('This cannot be done.')
                # Add 1 to player moves if function returns True
                if result:
                    player.moves += 1

                if noun != '':
                    previous_noun = noun
                else:
                    previous_noun = ''
                if player.location.dark and not player.has_light:
                    if dark_turn < turns:
                        print('A grue magically appeared. However, since '
                              'this isn\'t Zork, the grue didn\'t eat you;'
                              ' it just killed you instead. So that\'s alr'
                              'ight.')
                        player.die()
                    else:
                        dark_turn = turns
                turns += 1
                if not player.location.dark or player.has_light:
                    dark_turn = turns
        except KeyboardInterrupt:
            player.quit('', '')

if __name__ == '__main__':
    main()
