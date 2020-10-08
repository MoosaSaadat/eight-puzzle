from agents import *
import random

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

    def get_world(self, show_walls=True):
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


# ______________________________________________________________________________
# Main Task


puzzle = PuzzleEnvironment()


def print_world():
    grid = puzzle.get_world()
    for row in grid:
        for col in row:
            print(col, end=" ")
        print()


print_world()

while True:
    puzzle.step()
    print_world()
    input()
