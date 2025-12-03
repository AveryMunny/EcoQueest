BIOME_NAME = "tundra"

def generate_tundra(width, height):
    tiles = []
    for y in range(height):
        row = []
        for x in range(width):
            # snowy ground
            row.append(TILE_SNOW)
        tiles.append(row)
    return tiles
