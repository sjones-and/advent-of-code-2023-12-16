#!/usr/bin/env python3

import os
from time import perf_counter_ns

class Tile:
    tiles = {}
    max_x = None
    max_y = None

    def connect_all_neighbours():
        Tile.max_y = max(Tile.tiles.keys())
        Tile.max_x = max(Tile.tiles[0].keys())
        for tile_row in Tile.tiles.values():
            for tile in tile_row.values():
                tile.connect_neighbours()

    def reset_all():
        for tile_row in Tile.tiles.values():
            for tile in tile_row.values():
                tile.reset()

    def filter(fn):
        result = []
        for row in Tile.tiles.values():
            for tile in row.values():
                if fn(tile):
                    result.append(tile)
        return result

    def __init__(self, tile_type, x, y):
        self.tile_type = tile_type
        self.x = x
        self.y = y
        self.energised = False
        self.to_left = None
        self.to_right = None
        self.to_top = None
        self.to_bottom = None
        self.left_entrant = False
        self.right_entrant = False
        self.top_entrant = False
        self.bottom_entrant = False
        if not Tile.tiles.get(y, None):
            Tile.tiles[y] = {}
        Tile.tiles[y][x] = self

    def reset(self):
        self.energised = False
        self.left_entrant = False
        self.right_entrant = False
        self.top_entrant = False
        self.bottom_entrant = False

    def connect_neighbours(self):
        if self.x > 0:
            self.to_left = Tile.tiles[self.y][self.x - 1]
        if self.y > 0:
            self.to_top = Tile.tiles[self.y - 1][self.x]
        if self.x < Tile.max_x:
            self.to_right = Tile.tiles[self.y][self.x + 1]
        if self.y < Tile.max_y:
            self.to_bottom = Tile.tiles[self.y + 1][self.x]

    def from_left(self):
        self.energised = True
        if self.left_entrant:
            return []
        self.left_entrant = True
        if self.tile_type in ['-','.'] and self.to_right:
            return [self.to_right.from_left]
        elif self.tile_type == '/' and self.to_top:
            return [self.to_top.from_bottom]
        elif self.tile_type == '\\' and self.to_bottom:
            return [self.to_bottom.from_top]
        elif self.tile_type == '|':
            result = []
            if self.to_top:
                result.append(self.to_top.from_bottom)
            if self.to_bottom:
                result.append(self.to_bottom.from_top)
            return result
        else:
            return []
        
    def from_right(self):
        self.energised = True
        if self.right_entrant:
            return []
        self.right_entrant = True
        if self.tile_type in ['-','.'] and self.to_left:
            return [self.to_left.from_right]
        elif self.tile_type == '\\' and self.to_top:
            return [self.to_top.from_bottom]
        elif self.tile_type == '/' and self.to_bottom:
            return [self.to_bottom.from_top]
        elif self.tile_type == '|':
            result = []
            if self.to_top:
                result.append(self.to_top.from_bottom)
            if self.to_bottom:
                result.append(self.to_bottom.from_top)
            return result
        else:
            return []
        
    def from_top(self):
        self.energised = True
        if self.top_entrant:
            return []
        self.top_entrant = True
        if self.tile_type in ['|','.'] and self.to_bottom:
            return [self.to_bottom.from_top]
        elif self.tile_type == '\\' and self.to_right:
            return [self.to_right.from_left]
        elif self.tile_type == '/' and self.to_left:
            return [self.to_left.from_right]
        elif self.tile_type == '-':
            result = []
            if self.to_left:
                result.append(self.to_left.from_right)
            if self.to_right:
                result.append(self.to_right.from_left)
            return result
        else:
            return []
        
    def from_bottom(self):
        self.energised = True
        if self.bottom_entrant:
            return []
        self.bottom_entrant = True
        if self.tile_type in ['|','.'] and self.to_top:
            return [self.to_top.from_bottom]
        elif self.tile_type == '/' and self.to_right:
            return [self.to_right.from_left]
        elif self.tile_type == '\\' and self.to_left:
            return [self.to_left.from_right]
        elif self.tile_type == '-':
            result = []
            if self.to_left:
                result.append(self.to_left.from_right)
            if self.to_right:
                result.append(self.to_right.from_left)
            return result
        else:
            return []

def answer(input_file):
    start = perf_counter_ns()
    with open(input_file, 'r') as input_stream:
        data = input_stream.read().split('\n')

    range_x = list(range(len(data[0])))
    for iy in range(len(data)):
        for ix in range_x:
            Tile(data[iy][ix], ix, iy)

    Tile.connect_all_neighbours()

    starting_locations = []
    for ix in range(Tile.max_x + 1):
        starting_locations.append(Tile.tiles[0][ix].from_top)
        starting_locations.append(Tile.tiles[Tile.max_y][ix].from_bottom)
    for iy in range(Tile.max_y + 1):
        starting_locations.append(Tile.tiles[iy][0].from_left)
        starting_locations.append(Tile.tiles[iy][Tile.max_x].from_right)

    answer = 0
    while starting_location := starting_locations.pop() if starting_locations else False:
        Tile.reset_all()
        process = [starting_location]
        while to_process := process.pop() if process else False:
            process.extend(to_process())
        answer = max(answer, len(Tile.filter(lambda tile: tile.energised)))

    end = perf_counter_ns()

    print(f'The answer is: {answer}')
    print(f'{((end-start)/1000000):.2f} milliseconds')

input_file = os.path.join(os.path.dirname(__file__), 'input')
answer(input_file)
