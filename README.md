Divert excess solar to EV using OpenEVSE and Sense Energy

```
$ docker build -t ev-solar-divert .
$ docker run -dt --rm -p 5000:5000 --name ev-solar-divert ev-solar-divert
```
- Open a browser to http://docker-host:5000/start to start the loop every 5 minutes
- Open a browser to http://docker-host:5000/stop to stop the loop
