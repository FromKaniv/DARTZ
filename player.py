from funcs import *
from collections import Counter
from config import ranks
from combinations import is_comb

class Player:
    def __init__(self, props):
        self.props = props
        
        self.stats = {}
        self.scores = []

    def __str__(self):
        return self.props.name

    def make_move(self, res):
        if len(res) > self.props.darts:
            raise ValueError(f'Цей гравець кидає {self.props.darts} дротиків за один хід!')
        res = sort_move(res)

        self.scores.append(self.fill_with_b(res))
        self.update_stats()

    def fill_with_b(self, move):
        return move + 'b'*(self.props.darts - len(move))

    def convert_move(self, move):
        score = 0
        for symbol in move:
            if symbol == 'a':
                score += self.props.center
            elif symbol == 'b':
                score += self.props.lose
            elif symbol.isdigit:
                score += (10-int(symbol) if self.props.antidartz else int(symbol)) ** self.props.exponent * self.props.coeff

        return score

    def get_avg_shot(self):
        shoots = []

        for score in self.scores[-10:]:
            for symbol in score:
                if symbol == 'b':
                    shoots.append(0)
                elif symbol == 'a':
                    shoots.append(10)
                else:
                    shoots.append(int(symbol))

        return avg(shoots)

    def update_stats(self):
        self.stats['move'] = len(self.scores)
        self.stats['incomes'] = [self.convert_move(score) for score in self.scores]
        self.stats['score'] = sum(self.stats['incomes']) + self.props.score
        self.stats['scores'] = [ sum(self.stats['incomes'][:i]) + self.props.score for i in range(self.stats['move']) ]
        self.stats['income'] = self.stats['incomes'][-1]
        self.stats['avg'] = avg(self.stats['incomes'][-10:])
        self.stats['avg_delta'] = self.stats['avg'] if self.stats['move'] == 1 else self.stats['avg'] - avg(self.stats['incomes'][:-1])
        self.stats['loses'] = ''.join(self.scores).count('b')
        self.stats['shoots'] = self.stats['move'] * self.props.darts
        self.stats['lose_rate'] = self.stats['loses'] / self.stats['shoots']
        self.stats['accuracy'] = self.get_avg_shot()/10
        self.stats['avg_shot'] = round(self.stats['accuracy']*10)
        self.stats['reached'] = self.stats['score'] >= self.props.target
        self.stats['rank'] = ranks[-1] if self.stats['avg_shot'] == 10 else ranks[self.stats['avg_shot']]
        self.stats['progress'] = self.stats['score'] / self.props.target
        self.stats['prev_progress'] = 0 if len(self.stats['scores']) == 1 else self.stats['scores'][-1] / self.props.target
        self.stats['shoot_types'] = Counter(''.join(self.scores))
        self.stats['most_common_move'], self.stats['most_common_move_count'] = Counter(self.scores).most_common(1)[0]

        if self.props.target_type == 'score':
            self.stats['reached'] = self.stats['score'] >= self.props.target
            self.stats['progress'] = self.stats['score'] / self.props.target
            self.stats['prev_progress'] = 0 if len(self.stats['scores']) == 1 else self.stats['scores'][-1] / self.props.target
            self.stats['moves_to_win'] = -1 if (self.stats['avg'] == 0) else round((self.props.target - self.stats['score']) / self.stats['avg'])
        else:
            self.stats['reached'] = self.stats['move'] >= self.props.target
            self.stats['progress'] = self.stats['move'] / self.props.target
            self.stats['prev_progress'] = max(0, (self.stats['move']-1) / self.props.target)

        self.stats['coin_reward'], self.stats['comb'] = is_comb(self.scores[-1])

        if 'coins' not in self.stats:
            self.stats['coins'] = self.stats['coin_reward']
        else:
            self.stats['coins'] += self.stats['coin_reward']

    def __getitem__(self, key):
        return self.props[key]
