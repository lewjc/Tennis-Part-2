
import sys
from TournamentClasses import TournamentCircuit
import os
from TermColours import colours



def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')
    
# first menu options
def start_menu(tournament_circuit):
    print_title()
    do_print = True
    while True:
        if do_print:
            print(colours.WHITE + "[1] Start new season")
            print("[2] Load previous circuit data")
            print("[3] System Information")
            print("[0] Quit")
        do_print = False
        user_choice = input("--> ")
        # load new circuit
        if user_choice == "1":

            season_choice = choose_season(tournament_circuit.complete if tournament_circuit != None else False )        
            
            while True:
                print('Starting a new Season will erase all of the data associated with the previous season.')
                print('Continue? [Y/N]')
                choice = get_user_choice()
                if choice.lower() == 'y':
                    print("Starting New Season {0} \n".format(season_choice))
                    return (user_choice, season_choice)
                elif choice.lower() == 'n':
                    print('\n[CANCELLING NEW SEASON]\n')
                    do_print = True
                    break
                else:
                    print('Invalid choice')

        # import previous data
        elif user_choice == "2":

            season_choice = choose_season(tournament_circuit.complete if tournament_circuit != None else False )        
        
            print("Loading Previous Data for season {0}\n".format(season_choice))
            return (user_choice, season_choice) 
        # quit
        elif user_choice == "3":
            print(system_information())
            do_print = True
            continue
        elif user_choice == "0":
            quit_program()
        else:
            print("Invalid Choice")

def choose_season(unlock_second=False):

    season_two_text = '[2] Season 2'
    if not unlock_second:
        season_two_text = strike(season_two_text) + colours.WHITE
    
    print('[SEASON CHOICE]\n')
    print('[1] Season 1')
    print(season_two_text)
    while True:
        user_choice = get_user_choice()

        # load first season
        if user_choice == '1':
            return '1'
        # Second season is not currently available
        elif user_choice == '2' and not unlock_second:
            print('Season 2 is not currently available,\nPlease finish entering Season 1 results.')
            continue
        # Second season is now available
        elif user_choice == '2' and unlock_second:
            return '2'
        else:
            print('Invalid Choice')
            continue
        # load second season
def choose_gender():
    print("Choose Gender \n")
    print("[1] Male tournament")
    print("[2] Female tournament")

    while True:
        user_choice = get_user_choice()

        if user_choice == "1":
            clear_terminal()
            return '1'
            clear_terminal()
        elif user_choice == "2":
            return '2'
        else:
            print('Invalid Choice')
            continue

def circuit_population_menu(tournament_circuit):
    menu_dict = {}
    all_tournaments = tournament_circuit.list_of_tournaments

    print("Choose tournaments to be in this circuit\n")
    for i, tournament in enumerate(all_tournaments, 1):
        menu_dict[str(i)] = tournament.tournament_code
    
        print("[{0}] {1} {2}".format(str(i), menu_dict[str(i)], tournament.gender))

    default = str(i+1)
    finish = '0'
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
                print('\n[All tournaments added to this circuit]')
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

def choose_tournament(tournament_circuit):

    gender_choice = choose_gender()

    if gender_choice == '1':
         gender = TournamentCircuit.men
    else:
        gender = TournamentCircuit.ladies
    
    tournament_menu = dict()
    print("Choose Tournament\n")

    # loop through and get each tournament, and allocate it a menu space
    menu_choice = 0

    for current_tournament in tournament_circuit.list_of_tournaments:
        
        if current_tournament.gender == gender:
            code_menu_string = '{0} {1}'.format(current_tournament.tournament_code, current_tournament.gender)
            if current_tournament.complete:
                code_menu_string = strike(code_menu_string)
            menu_choice = menu_choice + 1
            tournament_menu[str(menu_choice)] = current_tournament.tournament_code
            print(colours.WHITE + "[{0}] {1}".format(str(menu_choice), code_menu_string))
        else:
            continue
    
    tournament_menu['0'] = "Return"
    print("[{0}] Return".format('0'))
 
    # add return option to menu

    while True:
        user_choice = input("--> ")
        if user_choice in tournament_menu:

            menu_code = tournament_menu[user_choice]

            if tournament_menu[user_choice] == "Return":
                return 0
            else:
                tournaments = tournament_circuit.list_of_tournaments
                # Returns current tournament
                choice = [tournament for tournament in tournament_circuit.list_of_tournaments if tournament.tournament_code == menu_code]
                tournament_choice = choice[0]

                if(tournament_choice.complete):
                    print('Tournament results already entered')
                    continue

                return tournament_choice 
        else:
            print("Invalid Choice")

def main_menu(season_number):
    clear_terminal()
    print('[MAIN MENU - SEASON {0}]\n'.format(season_number))
    print("[1] Input scores")
    print("[2] View current circuit points ranking")
    print("[3] View current circuit money ranking")
    print("[4] View Player Statistics")
    print("[5] Return")
    print("[0] Quit")
    while True:
        user_choice = input("--> ")
        if user_choice == "1":
            print("\n[INPUT DATA]\n")
        elif user_choice == "2":
            print("\n[LOADING CIRCUIT POINTS RANKING]\n")
        elif user_choice == "3":
            print("\n[LOADING CIRCUIT MONEY RANKING]\n")
        elif user_choice == "4":
            print('\n[LOADING STATISTICS]')
        elif user_choice == "5":
            print("--Returning to start--")
        elif user_choice == "0":
            quit_program()
        else:
            print("Invalid Choice")
            continue
        return user_choice


def statistics_menu():
    print('\n[STATISTICS MENU]\n')
    print('[1] Number of wins for a player with a particular score')
    print('[2] Percentage wins of a player')
    print('[3] Show the player with most wins in the season so far')
    print('[4] Show the player with most loses in the season so far.')
    print('[0] Return')

    while True:
        user_choice = get_user_choice()
        
        if user_choice == '1':
            print('Wins with particular score\n')
        elif user_choice == '2':
            print('Percentage wins of a player\n')
        elif user_choice == '3':
            print('Most wins\n')
        elif user_choice == '4':
            print('Most losses\n')
        elif user_choice == '0':
            return '0'
        else:
            print('Invalid Choice')
            continue
        break
    gender = choose_gender()
    
    if gender == '1':
        gender = TournamentCircuit.men
    elif gender == '2':
        gender = TournamentCircuit.ladies

    return (user_choice, gender)
def print_title():
    print(colours.BEIGE + """
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
    """ + colours.ENDC)


def system_information():
    return """
 -Design and Analysis of Data Structures and Algorithms-
 ---------------------------------------------------------------------------------
 
   =============================
   | DADSA COURSEWORK - PART B |
   | AUTHOR - LEWIS CUMMINS    |
   | STUDENT NUMBER - 16014766 |              
   =============================
     
   First Season:

   Each tournament has 5 rounds on file, with the opiton to enter the results yourself. 
   Should you choose this option, then you uwill not be able to input results from file 
   for the rest of the match, this protects the integrity of the scores and is the best 
   way to minimize conflicting score entry. There are statistics available for each player.

   [Namely]:

    The number of wins for a player with a particular score – either in a specific
     tournament, or overall for the season.

    The percentage wins of a player in a specific tournament or for a whole season.

    Show the player with most wins in the season so far.

    Show the player with most loses in the season so far.

   Second Season:
   

   
   ---------------------------------------------------------------------------------
   
   To add a new tournament, type the name of it into the prize money file, and
   write corresponding prize money
   
   """

# Exit
def quit_program():
    sys.exit("----BYE----")

# Return a choice given by the user
def get_user_choice():
    return input('-> ')

# Creates a strike through the text
def strike(text):
    i = 0
    new_text = ''
    while i < len(text):
        if text[i] == ' ':
            new_text = new_text + '-'
        else:
            new_text = colours.RED + new_text + (text[i] + u'\u0336') 
        i = i + 1
    return(new_text + colours.ENDC)