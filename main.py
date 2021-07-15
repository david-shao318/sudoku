# Sudoku Solver

class Sudoku:
    def __init__(self, file_name=None):
        # get sudoku grid from user
        input_grid = []
        if file_name is None:
            for i in range(9):
                input_grid.append(input(f'Input row {i + 1} (no spaces, use 0 for blanks): '))
                try:
                    for j in range(9):
                        if int(input_grid[i][j]) not in range(10):
                            raise ValueError
                except (ValueError, LookupError):
                    print('Input error. Exiting...')
                    quit()
        else:
            try:
                with open(file_name) as f:
                    input_grid = f.read().split()
                for i in range(9):
                    for j in range(9):
                        if int(input_grid[i][j]) not in range(10):
                            raise ValueError
            except FileNotFoundError:
                print('File not found error. Exiting...')
                quit()
            except (ValueError, LookupError):
                print('Input error. Exiting...')
                quit()

        # transfer input to 2D list of ints (9 * 9)
        self._grid = []
        for i in range(9):
            self._grid.append([int(char) for char in input_grid[i]])

    def print_grid(self):
        print()
        for i in range(9):
            print(' ', end='')
            for j in range(9):
                if self._grid[i][j] != 0:
                    print(self._grid[i][j], end=' ')
                else:
                    print(' ', end=' ')
                if j % 3 == 2 and j < 8:
                    print('|', end=' ')
            print()
            if i % 3 == 2 and i < 8:
                print(23 * '-')
        print()

    def _check_valid(self, row, col, num):
        # check entire row
        for c in range(9):
            if self._grid[row][c] == num:
                return False
        # check entire col
        for r in range(9):
            if self._grid[r][col] == num:
                return False
        # check box
        for r in range((row // 3) * 3, (row // 3) * 3 + 3):
            for c in range((col // 3) * 3, (col // 3) * 3 + 3):
                if self._grid[r][c] == num:
                    return False
        return True

    def _possible_numbers(self, row, col):
        for potential in range(1, 10):
            if self._check_valid(row, col, potential):
                yield potential

    def solve(self):
        for r in range(9):
            for c in range(9):
                if self._grid[r][c] == 0:
                    for potential in self._possible_numbers(r, c):
                        self._grid[r][c] = potential  # can only insert a valid number into puzzle grid
                        self.solve()  # continue solving
                        self._grid[r][c] = 0  # backtrack if solution failed
                    return

        # reaches this point once there are no empty squares left
        self.print_grid()


# driver
if __name__ == '__main__':

    new_grid = Sudoku('grid.txt')  # alternatively, ask for user input
    new_grid.print_grid()
    new_grid.solve()
