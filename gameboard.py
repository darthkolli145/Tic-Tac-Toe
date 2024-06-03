class BoardClass:
    def __init__(self, player1, player2):
        """
        Initializes the BoardClass with two players and an empty board.

        Args:
            player1 (str): Name of player 1.
            player2 (str): Name of player 2.
        """
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.player1 = player1
        self.player2 = player2
        self.games_played = 0
        self.player1_wins = 0
        self.player2_wins = 0
        self.ties = 0

    def displayBoard(self):
        """
        Displays the current state of the game board.
        """
        for row in self.board:
            print('|'.join(row))
            print('-' * 5)

    def updateGameBoard(self, row, col, player):
        """
        Updates the game board with a player's move.

        Args:
            row (int): The row of the move.
            col (int): The column of the move.
            player (str): The player making the move ('X' or 'O').

        Returns:
            bool: True if the move was valid and the board was updated, False otherwise.
        """
        if self.board[row][col] == ' ':
            self.board[row][col] = player
            return True
        return False

    def resetGameBoard(self):
        """
        Resets the game board to its initial empty state.
        """
        self.board = [[' ' for _ in range(3)] for _ in range(3)]

    def isWinner(self, player):
        """
        Checks if the specified player has won the game.

        Args:
            player (str): The player to check ('X' or 'O').

        Returns:
            bool: True if the player has won, False otherwise.
        """
        # Check rows, columns and diagonals
        for row in self.board:
            if all(s == player for s in row):
                return True
        for col in range(3):
            if all(self.board[row][col] == player for row in range(3)):
                return True
        if all(self.board[i][i] == player for i in range(3)) or all(self.board[i][2 - i] == player for i in range(3)):
            return True
        return False

    def boardIsFull(self):
        """
        Checks if the game board is full.

        Returns:
            bool: True if the board is full, False otherwise.
        """
        return all(all(cell != ' ' for cell in row) for row in self.board)

    def updateGamesPlayed(self):
        """
        Increments the count of games played.
        """
        self.games_played += 1

    def updateStats(self, winner):
        """
        Updates the statistics based on the winner of the game.

        Args:
            winner (str or None): The name of the winning player, or None if the game was a tie.
        """
        if winner == self.player1:
            self.player1_wins += 1
        elif winner == self.player2:
            self.player2_wins += 1
        else:
            self.ties += 1

    def printStats(self):
        """
        Prints the current game statistics.
        """
        print(f"Player 1: {self.player1}")
        print(f"Player 2: {self.player2}")
        print(f"Games played: {self.games_played}")
        print(f"{self.player1} wins: {self.player1_wins}")
        print(f"{self.player2} wins: {self.player2_wins}")
        print(f"Ties: {self.ties}")
