# Import kivy modules
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen

# Define the symbols for the players
X = "X"
O = "O"
EMPTY = " "

# Define the winning combinations
WINNING_COMBINATIONS = [
 [0, 1, 2], # top row
 [3, 4, 5], # middle row
 [6, 7, 8], # bottom row
 [0, 3, 6], # left column
 [1, 4, 7], # middle column
 [2, 5, 8], # right column
 [0, 4, 8], # diagonal from top left to bottom right
 [2, 4, 6] # diagonal from top right to bottom left
]

# Define a function to check if the board is full
def is_board_full(board):
    return EMPTY not in board

# Define a function to check if a player has won the game
def has_won(board, player):
    for combo in WINNING_COMBINATIONS:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] == player:
            return True
    return False

# Define a function to switch the player's turn
def switch_player(player):
    return O if player == X else X

# Define a class for the game screen
class GameScreen(Screen):

    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        self.board = [EMPTY] * 9 # initialize the board with empty spaces
        self.player = X # initialize the first player to X
        self.winner = None # initialize the winner to None

        # Create a grid layout for the board
        self.layout = GridLayout(cols=3)

        # Create buttons for each cell of the board and add them to the layout
        self.buttons = []
        for i in range(9):
            button = Button(text=EMPTY, font_size=50)
            button.bind(on_press=self.on_button_press) # bind the button press event to a function
            self.layout.add_widget(button)
            self.buttons.append(button)
                            
        # Add the layout to the screen
        self.add_widget(self.layout)


    def on_button_press(self, button):

        # Get the index of the button that was pressed
        index = self.buttons.index(button)

        # If the button is not empty or the game is over, do nothing
        if self.board[index] != EMPTY or self.winner is not None:
            return
        # Update the board and the button text with the current player's symbol
        self.board[index] = self.player
        button.text = self.player

        # Check if the current player has won the game or if the board is full
        if has_won(self.board, self.player):
            self.winner = self.player # set the winner to the current player
            self.show_message(f"{self.player} has won!") # show a message with the winner's name
        elif is_board_full(self.board):
            self.winner = "Tie" # set the winner to Tie
            self.show_message("It's a tie!") # show a message with a tie

        # Switch to the next player's turn
        else:
            self.player = switch_player(self.player)


    def show_message(self, message):

        # Remove the layout from the screen and create a new one with a label and a button
        self.clear_widgets()
        self.layout = GridLayout(cols=1)
        self.label = Label(text=message, font_size=50)
        self.button = Button(text="Play again", font_size=50)
        self.button.bind(on_press=self.on_play_again) # bind the button press event to a function

        # Add the label and the button to the layout and add it to the screen
        self.layout.add_widget(self.label)
        self.layout.add_widget(self.button)
        self.add_widget(self.layout)


    def on_play_again(self, button):
        # Reset the board, the player and the winner attributes and restart the game screen
        self.board = [EMPTY] * 9
        self.player = X 
        self.winner = None
        self.restart()


    def restart(self):
        # Remove the current layout from the screen and create a new one with buttons for each cell of the board 
        self.clear_widgets()
        self.layout = GridLayout(cols=3)
 
        # Update each button text with the board value and add them to the layout
        for i in range(9):
            self.buttons[i].text = self.board[i]
            self.layout.add_widget(self.buttons[i])

        # Add the layout to the screen
        self.add_widget(self.layout)


# Define a class for the start screen
class StartScreen(Screen):
    def __init__(self, **kwargs):
        super(StartScreen, self).__init__(**kwargs)

        # Create a grid layout with a label and a button
        self.layout = GridLayout(cols=1)
        self.label = Label(text="Welcome to Tic Tac Toe!", font_size=50)
        self.button = Button(text="Start the game", font_size=50)
        self.button.bind(on_press=self.on_start) # bind the button press event to a function

        # Add the label and the button to the layout and add it to the screen
        self.layout.add_widget(self.label)
        self.layout.add_widget(self.button)
        self.add_widget(self.layout)

    def on_start(self, button):
        # Switch to the game screen
        self.manager.current = "game"


# Define a class for the main app
class TicTacToeApp(App):
    def build(self):

        # Create a screen manager and add the start screen and the game screen to it
        self.screen_manager = ScreenManager()
        self.start_screen = StartScreen(name="start")
        self.game_screen = GameScreen(name="game")
        self.screen_manager.add_widget(self.start_screen)
        self.screen_manager.add_widget(self.game_screen)
        # Return the screen manager as the root widget of the app
        return self.screen_manager

# Run the app
if __name__ == "__main__":
    TicTacToeApp().run()