import random


class MazeGenerator(object):
    """Class to generate mazes written in Python."""

    VISITED = 2**0  # Flag if cell has been visited
    WALL_LEFT = 2**1    # Flag if there is a wall to left
    WALL_UP = 2**2  # Flag if there is a wall to top

    maze = None     # Maze object
    rows = None     # Number of rows in maze
    cols = None     # Number of columns in maze

    start_row = None    # Row number of start cell
    start_col = None    # Column number of start cell
    end_row = None  # Row number of end cell
    end_col = None  # Column number of end cell

    def generate(self, rows, cols):
        "Main execution method"
        self.rows = rows    # Sets the rows to rows arg
        self.cols = cols    # Sets the columns to cols arg
        self.initialize()   # Calls initialize method
        self.traverse()     # Traverses maze to generate
        self.setendcell()   # Sets end cell to farthest end
        self.display()      # Prints out maze

    def initialize(self):
        "Initialize the maze to be full of cells."
        # Maze is an array of arrays. Declare main array.
        self.maze = []
        # Go through loop to generate maze.
        # First and last rows are blanks because easy.
        for row_index in range(0, self.rows+2, 1):
            # Initialize column array for the row
            self.maze.append([])
            # If index is around the border, mark as visited
            # to keep the traverse within cell bounds
            for col_index in range(0, self.cols+2, 1):
                if (
                    row_index == 0 or
                    row_index == (self.rows+1) or
                    col_index == 0 or
                    col_index == (self.cols+1)
                ):
                    # Mark as visited
                    self.maze[row_index].append(self.VISITED)
                else:
                    # Marks as empty
                    self.maze[row_index].append(0)
                # Draw upper walls around all cells of maze
                if (
                    (
                        1 <= row_index and
                        row_index <= self.rows+1 and
                        col_index != 0 and
                        col_index != self.cols+1
                    )
                ):
                    # Set the upper wall as present
                    self.maze[row_index][col_index] |= self.WALL_UP
                # Draw left hand walls around all cells of maze
                if (
                    (
                        1 <= col_index and
                        col_index <= self.cols+1 and
                        row_index != 0 and
                        row_index != self.rows+1
                    )
                ):
                    # Set the left wall as present
                    self.maze[row_index][col_index] |= self.WALL_LEFT

    def traverse(self):
        # Go through cells and make a random maze.
        # Pick a random row for the start row
        self.start_row = random.randint(1, self.rows)
        # Pick a random column for the start column
        self.start_col = random.randint(1, self.cols)

        # Set the current row as the start row
        curr_row = self.start_row
        # Set the current column as the start column
        curr_col = self.start_col

        # Set the start cell as visited
        self.maze[curr_row][curr_col] |= self.VISITED

        # Traverse the maze
        while True:
            # Save the current row as the previous row
            prev_row = curr_row
            # Save the current column as the previous column
            prev_col = curr_col

            # Clear out the cells adjacent to the current cell
            rand_indices = []

            # If the cell above not visited, add to indices
            if not self.maze[curr_row-1][curr_col] & self.VISITED:
                rand_indices.append(((curr_row-1), (curr_col)))
            # If the cell to right not visited, add to indices
            if not self.maze[curr_row][curr_col+1] & self.VISITED:
                rand_indices.append(((curr_row), (curr_col+1)))
            # If the cell below not visited, add to indices
            if not self.maze[curr_row+1][curr_col] & self.VISITED:
                rand_indices.append(((curr_row+1), (curr_col)))
            # If the cell to left not visited, add to indices
            if not self.maze[curr_row][curr_col-1] & self.VISITED:
                rand_indices.append(((curr_row), (curr_col-1)))

            # If no indices have been added, do backtrack
            if not len(rand_indices):
                # Try to backtrack from current cell
                # Must always use the same handedness
                curr_coords = self.backtrack(
                    curr_row,
                    curr_col,
                    test_visited=True
                )
            else:
                # Choose a random non-visited adjacent cell
                curr_coords = random.choice(rand_indices)

            # Set current row to random row
            curr_row = curr_coords[0]
            # Set current column to random column
            curr_col = curr_coords[1]

            # If arrived at start cell, maze fully traversed 
            if (
                curr_row == self.start_row and
                curr_col == self.start_col
            ):
                # Get out of loop
                break

            # If the current cell has not been visited,
            # it means that we are traversing the maze
            # (ie. not backtracking)
            if not self.maze[curr_row][curr_col] & self.VISITED:
                #  If we turned up
                if (curr_row == prev_row-1 and curr_col == prev_col):
                    # Delete the upper wall of previous cell
                    self.maze[prev_row][prev_col] -= self.WALL_UP
                # If we went right
                elif (curr_row == prev_row and curr_col == prev_col+1):
                    # Delete the left wall current cell
                    self.maze[curr_row][curr_col] -= self.WALL_LEFT
                # If we went down
                elif (curr_row == prev_row+1 and curr_col == prev_col):
                    # Delete upper wall of current cell
                    self.maze[curr_row][curr_col] -= self.WALL_UP
                # If we went left
                elif (curr_row == prev_row and curr_col == prev_col-1):
                    # Delete left wall of previous cell
                    self.maze[prev_row][prev_col] -= self.WALL_LEFT

                # Mark current cell as visited
                self.maze[curr_row][curr_col] |= self.VISITED

    def backtrack(
        self,
        start_row,
        start_col,
        handedness=False,
        test_visited=True
    ):
        "Find our way to a cell adjacent to a non-visited cell"
        def backtrackUp(row, col):
            "Backtrack method to go back up."
            # Set the current row to the row arg
            curr_row = row
            # Set the current column to the col arg
            curr_col = col

            # Test if there is a wall above the current cell
            if not self.maze[curr_row][curr_col] & self.WALL_UP:
                # Move to cell above if it is clear
                curr_row -= 1
                # Return the new cell coords
                return (curr_row, curr_col)

        def backtrackRight(row, col):
            "Backtrack method to go back right."
            # Set the current row to the row arg
            curr_row = row
            # Set the current column to the col arg
            curr_col = col

            # Test if there is a wall to the right
            if not self.maze[curr_row][curr_col+1] & self.WALL_LEFT:
                # Move to right if it is clear
                curr_col += 1
                # Return the new cell coords
                return (curr_row, curr_col)

        def backtrackDown(row, col):
            "Backtrack method to go back down."
            # Set the current row to the row arg
            curr_row = row
            # Set the current column to the col arg
            curr_col = col

            # Test if there is a wall at the bottom
            if not self.maze[curr_row+1][curr_col] & self.WALL_UP:
                # Move down if it is clear
                curr_row += 1
                # Return the new cell coords
                return (curr_row, curr_col)

        def backtrackLeft(row, col):
            "Backtrack method to go back left."
            # Set the current row to the row arg
            curr_row = row
            # Set the current column to the col arg
            curr_col = col

            # Test if there is a wall to the left
            if not self.maze[curr_row][curr_col] & self.WALL_LEFT:
                # Move left if the left is clear
                curr_col -= 1
                # Return the new cell coords
                return (curr_row, curr_col)

        # Put the four backtrack directions into a list
        backtrackList = [
            backtrackUp,
            backtrackRight,
            backtrackDown,
            backtrackLeft
        ]

        # Set the backtrack direction index to an arbitrary index
        backtrack_index = 0
        # Set the current row to the start_row arg
        curr_row = start_row
        # Set the current column to the start_col arg
        curr_col = start_col
        # Set step_counter to None
        step_counter = None 

        # If not test_visited, means we are counting
        # distance from start
        if not test_visited:
            step_counter = 0    # Set step counter to 0
            # Go through all rows in maze
            for row_index in range(1, self.rows+1, 1):
                # Go through all columns in maze
                for col_index in range(1, self.cols+1, 1):
                    # Set the VISITED flag for a cell to 0
                    self.maze[row_index][col_index] &= (
                        self.WALL_UP +
                        self.WALL_LEFT
                    )

        # Go through backtrack loop
        while True:
            # Test to see if we can break out of the backtrack loop
            if (
                (
                    # Test if we are testing to for an exit
                    # This might be false if we are just testing
                    # to see if we are at the start cell
                    test_visited and (
                        # Test if cell above is open
                        not self.maze[curr_row-1][curr_col] & self.VISITED or
                        # Test if cell to right is open
                        not self.maze[curr_row][curr_col+1] & self.VISITED or
                        # Test if cell below is open
                        not self.maze[curr_row+1][curr_col] & self.VISITED or
                        # Test if cell to left is open
                        not self.maze[curr_row][curr_col-1] & self.VISITED
                    )
                ) or (
                    # Test if we are at the start cell
                    curr_row == self.start_row and
                    curr_col == self.start_col
                )
            ):
                # Exit from the backtrack loop
                break

            # Try to backtrack in a specified direction
            ret_tuple = backtrackList[backtrack_index](
                curr_row,
                curr_col
            )

            # If we find a cell using the backtrack methods
            # either a cell with an exit if test_visited is true
            # of if at start cell if test_visited is false
            if ret_tuple:
                # Set the row to the returned row
                curr_row = ret_tuple[0]
                # Set the column to the returned column
                curr_col = ret_tuple[1]

                # If we are not testing for visited cells,
                # measure greatest number of cells from start
                if not test_visited:
                    # If the current cell had been visited
                    if self.maze[curr_row][curr_col] & self.VISITED:
                        # subtract a step from the step_counter
                        step_counter -= 1
                    # Otherwise
                    else:
                        # Mark cell as visited
                        self.maze[curr_row][curr_col] |= self.VISITED
                        # add a step to the step_counter
                        step_counter += 1
                # If handedness is set, go down backtrack methods
                if handedness:
                    backtrack_index += 1
                # Else, go up backtrack methods
                else:
                    backtrack_index += 3
            # If we did not find a cell using the backtrack methods
            # either a cell with an exit if test_visited is true
            # of if at start cell if test_visited is false
            else:
                # If handedness is set, go down backtrack methods
                if handedness:
                    backtrack_index += 3
                # Else, go up backtrack methods
                else:
                    backtrack_index += 1
            # If backtrack_index is greater than four
            # start at remainder
            backtrack_index %= 4

        return (curr_row, curr_col, step_counter)

    def setendcell(self):
        "Method to determine end cell by selecting furthest end."
        # Initialize empty end_cell list
        end_cells = []
        # Initialize empty right handed steps count
        handed_steps = []
        # Initialize empty left handed steps count
        nonhand_steps = []
        # Highest number of steps count initialized to zero
        max_steps = 0

        # Go through every row
        for row_index in range(1, self.rows+1, 1):
            # Go through every column
            for col_index in range(1, self.cols+1, 1):
                # Initialize wall count to zero for cell
                wall_count = 0
                # If wall above cell
                if self.maze[row_index][col_index] & self.WALL_UP:
                    wall_count += 1     # Add 1 to count
                # If wall to left of cell
                if self.maze[row_index][col_index] & self.WALL_LEFT:
                    wall_count += 1     # Add 1 to count
                # If wall below cell
                if self.maze[row_index+1][col_index] & self.WALL_UP:
                    wall_count += 1     # Add 1 to count
                # If wall to right of cell
                if self.maze[row_index][col_index+1] & self.WALL_LEFT:
                    wall_count += 1     # Add 1 to count

                # If wall count is three (ie. dead end)
                # and not start cell
                if (
                    wall_count == 3 and
                    row_index != self.start_row and
                    col_index != self.start_col
                ):
                    # Append dead end as possible end to end_cells
                    end_cells.append((row_index, col_index))

        # For each possible end cell
        for cell_index in range(0, len(end_cells), 1):
            # Backtrack to find number of non-handed step count
            end_tuple = self.backtrack(
                end_cells[cell_index][0],
                end_cells[cell_index][1],
                handedness=False,
                test_visited=False
            )
            # Step count in 3rd item in tuple
            # Append to step counts for non-handed steps
            nonhand_steps.append(end_tuple[2])

            # Backtrack to find number of handed step count
            end_tuple = self.backtrack(
                end_cells[cell_index][0],
                end_cells[cell_index][1],
                handedness=True,
                test_visited=False
            )
            # Step count in 3rd item in tuple
            # Append to step count for handed steps
            handed_steps.append(end_tuple[2])

            # Find greatest difference between handed and non-handed
            abs_steps = abs(
                nonhand_steps[cell_index] -
                handed_steps[cell_index]
            )

            # If there is no difference
            if abs_steps == 0:
                # Pick maximum from the handed_steps list
                # (picked arbitrarily) vs. the max number of steps
                max_steps = max(max_steps, handed_steps[cell_index])

            # If the maximum number of steps is the maximum count
            if handed_steps[cell_index] == max_steps:
                # Set end row to the end cell row coord
                self.end_row = end_cells[cell_index][0]
                # Set end column to end cell column coord
                self.end_col = end_cells[cell_index][1]

    def display(self):
        "Method to display maze on screen."
        # Go through each row in the maze
        for row_index in range(0, self.rows+2, 1):
            # Go through each column in the maze
            for col_index in range(0, self.cols+2, 1):
                # If there is a wall to the top of the cell
                if self.maze[row_index][col_index] & self.WALL_UP:
                    # Print the upper wall
                    print('+--', end='')
                # If not
                else:
                    # Print a blank wall
                    print('+  ', end='')
            # Move to the next line
            print()

            # Next is to print the side walls
            for col_index in range(0, self.cols+2, 1):
                # If there is a wall to the left of the cell
                if self.maze[row_index][col_index] & self.WALL_LEFT:
                    # Print the left side wall
                    print('|', end='')
                # If not
                else:
                    # Print a blank wall
                    print(' ', end='')

                # Print the contents of the cell
                # If the cell is the start cell
                if (
                    row_index == self.start_row and
                    col_index == self.start_col
                ):
                    # Print a circle (open and close parentheses)
                    print('()', end='')
                # Else If the cell is the end cell
                elif (
                    row_index == self.end_row and
                    col_index == self.end_col
                ):
                    # Print an 'X' (greater than and less than)
                    print('><', end='')
                # Otherwise, the cell is just empty
                else:
                    # Print two blank spaces
                    print('  ', end='')
            # Move to the next line
            print()


# If this is the main method
if __name__ == '__main__':
    # Create a MazeGenerator object
    mg = MazeGenerator()
    # Tell the generator to generate a 10x10 maze
    #mg.generate(10, 10)
    mg.generate(28, 62)
