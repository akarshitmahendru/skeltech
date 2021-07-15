from collections import Counter

from django.shortcuts import render
import requests
import json
from django.views.generic import TemplateView

base_url = "http://www.mocky.io/v2/5d403d913300003a209d2ad3"


class UserMessageView(TemplateView):
    template_name = 'user_messages.html'

    def get_context_data(self, **kwargs):
        ctx = super(UserMessageView, self).get_context_data(**kwargs)
        resp_list = list()
        try:
            resp_obj = requests.get(
                base_url
            )
            data = json.loads(resp_obj.content)
            list_data = data.split(',')
            result = sorted(list_data, key=list_data.count,
                            reverse=True)
            usernames_list = []
            for obj in list_data:
                usernames = obj.split(':')
                usernames_list.append(usernames[0])
            # SL = sorted((x, i) for i, x in enumerate(list_data))
            user_count = dict(Counter(usernames_list))
            obj = sorted(user_count.items(), key=lambda x: x[1], reverse=True)[:5]
            resp_dict = dict()
            for value in obj:
                resp_dict["username"] = value[0]
                resp_dict["message_count"] = value[1]
                dict_copy = resp_dict.copy()
                resp_list.append(dict_copy)
            # list_obj = [list(val) for val in obj]
        except Exception as e:
            print(e)
        ctx['header'] = ['Username', 'Message Count']
        ctx['rows'] = resp_list
        return ctx
