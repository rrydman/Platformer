#!/usr/bin/python

import sys
import config
import platformer

def main():
    # check the command-line arguments
    if len(sys.argv) == 2:
        map_filename = sys.argv[1]
    else:
        map_filename = config.DEFAULT_MAP_FILENAME

    pg = platformer.Platformer(config.NAME,
                               map_filename,
                               config.TILES_FILENAME,
                               config.TILE_SIZE_X, config.TILE_SIZE_Y,
                               config.VIEW_SIZE_X, config.VIEW_SIZE_Y,
                               config.FRAMES_PER_SECOND)

    pg.main_loop()
    
main()
