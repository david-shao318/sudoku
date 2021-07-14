# Sudoku Solver

class Sudoku:
    def __init__(self, file_name=None):
        input_board = []

        if file_name is None:
            for i in range(9):
                input_board.append(input(f'Input row {i + 1} (no spaces, use 0 for blanks): '))
                try:
                    for j in range(9):
                        if int(input_board[i][j]) not in range(10):
                            raise ValueError
                except (ValueError, LookupError):
                    print('Input error. Exiting...')
                    quit()

        else:
            try:
                with open(file_name) as f:
                    input_board = f.read().split()
                for i in range(9):
                    for j in range(9):
                        if int(input_board[i][j]) not in range(10):
                            raise ValueError
            except FileNotFoundError:
                print('File not found error. Exiting...')
                quit()
            except (ValueError, LookupError):
                print('Input error. Exiting...')
                quit()

        self._board = []
        for i in range(9):
            self._board.append([int(char) for char in input_board[i]])

    def print_board(self):
        for i in range(9):
            for j in range(9):
                print(self._board[i][j], end=' ')
                if j % 3 == 2 and j < 8:
                    print('|', end=' ')
            print()
            if i % 3 == 2 and i < 8:
                print(21 * '-')


if __name__ == '__main__':
    new_board = Sudoku('board.txt')
    new_board.print_board()
