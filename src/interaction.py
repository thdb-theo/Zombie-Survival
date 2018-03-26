"""Handles all events"""

import sys
from math import pi
import logging
import pygame

import init as _
from options import Options
from bullet import Bullet
from zombie import Zombie
from maths import Vector
from miscellaneous import pause, game_over
from tile import Tile
from drop import full_ammo, Drop


def walking(survivor, keys):
    if survivor.to is not None:  # If the survivor is between two tiles
        return
    if keys[pygame.K_w]:  # North
        future_tile_num = survivor.get_number() - Options.tiles_x
        if Tile.on_screen(0, future_tile_num):
            future_tile = Tile.instances[future_tile_num]
            if future_tile.walkable or "trans" in Drop.actives:
                survivor.set_target(future_tile)
                survivor.rotate(pi / 2)
                survivor.vel = Vector(0, -Options.speed)

    if keys[pygame.K_s]:  # South
        future_tile_num = survivor.get_number() + Options.tiles_x
        if Tile.on_screen(1, future_tile_num):
            future_tile = Tile.instances[future_tile_num]
            if future_tile.walkable or "trans" in Drop.actives:
                survivor.set_target(future_tile)
                survivor.rotate(pi * 3 / 2)
                survivor.vel = Vector(0, Options.speed)

    if keys[pygame.K_d]:  # East
        future_tile_num = survivor.get_number() + 1
        if Tile.on_screen(2, future_tile_num):
            future_tile = Tile.instances[future_tile_num]
            if future_tile.walkable or "trans" in Drop.actives:
                survivor.set_target(future_tile)
                survivor.rotate(0)
                survivor.vel = Vector(Options.speed, 0)

    if keys[pygame.K_a]:  # West
        future_tile_num = survivor.get_number() - 1
        if Tile.on_screen(3, future_tile_num):
            future_tile = Tile.instances[future_tile_num]
            if future_tile.walkable or "trans" in Drop.actives:
                survivor.set_target(future_tile)
                survivor.rotate(pi)
                survivor.vel = Vector(-Options.speed, 0)


def other(screen, survivor):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            logging.debug("key %s", pygame.key.name(event.key))
            if event.key == pygame.K_e:
                survivor.current_gun += 1
                survivor.current_gun %= 4  # loop 0, 1, 2, 3

            if event.key == pygame.K_p:
                pause(screen, Zombie.level)

            if event.key == pygame.K_ESCAPE:
                game_over(screen, Zombie.level)
            if event.key == pygame.K_c and pygame.key.get_mods() & pygame.KMOD_CTRL:
                pygame.quit()
                sys.exit()
            if (Options.debug and event.key == pygame.K_r and
                    pygame.key.get_mods() & pygame.KMOD_CTRL):
                full_ammo(survivor)


def shooting(survivor, keys):

    if keys[pygame.K_LEFT]:
        survivor.rotate(pi)
        Bullet(survivor.centre, Vector(-Options.bullet_vel, 0), survivor.current_gun, survivor)
    elif keys[pygame.K_RIGHT]:
        survivor.rotate(0)
        Bullet(survivor.centre, Vector(Options.bullet_vel, 0), survivor.current_gun, survivor)
    elif keys[pygame.K_UP]:
        survivor.rotate(pi / 2)
        Bullet(survivor.centre, Vector(0, -Options.bullet_vel), survivor.current_gun, survivor)
    elif keys[pygame.K_DOWN]:
        survivor.rotate(pi * 3 / 2)
        Bullet(survivor.centre, Vector(0, Options.bullet_vel),
               survivor.current_gun, survivor)


def interaction(screen, survivor):
    other(screen, survivor)
    keys = pygame.key.get_pressed()
    walking(survivor, keys)
    shooting(survivor, keys)
