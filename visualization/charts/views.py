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
    data_file = '../../crawler/output/chart_data'
    render_data(request, data_file)


def render_data(request, data_file):
    # data_file = '../../../crawler/output/daily_cache'
    with open(data_file, "rb") as f:
        daily_data = pickle.load(f)

    # print(daily_data)

    # test_data = [("a", {'x_data': [121212], 'on': [1], 'up': [2], 'down': [3], 'inc': [5], 'dec': [6]})]
    names = [v[0] for v in daily_data]
    data = [v[1] for v in daily_data]
    print(names)
    print(data)
    return render(request, "charts/basic_statistic.html",
                  {'names': names, 'data': data})


def new_basic_statistic(request, city):
    data_file = '../../new_crawler/chart_data/' + city
    render_data(request, data_file)

