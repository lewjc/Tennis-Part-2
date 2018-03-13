
def input_results(current_tournament, ranking_points):

    prize_money = current_tournament.prize_money
    
    prize_money_string = locale.currency(int(prize_money["1"]), grouping=True)

    # output tournament info
    print("=================================================================")
    print("\n[{0}] Players: {1} | Top Prize: ${2} | Difficulty: {3} \n".format(current_tournament.tournament_code,
                                                                           len(current_tournament_players),
                                                                           prize_money_string,
                                                                           tournament_difficulty))
    print("=================================================================\n")
    input("--Press ENTER to start--\n")

    