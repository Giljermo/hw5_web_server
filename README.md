# hw5_web_server

Веб-сервер, частично реализующий протокол HTTP. Использована архитектура threading.


## Запуск Сервера

`python3 httpd.py`


## Тестирование
Запуск тестов осуществляется по комманде `python httptest.py`
Перед запуск теста необходимо запустить сервер.


## Результаты ab тестирования
hw5_web_server>ab -n 50000 -c 100 -r http://localhost:8098/httptest/dir2/
This is ApacheBench, Version 2.3 <$Revision: 1879490 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking localhost (be patient)
Completed 5000 requests
Completed 10000 requests
Completed 15000 requests
Completed 20000 requests
Completed 25000 requests
Completed 30000 requests
Completed 35000 requests
Completed 40000 requests
Completed 45000 requests
Completed 50000 requests
Finished 50000 requests


Server Software:        ('127.0.0.1',
Server Hostname:        localhost
Server Port:            8098

Document Path:          /httptest/dir2/
Document Length:        34 bytes

Concurrency Level:      100
Time taken for tests:   34.256 seconds
Complete requests:      50000
Failed requests:        0
Total transferred:      8900000 bytes
HTML transferred:       1700000 bytes
Requests per second:    1459.60 [#/sec] (mean)
Time per request:       68.512 [ms] (mean)
Time per request:       0.685 [ms] (mean, across all concurrent requests)
Transfer rate:          253.72 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   9.7      0     517
Processing:    12   62 110.2     46    2108
Waiting:        5   48 100.2     34    2099
Total:         12   62 111.2     46    2109

Percentage of the requests served within a certain time (ms)
  50%     46
  66%     49
  75%     50
  80%     50
  90%     52
  95%     55
  98%    556
  99%    563
 100%   2109 (longest request)
