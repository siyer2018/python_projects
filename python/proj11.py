# DO NOT COPY AND PASTE FROM YOUR BROWSER. 
# YOU MUST DOWNLOAD THIS FILE.

class GoPiece(object):
    __color = 'black'
    '''The class GoPiece represents black or white pieces used in the game.'''
    def __init__(self,color = 'black'):
        '''This method will create a Gomoku piece which has an attribute 'color'
           which can either be 'black' or 'white'.
        '''
        if not color in ['black', 'white']:
            raise MyError('Wrong color.')
        self.__color = color
    
    def __str__(self):
        '''This method displays the black piece and white piece.'''
        return ' ● ' if self.__color == 'black' else ' ○ '
    
    def get_color(self):
        '''This method returns the color of the piece as a string 'black' or 
           'white'.
        '''
        return self.__color
            
class MyError(Exception):
    def __init__(self,value):
        self.__value = value
    def __str__(self):
        return self.__value

class Gomoku(object):
    '''The class Gomoku represents methods for setting up the game, displaying
       the board game, and playing the game.
    '''
    def __init__(self,board_size = 15,win_count = 5,current_player='black'):
        '''This method has 4 attributes: self, board_size, win_count, and
           current_player.
        '''
        if not isinstance(board_size, int):
            raise ValueError('board size must be a digit')
        self.__board_size = board_size

        if not isinstance(win_count, int):
            raise ValueError('win count must be a digit')
        self.__win_count = win_count

        if not current_player in ['black', 'white']:
            raise MyError('Wrong color.')
        self.__current_player = current_player

        self.__go_board = [ [ ' - ' for j in range(self.__board_size)] for i in range(self.__board_size)]  
            
    def assign_piece(self,piece,row,col):
        '''This method places the piece at the specified position on the game
           board.
        '''
        if row < 1 or row > self.__board_size or col < 1 or col > self.__board_size:
            raise MyError('Invalid position.')
        if self.__go_board[row - 1][col - 1] != ' - ':
            raise MyError('Position is occupied.')
        self.__go_board[row - 1][col - 1] = piece
            
    def get_current_player(self):
        '''This method returns the current player as a string 'black' or 
           'white'.
        '''
        return self.__current_player
    
    def switch_current_player(self):
        '''This method returns the 'other' player as a string.'''
        self.__current_player = 'white' if self.__current_player == 'black' else 'black'
        return self.__current_player
        
    def __str__(self):
        s = '\n'
        for i,row in enumerate(self.__go_board):
            s += "{:>3d}|".format(i+1)
            for item in row:
                s += str(item)
            s += "\n"
        line = "___"*self.__board_size
        s += "    " + line + "\n"
        s += "    "
        for i in range(1,self.__board_size+1):
            s += "{:>3d}".format(i)
        s += "\n"
        s += 'Current player: ' + ('●' if self.__current_player == 'black' else '○')
        return s
        
    def current_player_is_winner(self):
        '''This method returns True when current_player is a winner, otherwise 
           it will return False.
        '''
        current_player_row_count = 1
        current_player_col_count = 1
        current_player_color = ' ● ' if self.__current_player == 'black' else ' ○ '
        for row in range(self.__board_size):
            for col in range(self.__board_size):
                if str(self.__go_board[row][col]) == current_player_color and \
                row + 1 <= self.__board_size - 1 and str(self.__go_board[row + 1][col]) == current_player_color:
                    current_player_row_count += 1
                    if current_player_row_count == self.__win_count:
                        return True
                else:
                    current_player_row_count = 1

                if str(self.__go_board[col][row]) == current_player_color and \
                col + 1 <= self.__board_size - 1 and  str(self.__go_board[col + 1][row]) == current_player_color:
                    current_player_col_count += 1
                    if current_player_col_count == self.__win_count:
                        return True
                else:

                    current_player_col_count = 1
        return False
        
def main():

    board = Gomoku()
    print(board)
    play = input("Input a row then column separated by a comma (q to quit): ")
    while play.lower() != 'q':
        play_list = play.strip().split(',')
        try:
            try:
                if not len(play_list) == 2:
                    raise MyError("Incorrect input.")
                play_list[0] = int(play_list[0])
                play_list[1] = int(play_list[1])
            except ValueError:
                raise MyError("Incorrect input.")
            piece = GoPiece(board.get_current_player())
            
            board.assign_piece(piece, int(play_list[0]), int(play_list[1]))
            if board.current_player_is_winner():
               print(board)
               print("{} Wins!".format(board.get_current_player()))
               return
            board.switch_current_player()
        except MyError as error_message:
            print("{:s}\nTry again.".format(str(error_message)))
        
        print(board)
        play = input("Input a row then column separated by a comma (q to quit): ")

if __name__ == '__main__':
    main()
