import Menu

import QuickSort

from TermColours import colours

from TournamentClasses import Player

import locale

def display_overall_points_leaderboard(gender, tournament_circuit, season_number, season_one_circuit=None):


    season_to_display = determine_what_season_to_display(season_number)

    # If we are viewing season 1
    if season_to_display == '1' or season_to_display == '2':
    
        if season_number == 1 and season_one_circuit == None and season_to_display == '1':
            circuit = tournament_circuit
    
        elif season_number == 2 and season_one_circuit != None and season_to_display == '1':
            circuit = season_one_circuit

        elif season_number == 2 and season_one_circuit != None and season_to_display == '2':
            circuit = tournament_circuit
        
        if gender == "1":
            players = circuit.male_circuit_players
        else:
            players = circuit.female_circuit_players
    # We are combining both seasons
    else:
        overall_players = list()
        if gender == "1":
            players = tournament_circuit.male_circuit_players
            season_one_players = season_one_circuit.male_circuit_players
        else:
            players = tournament_circuit.female_circuit_players
            season_one_players = season_one_circuit.female_circuit_players

    # We are combining both seasons
        for player in players:
            for season_one_player in season_one_players:
                if player == season_one_player:
                    player_with_both_points = Player(player.name) 
                    player_with_both_points.ranking_points = int(player.ranking_points) + int(season_one_player.ranking_points)
                    overall_players.append(player_with_both_points)

        players = overall_players    
    

    print("\n SEASON {}\n".format(season_to_display if season_to_display == '1' or season_to_display == '2' else 'BOTH')) 
    print(colours.BEIGE + "=====================================")
    print("|OVERALL RANKKING POINTS LEADERBOARD|")
    print("=====================================\n" + colours.WHITE)

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


def display_overall_money_leaderboard(gender, tournament_circuit, season_number, season_one_circuit=None):

    season_to_display = determine_what_season_to_display(season_number)

    # If we are viewing season 1
    if season_to_display == '1' or season_to_display == '2':
        if season_number == 1 and season_one_circuit == None and season_to_display == '1':
            circuit = tournament_circuit
        elif season_number == 2 and season_one_circuit != None and season_to_display == '1':
            [print(player.prize_money) for player in season_one_circuit.male_circuit_players]
            circuit = season_one_circuit
        elif season_number == 2 and season_one_circuit != None and season_to_display == '2':
            circuit = tournament_circuit
        
        if gender == "1":
            players = circuit.male_circuit_players
        else:
            players = circuit.female_circuit_players
    # We are combining both seasons
    else:
        overall_players = list()
        if gender == "1":
            players = circuit.male_circuit_players
            season_one_players = season_one_circuit.male_circuit_players
        else:
            players = circuit.female_circuit_players
            season_one_players = season_one_circuit.female_circuit_players

    # We are combining both seasons
        for player in players:
            for season_one_player in season_one_players:
                if player == season_one_player:
                    player_with_both_money = Player(player.name) 
                    player_with_both_money.prize_money = player.prize_money + season_one_player.prize_money
                    overall_players.append(player_with_both_money)

        players = overall_players    

    locale.setlocale( locale.LC_ALL, '' )

    print(colours.BEIGE + "====================================")
    print("|  OVERALL PRIZE MONEY LEADERBOARD  |")
    print("====================================\n" + colours.WHITE)

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


def determine_what_season_to_display(season_number):
    print('[What overall rankings would you like to view?]\n'.upper())
    print('[1] Season 1')
    print(Menu.strike('[2] Season 2')) if season_number != 2 else print('[2] Season 2')
    print(Menu.strike('[3] Both Seasons')) if season_number != 2 else print('[3] Both Seasons') 

    season_choice = Menu.get_user_choice()
    
    if season_choice == '1' or ((season_choice == '2' or season_choice == '3') and season_number == 2):

        return season_choice
    else:
        input('Invalid Choice \n')
        Menu.clear_terminal()
        return determine_what_season_to_display(season_number)
