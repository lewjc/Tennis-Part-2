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

            TournamentManager.input_results(current_tournament, tournament_circuit.ranking_points)# now we need to input results for the tournament


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
