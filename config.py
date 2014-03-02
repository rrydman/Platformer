# the name of the game; you are welcome to change this
NAME = 'Zeldrio'

# the name of the file containing the tile graphics
TILES_FILENAME = 'tiles.png'

# the default map file.  you can also provide a name on the command-line when
# running main.py
DEFAULT_MAP_FILENAME = 'jumper.map'

# the size of each tile, in pixels
(TILE_SIZE_X, TILE_SIZE_Y) = (32, 32)

# the size of the display window, in tiles
(VIEW_SIZE_X, VIEW_SIZE_Y) = (15, 15)

# the desired frame rate
FRAMES_PER_SECOND = 60

# how slim is the guy compared to other tiles?  this many pixels on each size
HOWSLIM = 5

# any motion will be rounded up to a multiple of this number of pixels
MINIMUM_PIXELS_PER_FRAME = 2

# how often should the guy's foot be raised and lowered (in pixels)
PIXELS_PER_STEP = 16

# how fast should the guy speed up when an arrow key is pressed
#(in pixels per frame)?
ACCELERATION_PER_FRAME = 1.0

# how fast should friction slow the player down (in pixels per frame)?
FRICTION_PER_FRAME = 0.5

# how fast does gravity pull the player down (in pixels per frame)?
GRAVITY_PER_FRAME = 0.5

# what is the guy's maximum horizontal speed (in pixels per frame)?
MAXIMUM_RATE_X = 8.0

# what is the guy's maximum vertical speed (in pixels per frame)?
MAXIMUM_RATE_Y = 9.0

#Death sound file name
DEATH_SOUND = 'deathsound.wav'