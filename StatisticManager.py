
import TournamentManager
import sys

import Menu

from TermColours import colours

def display_statistics(players, statistic_choice, gender, list_of_tournaments):

    # Number of wins for a player with a particular score
    if statistic_choice == '1':    
     
        player = get_player_choice()
        
        score = TournamentManager.user_input_score(gender, statistics=True)

        winning_score = score[0] if score[0] > score[1]  else score[1]
        losing_score = score[0] if score[0] < score[1] else score[1] 

        print('{0} {1}'.format(winning_score, losing_score))      

        matches_score_occured = list()

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
                    tournaments_to_view = [tournament.tournament_code for tournament in list_of_tournaments if tournament.gender == gender]
                else:
                    tournaments_to_view = [tournament.tournament_code for tournament in list_of_tournaments if tournament.tournament_code == tournament_menu[user_choice] and tournament.gender == gender]
                break
            else:
                print('Invalid choice')
                continue

        # if we are getting stats for the whole tournament
        if len(tournaments_to_view) > 1:
            scores_to_show = dict()
            for tournament in tournaments_to_view:
                scores_to_show[tournament] = list()
                for match in player.wins_in_circuit[tournament]:
                     if match.winner_score == winning_score and match.loser_score == losing_score:
                     # the match is what we are looking for
                        scores_to_show[tournament].append(match)
                
                if len(scores_to_show[tournament]) > 0:
                    print(tournament + ' -  Results \n')
                    for match in scores_to_show[tournament]:
                        print(colours.GREEN + '{0} won {1} - {2} against {3}\n'.format(player.name, match.winner_score, match.loser_score, match.loser) + colours.ENDC)
                else:                  
                    print(colours.RED + '\n{0} did not win by {1} - {2} in {3}\n'.format(player.name, winning_score, losing_score, tournament) + colours.ENDC)

                    [print('{0} {1} results have not been entered, maybe this is why no statistics are showing up.'.format(current_tournament.tournament_code, current_tournament.gender)) for current_tournament in list_of_tournaments if current_tournament.tournament_code == tournament and not current_tournament.complete and current_tournament.gender == gender]

        # if we are getting stats for one tournament
        else:
            tournament = tournaments_to_view[0]
            scores_to_show = list()
            for match in player.wins_in_circuit[tournament]:
                if match.winner_score == winning_score and match.loser_score == losing_score:
                    # the match is what we are looking for
                    scores_to_show.append(match)
            if len(scores_to_show) > 0:
                print('['+ tournament + '] -  Results \n')
                for match in scores_to_show:
                    print(colours.GREEN + '{0} won {1} - {2} against {3}\n'.format(player.name, match.winner_score, match.loser_score, match.loser) + colours.ENDC)
                
            else:
                print('\n{0} did not win by {1} - {2} in tournament [{3}]\n '.format(player.name, winning_score, losing_score, tournament))
                # If the user has not yet input results for this tournament, notify them that this maybe why no statistics are shown
                [print('{0} {1} results have not been entered, maybe this is why no statistics are showing up.'.format(current_tournament.tournament_code, current_tournament.gender)) for current_tournament in list_of_tournaments if current_tournament.tournament_code == tournament and not current_tournament.complete and current_tournament.gender == gender]


    # Percentage wins for a player
    elif statistic_choice == '2':
        player  = get_player_choice()
        
    # player with the most wins
    elif statistic_choice == '3':
        pass
    # player with the most losses.
    elif statistic_choice == '4':
        pass
    else:
        print('INVALID STATISTIC CHOICE [ERROR]')
        sys.exit('QUITTING')

def get_player_choice():

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
