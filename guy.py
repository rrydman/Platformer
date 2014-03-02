import config
import math
import pygame

class Guy():
    def __init__(self, tiles, map, screen, x_px, y_px):
        self.tiles = tiles
        self.map = map
        self.screen = screen
        self.guy_position_x_px = x_px
        self.guy_position_y_px = y_px
        self.guy_dx_px = (float(0))
        self.guy_dy_px = (float(0))
        self.guy_facing_right = True #Direction player is facing. True = right, false = left
        self.guy_foot_up = False
        self.guy_steps_taken = 0
        pygame.mixer.pre_init(44100, -16, 2)
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)

    def pushX(self, ddx):
        max_rate_px = config.MAXIMUM_RATE_X
        self.guy_dx_px += ddx
        if abs(self.guy_dx_px) > max_rate_px:
            if self.guy_dx_px < 0:
                self.guy_dx_px = max_rate_px * -1
            else:
                self.guy_dx_px = max_rate_px
        if self.guy_dx_px > 0:
            self.guy_facing_right = True
        elif self.guy_dx_px < 0:
            self.guy_facing_right = False
    def pushY(self, ddy):
        max_rate_px = config.MAXIMUM_RATE_Y
        self.guy_dy_px += ddy
        if abs(self.guy_dy_px) > max_rate_px:
            if self.guy_dy_px < 0:
                self.guy_dy_px = max_rate_px * -1
            else:
                self.guy_dy_px = max_rate_px
    def left(self):
        apf_px = config.ACCELERATION_PER_FRAME
        self.pushX(apf_px*-1)
    def right(self):
        apf_px = config.ACCELERATION_PER_FRAME
        self.pushX(apf_px)
    def friction(self):
        fpv_px = config.FRICTION_PER_FRAME
        dx_px = self.guy_dx_px
        if dx_px > 0: #If motion greater than zero, push guy left
            if (dx_px - fpv_px) >= 0: #If motion minus friction is positive, apply friction.
                self.pushX(fpv_px * -1)
            else:
                self.pushX(dx_px * -1)
        elif dx_px < 0: #If motion less than zero, push guy right
            if (dx_px - fpv_px) <= 0: #If motion minus friction is positive, apply friction.
                self.pushX(fpv_px)
            else:
                self.pushX(dx_px)
    def gravity(self):
        gpv_px = config.GRAVITY_PER_FRAME
        self.pushY(gpv_px)
    def jump(self):
        max_rate_y_px = config.MAXIMUM_RATE_Y
        if self.feetOnGround() == True:
            self.pushY(max_rate_y_px * -2)
    def roundUp(self, n):
        min_ppf_px = config.MINIMUM_PIXELS_PER_FRAME
        return ((int(math.ceil(n)) + min_ppf_px-1) / min_ppf_px) * min_ppf_px        
    def move(self):
        xpixels = self.roundUp(abs(self.guy_dx_px))
        ypixels = self.roundUp(abs(self.guy_dy_px))
        if self.guy_dx_px < 0:
            xsign = -1
        else:
            xsign = 1
        if self.guy_dy_px < 0:
            ysign = -1
        else:
            ysign = 1
        xmoves = 0
        for i in range(xpixels):
            if xsign == 1:      #Move right
                if self.collision(self.guy_position_x_px+1, self.guy_position_y_px) == False:
                    self.guy_position_x_px += 1
                    self.guy_steps_taken += 1
                else:
                    self.guy_dx_px = 0
                    break
            else:               #Move left
                if self.collision(self.guy_position_x_px-1, self.guy_position_y_px) == False:
                    self.guy_position_x_px -= 1
                    self.guy_steps_taken += 1
                else:
                    self.guy_dx_px = 0
                    break
        for i in range(ypixels):
            if ysign == 1:      #Move down
                if self.collision(self.guy_position_x_px, self.guy_position_y_px+1) == False:
                    self.guy_position_y_px += 1
                else:
                    self.guy_dy_px = 0
                    break
            else:               #Move up
                if self.collision(self.guy_position_x_px, self.guy_position_y_px-1) == False:
                    self.guy_position_y_px -= 1
                else:
                    self.guy_dy_px = 0
                    break
        pps = config.PIXELS_PER_STEP
        steps =  (self.guy_steps_taken + xmoves) % (2*pps) 
        if steps >= 0 and steps < pps:
            self.guy_foot_up = True
        else:
            self.guy_foot_up = False

        if (round(self.guy_dx_px) == 0.0):
            self.guy_foot_up = False
            steps_taken_in_current_state = 0
        if self.feetOnGround() == False:
            self.guy_foot_up = True
            steps_taken_in_current_state = 0
    def collision(self, x_px, y_px):
        left_px = x_px + config.HOWSLIM
        right_px = x_px + self.tiles.tile_size_x - 1 - config.HOWSLIM
        top_px = y_px
        bottom_px = y_px + self.tiles.tile_size_y - 1
        if self.map.isSolidAt(left_px, top_px): #Check for solid at Top left
            return True
        if self.map.isSolidAt(right_px, top_px): #Check for solid at Top right
            return True
        if self.map.isSolidAt(left_px, bottom_px): #Check for solid at Bottom left
            return True
        if self.map.isSolidAt(right_px, bottom_px): #Check for solid at Bottom right
            return True
        return False
    def feetOnGround(self):
        return self.collision(self.guy_position_x_px, self.guy_position_y_px + 1)
    def drawGuy(self):
        tilenum = 0
        #If the guy is facing left and has his foot up, use the first guy tile.
        if self.guy_facing_right == False and self.guy_foot_up == True:
            tilenum = self.tiles.getFirstCharacterTileNumber()
        #If the guy is facing left and has his foot down, use the second guy tile.
        if self.guy_facing_right == False and self.guy_foot_up == False:
            tilenum = self.tiles.getFirstCharacterTileNumber() + 1
        #If the guy is facing right and has his foot down, use the third guy tile.
        if self.guy_facing_right == True and self.guy_foot_up == False:
            tilenum = self.tiles.getFirstCharacterTileNumber() + 2
        #If the guy is facing right and has his foot up, use the fourth guy tile.
        if self.guy_facing_right == True and self.guy_foot_up == True:
            tilenum = self.tiles.getFirstCharacterTileNumber() + 3
        (tile_size_x_px, tile_size_y_px) = self.tiles.getTileSize()
        (view_size_x, view_size_y) = self.map.getViewSize()
        x = (view_size_x - 1) / 2 * tile_size_x_px
        y = (view_size_y - 1) / 2 * tile_size_y_px
        tile = self.tiles.getTile(tilenum)
        self.screen.blit(tile, (x, y))
    def death(self):
        left_px = self.guy_position_x_px + ((self.tiles.tile_size_x - (2 * config.HOWSLIM)) / 2)
        bottom_px = self.guy_position_y_px + self.tiles.tile_size_y + 1
        return self.map.isTrapAt(left_px, bottom_px)
    def repaint(self):
        (tilesize_x, tilesize_y) = self.tiles.getTileSize()
        (size_x, size_y) = self.map.getSize()
        if self.death() == True:
            self.guy_position_x_px = tilesize_x
            self.guy_position_y_px = tilesize_y * (size_y - 2)
            deathsound = pygame.mixer.Sound(config.DEATH_SOUND)
            deathsound.play(loops=0, maxtime=0, fade_ms=0)
        (tile_size_x_px, tile_size_y_px) = self.tiles.getTileSize()
        (view_size_x, view_size_y) = self.map.getViewSize()
        x = self.guy_position_x_px - ((view_size_x / 2) * tile_size_x_px)
        y = self.guy_position_y_px - ((view_size_y / 2) * tile_size_y_px)
        self.map.drawMap(x, y)
        self.drawGuy()

