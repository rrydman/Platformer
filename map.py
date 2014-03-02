#Ross Rydman 2012

class Map():
    def __init__(self, filename, tiles, screen, view_x, view_y):
        self.filename = filename
        self.tiles = tiles
        self.screen = screen
        self.view_x = view_x
        self.view_y = view_y
        f = open(filename, 'r')
        fcontents = f.read()
        self.map = eval(fcontents)
        f.close()
        self.rows = len(self.map)
        self.columns = len(self.map[0])
    def getSize(self):
        return self.columns, self.rows
    def getViewSize(self):
        return self.view_x, self.view_y
    def getTileNumber(self, x, y):
        if x < 0 or y < 0:
            return None
        if x > self.columns-1 or y > self.rows-1:
            return None
        if x == 0:
            return self.map[y][0]
        if y == 0:
            return self.map[0][x]
        else:
            return self.map[y][x]
    def getTileNumberAt(self, x_px, y_px):
        tile_x, tile_y = self.tiles.getTileCoordsAt(x_px,y_px)
        return self.getTileNumber(tile_x, tile_y)
    def getTile(self, x, y):
        tilenum = self.getTileNumber(x,y)
        if tilenum == None:
            return self.tiles.getBackgroundTile()
        else:
            return self.tiles.getTile(tilenum)
    def isSolidAt(self, x_px, y_px):
        tilenum = self.getTileNumberAt(x_px,y_px)
        if self.tiles.isSolid(tilenum) == True or tilenum == None:
            return True
        else:
            return False
    def isTrapAt(self, x_px, y_px):
        tilenum = self.getTileNumberAt(x_px,y_px)
        if self.tiles.isTrap(tilenum) == True:
            return True
        else:
            return False
    def drawMap(self, left_px, top_px):
        (tile_size_x_px, tile_size_y_px) = self.tiles.getTileSize()
        (corner_x, corner_y) = (left_px / tile_size_x_px, top_px / tile_size_y_px)
        (offset_x, offset_y) = (left_px % tile_size_y_px, top_px % tile_size_y_px)
        for screen_y in range(0, (self.view_y+1)):
            map_y = screen_y + corner_y
            for screen_x in range(0, (self.view_x+1)):
                map_x = screen_x + corner_x
                tile = self.getTile(map_x, map_y)
                self.screen.blit(tile, (screen_x * tile_size_x_px - offset_x, screen_y * tile_size_y_px - offset_y))