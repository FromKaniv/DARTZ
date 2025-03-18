from player_props import Props

target = 500

ranks = ['Мазило',
         'Новачок I',
         'Новачок II',
         'Новачок III',
         'Любитель I',
         'Любитель II',
         'Любитель III',
         'Молодший Експерт',
         'Експерт',
         'Мастер',
         'Великий Дартзер',
]

diffs = {
    'very-easy': (100, 85, 40, 10, 5, 1, 0.1, 0.1**2, 0.1**3, 0.1**4, 0.1**6),
    'easy'     : (50, 50, 75, 100, 40, 10, 2, 0.5, 0.1**2, 0.1**3, 0.1**4),
    'medium'   : (15, 20, 25, 30, 90, 100, 90, 60, 30, 10, 0.01),
    'hard'     : (10, 2, 4, 8, 16, 30, 60, 90, 100, 75, 1),
    'very-hard': (1, 0.1, 0.2, 0.5, 1, 4, 10, 25, 80, 100, 5),
    'champion' : (0.01, 0.01, 0.02, 0.05, 0.5, 1, 2, 4, 10, 100, 50),
    'random': (100,)*10 + (1,)
}

players = {
    'Vova': Props(
        name = 'Vova',
    ),

    'Taras': Props(
        name = 'Taras',
    ),

    'Alpha': Props(
        name = 'Alpha',
        bot = True,
        diff = diffs['champion'],
        autoskip = False,

    )
}

players_will_play = ['Vova', 'Taras', 'Alpha', 'Alpha']
