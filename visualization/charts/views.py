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
    ip_count = [850003.2, 821.4, 829, 1048, 1014]
    data = {'ip_time': ip_time, 'ip_count': ip_count}
    return render(request, "charts/chart_test.html",
                              {'data': data})


def basic_statistic(request):
    # current, just load the data from file
    print(os.getcwd())
    data_file = '../../crawler/output/chart_data'
    return render_data(request, data_file)


def render_data(request, data_file):
    # data_file = '../../../crawler/output/daily_cache'
    with open(data_file, "rb") as f:
        daily_data = pickle.load(f)

    # print(daily_data)

    # test_data = [("a", {'x_data': [121212], 'on': [1], 'up': [2], 'down': [3], 'inc': [5], 'dec': [6]})]
    names = [v[0] for v in daily_data]
    data = [v[1] for v in daily_data]
    # print(names)
    # print(data)
    return render(request, "charts/basic_statistic.html",
                  {'names': names, 'data': data})


def new_basic_statistic(request, city):
    data_file = '../../new_crawler/chart_data/' + city
    return render_data(request, data_file)


def jianwei_monthly(request):
    data_file = '../../new_crawler/chart_data/' + 'monthly_detail'
    with open(data_file, 'rb') as input_file:
        detail_data = pickle.load(input_file)
    detail_data = [value for key, value in detail_data['data'].items()]

    return render(request, "charts/jianwei_monthly_detail.html",
                  {'data': detail_data})


def load_jianwei_daily_data(data_file):
    with open(data_file, 'rb') as input_file:
        daily_data = pickle.load(input_file)
    title = daily_data['title']
    x_data = daily_data['date']
    names = []
    data = []
    count = 0
    for key, value in daily_data.items():
        if key == 'title' or key == 'date' or key == 'last':
            continue
        names.append(key)
        data.append(value)
        count += 1
    return title, x_data, names, data, count


def jianwei_daily(request):
    title_g = []
    x_data_g = []
    names_g = []
    data_g = []
    for data_file in ['../../new_crawler/chart_data/daily_check',
                      '../../new_crawler/chart_data/daily_signed']:
        title, x_data, names, data, count = load_jianwei_daily_data(data_file)
        title_g.append(title)
        x_data_g.append(x_data)
        names_g.append(names)
        data_g.append(data)
    return render(request, "charts/jianwei_daily_detail.html",
                  {'title': title_g,
                   'x_data': x_data_g,
                   'names': names_g,
                   'data': data_g})

