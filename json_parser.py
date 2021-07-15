import json
import requests
import itertools
import operator
from collections import Counter

base_url = "http://www.mocky.io/v2/5d403d913300003a209d2ad3"


def get_json_data():
    try:
        resp_obj = requests.get(
            base_url
        )
        data = json.loads(resp_obj.content)
        L = data.split(',')
        usernames_list = []
        for obj in L:
            usernames = obj.split(':')
            usernames_list.append(usernames[0])
        SL = sorted((x, i) for i, x in enumerate(L))
        d = dict(Counter(usernames_list))
        obj = sorted(d.items(), key=lambda x: x[1], reverse=True)[:5]
        resp_list = list()
        resp_dict = dict()
        for value in obj:
            resp_dict["username"] = value[0]
            resp_dict["message_count"] = value[1]
            resp_list.append(resp_dict)
        list_obj = [list(val) for val in obj]
    except Exception as e:
        print(e)


if __name__ == "__main__":
    get_json_data()
