import QuickSort

from TermColours import colours
import locale

def display_overall_points_leaderboard(gender, tournament_circuit):
    if gender == "1":
        players = tournament_circuit.male_circuit_players
    else:
        players = tournament_circuit.female_circuit_players

    print("\n\n")
    print(colours.BEIGE + "=====================================")
    print("|OVERALL RANKKING POINTS LEADERBOARD|")
    print("=====================================" + colours.WHITE)

    # use correct comparison method when performing quick-sort
    for player in players:
        player.compare_overall_points = True
        player.ranking_points = int(player.ranking_points)
    list_of_players = QuickSort.sort(players)
    for player in list_of_players:
        player.ranking_points = str(player.ranking_points)
        player.compare_overall_points = False

    for i, player in enumerate(list_of_players):
        rank = str(i+1)
        points = float(player.ranking_points)
        # String formatting for leader board display
        if i < 9:
            rank = "0" + rank
        if points < 10:
            points = "00" + str(points)
        elif 10 < points < 100:
            points = "0" + str(points)

        print("Rank:[{0}]  Name: {1}  Points: {2:g}".format(rank, player.name, float(points)))
    input("\n--ENTER--\n")

    return tournament_circuit


def display_overall_money_leaderboard(gender, tournament_circuit):
    locale.setlocale( locale.LC_ALL, '' )

    if gender == "1":
        players = tournament_circuit.male_circuit_players

    else:
        players = tournament_circuit.female_circuit_players

    print("\n\n")
    print(colours.BEIGE + "====================================")
    print("|  OVERALL PRIZE MONEY LEADERBOARD  |")
    print("====================================" + colours.WHITE)

    # use correct comparison method when performing quicksort
    for player in players:
        player.compare_overall_prize_money = True
    list_of_players = QuickSort.sort(players)
    for player in players:
        player.compare_overall_prize_money = False


    # string formatting for leaderboard display
    for i, player in enumerate(list_of_players):
        rank = str(i+1)
        money = int(player.prize_money)
        if i < 9:
            rank = "0" + rank
        if money == 0:
            money = "00000   "
        elif money < 100000:
            money = str(money) + "   "
        elif 100000 <= money < 1000000:
            money = str(money) + "  "
        else:
            money = str(money) + " "
    
        print("Rank:[{0}]  Name: {1}  Money: {2}".format(rank, player.name, locale.currency(int(money), grouping=True)))
    input("\n--ENTER--\n")

    return tournament_circuit

