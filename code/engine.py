from funcs import *
import bot
import time

class Engine:
    def __init__(self, players):
        self.players = players

        self.total_moves = 0
        self.move = 0
        self.submove = 0

        self.stop = False
        self.finished_players = []

    @property
    def leaderboard(self):
        playing_players = list(sorted(self.players, key=lambda player: player.stats['score'], reverse=True))
        playing_players = list(filter(lambda player: not player.stats['reached'], playing_players))
        res = []
        res.extend(self.finished_players)
        res.extend(playing_players)

        return res

    def make_move(self, res=''):
        for symbol in res:
            if symbol not in '123456789ab':
                raise ValueError('Невірний символ: %s' % symbol)

        if self.who_moves.props.bot:
            res = bot.generate_move(self.who_moves.props.diff, self.who_moves.props.darts)

        if not self.who_moves.stats.get('reached', False):
            self.who_moves.make_move(res)

        if self.who_moves.stats['reached'] and self.who_moves not in self.finished_players:
            self.finished_players.append(self.who_moves)
        
        self.total_moves += 1
        self.move, self.submove = divmod(self.total_moves, len(self.players))

    @property
    def who_moves(self):
        return self.players[self.submove]

    @property
    def is_finished(self):
        return len(self.finished_players) >= len(self.players)-1 or self.stop
