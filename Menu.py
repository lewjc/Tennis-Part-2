import sys

# first menu options
def start_menu():
    print_title()
    do_print = True
    while True:
        if do_print:
            print("[1] Start new tournament circuit")
            print("[2] Load previous circuit data")
            print("[3] System Information")
            print("[4] Quit")
        do_print = False
        user_choice = input("--> ")
        # load new circuit
        if user_choice == "1":
            print("Starting New Circuit \n")
            return user_choice
        # import previous data
        elif user_choice == "2":
            print("Loading Previous Data\n")
            return user_choice
        # quit
        elif user_choice == "3":
            print(system_information())
            do_print = True
            continue
        elif user_choice == "4":
            quit_program()
        else:
            print("Invalid Choice")

def circuit_population_menu(tournament_circuit):
    menu_dict = {}
    all_tournaments = tournament_circuit.list_of_tournaments
    print("Choose tournaments to be in this circuit\n")
    for i, tournament in enumerate(all_tournaments, 1):
        menu_dict[str(i)] = tournament.tournament_code
    
        print("[{0}] {1} {2}".format(str(i), menu_dict[str(i)], tournament.gender))

    default = str(i+1)
    finish = str(i+2)
    menu_dict[default] = "ALL"
    menu_dict[finish] = "Finish"
    print("[{0}] All".format(default))
    print("[{0}] Finish".format(finish))
    current_circuit_tournaments = []
    while True:
        user_choice = input("-> ")
        if user_choice in menu_dict:
            if user_choice == default:
                current_circuit_tournaments = [tournament for tournament in all_tournaments]
                tournament_circuit._list_of_tournaments = current_circuit_tournaments
                return tournament_circuit
            elif user_choice == finish:
                if len(current_circuit_tournaments) != 0:
                    tournament_circuit.list_of_tournaments = current_circuit_tournaments
                    return tournament_circuit
                else:
                    print("You have not selected any tournaments yet!")
                    continue
            else:
                tournament_to_add = all_tournaments[int(user_choice) - 1]
                current_circuit_tournaments.append(tournament_to_add)
                print("{0} {1} Added to circuit".format(tournament_to_add.tournament_code, tournament_to_add.gender))
                del menu_dict[user_choice]
        else:
            print("Invalid Choice")

def main_menu():
    print("[1] Input scores")
    print("[2] View current circuit points ranking")
    print("[3] View current circuit money ranking")
    print("[4] Return")
    print("[5] Quit")
    while True:
        user_choice = input("--> ")
        if user_choice == "1":
            print("---Input data--\n")
            return user_choice
        elif user_choice == "2":
            print("---Loading Circuit Points Ranking---\n")
            return user_choice
        elif user_choice == "3":
            print("---Loading Circuit Money Ranking---\n")
            return user_choice
        elif user_choice == "4":
            print("--Returning to start--")
            return user_choice
        elif user_choice == "5":
            quit_program()
        else:
            print("Invalid Choice")

def print_title():
    print("""
  _____              _      ___           _   _            
 |_   _|__ _ _  _ _ (_)___ | _ \__ _ _ _ | |_(_)_ _  __ _  
   | |/ -_) ' \| ' \| (_-< |   / _` | ' \| / / | ' \/ _` | 
   |_|\___|_||_|_||_|_/__/ |_|_\__,_|_||_|_\_\_|_||_\__, | 
                                                    |___/  
   ___         _                                            
  / __|_  _ __| |_ ___ _ __                                 
  \__ \ || (_-<  _/ -_) '  \                                
  |___/\_, /__/\__\___|_|_|_|                               
       |__/\n
    """)


def system_information():
    return """
 -Design and Analysis of Data Structures and Algorithms-
 
   =============================
   | DADSA COURSEWORK - PART A |
   | AUTHOR - LEWIS CUMMINS    |
   | STUDENT NUMBER - 16014766 |              
   =============================
     
   Each tournament currently has its own round 1 scores. From there you may 
   either input the results for the next round of the tournament from file 
   or alternatively input them yourself each round. Ranking points and 
   prize money are stored through out each round in the tournaments and are 
   viewable after each round's scores have been input. The system will 
   check and catch double entries of results, in case you make a mistake. 
   The system also saves data to  data files allowing you to exit and 
   come back to finish entering results. After all results have been input,
   you will be taken to a final menu which allows you to view the overall 
   rankings for both prize money and points
   
   ----------------------------------------------------------------------------
   
   To add a new tournament, type the name of it into the prize money file, and
   write corresponding prize money
   
   Functionality to be added:
   
   - user add their own tournaments with corresponding prize money allocation
   - use less amount of files for storing data
   - use json over csv (UNSURE)
   
   """

def quit_program():
    sys.exit("----BYE----")
