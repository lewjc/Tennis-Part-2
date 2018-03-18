
import TournamentManager
import sys

import Menu

from TermColours import colours

def display_statistics(players, statistic_choice, gender, list_of_tournaments):

    # Number of wins for a player with a particular score
    if statistic_choice == '1':    
     
        player = get_player_choice(players)

        score = TournamentManager.user_input_score(gender, statistics=True)

        winning_score = score[0] if score[0] > score[1]  else score[1]
        losing_score = score[0] if score[0] < score[1] else score[1] 

        matches_score_occured = list()

        tournaments_to_view = get_tournament_choice(list_of_tournaments, gender)
        print()
        # if we are getting stats for the whole tournament
        if len(tournaments_to_view) > 0:
            scores_to_show = dict()
            for tournament in tournaments_to_view:
                scores_to_show[tournament.tournament_code] = list()
                for match in player.wins_in_circuit[tournament.tournament_code]:
                     if match.winner_score == winning_score and match.loser_score == losing_score:
                     # the match is what we are looking for
                        scores_to_show[tournament.tournament_code].append(match)

                print('TOURNAMENT - [{}]'.format(tournament.tournament_code) + ' -  Results \n')

                if len(scores_to_show[tournament.tournament_code]) > 0:
                    for match in scores_to_show[tournament.tournament_code]:
                        print(colours.GREEN + '{0} won {1} - {2} against {3}\n'.format(player.name, match.winner_score, match.loser_score, match.loser) + colours.WHITE)
                elif len(scores_to_show[tournament.tournament_code]) == 0:
                    print(colours.RED + '{0} did not win by {1} - {2} in {3}\n'.format(player.name, winning_score, losing_score, tournament.tournament_code) + colours.WHITE)

                if (len(scores_to_show[tournament.tournament_code]) == 0) and (not tournament.started) or (tournament.started and not tournament.complete):                 
                    print(colours.WHITE + '{0} {1} results have not fully been entered, currently waiting on round '.format(tournament.tournament_code, tournament.gender) + colours.GREEN + '{}'.format(tournament.current_input_round + 1) + colours.WHITE + ' scores to be input ..\nMaybe this is why no statistics are showing up.\n')
        else:
            print('Error grabing tournament')

    # Percentage wins for a player
    elif statistic_choice == '2':
        player  = get_player_choice(players)
        tournaments_to_view = get_tournament_choice(list_of_tournaments, gender)

        wins = 0
        losses = 0
        for tournament in tournaments_to_view:
            # If we are viewing statistics for the whole tournament
            wins += len(player.wins_in_circuit[tournament.tournament_code])
            losses += len(player.losses_in_circuit[tournament.tournament_code])        
        
        total_matches = wins + losses
        try:

            win_percent = ((wins / (total_matches)  * 100))
        except ZeroDivisionError:
            print('\n`No results have been entered yet!')
            return
        # If we are only checking one tournament
        if len(tournaments_to_view) == 1:
            tournament = tournaments_to_view[0]
            input(tournament)
            print('\nWin percent in [{0}] is --> '.format(tournament.tournament_code) + (colours.GREEN if win_percent > 50 else colours.RED) + '{0:.2f}%'.format(win_percent) + colours.WHITE)
            print('Out of a total of {} matches \n'.format(total_matches))
        # If we are checking all of the tournaments
        else:
            print('\nWin percent in the entire circuit is ' + (colours.GREEN if win_percent > 50 else colours.RED) +'{0:.2f}%'.format(win_percent) + colours.WHITE)
            print('Out of a total of {0} matches\n'.format(total_matches))

    # player with the most wins
    elif statistic_choice == '3':
       get_highest_wins_or_losses(players, wins=True)
    # player with the most losses.
    elif statistic_choice == '4':
        get_highest_wins_or_losses(players, wins=False)
    else:
        print('INVALID STATISTIC CHOICE [ERROR]')
        sys.exit('QUITTING')

def get_player_choice(players):

    print('[Choose Player - Type their position in the menu] \n')

    player_menu = {i : player.name for i, player in enumerate(players)}
    count = 0

     # List all of the players available for selection.
    for i, (k,v) in enumerate(player_menu.items()):   
        print('[{0}] {1} '.format(f"{k:02}",v),end='')
        if (i + 1) % 4 == 0 or i == len(player_menu.items()) - 1:
            print()
    # Get a user to make a choice on what plaeyr theuy would like to display
    player = None
    
    while True:
        user_choice = Menu.get_user_choice()
        try:
            if int(user_choice) in player_menu.keys():
                print('\nChoosing Player: {} \n'.format(player_menu[int(user_choice)]))
                player = players[int(user_choice)]
                return player
            else:
                print('Invalid choice')
        except Exception:
            print('Invalid Choice')
            continue

def get_tournament_choice(list_of_tournaments, gender):

        print('\nFrom what tournament did you want to view this statistic? ')

        # Create menu out of tournaments in the circuit
        tournament_menu = dict()

        count = 1
        for tournament in list_of_tournaments:
            if tournament.gender == gender:
                tournament_menu[count] = tournament.tournament_code
                count += 1

        tournament_menu[0] = 'All'
        
        for position in tournament_menu.keys(): 
            print('[{0}] {1}'.format(position, tournament_menu[position]))

        tournaments_to_view = None

        while True:
            user_choice = Menu.get_user_choice()
            
            try:
                user_choice = int(user_choice)
            except Exception:
                print('Invalid choice')
                continue

            if user_choice in tournament_menu.keys():
                # If the user wants to view for all tournaments
                if user_choice == 0:
                    tournaments_to_view = [tournament for tournament in list_of_tournaments if tournament.gender == gender]
                else:
                    tournaments_to_view = [tournament for tournament in list_of_tournaments if tournament.tournament_code == tournament_menu[user_choice] and tournament.gender == gender]
                break
            else:
                print('Invalid choice')
                continue

        return tournaments_to_view

def get_highest_wins_or_losses(players, wins=True):
    
    print_text = ''
    players_with_highest_number = list()
    for i, player in enumerate(players):

        # get current wins or losses of the current player
        if wins:
            print_text = 'wins'
            matches = [match for tournament in players[i].wins_in_circuit.values() for match in tournament]
        else:
            print_text = 'losses'
            matches = [match for tournament in players[i].losses_in_circuit.values() for match in tournament]
        
        amount_of_matches = len(matches)

        # If it is the first player in the list
        if i == 0:
            players_with_highest_number.append((amount_of_matches, 0))
            continue
                
                # If it is the first player in the list
        else:
            # Get the win amount for the current highest player stored in the list
            current_highest =  players_with_highest_number[0][0]
            # If the player has the highest wins so far.

            if amount_of_matches > current_highest:
                players_with_highest_number.clear()
                # Store the player and their position in the list of players
                current_highest = (amount_of_matches, i)
                # add this tuple to the list of players with the highest number
                players_with_highest_number.append(current_highest)
            # If the player has the same amount of wins as the current highest wins
            elif amount_of_matches == current_highest:
                current_highest = (amount_of_matches, i)
                players_with_highest_number.append(current_highest)

    # If there is only one person with the top amount of wins.

    if len(players_with_highest_number) == 1:
        print('Player with the most {0} in the tournament so far is - [{1}] with {2} {0}'.format((colours.GREEN + print_text if print_text == 'wins' else colours.RED + print_text) + colours.WHITE , players[players_with_highest_number[0][1]].name, players_with_highest_number[0][0]) + colours.WHITE)
    # Else, there are multiple people who share the top spot.players
    else:
        print('[Players with {0} {1}]\n'.format(players_with_highest_number[0][0], colours.GREEN + print_text + colours.WHITE if print_text == 'wins' else colours.RED + print_text + colours.WHITE ))
        [print('[{0}]'.format(players[player[1]].name)) for player in players_with_highest_number]
                