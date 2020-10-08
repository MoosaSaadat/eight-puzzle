from agents import *
import random
import sys

# ______________________________________________________________________________
# 8-Puzzle Environment


class PuzzleAgent(Agent):
    def __init__(self):
        super().__init__(self.bfs)

    def bfs(self, percept):
        return random.choice(percept)

    def __str__(self):
        return "_"


class Block(Thing):
    def __init__(self, num):
        self.num = num

    def __str__(self):
        return f"{self.num}"

    def __repr__(self):
        return f"<Block: {self.num}>"


class PuzzleEnvironment(XYEnvironment):
    def __init__(self, width=3, height=3):
        super().__init__(width, height)
        self.totalBlocks = width * height - 1
        self.init_puzzle()

    def init_puzzle(self):
        """Creates puzzle with random position of agent and blocks"""
        gridCoords = [(i, j) for j in range(self.height) for i in range(self.width)]
        blockNums = list(range(1, self.totalBlocks + 1))
        randCoords = random.sample(gridCoords, self.totalBlocks + 1)
        randNums = random.sample(blockNums, self.totalBlocks)

        # Add Agent
        self.add_thing(PuzzleAgent(), randCoords[0], True)

        # Add blocks
        for loc, num in zip(randCoords[1:], randNums):
            self.add_thing(Block(num), loc, True)

    def get_world(self):
        """Return the items in the world"""
        result = []
        for i in range(self.width):
            row = []
            for j in range(self.height):
                row.extend(self.list_things_at((i, j)))
            result.append(row)
        return result

    def percept(self, agent):
        x, y = agent.location
        result = []

        # LEFT direction
        if not y - 1 < 0:
            result.append((x, y - 1))
        # RIGHT direction
        if not y + 1 >= self.height:
            result.append((x, y + 1))
        # DOWN direction
        if not x + 1 >= self.width:
            result.append((x + 1, y))
        # UP direction
        if not x - 1 < 0:
            result.append((x - 1, y))
        # NoOp: Agent remains at current position
        result.append((x, y))

        return result

    def execute_action(self, agent, action):

        swapLocation = action
        agentLocation = agent.location
        adjBlock = self.list_things_at(swapLocation)[0]

        # Swap Locations
        agent.location = swapLocation
        adjBlock.location = agentLocation

    def is_done(self):
        allNums = list(range(1, self.totalBlocks))
        for i in range(self.width):
            for j in range(self.height):
                currThing = self.list_things_at((i, j))[0]
                if isinstance(currThing, Block):
                    if allNums[i + j] != currThing.num:
                        return False
                else:
                    return False
                # Puzzle Solved - End game
                if i == self.width - 1 and j == self.height - 2:
                    return True

    def run(self, steps=1000):
        """Run the Environment for given number of time steps."""
        for step in range(steps):
            if self.is_done():
                return step + 1
            self.step()
        return steps

    def get_num_correct_pieces(self):
        correct_pieces = 0
        currPiece = 1
        for i in range(self.width):
            for j in range(self.height):
                currThing = self.list_things_at((i, j))[0]
                if isinstance(currThing, Block):
                    if currThing.num == currPiece:
                        correct_pieces += 1
                currPiece += 1

        return correct_pieces


# ______________________________________________________________________________
# Main Task

if __name__ == "__main__":
    puzzleSize = int(sys.argv[1])
    movesAllowed = int(sys.argv[2])

    puzzle = PuzzleEnvironment(puzzleSize, puzzleSize)

    def print_world():
        grid = puzzle.get_world()
        for row in grid:
            for col in row:
                print(col, end=" ")
            print()

    movesUtilized = puzzle.run(movesAllowed)
    correctPieces = puzzle.get_num_correct_pieces()

    print(
        f"No of correct pieces = {correctPieces}, no of moves utilized = {movesUtilized}"
    )

