import matplotlib.pyplot as plt

def show_graph(players):
    plt.figure(figsize=(10, 5))

    for player in players:
        moves = range(1, player.stats['move'] + 1)
        plt.plot(moves, player.stats['scores'], marker='o', label=player.props.name)

    # Labels and legend
    plt.xlabel("Ходи")
    plt.ylabel("Бали")
    plt.title("Графік розвитку гравців")
    plt.legend()
    plt.grid(True)

    # Show the graph
    plt.show()
