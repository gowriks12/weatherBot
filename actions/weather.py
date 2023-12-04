import requests

def Weather(city):
    city_api = "http://api.openweathermap.org/data/2.5/find?q={}&appid=d08af5634aa7ec71bd943b651ed453ca".format(city)
    city_json = requests.get(city_api).json()
    json_data = city_json['list'][0]
    format_add = json_data['main']
    temp = int(format_add['temp']-273)
    # print(format_add)
    return temp
