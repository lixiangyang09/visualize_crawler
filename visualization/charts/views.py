from django.shortcuts import render
from django.http import HttpResponse
import json
import pickle
import os
import datetime


# Create your views here.
def home(request):
    return render(request, 'charts/home.html')


def test_js(request):
    list_data = ['自强学堂', '渲染Json到模板']
    dict_data = {'site': '自强学堂', 'author': '涂伟忠'}
    return render(request, 'charts/test_js.html', {
            'List': json.dumps(list_data),
            'Dict': json.dumps(dict_data)
        })


def chart_test(request):
    ip_time = [20140501, 20140502, 20140503, 20140504, 20140505]
    ip_count = [853, 821, 829, 1048, 1014]
    return render(request, "charts/chart_test.html",
                              {'ip_time': ip_time, 'ip_count': ip_count})


def basic_statistic(request):
    # current, just load the data from file
    print(os.getcwd())
    data_file = '../../crawler/output/daily_cache'
    with open(data_file, "rb") as f:
        daily_data_tmp = pickle.load(f)
    daily_data = daily_data_tmp['data']
    # ignore the data of first day
    data = {'date': [], 'up': [], 'down': [], 'inc': [], 'dec': []}
    for key in sorted(list(daily_data.keys()))[1:]:
        value = daily_data[key]
        data['date'].append(key.strftime('%Y-%m-%d'))
        data['up'].append(value['up_count'])
        data['down'].append(value['down_count'])
        data['inc'].append(value['inc_count'])
        data['dec'].append(value['dec_count'])

    return render(request, "charts/basic_statistic.html",
                  {'data': data})
