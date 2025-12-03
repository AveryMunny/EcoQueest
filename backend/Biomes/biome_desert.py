BIOME_NAME = "desert"

def generate_desert(width, height):
    tiles = []
    for y in range(height):
        row = []
        for x in range(width):
            row.append(TILE_SAND)
        tiles.append(row)
    return tiles
