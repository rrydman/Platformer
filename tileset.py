#Ross Rydman 2012

import pygame

class Tileset():
    def __init__(self, filename, tile_size_x, tile_size_y):
        self.tile_size_x = tile_size_x
        self.tile_size_y = tile_size_y
        self.image = pygame.image.load(filename)
        image_size_x, image_size_y = self.image.get_size()
        self.tile_rows = image_size_y/tile_size_y
        self.tile_columns = image_size_x/tile_size_x
        self.tilelist = []
        for y in range(self.tile_rows):
            for x in range(self.tile_columns):
                x_start = x * self.tile_size_x
                y_start = y * self.tile_size_y
                r = pygame.rect.Rect(x_start, y_start, self.tile_size_x, self.tile_size_y)
                self.tilelist.append(self.image.subsurface(r))
        self.tile_count = len(self.tilelist)
    def getTileSize(self):
        return self.tile_size_x, self.tile_size_y
    def getTileCoordsAt(self, x_px, y_px):
        return x_px/self.tile_size_x, y_px/self.tile_size_y
    def getTile(self, tilenumber):
        return self.tilelist[tilenumber]
    def getBackgroundTile(self):
        return self.tilelist[0]
    def getFirstCharacterTileNumber(self):
        return self.tile_columns * 2
    def isSolid(self, tilenumber):
        if tilenumber > self.tile_columns-1 and tilenumber < self.tile_columns * 2 -1:
            return True
        else:
            return False
    def isTrap(self, tilenumber):
        if tilenumber == 12:
            return True
        else:
            return False