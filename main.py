# Sudoku Solver

from timeit import default_timer as timer


class Sudoku:
    def __init__(self, file_name: str):
        """
        initialize puzzle _grid, solution_count
        :param file_name: name of input file
        """
        self.solution_count = 0
        self.puzzle_incomplete = False  # assume inputted puzzle is completely filled (no blanks)

        # input sudoku grid from file
        # store as 2D list of ints (9 * 9)
        try:
            with open(file_name) as f:
                # take the first 9 characters from the first 9 lines
                self._grid = [[int(num) for num in f.readline()[:9]] for _ in range(9)]

            # verify grid is exactly 9 * 9
            if len(self._grid) != 9:
                raise ValueError
            for row in self._grid:
                if len(row) != 9:
                    raise ValueError

        # exit on input errors
        except FileNotFoundError:
            raise SystemExit('Input file not found.')
        except ValueError:
            raise SystemExit('Input invalid. Input file should contain 9 lines of 9 numerals each.')

    def __str__(self) -> str:
        """
        aesthetically display puzzle grid
        :return: formatted grid
        """
        out = ''
        for r in range(9):
            out += ' '
            for c in range(9):
                if self._grid[r][c] != 0:
                    out += str(self._grid[r][c]) + ' '
                else:
                    out += '  '
                if c % 3 == 2 and c < 8:
                    out += '| '
            out += '\n'
            if r % 3 == 2 and r < 8:
                out += 23 * '-' + '\n'
        return out

    def _seen_numbers(self, seen: list[bool], row: int, col: int):
        """
        find which numbers have been seen at given position
        :param seen: list of 10 booleans, whether number at index is seen at given position
        :param row: row position (0-8)
        :param col: column position (0-8)
        """
        # set seen numbers in row, column, box
        for i in range(9):
            seen[self._grid[i][col]] = True
            seen[self._grid[row][i]] = True
        for r in range((row // 3) * 3, (row // 3) * 3 + 3):
            for c in range((col // 3) * 3, (col // 3) * 3 + 3):
                seen[self._grid[r][c]] = True

    def _solution_invalid(self) -> bool:
        """
        test if current complete solution is invalid
        :return: True if invalid
        """
        # test every row and column
        for i in range(9):
            curr_row = curr_col = [False] * 9
            for j in range(9):
                curr_row[self._grid[i][j] - 1] = True
                curr_col[self._grid[j][i] - 1] = True
            if False in curr_row or False in curr_col:
                return True
        # test every box
        for i in range(3):
            for j in range(3):
                curr_box = [False] * 9
                for k in range(3):
                    for l in range(3):
                        curr_box[self._grid[i * 3 + k][j * 3 + l] - 1] = True
                if False in curr_box:
                    return True
        return False

    def solve(self, start_row=0, start_col=0):
        """
        solve sudoku through recursive backtracking
        start each recursion where previous solve left off
        print all possible solutions
        """
        for r in range(start_row, 9):
            for c in range(start_col, 9):
                if self._grid[r][c] == 0:

                    if not self.puzzle_incomplete:  # inputted puzzle is incomplete, will attempt to solve
                        self.puzzle_incomplete = True

                    # find all seen numbers
                    seen = [False] * 10
                    self._seen_numbers(seen, r, c)

                    for potential in range(1, 10):
                        if not seen[potential]:
                            self._grid[r][c] = potential  # insert a valid number into puzzle grid
                            self.solve(r, c)  # continue solving
                            self._grid[r][c] = 0  # backtrack if solution failed
                    return

            if r == start_row:
                start_col = 0

        # reaches here once there are no empty squares left

        # if original puzzle was complete (no blanks), test if solution is valid
        if not self.puzzle_incomplete:
            if self._solution_invalid():
                return

        # solution is valid
        print('\n———Possible Solution———', self, sep='\n', end='')
        self.solution_count += 1


# driver
if __name__ == '__main__':
    # load input grid
    new_grid = Sudoku('grid.txt')
    print('————Original Sudoku————', new_grid, sep='\n', end='')

    # solve puzzle, timed
    start = timer()
    new_grid.solve()
    end = timer()

    print('\nNumber of Solutions:', new_grid.solution_count)
    print('Seconds Elapsed:', round(end - start, 6))
