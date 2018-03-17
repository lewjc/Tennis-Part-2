import locale
import random
import Menu
import QuickSort
import sys

from TermColours import colours
import re

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
    print(colours.BEIGE + "==========================================================================")
    print("\n[{0} - {1}] Players: {2} | Top Prize: {3} | Difficulty: {4} \n".format(tournament.tournament_code, tournament.gender,
                                                                           len(players),
                                                                           prize_money_string,
                                                                           tournament_difficulty))
    print("==========================================================================\n" + colours.ENDC + colours.WHITE)
    input("--Press ENTER to start--\n")

 
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
            elif user_choice == '1' and tournament.import_from_file_disabled:
                print('You have previously chosen to input results from file. This option is disabled because the system '  
                      'cannot guarantee\n you have input results which will be the same as the results the system has on file.\n')
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
                return (round_number,list())
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
                player_menu = {i : player  for i, player in enumerate(current_round.list_of_players)}
                count = 0
            
                for i, (k,v) in enumerate(player_menu.items()):   
                    print('[{0}] {1} '.format(f"{k:02}",v),end='')
                    if (i + 1) % 4 == 0 or i == len(player_menu.items()) - 1:
                        print()
                # Let user choose 2 players
                print('\nPick 2 players, using their position in the list. write in format x,y ')

                # get user's choice of players 
                while True:
                    choice = Menu.get_user_choice()
                    if re.search('^\d,\d$', choice):
                        match_players = choice.split(',')
                        player_one_index = int(match_players[0])
                        player_two_index = int(match_players[1])

                        if player_one_index in player_menu.keys() and player_two_index in player_menu.keys():
                            player_one = current_round.list_of_players[player_one_index]
                            player_two = current_round.list_of_players[player_two_index]
                            
                        else:
                            print('Invalid player choice')
                            continue
                        break
                    else:
                        print('Invalid')
                
                # Get the user ot input the scores for the match.
                match_results = user_input_score(tournament.gender, player_one, player_two)

                match.winner = match_results[0]
                match.winner_score = match_results[1]
                match.loser = match_results[2]
                match.loser_score = match_results[3]
                # Print new line before result is displayed.
                print()

            # If match is incorrect
            if(match.is_invalid):
                print_match(player_one, player_one_score, player_two, player_two_score)
                # TODO: Only ask if not on round 5
                print('This result is invalid, should the system correct itself? [Y/N]')
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
                       
                    elif user_choice.lower() == 'n':

                        print('By choosing to manually correct the score, you are voiding the rest of the scores that are on file for this tournament.\n'
                              'You will be unable to import scores for the rest of the tournament and must type remaining scores in manually.\nPress [Y] to confirm, any other key to let the system correct the error.')
                       
                        user_choice = Menu.get_user_choice()
                       
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

            # allocate points for the tournament
            winning_player.tournament_points += (float(ranking_points[str(round_number)]) * float(Match.multiply_points(match.score_difference, tournament.gender)))

            winning_player.wins_in_circuit[tournament.tournament_code].append(match)
            losing_player.losses_in_circuit[tournament.tournament_code].append(match)

            # If we are on the second round of result input, then we need to start allocating prize money to winners.
            if round_number > 0:
                winning_player.tournament_money = prize_money[str(round_number)]
          
        # Increment current round
        tournament.current_input_round = round_number + 1

    # After the results are fully Input, we need to multiply the points earned by the tournament difficulty
    for player in players:
        player.tournament_points = float(float(player.tournament_points) * tournament_difficulty)
    
    input('[ANY KEY TO VIEW FINAL RANKINGS]\n')

    # print_current_points_ranking(players)
    # print_current_prize_money_ranking(players)

    print_final_leaderboard(players)

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
        line =  "Name: {0} Points: {1:g}".format(player.name, player.tournament_points)
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
        print('{0} Exists in the next round, this assumes {1} was injured during round {2}\nBy default, {0} wins.\n'.format(player_one, player_two, current_round_number + 1))
        return player_is_injured('1', gender, player_one, player_two)
    elif(player_two in next_round.list_of_players):
        print('{0} Exists in the next round, this assumes {1} was injured during round {2}\nBy default, {0} wins.\n'.format(player_two, player_one, current_round_number + 1))
        return player_is_injured('2', gender, player_one, player_two)
    else:
        print('Neither player exists in the next round, {MATCH ERROR}')
        sys.exit()

def print_final_leaderboard(players):
    points = print_current_points_ranking(players, True)
    money  = print_current_prize_money_ranking(players, True)
    

    header_1 = points.pop(0)
    header_2 = money.pop(0)
    
    header_1_print = header_1.split('\n')
    header_2_print = header_2.split('\n')
    for line1,line2 in zip(header_1_print, header_2_print):
        print(colours.BEIGE +  line1 + "     ", end='' )
        print(line2 + colours.ENDC)
    first_elm = points[0]

    colours_count = 0

    for i,line in enumerate(points):
        
        if colours_count == (len(colours.list_of_colours) - 1):
            colours_count = 0
        spaces = len(first_elm) - len(line)
        print(colours.list_of_colours[colours_count] + str(line.strip('\n') + ' '* spaces), end='')
        print('      ' + str(money[i]) + colours.ENDC)

        colours_count += 1

    print(colours.WHITE +  '')
