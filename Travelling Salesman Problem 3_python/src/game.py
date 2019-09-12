import sys
import time

import pygame
from pygame.constants import *

from Coordinate import Coordinate
from Maze import Maze

BLOCK_SIZE = 32
title = "Ant Colony Optimization"


class AntPlayer:
    speed = 1

    def __init__(self, start_loc):
        self.x = start_loc.x
        self.y = start_loc.y

    def update_loc(self, new_pos):
        self.x = new_pos.x
        self.y = new_pos.y


class MazeDisplay:
    def __init__(self, maze: Maze):
        self.rows = maze.get_width()
        self.columns = maze.get_length()
        self.maze = maze

    def draw(self, display_surf, image_surf):
        for i in range(self.rows):
            for j in range(self.columns):
                if self.maze.walls[i][j] == 0:
                    display_surf.blit(image_surf, (i * BLOCK_SIZE, j * BLOCK_SIZE))


class App:
    ant = 0
    target_fps = 60

    def __init__(self, maze, start_loc):
        self._running = True
        self._display_surf = None
        self._image_surf = None
        self._block_surf = None
        self.oldx = start_loc.x
        self.oldy = start_loc.y
        self.ant = AntPlayer(start_loc)
        self.windowHeight = maze.get_length() * BLOCK_SIZE
        self.windowWidth = maze.get_width() * BLOCK_SIZE
        self.lastupdate = time.time()
        self.maze = MazeDisplay(maze)

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((self.windowWidth, self.windowHeight), pygame.HWSURFACE)

        pygame.display.set_caption('Ant Colony Optimization')
        self._running = True
        self._image_surf = pygame.image.load("ant.png").convert()
        self._block_surf = pygame.image.load("block.png").convert()
        self.lastupdate = time.time()
        self.maze.draw(self._display_surf, self._block_surf)
        return True

    def on_render(self):
        # newclip = pygame.rect.Rect(self.oldx, self.oldy, self.oldx + BLOCK_SIZE, self.oldy + BLOCK_SIZE)
        # print(newclip)
        # self._display_surf.set_clip(newclip)
        self._display_surf.fill((0, 0, 0))
        # self._display_surf.set_clip(None)
        self._display_surf.blit(self._image_surf, (self.ant.x * BLOCK_SIZE, self.ant.y * BLOCK_SIZE))
        # self.oldx = self.ant.x
        # self.oldy = self.ant.y
        self.maze.draw(self._display_surf, self._block_surf)
        pygame.display.flip()

    @staticmethod
    def on_cleanup():
        pygame.quit()

    def update(self, location: Coordinate):
        curr_time = time.time()
        diff = curr_time - self.lastupdate
        delay = max(1.0 / self.target_fps - diff,
                    0)  # if we finished early, wait the remaining time to desired fps, else wait 0 ms!
        time.sleep(delay)
        fps = 1.0 / (delay + diff)  # fps is based on total time ("processing" diff time + "wasted" delay time)
        pygame.display.set_caption("{0}: {1:.2f}".format(title, fps))
        pygame.event.pump()
        keys = pygame.key.get_pressed()

        if keys[K_UP]:
            self.target_fps += 1
        if keys[K_DOWN]:
            if self.target_fps > 1:
                self.target_fps -= 1
            print(self.target_fps)
        if keys[K_SPACE]:
            self.target_fps = 60
        if keys[K_ESCAPE]:
            self.on_cleanup()
            sys.exit(0)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.on_cleanup()
                sys.exit(0)

        self.ant.update_loc(location)
        self.on_render()
        # print("rendering")
        self.lastupdate = curr_time
