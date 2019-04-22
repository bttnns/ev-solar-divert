# EV-Solar-Divert

Divert excess solar PV Generation to EV using OpenEVSE and Sense Energy.  This takes the current usage and current pv generation from Sense Energy and configures OpenEVSE request an EV plugged in and charging to only pull from the excess solar generation.

Basically it results in your vehicle only charging on excess solar, not taking from the grid unless excess solar generation is small (less than the AMP_MIN).  If excess solar generation is small then we will continue charging at AMP_MIN to reduce wear on the OpenEVSE contactor.

## Instructions

Get this up and running by running it within a container:

```
$ docker run -dt -p 5000:5000 -e AMP_MIN=10 -e AMP_MAX=10 -e SENSE_USER="<sense-user>" -e SENSE_PASS="<sense-pass>" -e OPENEVSE_IP="<192.168.0.0>" -e LOOP_SLEEP=300 --name ev-solar-divert quay.io/quaa/ev-solar-divert:latest
```

## Configuration

- Set your env variables to your system:
  - AMP_MIN: Minimum amp to operate at. As of now OpenEVSE has a bottom limit of 6, don't go lower than that. *This value is optional, the default value is **10***
  - AMP_MAX: Maximum amp to operate at.
    - **WARNING:** Be sure to set this according to your breaker/system. A simple formula to figure it out would be BREAKER_SIZE * .80 = AMP_MAX. *This value is optional, the default value is **40**, which assumes a 50 amp breaker.*  Be sure to adjust this if neccessary.
  - SENSE_USER: Username for sense.com
  - SENSE_PASS: Password for sense.com
  - OPENEVSE_IP: Local IP Adress for OpenEVSE
  - LOOP_SLEEP: The amount of seconds we will wait to rerun the loop.  *This value is optional, the default value is **300**, which is 5 minutes.*

## How to use

- Open a browser to http://<docker-host>:5000/start to start the loop every 5 minutes
  - Once started the loop will check conditions every 5 minutes and adjust the configuration based on realtime values from Sense and OpenEVSE
- Open a browser to http://<docker-host>:5000/stop to stop the loop
