__author__ = 'Al-Ramessi, 8658986'

import random

def create_map():
    size = 5
    game_map = [['.' for _ in range (size)] for _ in range (size)]
    return game_map

def place_element(game_map, element):
    size = len(game_map)

    free_positions = [
    (x,y) for y in range(size) 
     for x in range(size)
     if (x,y) != (0,0) and game_map[y][x] == '.']

    if not free_positions : return None

    x,y = random.choice(free_positions)

    if element == 'X' :
        game_map[y][x] = 'X'

    return (x,y)

def print_map(game_map):
    for row in (game_map):
        print(" ".join(row))

def move_player(position,direction,game_map,obstacles):
    x,y = position
    
    deltas = {
        'o' : (0, -1), # here we subtract on the y axis when moving up           0
        'u' : (0, 1),  # because the rows start from 0 to 4 and from up to down  1
        'l' : (-1, 0),                                                    #      2 ....
        'r' : (+1, 0)
    }

    delta_x, delta_y = deltas.get(direction, (0,0)) # gets the value for key in dictionary, or gives default value (0,0)

    new_x = x + delta_x
    new_y = y + delta_y

    #checks borders
    size = len(game_map)

    if not (0<= new_x < size and 0 <= new_y < size): #not including the 5 because indexing starts at 0
        return position # this means unvalid move
    
    #checks borders
    if game_map[new_y][new_x] == 'O':
        return position 
    
    #valid move
    return (new_x,new_y)





