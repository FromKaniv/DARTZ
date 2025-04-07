from config import *
from engine import Engine
from console_app.app import App
from player import Player

App(Engine(
    [Player(players[player]) for player in players_will_play]
)).mainloop()
