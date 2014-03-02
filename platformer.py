import pygame
import game
import tileset as tileset
import map as map
import guy as guy

class Platformer(game.Game):

    # name is the title to display on the window
    # width and height are the size of the window, in pixels
    # map_filename is the name of the file that contains the map
    # tiles_filename is the name of the file that contains the tiles
    # tile_size_x and tile_size_y are the dimensions of each tile, in pixels
    # view_size_x and view_size_y are the dimensions of the view, in tiles
    # frames_per_second is the desired frame rate
    def __init__(self, name, map_filename,
                 tiles_filename, tile_size_x, tile_size_y,
                 view_size_x, view_size_y,
                 frames_per_second):
        self.map_filename = map_filename
        self.tiles_filename = tiles_filename
        self.tile_size_x = tile_size_x
        self.tile_size_y = tile_size_y
        self.view_size_x = view_size_x
        self.view_size_y = view_size_y
        game.Game.__init__(self, name,
                           view_size_x * tile_size_x,
                           view_size_y * tile_size_y,
                           frames_per_second)
        
        # initialize the set of tiles
        self.tiles = tileset.Tileset(self.tiles_filename, self.tile_size_x, self.tile_size_y)
        
        # initialize the map
        self.themap = map.Map(self.map_filename, self.tiles, self.screen,
                              self.view_size_x, self.view_size_y)

        # initialize the player
        (size_x, size_y) = self.themap.getSize()
        start_x = self.tile_size_x
        start_y = self.tile_size_y * (size_y - 2)
        self.theguy = guy.Guy(self.tiles, self.themap, self.screen, start_x, start_y)

        
    def game_logic(self, keys, newkeys):
        # adjust horizontal acceleration
        # 1. first apply friction
        self.theguy.friction()

        # 2. then accelerate if left or right keys pressed
        # note: this happens as long as the key is held down
        if pygame.K_LEFT in keys:
            self.theguy.left()
        if pygame.K_RIGHT in keys:
            self.theguy.right()

        # adjust vertical acceleration
        # 1. first apply gravity
        self.theguy.gravity()

        # 2. then jump if user just pushed space or up keys
        if (pygame.K_UP in newkeys) or (pygame.K_SPACE in newkeys):
            self.theguy.jump()

        # apply motion
        self.theguy.move()

    def paint(self, surface):
        # redraw the screen
        self.theguy.repaint()
