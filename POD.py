#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 10 15:18:45 2018

@author: tomas
"""

import pygame
from pygame.locals import *
import os
import time
import random

pygame.init()
pygame.font.init()

# Funções
def get_level_str(file_path, level):
    file = open(file_path)
    levels = file.readlines()
    return levels[level]


def get_starting_pos(astring):
    x = int(astring[:2])-1
    y = int(astring[2:4])-1
    return (y, x)

def create_matrix(astring):
    matrix_str = astring[4:]
    matrix = []
    for i in range(12):
        row = []
        for j in range(12):
            row.append(matrix_str[i*12 + j])
        matrix.append(row)
    return matrix

def count_tiles(matrix):
    n = 0
    for line in matrix:
        for i in line:
            if i in ('1', '2', '3'):
                n += int(i)
    return n

# Recursos
player = pygame.image.load("data/graphics/player.bmp")
tiles = [pygame.image.load("data/graphics/tile%d.bmp" % i) for i in range(1, 7)]
for surface in [player] + tiles:
    surface.set_colorkey((255, 0, 255))
font = pygame.font.SysFont('Comic Sans MS', 30)

# Janela
tile_width = 50
tile_height = 50
window_width = 12*tile_width
window_height = 13*tile_height
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("POD clone")

def start_menu():
    has_continue = os.path.exists("user.txt")
    if has_continue:
        texts = ('Continue', 'Start New Game', 'Quit')
        first_menu = 0
    else:
        texts = ('Start New Game', 'Quit')
        first_menu = 1
    total_menus = len(texts)
    texts = [font.render(text, False, (255, 255, 255)) for text in texts]
    choice = 0
    while True:
        # desenhar
        window.fill((0, 0, 0))
        for i, text in enumerate(texts):
            if choice == i:
                window.blit(player, (120, 160 + i*60))
            window.blit(text, (200, 180 + i*60))
        pygame.display.flip()

        # eventos
        event = pygame.event.wait()
        if event.type == QUIT:
            return 2
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return 2
            elif event.key == pygame.K_UP:
                choice = (choice-1) % total_menus
            elif event.key == pygame.K_DOWN:
                choice = (choice+1) % total_menus
            elif event.key == pygame.K_RETURN:
                return choice + first_menu

def game_loop(level):
    level_str = get_level_str('data/levels/series1.pod', level)
    player_x, player_y = get_starting_pos(level_str)
    matrix = create_matrix(level_str)
    number_to_beat = count_tiles(matrix)
    text = font.render("Nível: {}/20".format(level + 1), False, (255, 255, 255))
    stars = []
    for _ in range(1000):
        x = random.randrange(12*tile_width)
        y = random.randrange(12*tile_height)
        stars.append((x, y))

    won = False
    while not won:
        # Desenhar
        window.fill((0, 0, 0))
        for star in stars:
            window.set_at((star[0], star[1]), (128, 128, 128, 255))
        for y in range(12):
            for x in range(12):
                tile = int(matrix[y][x])
                if tile > 0:
                    tile = tiles[tile-1]
                    window.blit(tile, (x*tile_width, y*tile_height))
        window.blit(player, (player_x*tile_width, player_y*tile_height))
        window.blit(text, (0, window_height - tile_height))
        pygame.display.flip()

        # Eventos
        old_player_x = player_x
        old_player_y = player_y

        event = pygame.event.wait()
        if event.type == QUIT:
            return False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False
            if event.key == pygame.K_LEFT:
                player_x -= 1
            if event.key == pygame.K_RIGHT:
                player_x += 1
            if event.key == pygame.K_UP:
                player_y -= 1
            if event.key == pygame.K_DOWN:
                player_y += 1

        if old_player_x != player_x or old_player_y != player_y:
            if matrix[old_player_y][old_player_x] == "5":
                player_x, player_y = get_starting_pos(level_str)
            if player_x < 0 or player_x >= 12 or player_y < 0 or player_y >= 12 or matrix[player_y][player_x] == "0":
                # nao permitir mover para ali
                player_x = old_player_x
                player_y = old_player_y
            elif matrix[old_player_y][old_player_x] in ('1', '2', '3'):
                matrix[old_player_y][old_player_x] = str(int(matrix[old_player_y][old_player_x])-1)
                number_to_beat -= 1
                if number_to_beat <= 0:
                    won = True
    return True

pygame.event.set_allowed(None)
pygame.event.set_allowed(pygame.QUIT)
pygame.event.set_allowed(pygame.KEYDOWN)
pygame.key.set_repeat(1, 150)

current_level = 5
while True:
    choice = start_menu()
    if choice == 0:
        current_level = int(open('user.txt').read())
    elif choice == 1:
        current_level = 0
    elif choice == 2:
        break
    while game_loop(current_level):
        if current_level == 19:
            break

        else:
            current_level += 1
        with open("user.txt", "w") as save_file:
            save_file.write(str(current_level))
pygame.quit()
