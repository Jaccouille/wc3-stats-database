from random import randint
from datetime import date, timedelta

def gen_dif_record(record_dic):
    for record in record_dic:
        game_played = randint(0, 20)
        record["date"] = date.today() + timedelta(1)

        if game_played > 0:
            wins = game_played - randint(0, game_played)
            losses = game_played - wins

            rating_gain = sum([randint(10, 25) for _ in range(0, wins)])
            rating_loss = sum([randint(10, 25) for _ in range(0, losses)])

            rating_change = rating_gain - rating_loss
            record["played"] = record.get('played') + game_played
            record["wins"] = record.get('wins') + wins
            record["losses"] = record.get('losses') + losses
            record["rating"] = record.get('rating') + rating_change
