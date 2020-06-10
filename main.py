import pygame as pg
from settings import *
from game import *
from sprites import *
import os

g = Game()
g.Show_Start_Screen()
while True:
    g.New()
    g.Run()
    g.Show_GO_Screen()

pg.quit()