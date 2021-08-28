import requests
import json
import copy
from datetime import date, timedelta
from utils import gen_dif_record

GAME = "Footmen%20Vs%20Grunts"
SEASON = "Season%205"
# ET /leaderboard&map=Broken%20Alliances&ladder=Public&season=Season%201&round=Global&mode=2&sort=rank&order=asc&page=1&limit=15
ADDRESS =



dif_dic = gen_dif_record(copy.deepcopy(body))

def diff_stat(dic1, dic2):
    output = {}
    key_list = ["played", "wins", "losses", "rating", "rank"]
    if set(dic1.keys()) != set(dic2.keys()):
        raise KeyError
    for (k, v1, v2) in zip(key_list, dic1.values(), dic2.values()):
        diff = v2 - v1
        diff_str = ("+" if diff > 0 else "") + str(diff)
        output[k] = f"{v2}({diff_str})"
    output["battletag"] = dic1["battletag"]
    return output

diff_stat(body[0], dif_dic[0])
