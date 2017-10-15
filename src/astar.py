import heapq

from options import Options
from tile import Tile


class AStar:
    NSEW = -Options.line_length, Options.line_length, 1, -1  # Add to find tile in a direction

    def __init__(self, zombie, survivor):
        for tile in Tile.instances:  # Reset from last search
            tile.parent = None
            tile.h, tile.f, tile.g = 0, 0, 0
        zombie.path = []
        self.open = []
        heapq.heapify(self.open)
        self.closed = set()
        self.zombie = zombie
        self.start = zombie.get_tile()
        self.end = survivor.get_tile()
        heapq.heappush(self.open, (self.start.f, self.start))

    @staticmethod
    def tile_on_screen(direction, tile_num):
        if direction == 2:  # East
            return tile_num % Options.line_length != 0
        if direction == 3:
            return tile_num % Options.line_length != Options.line_length - 1  # West
        return 0 < tile_num < Tile.amnt_tiles  # North and South

    def get_neighbours(self, cell):
        for direction, sur_tile_num in enumerate(cell.number + direction
                                                 for direction in AStar.NSEW):
            try:
                sur_tile = Tile.instances[sur_tile_num]
            except IndexError:
                continue
            if (sur_tile.walkable and sur_tile not in self.closed and
                    AStar.tile_on_screen(direction, sur_tile_num)):
                yield sur_tile

    def get_heuristic(self, cell):
        """:return the Manhattan distance between end and cell
        https://en.wikipedia.org/wiki/Taxicab_geometry"""
        return self.end.pos.manhattan_dist(cell.pos) / 3

    def update_cell(self, neighbour, cell):
        neighbour.g = cell.g + 10
        neighbour.h = self.get_heuristic(neighbour)
        neighbour.f = neighbour.h + neighbour.g
        neighbour.parent = cell

    def solve(self):
        while self.open and self.end not in self.closed:
            f, cell = heapq.heappop(self.open)
            self.closed.add(cell)
            neighbours = self.get_neighbours(cell)
            for neighbour in neighbours:
                if (neighbour.f, neighbour) in self.open:
                    if neighbour.g > cell.g + 10:
                        self.update_cell(neighbour, cell)
                else:
                    self.update_cell(neighbour, cell)
                    heapq.heappush(self.open, (neighbour.f, neighbour))

        parent = self.end
        while not (parent is None or parent is self.start):
            child = parent
            parent = parent.parent
            self.zombie.path.append(child)
        self.zombie.set_target(child)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
