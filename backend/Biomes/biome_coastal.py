import random
from tile_types import (
    TILE_SAND,
    TILE_OCEAN,
    TILE_SEAL,
    TILE_CRAB,
    TILE_SHELL,
    TILE_EMPTY,
)
BIOME_NAME = "coastal"

def generate_coastal(width, height):
    tiles = []

    for y in range(height):
        row = []
        for x in range(width):
            r = random.random()

            # Beach gradient: left (x=0) is sand/beach, right (x=width-1) is ocean
            pct = x / max(1, width - 1)

            if pct < 0.3:
                # Left side: mostly sand with some shells.
                # FIX: this used to check `r < 0.35` for sand BEFORE
                # `r < 0.15` for shells. Since every value under 0.15 is
                # also under 0.35, the shell branch could never be reached.
                # Smaller thresholds now come first so each band gets its
                # own real slice of probability.
                if r < 0.10:
                    row.append(TILE_SHELL)
                elif r < 0.40:
                    row.append(TILE_SAND)
                else:
                    row.append(TILE_EMPTY)
            elif pct < 0.6:
                # Middle transition: mix of sand, ocean, and crabs.
                # FIX: same bug here, plus ocean and crab both checked the
                # exact same `r < 0.05` threshold, so crab was unreachable
                # twice over and this whole zone only ever produced sand or
                # empty tiles -- no water in the "transition" strip at all.
                if r < 0.05:
                    row.append(TILE_CRAB)
                elif r < 0.15:
                    row.append(TILE_OCEAN)
                elif r < 0.25:
                    row.append(TILE_SAND)
                else:
                    row.append(TILE_EMPTY)
            else:
                # Right side: mostly ocean with some crabs.
                # FIX: `r < 0.25` for crab was a subset of `r < 0.35` for
                # ocean (checked first), so crabs never spawned here either.
                if r < 0.10:
                    row.append(TILE_CRAB)
                elif r < 0.45:
                    row.append(TILE_OCEAN)
                else:
                    row.append(TILE_EMPTY)

        tiles.append(row)

    return tiles