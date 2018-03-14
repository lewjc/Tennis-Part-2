import locale
import random
import Menu
import QuickSort

from TournamentClasses import *

def input_results(tournament, ranking_points):
    # Used for money formatting at torunament display start
    locale.setlocale( locale.LC_ALL, '' )

    input_from_file = False
    
    players = tournament.players
    tournament_difficulty = tournament.difficulty
    prize_money = tournament.prize_money

    # Manipulate money for better output
    prize_money_string = locale.currency(int(prize_money["4"]), grouping=True)

    # output tournament info
    print("==========================================================================")
    print("\n[{0} - {1}] Players: {2} | Top Prize: {3} | Difficulty: {4} \n".format(tournament.tournament_code, tournament.gender,
                                                                           len(players),
                                                                           prize_money_string,
                                                                           tournament_difficulty))
    print("==========================================================================\n")
    input("--Press ENTER to start--\n")

 
    # enumerate through the list of matches in the tournament
    for round_number, current_round in enumerate(tournament.list_of_rounds):

        # if user has not finished inputting results yet, loop until we are back to the current round
        if(round_number < tournament.current_input_round):
            continue
    
        # get user choice for input method

        print_input_menu()

        # wait for user input
        while True:            
            user_choice = Menu.get_user_choice()
            if user_choice == '1':
                input_from_file = True
                break
            elif user_choice == '2':
                input_from_file = False
                break
            elif user_choice == '3':
                print_current_prize_money_ranking(tournament.players)
                print_input_menu()
                continue
            elif user_choice == '4':
                print_current_points_ranking(tournament.players)
                print_input_menu()
                continue
            elif user_choice == '5':
                return (round_number,list())
            else:
                print('Invalid Input')

        round_text = '      ROUND : {0}     '.format(round_number + 1)

        if((round_number) == tournament.amount_of_rounds - 1):
            round_text = '        FINAL           '

        print('======================')
        print(round_text)
        print('======================\n')
            
        # Loop through all of the matches in the round
        for match in current_round.list_of_matches:

            # randmoise display input, makes it look better. 
            display_descision = random.randint(1,2)
            if input_from_file:
                if(display_descision == 1):

                    player_one = match.winner
                    player_one_score = match.winner_score
                    player_two = match.loser
                    player_two_score = match.loser_score

                else:

                    player_one = match.loser
                    player_one_score = match.loser_score
                    player_two = match.winner
                    player_two_score = match.winner_score
            else:
                # User input manually
                pass

            # Output info about the winner and loser
            print('{0} Score: {1} {2} Score: {3}'.format(player_one, player_one_score, player_two,
                                                         player_two_score)) 

            print('Winner - {0}\n'.format(match.winner))

            # Get the actual player object from the 
            temp = [player for player in tournament.players if player.name == match.winner]
            winning_player = temp[0]
            
            winning_player.tournament_points += (float(ranking_points[str(round_number)]) * float(Match.multiply_points(match.score_difference, tournament.gender)))

            # If we are on the thid round of result input, then we need to start allocating prize money
            if round_number > 0:
                winning_player.tournament_money = prize_money[str(round_number)]

        # Increment current round
        tournament.current_input_round = round_number + 1

    
    pass 
    # After the results are fully Input
    for player in players:
        player.tournament_points = float(player.tournament_points) * tournament_difficulty

    print_current_points_ranking(players)
    print_current_prize_money_ranking(players)

    tournament.complete = True

    return (None, players)

def print_current_prize_money_ranking(players):
    QuickSort.sort(players)
    print('\n============================')
    print("Current Prize Money Rankings")
    print('============================\n')

    for player in players:
        print(" Name: {0} Prize Money: {1}".format(player.name, player.tournament_money))
    print()

def print_current_points_ranking(players):
    QuickSort.sort(players)
    print('\n============================')
    print("Current Tournament Rankings")
    print('============================\n')

    for player in players:
        print(" Name: {0} Points: {1:g}".format(player.name, player.tournament_points))
    print()

def print_input_menu():

    print('[Input Menu]\n')
    print("[1] Input next round from file")
    print("[2] Input next round manually")
    print("[3] Display current prize money rankings")
    print("[4] Display current ranking points rankings")
    print("[5] Return")
