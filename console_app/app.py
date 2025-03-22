import time
import traceback

from funcs import *
from console_app.loadbar import loadbar
from graph import show_graph
from progress_saver import save_progress, load_progress

class App:
    def __init__(self, engine):
        self.engine = engine

    def output_header(self):
        player = self.engine.who_moves
        print(f'{WHITE}Хід %s. Ходить %s' % (self.engine.move + 1, player.props.name))

    def output_progresses(self):
        padding = len(max([player.props.name for player in self.engine.players], key=lambda i: len(i)))

        if all(player.props.target_type == 'moves' for player in self.engine.players) and \
           all(player.props.target == self.engine.players[0].props.target for player in self.engine.players):
            player = self.engine.who_moves

            print(loadbar(player.stats['prev_progress'], player.stats['progress'], 1, 50),
                  convert_to_percents(player.stats['progress']))

            return

        for pl in self.engine.players:
            print(pl.props.name.ljust(padding), loadbar(pl.stats['prev_progress'], pl.stats['progress'], 1, 50),
                  convert_to_percents(pl.stats['progress']))

    def output_section(self):
        player = self.engine.who_moves

        crown = ' ' if (self.engine.move == 0 or self.engine.who_moves != self.engine.leaderboard[0]) else ' 👑 '

        print(f'{WHITE}---{crown}{player.props.name}{crown}---')
        print(f'{WHITE}|{RESET} {'Бали:'.ljust(15)}{WHITE}%s\t%s' % (round(player.stats['score'], 2), add_arrow(player.stats['income'])))
        print(f'{WHITE}|{RESET} {'СерЗар:'.ljust(15)}{WHITE}%s\t%s' % (
        round(player.stats['avg'], 2), add_arrow(player.stats['avg_delta'])))
        print(f'{WHITE}|{RESET} {'Промахи:'.ljust(15)}{WHITE}%s/%s\t%s' % (
        player.stats['loses'], player.stats['shoots'], convert_to_percents(player.stats['lose_rate'])))

        if self.engine.move >= 4:
            print(f'{WHITE}|{RESET} {'Точність:'.ljust(15)}{WHITE}%s\t%s' % (convert_to_percents(player.stats['accuracy']), player.stats['avg_shot']))
            if player.props.target_type == 'score':
                print(f'{WHITE}|{RESET} {"До перемоги:".ljust(15)}{WHITE}{"∞" if player.stats["moves_to_win"] < 0 else "~" + correct_word_form(player.stats["moves_to_win"], ("хід", "ходи", "ходів"))}')
            print(f'{WHITE}|{RESET} {'Звання:'.ljust(15)}{RESET}%s' % color_the_rank(player.stats['accuracy'], player.stats['rank']))
        else:
            moves_to_unlock = 4 - self.engine.move
            moves_to_unlock_correct_form = correct_word_form(moves_to_unlock, ("хід", "ходи", "ходів"))
            print(f'{WHITE}|{RESET} {'Точність:'.ljust(15)}{RED}🔒 {moves_to_unlock_correct_form}')
            print(f'{WHITE}|{RESET} {'До перемоги:'.ljust(15)}{RED}🔒 {moves_to_unlock_correct_form}')
            print(f'{WHITE}|{RESET} {'Звання:'.ljust(15)}{RED}🔒 {moves_to_unlock_correct_form}')

        print(f'{WHITE}|{RESET} {'Монети:'.ljust(15)}{YELLOW}{player.stats['coins']}🪙')

    def output_stats(self):
        self.output_header()
        print()
        self.output_progresses()
        print()
        self.output_section()
        print()
        self.output_leaderboard()

    def minimal_stats(self):
        self.output_header()
        print()
        print('Статистика буде доступна після першого ходу')

    def mainloop(self):
        while not self.engine.is_finished:
            if self.engine.move != 0 and self.engine.who_moves.stats['reached']:
                self.engine.make_move()
                continue

            clear()

            if not self.engine.who_moves.props.autoskip:
                if self.engine.move != 0:
                    self.output_stats()
                else:
                    self.minimal_stats()

                print()

            if self.engine.who_moves.props.bot:
                bot = self.engine.who_moves
                self.engine.make_move()
                if not bot.props.autoskip:
                    input(WHITE + 'Бали: ' + bot.scores[-1] + '\n\nНатисніть на ENTER щоб продовжити')

                continue
                
            res = input(f'{WHITE}Бали: ')
            if res == '':
                clear()
                print(f'{YELLOW}[ ! ] Увага\n\nВи ввели пусте значення')
                if input(f'{WHITE}Підтвердити? [y/n]: ') != 'y':
                    continue

            try:
                if not self.handle_commands(res):
                    self.engine.make_move(res)
                    save_progress('AUTOSAVE', self.engine)
            except Exception as e:
                clear()
                print(f'{RED}[ ! ] Сталася помилка\n')
                print(RED+str(e))
                print(RED+'\nДеталі:')
                print(RED+traceback.format_exc())
                input(f'{WHITE}Натисність ENTER щоб повернутися')
                clear()

        clear()
        self.end()

    def handle_commands(self, command):
        if len(command) == 0 or command[0] != '/':
            return False

        command = command[1:]
        command = command.split()

        match command[0]:
            case 'stop':
                if self.engine.move == 0:
                    self.show_error('Я рекомендую протестити цю команду після першого ходу')
                    return True

                self.engine.stop = True

            case 'save':
                save_progress(command[1], self.engine)

            case 'recover':
                self.engine = load_progress('AUTOSAVE')

            case 'load':
                self.engine = load_progress(command[1])

            case 'stats':
                player = next((player for player in self.engine.players if player.props.name == command[1]), None)
                self.show_info(player.stats)

            case 'props':
                player = next((player for player in self.engine.players if player.props.name == command[1]), None)
                if player:
                    props = vars(player.props)
                    formatted_props = "\n".join(f"{key} : {value!r}" for key, value in props.items())
                    self.show_info(formatted_props)
                else:
                    self.show_error(f"Гравця не знайдено")


            case 'players':
                self.show_info(', '.join([player.props.name for player in self.engine.players]))

            case 'moves':
                player = next((player for player in self.engine.players if player.props.name == command[1]), None)
                self.show_info(player.scores)

            case _:
                self.show_error('Такої команди не існує')

        return True

    def show_error(self, text):
        clear()
        input(f'{RED}[ ! ] Сталася помилка\n\n{text}\n\n{WHITE}Натисніть ENTER щоб продовжити')
        clear()

    def show_info(self, text):
        clear()
        input('%s\n\nНатисніть на ENTER щоб продовжити' % text)
        clear()

    def end(self):
        self.output_leaderboard(False)

        save_name = input('\nВведіть назву збереження (залиште поле пустим, щоб пропустити цей крок): ')
        if save_name != '':
            save_progress(save_name, self.engine)
        clear()

        print(f'{WHITE}=== Графік попадань ===\n')
        
        self.output_shoots_graph()

        input('Натисніть знову на ENTER щоб відкрити графік розвитку (закрийте графік щоб активувати "нескінченну консоль")')
        clear()
        
        show_graph(self.engine.players)

        clear()

        self.inf_console()

    def inf_console(self):
        while 1:
            command = input('--> ')
            try:
                self.handle_commands(command)
            except Exception as e:
                self.show_error(str(e))

    def output_leaderboard(self, show_score=True):
        leaderboard = self.engine.leaderboard
        padding = len(max([player.props.name for player in self.engine.players], key=lambda i: len(i)))+1

        print(f'{WHITE}--- Таблиця балів ---')
        if show_score:
            for i, player in enumerate(leaderboard, 1):
                if i == 1:
                    emoji = '🥇 '
                elif i == 2:
                    emoji = '🥈 '
                elif i == 3:
                    emoji = '🥉 '
                else:
                    emoji = '   '

                if player.stats['reached']:
                    print(f'%s. {emoji}{YELLOW if i == 1 else WHITE}%s{WHITE}🏁 Фінішував 🏁' % (i, player.props.name.ljust(padding)))
                else:
                    print(f'%s. {emoji}{YELLOW if i == 1 else WHITE}%s{WHITE}%s %s' % (i, player.props.name.ljust(padding), round(player.stats['score'], 2), add_arrow(player.stats['income']) ))
        else:
            for i, player in enumerate(leaderboard, 1):
                if i == 1:
                    emoji = '🥇 '
                elif i == 2:
                    emoji = '🥈 '
                elif i == 3:
                    emoji = '🥉 '
                else:
                    emoji = '   '

                print(f'%s. {emoji}{YELLOW if i == 1 else WHITE}%s' % (i, player.props.name))

    def output_shoots_graph(self):
        max_width = 50
        for player in self.engine.players:
            max_count = max(player.stats['shoot_types'].values())
            print(f'{WHITE}--- {player.props.name} ---')
            for shoot in 'b123456789a':
                count = player.stats['shoot_types'][shoot]
                if count == 0:
                    width = 0
                else:
                    width = round(count / max_count * max_width)
                print((GREEN if (count == max_count) else RESET) + f'{shoot}|' + '█'*width + f' {count}')
            print('\n\n')
