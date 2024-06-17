import socket
from gameboard import BoardClass

def play_game(conn, board):
    """
    Handle the gameplay between Player 1 and Player 2.

    Args:
        conn (socket.socket): The connection object to communicate with Player 1.
        board (BoardClass): The game board object.

    Returns:
        bool: True if the game is over, False otherwise.
    """
    empty_move_counter = 0
    max_empty_moves = 5  # maximum number of allowed empty moves

    while True:
        board.displayBoard()
        print("Waiting for Player 1's move...")
        while True:
            try:
                move = conn.recv(1024).decode()
                if not move:
                    empty_move_counter += 1
                    print("Received empty move from Player 1.")
                    if empty_move_counter >= max_empty_moves:
                        print("Too many empty moves received. Ending game.")
                        return False
                    continue

                print(f"Received move from Player 1: {move}")
                row, col = map(int, move.split(","))
                if 0 <= row < 3 and 0 <= col < 3:
                    board.updateGameBoard(row, col, 'X')
                    empty_move_counter = 0  # reset counter after a valid move
                    break
                else:
                    print("Received invalid move from Player 1 (out of bounds).")
            except Exception as e:
                print(f"Error receiving move from Player 1: {e}")
                return False

        board.displayBoard()

        if board.isWinner('X'):
            board.updateStats(board.player1)
            board.updateGamesPlayed()
            return True

        if board.boardIsFull():
            board.updateStats(None)
            board.updateGamesPlayed()
            return True

        while True:
            move = input("Enter your move (row,col): ")
            try:
                row, col = map(int, move.split(","))
                if 0 <= row < 3 and 0 <= col < 3:
                    if board.updateGameBoard(row, col, 'O'):
                        conn.sendall(move.encode())
                        break
                    else:
                        print("Invalid move, spot already taken. Try again.")
                else:
                    print("Invalid move, out of bounds. Try again.")
            except ValueError:
                print("Invalid input, please enter row and column as numbers separated by a comma.")

        board.displayBoard()

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
    host = input("Enter your host name/IP address: ")
    port = int(input("Enter the port number to use: "))

    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((host, port))
            s.listen()
            print(f"Listening on {host}:{port}")
            print("Waiting for Player 1 to connect...")
            conn, addr = s.accept()

            with conn:
                print(f"Connected by {addr}")
                player1_name = conn.recv(1024).decode()
                print(f"Player 1's username: {player1_name}")
                username = input("Enter your username: ")
                conn.sendall(username.encode())

                print(f"You are playing with {player1_name}")

                board = BoardClass(player1_name, username)

                while True:
                    game_over = play_game(conn, board)
                    if game_over:
                        if board.isWinner('X'):
                            print("Player 1 wins!")
                        elif board.isWinner('O'):
                            print("Player 2 wins!")
                        else:
                            print("It's a tie!")

                        board.printStats()
                        play_again = conn.recv(1024).decode().strip().lower()

                        if play_again == 'n':
                            print("Fun Times")
                            return
                        else:
                            print("Starting a new game...")
                            board.resetGameBoard()
                    else:
                        break

if __name__ == "__main__":
    main()
