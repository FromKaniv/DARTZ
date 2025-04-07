from engine import Engine
from player import Player
from config import players, players_will_play

'''
Типи досягнень

1 - Звичайний
2 - Рідкісний
3 - Епічний
4 - Легендарний

'''

ACHIEVEMENTS = {
    'Перша ашка': lambda player: 'a' in ''.join(player.scores),
    'Дві ашки за один хід!': lambda player: any([move.count('a') >= 2 for move in player.scores]),
    'Три ашки за один хід!!!': lambda player: any([move.count('a') >= 3 for move in player.scores]),
}

class AchievementList:
    def __init__(self, player):
        self.player = player
        self.achieved = []

        self.update()

    def __str__(self):
        if len(self.achieved) == 0:
            return 'Нема досягнень'

        string = ''
        for i, achievement in enumerate(self.achieved, 1):
            string += f'{i}. {achievement}\n'

        return string[:-1]

    def update(self):
        self.achieved = [achievement for achievement in ACHIEVEMENTS if ACHIEVEMENTS[achievement](self.player)]

engine = Engine(
    [Player(players[player]) for player in players_will_play]
)

engine.make_move('aaa')
engine.make_move('abb')

print(AchievementList(engine.players[0]))
print()
print(AchievementList(engine.players[1]))
