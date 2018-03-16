from __future__ import print_function # so works on Python 2 and 3 alike

import Menu
import FileManager

import TournamentManager
import Leaderboard
import os
import sys

import pickle

from TermColours import colours
tournament_circuit = None


# Save the circuit as pickle fiel
def save_current_season(tournament_circuit):
    with open(os.path.join(os.path.dirname(__file__), 'DATA/main.pickle'), 'wb') as file:
        pickle.dump(tournament_circuit, file, protocol=pickle.HIGHEST_PROTOCOL)

def load_season():
    with open(os.path.join(os.path.dirname(__file__), 'DATA/main.pickle'), 'rb') as file:
         return pickle.load(file)


def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

while True:

    user_choice = Menu.start_menu()
    
    # Start new tournament
    if user_choice == "1":
        tournament_circuit = Menu.circuit_population_menu(FileManager.get_main_data())

        for male_player, female_player in zip(tournament_circuit.male_circuit_players, tournament_circuit.female_circuit_players):
            male_player.initialise_statistics(tournament_circuit.list_of_tournaments)
            female_player.initialise_statistics(tournament_circuit.list_of_tournaments)

        tournament_codes = [tournament.tournament_code for tournament in
        tournament_circuit.list_of_tournaments]
        
        save_current_season(tournament_circuit)
    # Import old results
    elif user_choice == "2":
        tournament_circuit = load_season()

    else:
       print('Invalid Choice')

    # start main menu
    while True:
        print()
        user_choice = Menu.main_menu()

        # start tournament imports
        if user_choice == '1':
            tournament_to_input_results = Menu.choose_tournament(tournament_circuit)

            # If user wants to return to the main menu
            if tournament_to_input_results == 0:
                continue

            tournament_results = TournamentManager.input_results(tournament_to_input_results, tournament_circuit.ranking_points)# now we need to input results for the tournament

            current_input_round = tournament_results[0]

            # Is none when the results are fully entered, will allocate the tournament points and money in 
            # that the players have achieved in the tournament and add to their overall points and prize money
            if current_input_round == None:
                players_in_tournament = tournament_results[1]
                if tournament_to_input_results.gender == "LADIES":
                    overall_players = tournament_circuit.female_circuit_players
                else:
                    overall_players = tournament_circuit.male_circuit_players

                # Loop through the the players in the tournament and the overall players and 
                # add overall points and money to the right person
                for player in players_in_tournament:
                    temp = [overall_player for overall_player in overall_players if player.name == overall_player.name]
                    player_to_add = temp[0]
                    player_to_add.wins_in_circuit[tournament_to_input_results.tournament_code] = player.wins_in_circuit[tournament_to_input_results.tournament_code]
                    player_to_add.losses_in_circuit[tournament_to_input_results.tournament_code] = player.losses_in_circuit[tournament_to_input_results.tournament_code]

                    player_to_add.ranking_points += float(player.tournament_points)
                    player_to_add.prize_money += int(player.tournament_money)
                    # reset tournament points and money
                    player_to_add.tournament_money = 0
                    player_to_add.tournament_points = 0

            # Save the information about the season
            save_current_season(tournament_circuit)

        # view current season ranking points
        elif user_choice == '2':
            gender = Menu.choose_gender()
            Leaderboard.display_overall_points_leaderboard(gender, tournament_circuit)
            
        # view current season prize money
        elif user_choice == '3':
            gender = Menu.choose_gender()
            Leaderboard.display_overall_money_leaderboard(gender, tournament_circuit)
        # return to the original menu
        elif user_choice == '0':
            break;
