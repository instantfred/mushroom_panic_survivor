# src/map_layout.py
# "X" = solid ground/wall
# "P" = player spawn
# "E" = enemy spawn point
# "." = empty space (walkable)
# "W" = water/hazard
# "C" = chest

level_map = [
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "X.....E..............E...........E...............X",
    "X................................................X",
    "X........XXXXX..........XX.XX...........XXXXX....X",
    "X............X..........X...X...........X........X",
    "X....E.......X....E.....X...X.....E.....X........X",
    "X........XXXXX..........XXXXX...........XXXXX....X",
    "X................................................X",
    "X................................................X",
    "X................................................X",
    "X................................................X",
    "X................................................X",
    "X................................................X",
    "X................................................X",
    "X................................................X",
    "X........XXXXX..........XXXXX...........XXXXX....X",
    "X............X..........X...X...........X........X",
    "X....E.......X....E.....X...X.....E.....X........X",
    "X........XXXXX..........XX.XX...........XXXXX....X",
    "X................................................X",
    "X.....E..............E...........E...............X",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
]

# Add some chests in strategic locations
chest_positions = [
    (15, 5),   # Top room
    (35, 5),   # Top right
    (15, 15),  # Bottom left
    (35, 15),  # Bottom right
    #(25, 10),  # Center
]

# Place chests in the map
# for x, y in chest_positions:
#     row = list(level_map[y])
#     row[x] = 'C'
#     level_map[y] = ''.join(row)
