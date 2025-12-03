BIOME_NAME = "swamp"

def generate_swamp(width, height):
    tiles = []
    for y in range(height):
        row = []
        for x in range(width):
            row.append(TILE_SWAMP)
        tiles.append(row)
    return tiles
