from collections import Counter

from django.http import JsonResponse
import requests
import json

from django.shortcuts import render
from django.views.generic import TemplateView
from requests.exceptions import ConnectionError

base_url = "http://www.mocky.io/v2/5d403d913300003a209d2ad3"


def user_message_data(request):
    resp_list = list()
    try:
        resp_obj = requests.get(
            base_url
        )
        if resp_obj.status_code == 200:
            try:
                data = json.loads(resp_obj.content)
                list_data = data.split(',')
                result = sorted(list_data, key=list_data.count,
                                reverse=True)
                usernames_list = []
                for obj in list_data:
                    usernames = obj.split(':')
                    usernames_list.append(usernames[0])
                user_count = dict(Counter(usernames_list))
                obj = sorted(user_count.items(), key=lambda x: x[1], reverse=True)[:5]
                resp_dict = dict()
                frequent_message_dict = dict()
                for var in result:
                    formatted_string = var.split(":")[0].replace(" ", "")
                    if formatted_string in frequent_message_dict.keys():
                        continue
                    frequent_message_dict[formatted_string] = var.split(':')[1]
                for value in obj:
                    resp_dict["username"] = value[0].replace(" ", "")
                    resp_dict["message_count"] = value[1]
                    resp_dict["frequent_message"] = frequent_message_dict.get(value[0].replace(" ", ""))
                    dict_copy = resp_dict.copy()
                    resp_list.append(dict_copy)
                ctx = dict()
                ctx['header'] = ['User Name', 'Message Count', 'Most Frequently Sent Message']
                ctx['rows'] = resp_list
                return render(request, template_name='user_messages.html', context=ctx)

            except Exception as e:
                return JsonResponse({'error': e.args[0]})
        else:
            return JsonResponse({'error': f"Unable to connect to {base_url}"})
    except ConnectionError as e:
        return JsonResponse({'error': 'It looks like you are not connected to Internet'})

