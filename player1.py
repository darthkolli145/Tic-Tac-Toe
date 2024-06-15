import socket
from gameboard import BoardClass

def play_game(conn, board):
    """
    Handle the gameplay between Player 1 and Player 2.

    Args:
        conn (socket.socket): The connection object to communicate with Player 2.
        board (BoardClass): The game board object.

    Returns:
        bool: True if the game is over, False otherwise.
    """
    while True:
        board.displayBoard() #Displays the board
        while True:
            move = input("Enter your move (row,col): ")
            try:
                row, col = map(int, move.split(","))
                if 0 <= row < 3 and 0 <= col < 3:
                    if board.updateGameBoard(row, col, 'X'):
                        conn.sendall(move.encode())
                        break
                    else:
                        print("Invalid move, spot already taken. Try again.")
                else:
                    print("Invalid move, out of bounds. Try again.")
            except ValueError:
                print("Invalid input, please enter row and column as numbers separated by a comma.")

        board.displayBoard()

        if board.isWinner('X'):
            board.updateStats(board.player1)
            board.updateGamesPlayed()
            return True

        if board.boardIsFull():
            board.updateStats(None)
            board.updateGamesPlayed()
            return True

        print("Waiting for Player 2's move...")
        try:
            move = conn.recv(1024).decode()
            if not move:
                print("Player 2 disconnected.")
                return False
            print(f"Received move from Player 2: {move}")
            row, col = map(int, move.split(","))
            board.updateGameBoard(row, col, 'O')
        except Exception as e:
            print(f"Error receiving move from Player 2: {e}")
            return False

        if board.isWinner('O'):
            board.updateStats(board.player2)
            board.updateGamesPlayed()
            return True

        if board.boardIsFull():
            board.updateStats(None)
            board.updateGamesPlayed()
            return True

def main():
    """
    Main function to set up the connection and start the game.
    """
    host = input("Enter the host name/IP address to connect to: ")
    port = int(input("Enter the port number to use: "))

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        print("Connected to the server.")

        username = input("Enter your username: ")
        s.sendall(username.encode())

        player2_name = s.recv(1024).decode()
        print(f"You are playing with {player2_name}")

        board = BoardClass(username, player2_name)

        while True:
            game_over = play_game(s, board)
            if game_over:
                if board.isWinner('X'):
                    print("Player 1 wins!")
                elif board.isWinner('O'):
                    print("Player 2 wins!")
                else:
                    print("It's a tie!")

                board.printStats()
                play_again = input("Play Again? (y/n): ").strip().lower()

                if play_again == 'n':
                    s.sendall(play_again.encode())
                    print("Fun Times")
                    break
                else:
                    s.sendall(play_again.encode())
                    print("Starting a new game...")
                    board.resetGameBoard()
            else:
                break

if __name__ == "__main__":
    main()
