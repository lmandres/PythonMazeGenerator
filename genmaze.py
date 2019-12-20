import random

class MazeGenerator(object):

    VISITED = 2**0
    WALL_LEFT = 2**1
    WALL_UP = 2**2

    maze = None
    rows = None
    cols = None

    start_row = None
    start_col = None
    end_row = None
    end_col = None

    step_counter = None
    max_steps = None

    def generate(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.initialize()
        self.traverse()
        self.setendcell()
        self.display()

    def initialize(self):
        self.maze = []
        self.step_counter = 0
        for row_index in range(0, self.rows+2, 1):
            self.maze.append([])
            for col_index in range(0, self.cols+2, 1):
                if (
                    row_index == 0 or
                    row_index == (self.rows+1) or 
                    col_index == 0 or 
                    col_index == (self.cols+1)
                ):
                    self.maze[row_index].append(self.VISITED)
                else:
                    self.maze[row_index].append(0)
                if (
                    (
                        1 <= row_index and 
                        row_index <= self.rows+1 and
                        col_index != 0 and
                        col_index != self.cols+1
                    )
                ):
                    self.maze[row_index][col_index] |= self.WALL_UP
                if (
                    (
                        1 <= col_index and
                        col_index <= self.cols+1 and
                        row_index != 0 and
                        row_index != self.rows+1
                    )
                ):
                    self.maze[row_index][col_index] |= self.WALL_LEFT

    def traverse(self):
        self.start_row = random.randint(1, self.rows)
        self.start_col = random.randint(1, self.cols)

        curr_row = self.start_row
        curr_col = self.start_col
        self.maze[curr_row][curr_col] |= self.VISITED

        while True:
            prev_row = curr_row
            prev_col = curr_col
            rand_indices = []

            if not self.maze[curr_row-1][curr_col] & self.VISITED:
                rand_indices.append(((curr_row-1), (curr_col)))
            if not self.maze[curr_row][curr_col+1] & self.VISITED:
                rand_indices.append(((curr_row), (curr_col+1)))
            if not self.maze[curr_row+1][curr_col] & self.VISITED:
                rand_indices.append(((curr_row+1), (curr_col)))
            if not self.maze[curr_row][curr_col-1] & self.VISITED:
                rand_indices.append(((curr_row), (curr_col-1)))

            if not len(rand_indices):
                curr_coords = self.backtrack(
                    curr_row,
                    curr_col,
                    test_visited=True
                )
            else:
                curr_coords = random.choice(rand_indices)
            curr_row = curr_coords[0]
            curr_col = curr_coords[1]

            if (
                curr_row == self.start_row and
                curr_col == self.start_col
            ):
                break

            if not self.maze[curr_row][curr_col] & self.VISITED:
                if (curr_row == prev_row-1 and curr_col == prev_col):
                    self.maze[prev_row][prev_col] &= (self.VISITED + self.WALL_LEFT)
                elif (curr_row == prev_row and curr_col == prev_col+1):
                    self.maze[curr_row][curr_col] &= (self.VISITED + self.WALL_UP)
                elif (curr_row == prev_row+1 and curr_col == prev_col):
                    self.maze[curr_row][curr_col] &= (self.VISITED + self.WALL_LEFT)
                elif (curr_row == prev_row and curr_col == prev_col-1):
                    self.maze[prev_row][prev_col] &= (self.VISITED + self.WALL_UP)
                self.maze[curr_row][curr_col] |= self.VISITED

    def backtrack(
        self,
        start_row,
        start_col,
        handedness=False,
        test_visited=True
    ):
        def backtrackUp(row, col):
            curr_row = row
            curr_col = col
            if not self.maze[curr_row][curr_col] & self.WALL_UP:
                curr_row -= 1
                return (curr_row, curr_col)
        def backtrackRight(row, col):
            curr_row = row
            curr_col = col
            if not self.maze[curr_row][curr_col+1] & self.WALL_LEFT:
                curr_col += 1
                return (curr_row, curr_col)
        def backtrackDown(row, col):
            curr_row = row
            curr_col = col
            if not self.maze[curr_row+1][curr_col] & self.WALL_UP:
                curr_row += 1
                return (curr_row, curr_col)
        def backtrackLeft(row, col):
            curr_row = row
            curr_col = col
            if not self.maze[curr_row][curr_col] & self.WALL_LEFT:
                curr_col -= 1
                return (curr_row, curr_col)

        backtrackList = [
            backtrackUp,
            backtrackRight,
            backtrackDown,
            backtrackLeft
        ]
        backtrack_index = 0
        curr_row = start_row
        curr_col = start_col

        while True:
            if (
                test_visited and (
                    not self.maze[curr_row-1][curr_col] & self.VISITED or
                    not self.maze[curr_row][curr_col+1] & self.VISITED or
                    not self.maze[curr_row+1][curr_col] & self.VISITED or
                    not self.maze[curr_row][curr_col-1] & self.VISITED
                ) or (
                    curr_row == self.start_row and
                    curr_col == self.start_col
                )
            ):
                break
            ret_tuple = backtrackList[backtrack_index](
                curr_row,
                curr_col
            )
            if ret_tuple:
                curr_row = ret_tuple[0]
                curr_col = ret_tuple[1]
                if not test_visited:
                    if self.maze[curr_row][curr_col] & self.VISITED:
                        self.step_counter -= 1
                    else:
                        self.maze[curr_row][curr_col] |= self.VISITED
                        self.step_counter += 1
                if handedness:
                    backtrack_index += 1
                else:
                    backtrack_index += 3
                
            else:
                if handedness:
                    backtrack_index += 3
                else:
                    backtrack_index += 1
            backtrack_index %= 4

        return (curr_row, curr_col)

    def setendcell(self):
        end_cells = []
        handed_steps = []
        nonhand_steps = []
        max_steps = 0
        for row_index in range(1, self.rows+1, 1):
            for col_index in range(1, self.cols+1, 1):
                wall_count = 0
                if self.maze[row_index][col_index] & self.WALL_UP:
                    wall_count += 1
                if self.maze[row_index][col_index] & self.WALL_LEFT:
                    wall_count += 1
                if self.maze[row_index+1][col_index] & self.WALL_UP:
                    wall_count += 1
                if self.maze[row_index][col_index+1] & self.WALL_LEFT:
                    wall_count += 1
                if (
                    wall_count == 3 and
                    row_index != self.start_row and
                    col_index != self.start_col
                ):
                    end_cells.append((row_index, col_index))
        for cell_index in range(0, len(end_cells), 1):
            for row_index in range(1, self.rows+1, 1):
                for col_index in range(1, self.cols+1, 1):
                    self.maze[row_index][col_index] &= (
                        self.WALL_UP +
                        self.WALL_LEFT
                    )
            self.step_counter = 0
            self.backtrack(
                end_cells[cell_index][0],
                end_cells[cell_index][1],
                handedness=False,
                test_visited=False
            )
            nonhand_steps.append(self.step_counter)
            for row_index in range(1, self.rows+1, 1):
                for col_index in range(1, self.cols+1, 1):
                    self.maze[row_index][col_index] &= (
                        self.WALL_UP +
                        self.WALL_LEFT
                    )
            self.step_counter = 0
            self.backtrack(
                end_cells[cell_index][0],
                end_cells[cell_index][1],
                handedness=True,
                test_visited=False
            )
            handed_steps.append(self.step_counter)
            abs_steps = abs(
                nonhand_steps[cell_index] -
                handed_steps[cell_index]
            )
            if abs_steps == 0:
                max_steps = max(max_steps, handed_steps[cell_index])
            if handed_steps[cell_index] == max_steps:
                self.end_row = end_cells[cell_index][0]
                self.end_col = end_cells[cell_index][1]


    def display(self):
        for row_index in range(0, self.rows+2, 1):
            for col_index in range(0, self.cols+2, 1):
                if self.maze[row_index][col_index] & self.WALL_UP:
                    print('+--', end='')
                elif row_index != 0 and col_index != 0:
                    print('+  ', end='')
                else:
                    print('   ', end='')
            print()
            for col_index in range(0, self.cols+2, 1):
                if self.maze[row_index][col_index] & self.WALL_LEFT:
                    print('|', end='')
                else:
                    print(' ', end='')
                if (
                    row_index == self.start_row and
                    col_index == self.start_col
                ):
                    print('()', end='')
                elif (
                    row_index == self.end_row and
                    col_index == self.end_col
                ):
                    print('><', end='')
                else:
                    print('  ', end='')
            print()

if __name__ == '__main__':
    mg = MazeGenerator()
    mg.generate(10, 10)

