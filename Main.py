import Menu
import FileManager
import TournamentManager
import Leaderboard
import os
import sys

tournament_circuit = None

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

    # View system informataion
    elif user_choice == "3":
        pass

    else:
       print('Invalid Choice')

    # start main menu
    while True:
        user_choice = Menu.main_menu()

        # start tournament imports
        if user_choice == 1:

        # view current season ranking points
        elif user_choice == 2:

        # view current season prize money
        elif user_choice == 3:

        # return to the original menu
        elif user_choice == 4:
            break;


