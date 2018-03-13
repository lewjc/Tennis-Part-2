import csv
import os
from ADT import *
from TournamentClasses import *
import re


def get_main_data():
    # defined data directory
    data_directory = os.path.dirname(__file__)

    file_name = "Data/MALE PLAYERS.csv"
    full_path = os.path.join(data_directory, file_name)
    male_players = import_players(open_file(full_path))

    file_name = "Data/FEMALE PLAYERS.csv"
    full_path = os.path.join(data_directory, file_name)
    female_players = import_players(open_file(full_path))

    file_name = "Data/RANKING POINTS.csv"
    full_path = os.path.join(data_directory, file_name)
    ranking_points = import_points(open_file(full_path))

    file_name = "Data/PRIZE MONEY.csv"
    full_path = os.path.join(data_directory, file_name)
    list_of_tournaments = import_tournaments(open_file(full_path),
                                             male_players, female_players)

    # Now have a circuit populated by players and tournaments, along with points and prize money
    return TournamentCircuit(list_of_tournaments, ranking_points,
                             male_players, female_players)

def open_file(file_name):
    # open file and store each row into a list
        try:
            # open using 'with' command closes file after everything is executed
            with open(file_name, "r") as csv_file:
                # delimit by comma because csv files
                file = csv.reader(csv_file, delimiter=',')
                file_row_list = list()
                # for each row in the csv, write to new file
                for row in file:
                    file_row_list.append(row)
                return file_row_list
        # exception catching
        except FileNotFoundError:
            print("No File with name {0}".format(file_name))
            return list()
        except IsADirectoryError:
            print("Is a directory not a file")
            return list()

            
# handles player import
def import_players(file_row_list):
    list_of_players = list()
    for row in file_row_list:
        list_of_players.append(Player(row[0]))
    return list_of_players


# handles points to be input
def import_points(file_row_list):
    points = dict()
    # get points from file
    for i in range(len(file_row_list) - 1, 0, -1):
        row = file_row_list[i]
        # only import unique values
        if row[0] in points.values():
            continue
        else:
            points[row[1]] = row[0]

    return points


# handles importing tournaments and prize money
def import_tournaments(file_row_list, male_players, female_players):
        q = Queue()
        s = Stack()
        temp = list()
        tournament_codes = list()
        list_of_tournaments = list()

        # loop through each row imported
        for row in file_row_list:
            for i in range(len(row)):
                # if row is tournament code
                if len(row[0]) > 0 and i == 0:
                    tournament_codes.append(row[0])
                # if row is empty
                if len(row[i]) == 0:
                    continue
                q.enqueue(row[i])
        # use this bool to not start adding to list until first tournament code
        # is found
        add_to_list = False
        # remove header from tournament codes
        # Sort data into lists
        for i in range(q.size()):
            # grabs current item at head of queue
            current_item = q.dequeue()
            # if item is not a tournament code but is a value add to temp list
            if add_to_list and current_item not in tournament_codes:
                temp.append(current_item)
            # if current item is a tournament code
            if current_item in tournament_codes:
                # add temp(tournament code and values for prize money) to list
                s.push(temp)
                # re-create empty list to add next load of values
                temp = list()
                # add tournament code to new list
                temp.append(current_item)
                # used to remove header
                add_to_list = True

        # push last code to stack
        s.push(temp)

        # loop through stack that holds lists with info about each tournament and
        # respective prize money allocations
        for i in range(s.size()):
            current = s.pop()
            if len(current) > 0:
                # get tournament code which is at start of list
                code = current.pop(0)
                # sort list values into dict of position ranked and money earned
                prize_money = dict()
                for j in range(len(current)):
                    if len(current) > 0:
                        position = current.pop(0)
                        money = current.pop(0)
                        money = money.replace(',', '')
                        # strip unwanted characters
                        # put tournament prize money into dictionary
                        prize_money[position] = money
                    else:
                        continue
                # create new male tournament object
                code.replace(" ","")
                if(code == "Tournament"):
                    break
                gender = 'MEN'
                rounds = import_round_results(code, gender)
                current_tournament = Tournament(code, prize_money, male_players, gender, rounds)
                list_of_tournaments.append(current_tournament)

                # create new female tournament object
                gender = 'LADIES'
                rounds = import_round_results(code, gender)
                current_tournament = Tournament(code, prize_money, female_players, gender, rounds);
                list_of_tournaments.append(current_tournament)
                
            else:
                continue

        # removes header from list

        return list_of_tournaments
    
# managing the first round results
def import_round_results(tournament_code, gender):

    list_of_rounds = list()
    # loop through all of the rounds for the tournament
    for i in range(0, 5):
        file_row_list = open_file(os.path.join(os.path.dirname(__file__), "Data/{0} {1}/{0} ROUND {2} {1}.csv".format(tournament_code, gender, i+1)))
        file_row_list.pop(0)
        list_of_matches = list()

        # loop through all matches imported from the file
        for row in file_row_list:
            
            player_one = row[0]
            score_one = row[1]
            player_two = row[2]
            score_two = row[3]

            match_results = Match.evaluate_match_score(int(score_one), int(score_two), gender)

            winning_score = match_results[0]
            score_difference = match_results[1]

            # Determine the winner and create the match 
            if winning_score == 1:
                current_match = Match(player_one, player_two, score_difference)
            elif winning_score == 2:
                current_match = Match(player_two, player_one, score_difference)
            # if the score is 3, this means that we have an incorrect match. durinng processing this will be corrected
            elif winning_score == 3:
                current_match = Match(player_one, player_two,score_difference, True)

            list_of_matches.append(current_match)

        # Create new round object and append it to the list of rounds to be stored wihtin the tournament
        list_of_rounds.append(Round(i+1, list_of_matches))

    return list_of_rounds


# writing to files
def write_to_file(list_to_write, directory, name_of_file):
    # use 'with' command closes file after everything is executed
    # open file, write rows in list to file
    with open('{0}/{1}.csv'.format(directory, name_of_file), 'w', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerows(list_to_write)
