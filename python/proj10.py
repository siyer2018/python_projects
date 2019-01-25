

import NMM #This is necessary for the project


BANNER = """
    __        _____ _   _ _   _ _____ ____  _ _ _ 
    \ \      / /_ _| \ | | \ | | ____|  _ \| | | |
     \ \ /\ / / | ||  \| |  \| |  _| | |_) | | | |
      \ V  V /  | || |\  | |\  | |___|  _ <|_|_|_|
       \_/\_/  |___|_| \_|_| \_|_____|_| \_(_|_|_)

"""


RULES = """
  _   _ _              __  __            _       __  __                 _     
 | \ | (_)_ __   ___  |  \/  | ___ _ __ ( )___  |  \/  | ___  _ __ _ __(_)___ 
 |  \| | | '_ \ / _ \ | |\/| |/ _ \ '_ \|// __| | |\/| |/ _ \| '__| '__| / __|
 | |\  | | | | |  __/ | |  | |  __/ | | | \__ \ | |  | | (_) | |  | |  | \__ \
 |_| \_|_|_| |_|\___| |_|  |_|\___|_| |_| |___/ |_|  |_|\___/|_|  |_|  |_|___/
                                                                                        
    The game is played on a grid where each intersection is a "point" and
    three points in a row is called a "mill". Each player has 9 pieces and
    in Phase 1 the players take turns placing their pieces on the board to 
    make mills. When a mill (or mills) is made one opponent's piece can be 
    removed from play. In Phase 2 play continues by moving pieces to 
    adjacent points. 
    
    The game is ends when a player (the loser) has less than three 
    pieces on the board.

"""


MENU = """

    Game commands (first character is a letter, second is a digit):
    
    xx        Place piece at point xx (only valid during Phase 1 of game)
    xx yy     Move piece from point xx to point yy (only valid during Phase 2)
    R         Restart the game
    H         Display this menu of commands
    Q         Quit the game
    
"""
        
def count_mills(board, player):
    """The function count_mills counts how many of the mills are held by player
       and returns the count.
    """
    counter = 0
    player_mill = player * 3
    for mill in board.MILLS:
        points_mill = ''.join([board.points[point] for point in mill])
        if points_mill == player_mill:
            counter += 1
    return counter
            
def place_piece_and_remove_opponents(board, player, destination):
    """The function place_piece_and_remove_opponents places a piece for the
       player and if mill is created, it removes an opponent's piece by calling
       the function remove_piece.
    """
    player_mills = count_mills(board, player)
    if not destination in board.points:

        raise RuntimeError("Invalid command: Not a valid point")

    if board.points[destination] != " ":

        raise RuntimeError("Invalid command: Destination point already taken")

    board.assign_piece(player, destination)
    new_player_mills = count_mills(board, player)
   
    if new_player_mills > player_mills:
        print("A mill was formed!")
        print()
        print(board)
        remove_piece(board, get_other_player(player))

def move_piece(board, player, origin, destination):
    """The function move_piece is used to move a piece.
    """
    if board.points[origin] != player:

        raise RuntimeError("Invalid command: Origin point does not belong to player")

    origin_adjacent_points = board.ADJACENCY[origin]
    if not destination in origin_adjacent_points:

        raise RuntimeError("Invalid command: Not a valid point")
    board.clear_place(origin)
    place_piece_and_remove_opponents(board, player, destination)
    
    
def points_not_in_mills(board, player):
    """The function points_not_in_mills finds all points that belong to player
       that aren't in mills and returns them.
    """
    player_points = placed(board, player)
    player_points_mill = set()
    player_mill = player * 3

    for mill in board.MILLS:
        points_mill = [board.points[point] for point in mill]
        points_mill_str = ''.join(points_mill)
        if points_mill_str == player_mill:
            player_points_mill.update(mill)

    result = player_points.difference(player_points_mill)
    
    return player_points if len(result) == 0 else result

def placed(board,player):
    """The function placed returns points where the player's pieces have been 
       placed.
    """
    player_points = set([point for point in board.points if board.points[point] == player])

    return player_points

    
def remove_piece(board, player):
    """The function remove_piece removes a piece belonging to player from 
       board.
    """
    while True:
        command = input("Remove a piece at :> ").strip().lower()
        try:
            if not command in board.points:
                raise RuntimeError("Invalid command: Not a valid point")

            if board.points[command] != player:

                raise RuntimeError("Invalid command: Point does not belong to player")
    
            play_points_not_in_mills = points_not_in_mills(board, player)
            if not command in play_points_not_in_mills:
                raise RuntimeError("Invalid command: Point is in a mill")
            board.clear_place(command)
            return

        #Any RuntimeError you raise inside this try lands here
        except RuntimeError as error_message:
            print("{:s}\nTry again.".format(str(error_message)))

    
           
def is_winner(board, player):
    """The function is_winner decides if a game is won."""
    player_points = placed(board, get_other_player(player))

    return len(player_points) == 2
   
def get_other_player(player):
    """The function get_other_player gets the other player and returns it."""
    return "X" if player == "O" else "O"
    
def main():
    #Loop so that we can start over on reset
    while True:
        #Setup stuff.
        print(RULES)
        print(MENU)
        board = NMM.Board()
        print(board)
        player = "X"
        placed_count = 0 # total of pieces placed by "X" or "O", includes pieces placed and then removed by opponent
        
        # PHASE 1
        print(player + "'s turn!")
        #placed = 0
        command = input("Place a piece at :> ").strip().lower()
        print()
        #Until someone quits or we place all 18 pieces...
        while command != 'q' and placed_count != 18:
            try:
                place_piece_and_remove_opponents(board, player, command)
                player = get_other_player(player)
                placed_count +=1
            #Any RuntimeError you raise inside this try lands here
            except RuntimeError as error_message:
                print("{:s}\nTry again.".format(str(error_message)))
            #Prompt again
            print(board)
            print(player + "'s turn!")
            if placed_count < 18:
                command = input("Place a piece at :> ").strip().lower()
            else:
                print("**** Begin Phase 2: Move pieces by specifying two points")
                command = input("Move a piece (source,destination) :> ").strip().lower()
                break
            print()
            if command == 'r':
                break
            if command == 'h':
                print()
                print(MENU)
                command = input("Place a piece at :> ").strip().lower()

        
        #Go back to top if reset
        if command == 'r':
            continue
        # PHASE 2 of game
        while command != 'q':
            # commands should have two points
            command = command.split()
            try:
                if len(command) != 2:

                    raise RuntimeError("Invalid number of points")

                move_piece(board, player, command[0], command[1])
                if is_winner(board, player):
                    print(BANNER)
                    return
                player = get_other_player(player)
                
            #Any RuntimeError you raise inside this try lands here
            except RuntimeError as error_message:
                print("{:s}\nTry again.".format(str(error_message)))         
            #Display and reprompt
            print(board)
            #display_board(board)
            print(player + "'s turn!")
            command = input("Move a piece (source,destination) :> ").strip().lower()
            print()
            
        #If we ever quit we need to return
        if command == 'q':
            return

            
if __name__ == "__main__":
    main()