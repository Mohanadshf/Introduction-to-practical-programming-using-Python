__author__ = 'Al-Ramessi, 8658986'

"""
Treasure Hunter Game:


This program implements a simple console-based treasure hunt game on a 5x5 grid.
The player starts at the top-left corner and has 10 moves to find a randomly
placed treasure. Several hidden obstacles are also placed on the map. These
obstacles remain invisible until the player steps on one—when this happens, the
obstacle becomes visible and blocks future movement.

The player moves using the keys:
    'o' = up, 'u' = down, 'l' = left, 'r' = right, 'q' = quit

The game ends when:
    - the player finds the treasure,
    - the player runs out of moves,
    - or the player quits manually.

The map updates after every move, showing the player's position and any revealed
obstacles. The goal is to navigate efficiently and reach the treasure in time.
"""

from game_util import (
    create_map,
    place_element,
    print_map,
    move_player
)

def main():
    while True:
        try:
            num_obstacles = int(input("Number of Obstacles: "))
            if not (0 < num_obstacles <=10): #this is optional i chose 10 obstacles as the limit
                print("Enter a positive integer between 0 and 10.")
                continue
            break
        except ValueError:
            print("Please enter a valid number.")

    game_map = create_map()

    player_pos = (0,0)
    game_map [player_pos[1]][player_pos[0]] = 'P' # the 1 is the y position and 0 is x

    treasure_pos = place_element(game_map , 'X')

    obstacles = [] 
    for _ in range (num_obstacles):
        pos = place_element(game_map , 'O')
        obstacles.append(pos) #sets the position in the list
        game_map[pos[1]][pos[0]] = "." #the hide it directly


    moves = 10
    print("\n Game Started! Press 'o'=oben , 'u'=unten, 'r'=rechts, 'l'=links, 'q'= quit\n ")

    while moves > 0: #main game loop
        print_map(game_map)
        print(f"Moves left: {moves}")
        direction = input("Your move: ").strip().lower()
        if direction == "q":
            print("End Game")
            return
        new_pos = move_player(player_pos, direction, game_map, obstacles)

        # do nothing if position is the same position 
        if new_pos == player_pos:
            print("Unvalid Move!")
            continue   

        # show obstacle if walked into one
        if new_pos in obstacles:
            ox, oy = new_pos
            game_map[oy][ox] = "O"
            print("You bumped into an obstacle!")
            continue  

        #valid move
        old_x, old_y = player_pos
        game_map[old_y][old_x] = "."
        player_pos = new_pos
        px, py = player_pos
        game_map[py][px] = "P"

        moves -= 1
        if player_pos == treasure_pos:
            print_map(game_map)
            print("\n🎉 Congrats you found the Treasure! 🎉")
            return

    else:
        print("\nGame Over. No more Moves")
        print(f"The Treasure was at {treasure_pos}.")

if __name__ == "__main__":
    main()

