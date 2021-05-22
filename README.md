# Wat's bugging me

Nameko uses greenlets, implicating `implicit cooperative` green threads.  
There's no need for `async` and `await`  keywords, and everything is single-threaded until
the application hits a point where eventlet has monkey-patched the standard library and a
greenthread-switch is performed, while waiting for IO.

I'n this example i'm booting 2 clients who query the same nameko http service.
1 client is requesting /simple that's, well, fairly simple. Returning just a string.

The other client requests only `/sleep/5`, which will `eventlet.sleep(5)`. Since this is
greenlets, you'd image a couple of sleeping threads won't bother, because that's what
greenlets are all about. Right?

Given the nameko output you'll notice the first batch of requests is as excepted.  
Only /simple is requested, and it's quite fast. but as soon as `/sleep/5` kicks in, everything  
is going really slow. Even the simple requests.

If you have any clue, please help me solve this because i'm having trouble using Nameko this way
and i've built quite a stack depending on nameko already.


## Sample output
```log
$ i run --no-web
starting services: Service
127.0.0.1 - - [22/May/2021 17:20:48] "GET /simple HTTP/1.1" 200 158 0.000649
127.0.0.1 - - [22/May/2021 17:20:48] "GET /simple HTTP/1.1" 200 158 0.000513
127.0.0.1 - - [22/May/2021 17:20:48] "GET /simple HTTP/1.1" 200 158 0.000463
... 
127.0.0.1 - - [22/May/2021 17:20:54] "GET /simple HTTP/1.1" 200 158 0.000607
127.0.0.1 - - [22/May/2021 17:20:54] "GET /simple HTTP/1.1" 200 158 0.000293
127.0.0.1 - - [22/May/2021 17:20:58] "GET /sleep/5 HTTP/1.1" 200 145 5.002514
127.0.0.1 - - [22/May/2021 17:20:58] "GET /simple HTTP/1.1" 200 158 4.739142
127.0.0.1 - - [22/May/2021 17:20:58] "GET /simple HTTP/1.1" 200 158 4.731989
127.0.0.1 - - [22/May/2021 17:20:58] "GET /simple HTTP/1.1" 200 158 4.718804
127.0.0.1 - - [22/May/2021 17:20:58] "GET /simple HTTP/1.1" 200 158 4.711290
127.0.0.1 - - [22/May/2021 17:20:58] "GET /simple HTTP/1.1" 200 158 4.699881
127.0.0.1 - - [22/May/2021 17:20:58] "GET /simple HTTP/1.1" 200 158 4.691378
127.0.0.1 - - [22/May/2021 17:20:58] "GET /sleep/5 HTTP/1.1" 200 145 5.001213
127.0.0.1 - - [22/May/2021 17:20:58] "GET /simple HTTP/1.1" 200 158 4.682589
127.0.0.1 - - [22/May/2021 17:20:58] "GET /sleep/5 HTTP/1.1" 200 145 5.001025
127.0.0.1 - - [22/May/2021 17:20:58] "GET /simple HTTP/1.1" 200 158 4.686706
127.0.0.1 - - [22/May/2021 17:20:58] "GET /simple HTTP/1.1" 200 158 4.679246
127.0.0.1 - - [22/May/2021 17:20:58] "GET /sleep/5 HTTP/1.1" 200 145 5.001257
127.0.0.1 - - [22/May/2021 17:20:58] "GET /sleep/5 HTTP/1.1" 200 145 5.001302
127.0.0.1 - - [22/May/2021 17:20:58] "GET /simple HTTP/1.1" 200 158 4.672692
127.0.0.1 - - [22/May/2021 17:20:58] "GET /simple HTTP/1.1" 200 158 4.651805
127.0.0.1 - - [22/May/2021 17:20:58] "GET /sleep/5 HTTP/1.1" 200 145 5.001194
127.0.0.1 - - [22/May/2021 17:20:58] "GET /simple HTTP/1.1" 200 158 4.724382
127.0.0.1 - - [22/May/2021 17:20:58] "GET /simple HTTP/1.1" 200 158 4.716970
127.0.0.1 - - [22/May/2021 17:20:59] "GET /sleep/5 HTTP/1.1" 200 145 5.001458
127.0.0.1 - - [22/May/2021 17:20:59] "GET /simple HTTP/1.1" 200 158 4.739390
127.0.0.1 - - [22/May/2021 17:20:59] "GET /simple HTTP/1.1" 200 158 4.718318
127.0.0.1 - - [22/May/2021 17:20:59] "GET /simple HTTP/1.1" 200 158 4.689685
127.0.0.1 - - [22/May/2021 17:20:59] "GET /simple HTTP/1.1" 200 158 4.658947
127.0.0.1 - - [22/May/2021 17:20:59] "GET /sleep/5 HTTP/1.1" 200 145 5.000932
127.0.0.1 - - [22/May/2021 17:20:59] "GET /simple HTTP/1.1" 200 158 4.665101
127.0.0.1 - - [22/May/2021 17:20:59] "GET /sleep/5 HTTP/1.1" 200 145 5.000695
127.0.0.1 - - [22/May/2021 17:20:59] "GET /simple HTTP/1.1" 200 158 4.688624
127.0.0.1 - - [22/May/2021 17:20:59] "GET /simple HTTP/1.1" 200 158 4.680312
127.0.0.1 - - [22/May/2021 17:20:59] "GET /sleep/5 HTTP/1.1" 200 145 5.001179
127.0.0.1 - - [22/May/2021 17:20:59] "GET /simple HTTP/1.1" 200 158 4.685481
127.0.0.1 - - [22/May/2021 17:21:03] "GET /sleep/5 HTTP/1.1" 200 145 9.683068
127.0.0.1 - - [22/May/2021 17:21:03] "GET /simple HTTP/1.1" 200 158 9.405685
127.0.0.1 - - [22/May/2021 17:21:03] "GET /simple HTTP/1.1" 200 158 9.396326
127.0.0.1 - - [22/May/2021 17:21:03] "GET /simple HTTP/1.1" 200 158 9.376180
127.0.0.1 - - [22/May/2021 17:21:03] "GET /sleep/5 HTTP/1.1" 200 145 9.674844
127.0.0.1 - - [22/May/2021 17:21:03] "GET /simple HTTP/1.1" 200 158 9.374422
127.0.0.1 - - [22/May/2021 17:21:03] "GET /simple HTTP/1.1" 200 158 9.331865
127.0.0.1 - - [22/May/2021 17:21:03] "GET /sleep/5 HTTP/1.1" 200 145 9.656672
127.0.0.1 - - [22/May/2021 17:21:03] "GET /simple HTTP/1.1" 200 158 9.340237
127.0.0.1 - - [22/May/2021 17:21:03] "GET /sleep/5 HTTP/1.1" 200 145 9.657066
127.0.0.1 - - [22/May/2021 17:21:03] "GET /simple HTTP/1.1" 200 158 9.335121
127.0.0.1 - - [22/May/2021 17:21:03] "GET /sleep/5 HTTP/1.1" 200 145 9.641011
127.0.0.1 - - [22/May/2021 17:21:03] "GET /simple HTTP/1.1" 200 158 9.343450
127.0.0.1 - - [22/May/2021 17:21:03] "GET /simple HTTP/1.1" 200 158 9.321959
127.0.0.1 - - [22/May/2021 17:21:03] "GET /simple HTTP/1.1" 200 158 9.312526
127.0.0.1 - - [22/May/2021 17:21:03] "GET /simple HTTP/1.1" 200 158 9.302031
127.0.0.1 - - [22/May/2021 17:21:03] "GET /sleep/5 HTTP/1.1" 200 145 9.709452
127.0.0.1 - - [22/May/2021 17:21:03] "GET /simple HTTP/1.1" 200 158 9.337265
127.0.0.1 - - [22/May/2021 17:21:03] "GET /simple HTTP/1.1" 200 158 9.324089
127.0.0.1 - - [22/May/2021 17:21:04] "GET /sleep/5 HTTP/1.1" 200 145 9.658721
127.0.0.1 - - [22/May/2021 17:21:04] "GET /simple HTTP/1.1" 200 158 9.338679
127.0.0.1 - - [22/May/2021 17:21:04] "GET /simple HTTP/1.1" 200 158 9.333464
127.0.0.1 - - [22/May/2021 17:21:04] "GET /sleep/5 HTTP/1.1" 200 145 9.656940
127.0.0.1 - - [22/May/2021 17:21:04] "GET /sleep/5 HTTP/1.1" 200 145 9.674305
127.0.0.1 - - [22/May/2021 17:21:04] "GET /simple HTTP/1.1" 200 158 9.346639
127.0.0.1 - - [22/May/2021 17:21:04] "GET /simple HTTP/1.1" 200 158 9.342410
127.0.0.1 - - [22/May/2021 17:21:04] "GET /simple HTTP/1.1" 200 158 9.325942
127.0.0.1 - - [22/May/2021 17:21:04] "GET /simple HTTP/1.1" 200 158 9.303735
127.0.0.1 - - [22/May/2021 17:21:04] "GET /sleep/5 HTTP/1.1" 200 145 9.657346
127.0.0.1 - - [22/May/2021 17:21:04] "GET /simple HTTP/1.1" 200 158 9.296511
127.0.0.1 - - [22/May/2021 17:21:04] "GET /simple HTTP/1.1" 200 158 9.296448
127.0.0.1 - - [22/May/2021 17:21:04] "GET /simple HTTP/1.1" 200 158 9.280173
127.0.0.1 - - [22/May/2021 17:21:08] "GET /sleep/5 HTTP/1.1" 200 145 14.377962
127.0.0.1 - - [22/May/2021 17:21:08] "GET /simple HTTP/1.1" 200 158 14.032168
127.0.0.1 - - [22/May/2021 17:21:08] "GET /sleep/5 HTTP/1.1" 200 145 14.331260
127.0.0.1 - - [22/May/2021 17:21:08] "GET /simple HTTP/1.1" 200 158 14.015880
127.0.0.1 - - [22/May/2021 17:21:08] "GET /simple HTTP/1.1" 200 158 13.994989
127.0.0.1 - - [22/May/2021 17:21:08] "GET /simple HTTP/1.1" 200 158 13.976440
... 
127.0.0.1 - - [22/May/2021 17:21:38] "GET /simple HTTP/1.1" 200 158 13.797184
127.0.0.1 - - [22/May/2021 17:21:38] "GET /simple HTTP/1.1" 200 158 13.797421
127.0.0.1 - - [22/May/2021 17:21:38] "GET /simple HTTP/1.1" 200 158 13.784482
127.0.0.1 - - [22/May/2021 17:21:38] "GET /simple HTTP/1.1" 200 158 13.784547
127.0.0.1 - - [22/May/2021 17:21:38] "GET /sleep/5 HTTP/1.1" 200 145 14.026057
127.0.0.1 - - [22/May/2021 17:21:38] "GET /sleep/5 HTTP/1.1" 200 145 14.017973
127.0.0.1 - - [22/May/2021 17:21:38] "GET /sleep/5 HTTP/1.1" 200 145 14.092852
127.0.0.1 - - [22/May/2021 17:21:39] "GET /sleep/5 HTTP/1.1" 200 145 14.041391
127.0.0.1 - - [22/May/2021 17:21:39] "GET /sleep/5 HTTP/1.1" 200 145 14.016351
127.0.0.1 - - [22/May/2021 17:21:39] "GET /sleep/5 HTTP/1.1" 200 145 14.042032
127.0.0.1 - - [22/May/2021 17:21:39] "GET /sleep/5 HTTP/1.1" 200 145 14.015985
127.0.0.1 - - [22/May/2021 17:21:43] "GET /sleep/5 HTTP/1.1" 200 145 18.787904
127.0.0.1 - - [22/May/2021 17:21:43] "GET /sleep/5 HTTP/1.1" 200 145 18.787904
```