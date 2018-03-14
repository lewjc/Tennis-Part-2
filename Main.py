import Menu
import FileManager
import TournamentManager
import Leaderboard
import os
import sys

tournament_circuit = None

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

while True:
    user_choice = Menu.start_menu()
    
    # Start new tournament
    if user_choice == "1":
        tournament_circuit = Menu.circuit_population_menu(FileManager.get_main_data())

        tournament_codes = [tournament.tournament_code for tournament in
        tournament_circuit.list_of_tournaments]
                            
        FileManager.write_to_file(tournament_codes, os.path.dirname(os.path.abspath(__file__)),
                                  "Data/TOURNAMENTS IN CIRCUIT")
    # Import old results
    elif user_choice == "2":
        pass

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
                    player_to_add.ranking_points += float(player.tournament_points)
                    player_to_add.prize_money += int(player.tournament_money)

        # view current season ranking points
        elif user_choice == '2':
            gender = Menu.choose_gender()
            Leaderboard.display_overall_points_leaderboard(gender, tournament_circuit)
            
        # view current season prize money
        elif user_choice == '3':
            gender = Menu.choose_gender()
            Leaderboard.display_overall_money_leaderboard(gender, tournament_circuit)
        # return to the original menu
        elif user_choice == '4':
            break;
