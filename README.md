###Решение тестового задания 
https://yandex.ru/jobs/vacancies/analytics/data_proc_an_drone/

`author`: @chistopat

**Disclaimer**

Не судите строго, код написан за ночь в поезде Москва-Вологда =)


**Web-UI**
Сверстал макет на вебиксе, но не успел подключить Ajax =(
Он пока очень "деревянный", однако, при наличии еще одной свободной ночи, 
его можно привести к состоянию полноценной админки.

Посмотреть можно тут: https://snippet.webix.com/5kdjoiuz


**Backend**

не успел доделать web - интерфейс, поэтому офоримил рассчет данных в виде 
консольной утилиты


```
python3.7 run.py --url 'https://sdcimages.s3.yandex.net/test_task/data'


{"is_selfdrived": false, "distance": 11.680845877198225, "units": "Meters", "trip_time": 72, "arrival_point": "(36.10892122044222, -115.15558840811516)", "arrival_time": "2019-01-07T01:33:48", "destination_point": "(36.108816686453586, -115.15558696493633)", "destination_time": "2019-01-07T01:35:00"}
{"is_selfdrived": true, "distance": 26.441631669538094, "units": "Meters", "trip_time": 11, "arrival_point": "(36.108816686453586, -115.15558696493633)", "arrival_time": "2019-01-07T01:35:00", "destination_point": "(36.10857904438409, -115.15557722043133)", "destination_time": "2019-01-07T01:35:11"}
{"is_selfdrived": false, "distance": 155.62006639200712, "units": "Meters", "trip_time": 45, "arrival_point": "(36.10857904438409, -115.15557722043133)", "arrival_time": "2019-01-07T01:35:11", "destination_point": "(36.108061842432654, -115.15675158519913)", "destination_time": "2019-01-07T01:35:56"}
{"is_selfdrived": true, "distance": 2554.2535861729675, "units": "Meters", "trip_time": 489, "arrival_point": "(36.108061842432654, -115.15675158519913)", "arrival_time": "2019-01-07T01:35:56", "destination_point": "(36.100759105185894, -115.1514586469808)", "destination_time": "2019-01-07T01:44:05"}
{"is_selfdrived": false, "distance": 84.31702287672321, "units": "Meters", "trip_time": 6, "arrival_point": "(36.100759105185894, -115.1514586469808)", "arrival_time": "2019-01-07T01:44:05", "destination_point": "(36.100771459084264, -115.15052042680973)", "destination_time": "2019-01-07T01:44:11"}
```
