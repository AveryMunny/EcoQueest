import random
from tile_types import (
    TILE_EMPTY,
    TILE_ROCK,
    TILE_STONE,
    TILE_CAVE,
    TILE_ORE,
    TILE_CRYSTAL,
    TILE_SNOW_ROCK,
)

def generate_mountain(width, height):
    tiles = []

    for y in range(height):
        row = []

        # Elevation factor: more snow & crystal higher up
        elevation = y / height

        for x in range(width):

            r = random.random()

            # --------------------------
            # EMPTY SPACE (big increase)
            # --------------------------
            if r < 0.60:
                row.append(TILE_EMPTY)

            # --------------------------
            # COMMON MINEABLE MATERIALS
            # --------------------------
            elif r < 0.75:
                # mostly rock + some stone
                if random.random() < 0.7:
                    row.append(TILE_ROCK)
                else:
                    row.append(TILE_STONE)

            # --------------------------
            # SNOW ROCKS IN HIGH ELEVATION
            # --------------------------
            elif r < 0.80:
                if elevation > 0.5:
                    row.append(TILE_SNOW_ROCK)
                else:
                    row.append(TILE_STONE)

            # --------------------------
            # ORE (rare, but more fun)
            # --------------------------
            elif r < 0.88:
                row.append(TILE_ORE)

            # --------------------------
            # CAVES (rare but present)
            # --------------------------
            elif r < 0.91:
                row.append(TILE_CAVE)

            # --------------------------
            # CRYSTALS (very rare)
            # --------------------------
            elif r < 0.93:
                row.append(TILE_CRYSTAL)

            # --------------------------
            # FALLBACK EMPTY
            # --------------------------
            else:
                row.append(TILE_EMPTY)

        tiles.append(row)

    return tiles
