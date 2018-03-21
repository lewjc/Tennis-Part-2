import locale
import random
import Menu
import QuickSort
import sys
import FileManager
from TermColours import colours
import re

from TournamentClasses import *

def input_results(tournament, tournament_circuit, season_number, season_one_players=None, season_one_tournament=None):

    if season_number == 2:
        season_two = True
        print(tournament.overall_rankings)
    else: 
        season_two = False

    # Used for money formatting at torunament display start
    locale.setlocale( locale.LC_ALL, '' )

    input_from_file = False
    
    players = tournament.players
    tournament_difficulty = tournament.difficulty
    prize_money = tournament.prize_money
    ranking_points = tournament_circuit.ranking_points

    # Manipulate money for better output
    prize_money_string = locale.currency(int(prize_money["4"]), grouping=True)

    # output tournament info
    print(colours.BEIGE + "==========================================================================")
    print("\n[{0} - {1}] Players: {2} | Top Prize: {3} | Difficulty: {4} \n".format(tournament.tournament_code, tournament.gender,
                                                                           len(players),
                                                                           prize_money_string,
                                                                           tournament_difficulty))
    print("==========================================================================\n" + colours.ENDC + colours.WHITE)
    input("--Press ENTER to start--\n")

    
    if tournament.current_input_round >= 1:
        print('LOADING')
        load_current_tournament_rankings(tournament)

    # enumerate through the list of matches in the tournament
    for round_number, current_round in enumerate(tournament.list_of_rounds):
        # if user has not finished inputting results yet, loop until we are back to the current round

        if(round_number < tournament.current_input_round):
            continue
    
        # get user choice for input method

        print_input_menu(round_number, tournament.import_from_file_disabled)

        # wait for user input
        while True: 

            user_choice = Menu.get_user_choice()
            if user_choice == '1' and not tournament.import_from_file_disabled:
                input_from_file = True
                break
            elif user_choice == '1' and tournament.import_from_file_disabled and not season_two:
                print('You have previously chosen to input results from file. This option is disabled because the system '  
                      'cannot guarantee\n you have input results which will be the same as the results the system has on file.\n')
                continue
            elif user_choice == '1' and season_two:
                print('You are unable to import results from file in season 2 as we do not have any results on file for it.\n')
                continue    
            elif user_choice == '2' and not tournament.import_from_file_disabled:
                print('By selecting to input from the results yourself, you are voiding the rest of the scores for ' +
                    'this tournament stored in the file system\nYou are unable to import results from file from here on out for this tournement.\ncontinue? [Y/N]')
                  # Once the user has chosen to input the results themselves, they can no longer import from file because
            # the data may be different to that on file.
                while True:
                    void_file_inputs = Menu.get_user_choice()
                    if void_file_inputs.lower() == 'y':
                        input_from_file = False
                        tournament.import_from_file_disabled = True
                        continue_menu = False
                        break
                    elif void_file_inputs.lower() == 'n':
                        continue_menu = True
                        break
                    else:
                        print('Invalid choice')
                        continue
                
                if continue_menu:
                    print('Please make menu choice')
                    continue
                else:
                    break
            # If user wants to input from file 
            elif user_choice == '2' and tournament.import_from_file_disabled:
                input_from_file = False
                break
            # If user wants to view the tournament prize money
            elif user_choice == '3':
                print_current_prize_money_ranking(tournament.players)
                print_input_menu(round_number, tournament.import_from_file_disabled)
                continue
            elif user_choice == '4':
                print_current_points_ranking(tournament.players)
                print_input_menu(round_number, tournament.import_from_file_disabled)
                continue
            elif user_choice == '5':
                save_current_tournament_rankings(tournament)
                return (round_number, tournament.players)
            else:
                print('Invalid Input')
        
        round_text = '      ROUND : {0}     '.format(round_number + 1)

        if((round_number) == tournament.amount_of_rounds - 1):
            round_text = '        FINAL           '

        print(colours.BEIGE + '======================')
        print(round_text)
        print('======================\n ' + colours.ENDC + colours.WHITE)
            
        # Loop through all of the matches in the round
        for i,match in enumerate(current_round.list_of_matches):
            # randmisse display input, makes it look better. 
            display_descision = random.randint(1,2)

            if input_from_file:
                # Randomise player display
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
                # Manual Input

                # Display players available in round
                print('Players available in this round:\n')
                if len(current_round.list_of_players) == 0:
                    break

                player_menu = {i : player for i, player in enumerate(current_round.list_of_players)}
                count = 0
                
                for j, (k,v) in enumerate(player_menu.items()):   
                    print('[{0}] {1} '.format(f"{k:02}",v),end='')
                    if (j + 1) % 4 == 0 or j == len(player_menu.items()) - 1:
                        print()

                if season_two and current_round.number == 1:
                   print('\nPick one player from the list using their positon, for example 1 is the first person in the list.')
                else:    # Let user choose 2 players
                    print('\nPick 2 players, using their position in the list. write in format 1,2 for example.\n')

                # get user's choice of players 
                while True:

                    choice = Menu.get_user_choice()

                    if season_two and re.search('^(\d*)$', choice) and current_round.number == 1:

                        player_one_index = int(choice)

                        if player_one_index in player_menu.keys():
                            player_one = current_round.list_of_players[player_one_index]
                            player_in_first_16 = [player.in_first_16 for player in season_one_players if player == player_one]

                            available_players = [player for player in season_one_players if (player.name in current_round.list_of_players) and  ((player.in_first_16 and not player_in_first_16[0]) or (player_in_first_16[0] and not player.in_first_16))]

                            player_menu = {i : player.name for i, player in enumerate(available_players)}

                            print('Pick another player from the available players list Below.\n')

                            for j, (k,v) in enumerate(player_menu.items()):   
                                print('[{0}] {1} '.format(f"{k:02}",v),end='')
                                if (j + 1) % 4 == 0 or j == len(player_menu.items()) - 1:
                                    print()
                                    
                            while True:

                                second_choice = Menu.get_user_choice()

                                if re.search('^(\d*)$', second_choice):
                                    try: 
                                        if int(second_choice) in player_menu.keys():
                                            player_two_index = int(second_choice)
                                            player_two = available_players[player_two_index].name
                                            break
                                        else:
                                            print('Invalid player choice')
                                    except ValueError:
                                        print('Invalid option')
                                        continue
                                else:
                                    print('Invalid Choice')         
                            break
                                
                        else:
                            print('Invalid player choice')

                    elif (re.search('^(\d*),(\d*)$', choice)) and (not season_two and current_round.number == 1) or (season_two and current_round.number > 1):
                        match_players = choice.split(',')
                        try:
                            player_one_index = int(match_players[0])
                            player_two_index = int(match_players[1])
                        except ValueError:
                            print('[Invalid player choice]')
                            continue

                        # 
                        if player_one_index in player_menu.keys() and player_two_index in player_menu.keys() and  player_one_index != player_two_index:
                            player_one = current_round.list_of_players[player_one_index]
                            player_two = current_round.list_of_players[player_two_index]         

                            # if we are on round 1 of season 2 we need to make sure that these players were not in the last 16
                            if season_two and current_round.number == 1:  
                                # Get the player record of if they were in the first 16 and 
                                player_one_in_first_16 = [player.in_first_16 for player in season_one_players if player == player_one]
                                player_two_in_first_16 = [player.in_first_16 for player in season_one_players if player == player_two]

                                if player_one_in_first_16[0] and player_two_in_first_16[0]:
                                    print('\n[Both {0} and {1} were in the first 16 of season 1. please choose a different pairing in format 1,2 for example]\n'.format(player_one, player_two))
                            # If we are inputting season 2 rounds, we need to check positions of the last tournaments
                                    continue
                            elif season_two and 1 < current_round.number < 5:
                                next_round = current_round.number
                                # Get the next round of this one but in season 2
                                season_one_round = season_one_tournament.list_of_rounds[next_round]
                                played_each_other = False 

                                # Compare the matches of the last season round and if these players have already played each other, they cannot play 
                                # eachother again

                                for match in season_one_round.list_of_matches:
                                    played_each_other = True if match.winner == player_one and match.loser == player_two or match.winner == player_two and match.loser == player_one else False
                                   
                                    if played_each_other:
                                        break

                                if played_each_other:
                                    print('\n[These players played each other in Round {0} of season 1, please choose a different pairing in format 1,2 for example]\n'.format(current_round.number + 1))
                                    continue
                        else:
                            print('Invalid player choice')
                            continue
                        break
                    else:
                        print('Invalid')
                
                # Get the user to input the scores for the match.
                match_results = user_input_score(tournament.gender, player_one, player_two)
                
                # Allocate winner and loser from the user input score

                match.winner = player_one = match_results[0]
                match.winner_score = player_one_score = match_results[1]
                match.loser = player_two = match_results[2]
                match.loser_score = player_two_score = match_results[3]
                # Print new line before result is displayed.
                print()

            # If match is incorrect
            if(match.is_invalid):
                print_match(player_one, player_one_score, player_two, player_two_score)
                # TODO: Only ask if not on round 5
                print('\nThis result is invalid, should the system correct itself? [Y/N]')
                # Ask user if they would like to correct the score themselves or have the system do it.
                score_corrected = False
                while True:
                    if score_corrected:
                        break

                    user_choice = Menu.get_user_choice()
                    # The system will correct the score.
                    if user_choice.lower() == 'y':
                       new_match_results = correct_invalid_score(round_number, tournament.list_of_rounds, player_one, player_two, tournament.gender)

                       match.winner = new_match_results[0]
                       match.winner_score = new_match_results[1]
                       match.loser = new_match_results[2]
                       match.loser_score = new_match_results[3]
                       score_corrected = True
                    # User wants to correct the score themselves.
                    elif user_choice.lower() == 'n':

                        print('By choosing to manually correct the score, you are voiding the rest of the scores that are on file for this tournament.\n'
                              'You will be unable to import scores for the rest of the tournament and must type remaining scores in manually.\nPress [Y] to confirm, any other key to let the system correct the error.')
                       
                        user_choice = Menu.get_user_choice()
                        # The user wants to correct the score themselves. 
                        if user_choice.lower() == 'y':

                            tournament.import_from_file_disabled = True
                            print('The result is invalid, was Either player injured?')
                            print('[1] {0}\n[2] {1}\n[0] No'.format(player_one, player_two))

                            while True:
                                # Check if a player is injured, if not get the user to correct the score.
                                user_input = Menu.get_user_choice()
                                # Player is injured
                                if(user_input =='1' or user_input == '2'):
                                    
                                    match_results = player_is_injured(user_input, tournament.gender, player_one, player_two)

                                    if match_results == 0:
                                        # Should never occur, here just in case.
                                        print('Invalid user input given - {}'.format(user_input))
                                    else:
                                        input(match_results[0])
                                        match.winner = match_results[0]
                                        match.winner_score = match_results[1]
                                        match.loser = match_results[2]
                                        match.loser_score = match_results[3]
                                        score_corrected = True
                                     
                                        for i in range((round_number + 1), len(tournament.list_of_rounds)):
                                            round_list_of_players = tournament.list_of_rounds[i].list_of_players
                                            if match.loser in round_list_of_players:
                                                loser_index = round_list_of_players.index(match.loser)
                                                round_list_of_players[loser_index] = match.winner

                                        break

                                # If there were no injuries, get the user to correct the score
                                elif user_input == '0':                           
                                    # This get score input and processes the scores and 
                                    # determines whether or not it is a valid score line.

                                    match_results = user_input_score(tournament.gender, player_one, player_two)

                                    if match_results == 0:
                                        # match results are incorrect
                                        print('Invalid score given')
                                    else:
                                        match.winner = match_results[0]
                                        match.winner_score = match_results[1]
                                        match.loser = match_results[2]
                                        match.loser_score = match_results[3]

                                        for i in range((round_number + 1), len(tournament.list_of_rounds)):
                                            round_list_of_players = tournament.list_of_rounds[i].list_of_players
                                            if match.loser in round_list_of_players:
                                                loser_index = round_list_of_players.index(match.loser)
                                                round_list_of_players[loser_index] = match.winner

                                        score_corrected = True

                                    # This ends the loop for sorting out invalid matches.
                                    break
                                else:
                                    print('Invalid choice')
                            # Prints new line, meny looks cleaner 
                            print()
                        else:
                            # the user wants the system to correct the invalid score.
                            new_match_results = correct_invalid_score(round_number, tournament.list_of_rounds, player_one, player_two, tournament.gender)
                       
                            match.winner = new_match_results[0]
                            match.winner_score = new_match_results[1]
                            match.loser = new_match_results[2]
                            match.loser_score = new_match_results[3]

                            score_corrected = True

                    else:
                        print('Invalid Choice')
                
                print_match(match.winner, match.winner_score, match.loser, match.loser_score)
            else:
                 # If the match is alll okay
                print_match(player_one, player_one_score, player_two, player_two_score)
                
            # Output info about the winner and loser
         
            print(colours.GREEN + colours.BLINK + 'Winner - {0}\n'.format(match.winner) + colours.ENDC + colours.WHITE)

            current_round.list_of_players.remove(match.winner)
            current_round.list_of_players.remove(match.loser)

            # Get the actual player object from the list of players
            temp = [player for player in tournament.players if player.name == match.winner]
            winning_player = temp[0]
            temp = [player for player in tournament.players if player.name == match.loser]
            losing_player = temp[0] 

            # allocate points for the tournament HERE IS THE ORIGINAL POINTS ALLOCATION,  
            # IF USING THIS BE SURE TO UPDATE THE FILE MANAGER FUNCTION IMPORT POINTS, 
            # AS TO IMPORT CORRECTLY

            #winning_player.tournament_points += (float(ranking_points[str(round_number)]) * float(Match.multiply_points(match.score_difference, tournament.gender) * tournament.difficulty))

            # START ALTERNATE POINTS ALLOCATION
            multiplier = float(Match.multiply_points(match.score_difference, tournament.gender))

            # If we are on rounds 2 - 4, allocate points as normal, we dont add any points 
            # to players when they go into the final from the semi final
            if 0 < current_round.number < 4:
                winning_player.tournament_points += (float(ranking_points[str(round_number)]) * multiplier * tournament.difficulty if season_two else 1 )
            
            # HERE WE ADD FINAL POINTS, DEPENDING ON WINNER OR LOSER. LOSER = 50 * TOURNAMENT DIFFICULTY,  
            # WINNER = 100  * DIFFICULTY * MULTIPLIER (IF APPLICABLE)

            elif current_round.number == 5:
                winning_player.tournament_points += (float(ranking_points[str(round_number)]) * multiplier * tournament.difficulty if season_two else 1 )
                losing_player.tournament_points += (float(ranking_points[str(round_number - 1)]) * tournament.difficulty  if season_two else 1 )
           
            # Add this match to the winnner or losers respective wins or losses ( Statistics )
            winning_player.wins_in_circuit[tournament.tournament_code].append(match)
            losing_player.losses_in_circuit[tournament.tournament_code].append(match)

            FileManager.save_current_season(tournament_circuit, season_number)
            # If we are on the second round of result input, then we need to start allocating prize money to winners.
            if round_number > 0:
                winning_player.tournament_money = prize_money[str(round_number)]
            elif round_number == 0:
                tournament.started = True
          
        # Increment current round
        tournament.current_input_round = round_number + 1
        save_current_tournament_rankings(tournament)


    if season_two:
        for player in players:
            for season_one_player in season_one_tournament.players:
                if player == season_one_player:
                    season_one_round = len(season_one_player.wins_in_circuit[tournament.tournament_code])

                    this_round = len(player.wins_in_circuit[tournament.tournament_code])

                    # if they have the same amount of wins as the last tournament, or if they have reached the final and lost
                    if season_one_round >= this_round or (season_one_round >= 4 and this_round >= 4):
                        print('\n[Player {} reached the same round as last time, they have the {} multiply factor]\n'.format(player.name,tournament_difficulty))
                        player.tournament_points = float(float(player.tournament_points) * tournament_difficulty)
                    else:
                        print('\n[{} did not achieve the same round that they achieved in season 1.]\n'.format(player.name))
                    break

    input('[ANY KEY TO VIEW FINAL RANKINGS]\n')

    # print_current_points_ranking(players)
    # print_current_prize_money_ranking(players)

    print_final_leaderboard(players, tournament)

    save_current_tournament_rankings(tournament)

    tournament.complete = True

    input('[ANY KEY TO RETURN TO MAIN MENU]')
    
    return (None, players)


def print_current_prize_money_ranking(players, return_value=False):

    leaderboard_in_list = list()

    header = '''============================
Current Prize Money Rankings
============================'''

    if not return_value:
        print(header)
    
    leaderboard_in_list.append(header)

    for player in players:
        player.compare_tournament_money = True
    QuickSort.sort(players)
    for player in players:
        player.compare_tournament_money = False

    for player in players:
        ranking_string = " Name: {0} Prize Money: {1}".format(player.name, player.tournament_money)
        leaderboard_in_list.append(ranking_string)
        if not return_value:
            print(" Name: {0} Prize Money: {1}".format(player.name, player.tournament_money))

    print
    if return_value:
        return leaderboard_in_list



def print_current_points_ranking(players, return_value=False):

    leaderboard_in_list = list()
    QuickSort.sort(players)

    header = '''============================
Current Tournament Rankings 
============================'''

    leaderboard_in_list.append(header)

    if not return_value:
        print(header)

    for player in players:
        line =  " Name: {0} Points: {1:.2f}".format(player.name, player.tournament_points)
        leaderboard_in_list.append(line)
        if not return_value:
            print(line)
    if(return_value):
        return leaderboard_in_list
    print()

def print_input_menu(round_number, input_from_file_disabled):
    print('[Input Menu - Next Round -> {0}]\n'.format(round_number+1))
    if(input_from_file_disabled):
        print(Menu.strike("[1] Input next round from file"))
    else:
        print("[1] Input next round from file")        
    print("[2] Input next round manually")
    print("[3] Display current prize money rankings")
    print("[4] Display current ranking points rankings")
    print("[5] Save and return to main menu")

def print_match(player_one, score_one, player_two, score_two):
    print('{0} Score: {1} {2} Score: {3}'.format(player_one, score_one, player_two,
                                                    score_two)) 


def user_input_score(gender, player_one=None, player_two=None,statistics=False):
    if(statistics):
        print('Input score you would like to check in format 1,3 for example ')
    else:
        print('Input score for {0} and {1} seperated by a (,) '.format(player_one, player_two))

    while True:
        new_scores = Menu.get_user_choice()
        if re.search('^\d,\d$', new_scores):
            scores = new_scores.split(',')

            score_one = int(scores[0])
            score_two = int(scores[1])

            # check if match score is valid and get the score difference
            score_evaluation_results = Match.evaluate_match_score(score_one, score_two, gender)

            # If the evaluation returns 3, this means that the score was incorrect

            if score_evaluation_results[0] != 3 and statistics:
                return scores
            elif score_evaluation_results[0] == 3:
                print('Invalid score input')
                continue
            # Else, these two conditions set winner and loser based on the 
            elif score_evaluation_results[0] == 2 and not statistics:
                return (player_two, score_two, player_one, score_one)

            elif score_evaluation_results[0] == 1 and not statistics:
                return(player_one, score_one, player_two, score_two)
        else:
            print('Incorrect format')
            continue
        
  
def player_is_injured(player_choice, gender, player_one, player_two):
    if player_choice == '1':
        # Winner is player one
        if gender == 'MEN':
            return (player_two, 3, player_one,2)
        else:
            return (player_two, 2, player_one, 1)
    elif player_choice == '2':
        # Winner is player two
        if gender == 'MEN':
            return(player_one, 3, player_two, 2)
        else:
            return(player_one, 2, player_two, 1)
    else:
        print('Invalid choice')
        return 0


def correct_invalid_score(current_round_number, list_of_rounds, player_one, player_two, gender):

    next_round = list_of_rounds[current_round_number+1]
    
    if(player_one in next_round.list_of_players):
        print('\n{0} Exists in the next round, this assumes {1} was injured during round {2}\nBy default, {0} wins.\n'.format(player_one, player_two, current_round_number + 1))
        return player_is_injured('2', gender, player_one, player_two)
    elif(player_two in next_round.list_of_players):
        print('\n{0} Exists in the next round, this assumes {1} was injured during round {2}\nBy default, {0} wins.\n'.format(player_two, player_one, current_round_number + 1))
        return player_is_injured('1', gender, player_one, player_two)
    else:
        print('Neither player exists in the next round, {MATCH ERROR}')
        sys.exit()

def print_final_leaderboard(players, Tournament):
    points = print_current_points_ranking(players, True)
    money = print_current_prize_money_ranking(players, True)

    header_1 = points.pop(0)
    header_2 = money.pop(0)
    
    header_1_print = header_1.split('\n')
    header_2_print = header_2.split('\n')
    for line1, line2 in zip(header_1_print, header_2_print):
        print(colours.BEIGE +  line1 + "     ", end='' )
        print(line2 + colours.ENDC)
    first_elm = points[0]

    colours_count = 0

    for i,line in enumerate(points):
        
        if colours_count == (len(colours.list_of_colours) - 1):
            colours_count = 0
        spaces = len(first_elm) - len(line)
        print(colours.list_of_colours[colours_count]  +  str(line.strip('\n') + ' '* spaces), end='')
        print('      ' + str(money[i]) + colours.ENDC)

        colours_count += 1

    print(colours.WHITE +  '')

def check_if_all_tournaments_complete(list_of_tournaments, to_print=True):
    # checking if all tournaments complete
    for tournament in list_of_tournaments:
        if not tournament.complete:
            return False
    if to_print:
        input("\n[ALL TOURNAMENTS COMPLETE]\n")

    return True         

def save_current_tournament_rankings(tournament):
     # when the user quits, we need to save the current rankings
    if len(tournament.overall_rankings) > 0:
        {tournament.overall_rankings[player.name]: (player.tournament_points, player.tournament_money) for player in tournament.players}

    else:
        tournament.overall_rankings = { player.name : (player.tournament_points, player.tournament_money) for player in tournament.players}


def load_current_tournament_rankings(tournament):
    input(tournament.overall_rankings)
    for player in tournament.players:
        player.tournament_points, player.tournament_money = tournament.overall_rankings[player.name][0], tournament.overall_rankings[player.name][1]