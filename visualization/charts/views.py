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
    # data_file = '../../../crawler/output/daily_cache'
    with open(data_file, "rb") as f:
        daily_data_tmp = pickle.load(f)
    daily_data = daily_data_tmp['data']
    districts = dict()
    for key in sorted(list(daily_data.keys())):
        value = daily_data[key]['districts']
        for dis_name, dis_value in value.items():
            if dis_name not in districts:
                districts[dis_name] = {'x_data': [], 'on': [], 'up': [], 'down': [], 'inc': [], 'dec': []}
                break  # ignore the data of first day, because all the data is marked as new up.
            districts[dis_name]['x_data'].append(key.strftime('%Y-%m-%d'))
            districts[dis_name]['on'].append(dis_value['on_sell_count'])
            districts[dis_name]['up'].append(dis_value['up_count'])
            districts[dis_name]['down'].append(dis_value['down_count'])
            districts[dis_name]['inc'].append(dis_value['inc_count'])
            districts[dis_name]['dec'].append(dis_value['dec_count'])

    sorted_data = dict()
    for k in sorted(districts.keys(), reverse=True):
        if k == '':
            sorted_data['abnormal'] = districts[k]
        else:
            sorted_data[k] = districts[k]
    print(sorted_data)
    return render(request, "charts/basic_statistic.html",
                  {'data': sorted_data})


