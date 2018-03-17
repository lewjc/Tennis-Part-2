class TournamentCircuit:

    men = 'MEN'
    ladies = 'LADIES'

    def __init__(self, list_of_tournaments, ranking_points,
                 male_circuit_players, female_circuit_players):

        self.list_of_tournaments = list_of_tournaments
        self.ranking_points = ranking_points
        self.male_circuit_players = male_circuit_players
        self.female_circuit_players = female_circuit_players

class Player:

    initialize_tournament_points = 0

    def __init__(self, player_name):
        self.name = player_name
        self.prize_money = 0
        self.ranking_points = 0
        self.tournament_points = 0
        self.tournament_money = 0
        self.wins_in_circuit = dict()
        self.losses_in_circuit = dict()
        self.compare_overall_prize_money = False
        self.compare_tournament_money = False
        self.compare_overall_points = False

    # below are methods of comparison for the player objects, each one is determined by a boolean value.

    def __eq__(self, other):
        return self.name == other.name


    def __gt__(self, other):
        if self.compare_overall_points:
            return self.ranking_points > other.ranking_points
        elif self.compare_overall_prize_money:
            return self.prize_money > other.prize_money
        elif self.compare_tournament_money:
            return int(self.tournament_money) > int(other.tournament_money)
        else:
            return self.tournament_points > other.tournament_points
          

    def __lt__(self, other):
        if self.compare_overall_points:
            return self.ranking_points < other.ranking_points
        elif self.compare_overall_prize_money:
            return self.prize_money < other.prize_money
        elif self.compare_tournament_money:
            return int(self.tournament_money) < int(other.tournament_money)
        else:
            return self.tournament_points < other.tournament_points
               

    def __ge__(self, other):
        if self.compare_overall_points:
            return self.ranking_points >= other.ranking_points
        elif self.compare_overall_prize_money:
            return self.prize_money >= other.prize_money
        elif self.compare_tournament_money:
            return int(self.tournament_money) >= int(other.tournament_money)
        else:
            return self.tournament_points >= other.tournament_points

    def __le__(self, other):
        if self.compare_overall_points:
            return self.ranking_points <= other.ranking_points
        elif self.compare_overall_prize_money:
            return self.prize_money <= other.prize_money
        elif self.compare_tournament_money:
            return int(self.tournament_money) <= int(other.tournament_money)
        else:
            return self.tournament_points <= other.tournament_points

    # clear current tournament points

    def reset_tournament_points(self):
        self.tournament_points = 0

    def reset_tournament_money(self):
        self.tournament_money = 0
    
    def initialise_statistics(self, list_of_tournaments):

       self.wins_in_circuit =  {tournament.tournament_code : list() for tournament in list_of_tournaments}
       self.losses_in_circuit = {tournament.tournament_code : list() for tournament in list_of_tournaments}

class Tournament:

    def __init__(self, tournament_code, prize_money_allocation,
                 tournament_players, gender, list_of_rounds):

        self.tournament_code = tournament_code
        self.list_of_rounds = list_of_rounds
        self.gender = gender
        self.prize_money = prize_money_allocation
        self.difficulty = self.assign_tournament_difficulty()
        self.players = tournament_players
        self.complete = False
        self.current_input_round = 0
        self.import_from_file_disabled = False
        self.amount_of_rounds = self.set_amount_of_rounds()
       
    # determine tournament difficulty
    def assign_tournament_difficulty(self):
        if "TAC1" in self.tournament_code:
            return 2.7
        elif "TAE21" in self.tournament_code:
            return 2.3
        elif "TAW11" in self.tournament_code:
            return 3.1
        elif "TBS2"in self.tournament_code:
            return 3.25
        else:
            if self.tournament_code == "Tournament":
                return 0
            while True:
                try:
                    difficulty = float(input("Set {0} Difficulty (Between 1 & 5) :".format(self.tournament_code)))
                    if 1 <= difficulty <= 5:
                        return difficulty
                    else:
                        print("Incorrect Input")
                except ValueError:
                    print("Incorrect Input")

    def set_amount_of_rounds(self):
        i = len(self.players)
        r = 0
        while i != 1:
            i = i / 2
            r += 1
        return r

class Round:   

    def __init__(self, number, list_of_matches, list_of_players):
        self.number = number
        self.list_of_matches = list_of_matches
        self.list_of_players = list_of_players

class Match:

    def __init__(self, winner, winner_score, loser, loser_score, score_difference, is_invalid=False):

        self.winner = winner
        self.winner_score = winner_score
        self.loser = loser
        self.loser_score = loser_score
        self.score_difference = score_difference
        self.is_invalid = is_invalid

    @staticmethod
    def evaluate_match_score(score_one, score_two, gender):

        winning_score = 3
        score_difference = 0
        

        # if the match is a mens score and neither player has reached 3 sets, or either of the mens scores are not between 0 - 3
        if gender == "MEN" and ((score_one !=3 and score_two !=3) or not(0 <= score_one <=3) or not(0 <= score_two <=3)):
            # neither player scored 3, so there is an error
            return (winning_score, score_difference)
        
        elif gender == "LADIES" and ((score_one !=2 and score_two !=2) or not(0 <= score_one <=2) or not(0 <= score_two <=2)):
            # neither player scored 2, so there is an error
            return (winning_score, score_difference)
        
        elif score_one >  score_two:
            score_difference = score_one - score_two
            winning_score = 1
            
        elif score_two > score_one:
            score_difference = score_two - score_one
            winning_score = 2

        return (winning_score, score_difference)

        
    @staticmethod
    def multiply_points(score_difference, gender):

        if score_difference < 2:
            return 1
        elif gender == "LADIES" and score_difference == 2:
            return 2.5
        elif gender == "MEN" and score_difference == 3:
            return 2.5
        elif gender == "MEN" and score_difference == 2:
            return 1.5
        else:
            print('Invalid Gender {0}'.format(gender))
            return 1
