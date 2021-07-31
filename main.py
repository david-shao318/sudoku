# Sudoku Solver

from timeit import default_timer as timer


class Sudoku:
    def __init__(self, file_name: str):
        """
        initialize puzzle _grid, solution_count
        :param file_name: name of input file
        """
        self.solution_count = 0

        # input sudoku grid from file
        # store as 2D list of ints (9 * 9)
        try:
            with open(file_name) as f:
                # only take the first 9 characters from the first 9 lines
                self._grid = [[int(num) for j, num in enumerate(line) if j < 9] for i, line in enumerate(f) if i < 9]

            # verify grid is exactly 9 * 9
            if len(self._grid) != 9:
                raise IndexError
            for row in self._grid:
                if len(row) != 9:
                    raise IndexError

        # exit on input errors
        except FileNotFoundError:
            raise SystemExit('Input file not found.')
        except (ValueError, IndexError):
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

    def _possible_numbers(self, row: int, col: int):
        """
        generate possible numbers for given grid position
        :param row: row position (0-8)
        :param col: column position (0-8)
        """
        # add seen numbers in row, column, box to set
        seen = {0}
        for i in range(9):
            seen.add(self._grid[i][col])
            seen.add(self._grid[row][i])
        for r in range((row // 3) * 3, (row // 3) * 3 + 3):
            for c in range((col // 3) * 3, (col // 3) * 3 + 3):
                seen.add(self._grid[r][c])

        # yield potential numbers not seen
        for potential in range(1, 10):
            if potential not in seen:
                yield potential

    def solve(self):
        """
        solve sudoku through recursive backtracking
        print all possible solutions
        """
        for r in range(9):
            for c in range(9):
                if self._grid[r][c] == 0:
                    for potential in self._possible_numbers(r, c):
                        self._grid[r][c] = potential  # insert a valid number into puzzle grid
                        self.solve()  # continue solving
                        self._grid[r][c] = 0  # backtrack if solution failed
                    return

        # reaches this point once there are no empty squares left
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
