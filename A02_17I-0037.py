from agents import PuzzleEnvironment

####################
#    PARAMETERS    #
####################
INITIAL_STATE = [
    ["0", "1", "2"],
    ["3", "4", "5"],
    ["6", "7", "8"],
]

puzzle = PuzzleEnvironment()
grid = puzzle.get_world()

for row in grid:
    for col in row:
        print(col, end=" ")
    print()
