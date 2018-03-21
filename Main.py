from __future__ import print_function # so works on Python 2 and 3 alike

import Menu


import atexit
import FileManager
import StatisticManager

import TournamentManager
import Leaderboard
import os
import sys

from TournamentClasses import Season, TournamentCircuit

from TermColours import colours

# always load season 1 at start. 
tournament_circuit = FileManager.load_season(1)
tournament_circuit.complete = TournamentManager.check_if_all_tournaments_complete(tournament_circuit.list_of_tournaments,to_print=False)

# Initialise our 2 seasons
list_of_seasons = [Season(1, tournament_circuit), Season(2, None)]

def on_exit():

    print('\n[Saving Season {0} Session Data]\n'.format(current_season.number))
    FileManager.save_current_season(tournament_circuit, current_season.number)

atexit.register(on_exit)

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

current_season = list_of_seasons[0]

while True:
         
    choice = Menu.start_menu(tournament_circuit, (current_season.number if current_season != None else 0 ))
    
    user_choice = choice[0]
    season_to_start = choice[1]

    ting = int(season_to_start) - 1
    current_season = list_of_seasons[ting]

    # Start new tournament
    if user_choice == "1":
        clear_terminal()
        # Determine which season to start
        # if season 2, we need to set up the tournament circuit differently,
        # due to the constraints on players.
        if current_season.number == 2:
            current_season.tournament_circuit = Menu.circuit_population_menu(FileManager.get_main_data(True))
            tournament_circuit = current_season.tournament_circuit
        # If season 1, do normal stuff
        else:
            current_season.tournament_circuit = Menu.circuit_population_menu(FileManager.get_main_data())
            tournament_circuit = current_season.tournament_circuit
            FileManager.save_current_season(None, 2)

        # Initialise the player statistic library
        for male_player, female_player in zip(tournament_circuit.male_circuit_players, tournament_circuit.female_circuit_players):
            male_player.initialise_statistics(tournament_circuit.list_of_tournaments)
            female_player.initialise_statistics(tournament_circuit.list_of_tournaments)
        # Get all of the tournament codes.
        tournament_codes = [tournament.tournament_code for tournament in
        tournament_circuit.list_of_tournaments]
        
        FileManager.save_current_season(tournament_circuit, current_season.number)

    # Import previous results
    elif user_choice == "2":
        clear_terminal()
        # Load the circuit
        circuit = FileManager.load_season(current_season.number)
        
        if circuit == None:
            input('[SEASON {} not yet started, no data to load]'.format(current_season.number))
            continue
        else:
            current_season.tournament_circuit = circuit

        tournament_circuit = current_season.tournament_circuit
    else:
       print('Invalid Choice')

    clear_terminal()

    # start main menu
    while True:
        # Mark the current season as started now, flag used for determining whether or not 
        if not current_season.started:
            current_season.started = True
        # If all of the tournaments are complete, we need to mark the circuit as complete
        if not tournament_circuit.complete and TournamentManager.check_if_all_tournaments_complete(tournament_circuit.list_of_tournaments):
            tournament_circuit.complete = True
            TournamentCircuit.determine_first_16(tournament_circuit.male_circuit_players)
            TournamentCircuit.determine_first_16(tournament_circuit.female_circuit_players)
            FileManager.save_current_season(tournament_circuit, current_season.number)
            
        user_choice = Menu.main_menu(current_season.number)
        clear_terminal()
        # start tournament imports
        if user_choice == '1':              
            tournament_to_input_results = Menu.choose_tournament(tournament_circuit)

            # If user wants to return to the main menu
            if tournament_to_input_results == 0:
                continue
            
            # now we need to input results for the tournament
            if current_season.number == 2:
                season_one_circuit = list_of_seasons[0].tournament_circuit
                if tournament_to_input_results.gender == TournamentCircuit.men:
                    players = season_one_circuit.male_circuit_players
                else:
                    players = season_one_circuit.female_circuit_players
                season_one_tournament = [tournament for tournament in season_one_circuit.list_of_tournaments if tournament == tournament_to_input_results]
                tournament_results = TournamentManager.input_results(tournament_to_input_results, tournament_circuit, current_season.number, players, season_one_tournament=season_one_tournament[0])
            else:
                tournament_results = TournamentManager.input_results(tournament_to_input_results, tournament_circuit, current_season.number)
                
            current_input_round = tournament_results[0]

            # Is none when the results are fully entered, will allocate the tournament points and money in 
            # that the players have achieved in the tournament and add to their overall points and prize money7


            players_in_tournament = tournament_results[1]

            if current_input_round == None:
                if tournament_to_input_results.gender == "LADIES":
                    overall_players = tournament_circuit.female_circuit_players
                else:
                    overall_players = tournament_circuit.male_circuit_players

                # Loop through the the players in the tournament and the overall players and 
                # add overall points and money to the right person
                for player in players_in_tournament:
                    temp = [overall_player for overall_player in overall_players if player == overall_player]
                    # get the player
                    player_to_add = temp[0]
                    # add wins and losses  from this tournament to their record, used for statistics
                    player_to_add.wins_in_circuit[tournament_to_input_results.tournament_code] = player.wins_in_circuit[tournament_to_input_results.tournament_code]
                    player_to_add.losses_in_circuit[tournament_to_input_results.tournament_code] = player.losses_in_circuit[tournament_to_input_results.tournament_code]

                    # add points and prize money to the overall player records.
                    
                    player_to_add.set_ranking_points(player.tournament_points)

                    player_to_add.prize_money += int(player.tournament_money)
            
            for player in players_in_tournament:
                # reset tournament points and money
                player.tournament_money = 0
                player.tournament_points = 0

                    
            # Save the information about the season
            FileManager.save_current_season(tournament_circuit, current_season.number)
            continue

        # view current season ranking points
        elif user_choice == '2':
            gender = Menu.choose_gender()
            Leaderboard.display_overall_points_leaderboard(gender, tournament_circuit, current_season.number, list_of_seasons[0].tournament_circuit if current_season.number == 2 else None)
            
        # view current season prize money
        elif user_choice == '3':
            gender = Menu.choose_gender()
            Leaderboard.display_overall_money_leaderboard(gender, tournament_circuit, current_season.number, list_of_seasons[0].tournament_circuit if current_season.number == 2 else None)

        # Loading statistics
        elif user_choice == '4':
            show_statistic_menu = True
            while show_statistic_menu == True:

                statistic_choice = Menu.statistics_menu()

                if statistic_choice == '0':
                    show_statistic_menu = False
                    continue
                
                choice = statistic_choice[0]
                gender = statistic_choice[1]

                if gender == tournament_circuit.men:
                    players = tournament_circuit.male_circuit_players
                else:
                    players = tournament_circuit.female_circuit_players

                StatisticManager.display_statistics(players, choice, gender, tournament_circuit.list_of_tournaments)

        # return to the original menu
        elif user_choice == '5':
            break;
