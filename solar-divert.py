#!/usr/bin/env python3

import sense_energy
import requests
import re
import time
import config
import asyncio
from flask import Flask, Response
from threading import Thread

app = Flask(__name__)

runSenseLoop = False

def refreshSense(sense):
    try:
        sense.get_realtime()
    except:
        # assume we are logged out
        sense = sense_energy.Senseable(config.sense_user, config.sense_pass, wss_timeout=60, api_timeout=60)
        sense.get_realtime()

def senseloop():
    asyncio.set_event_loop(asyncio.new_event_loop())
    global runSenseLoop

    sense = sense_energy.Senseable(config.sense_user, config.sense_pass, wss_timeout=60, api_timeout=60)
    sense.rate_limit = 30

    while runSenseLoop:
        # first check if the evse is even charging
        r = requests.get("http://" + config.openevse_ip + "/r?rapi=%24GS")
        result = re.search('\$OK (\d+) ', r.text)
        evse_state = int(result.group(1))

        if evse_state is not 3:
            # not charging
            print('sleep 900:', evse_state)
            time.sleep(900)
            refreshSense(sense)

        act_kW = sense.active_power
        act_pv_kW = sense.active_solar_power
        act_voltage = sense.active_voltage

        r = requests.get("http://" + config.openevse_ip + "/r?rapi=%24GE")
        result = re.search('\$OK (\d+) ', r.text)
        set_evse_current = int(result.group(1))

        r = requests.get("http://" + config.openevse_ip + "/r?rapi=%24GG")
        result = re.search('\$OK (\d+) ', r.text)
        live_evse_current = int(result.group(1)) // 1000 + 1

        two_phase_voltage = sum(act_voltage)
        avail_kW = act_pv_kW - act_kW
        avail_current = avail_kW / two_phase_voltage

        if avail_current < 0 and avail_current > -1:
            avail_current = avail_current - 1

        new_curr = live_evse_current + int(avail_current)

        if config.debug:
            localtime = time.asctime(time.localtime(time.time()))
            print("Local current time:", localtime)
            print('act_kW:', act_kW)
            print('act_pv_kW:', act_pv_kW)
            print('avail_kW:', avail_kW)
            print('avail_current', avail_current)
            print('act_voltage:', act_voltage)
            print('two_phase_voltage', two_phase_voltage)
            print('set_evse_current:', set_evse_current)
            print('live_evse_current', live_evse_current)
            print('new_curr', new_curr)

        if abs(avail_current) < 1:
            print("no change: avail_current < 1")
        elif set_evse_current > live_evse_current and new_curr >= set_evse_current:
            print('no change: set > live and new >= set')
        elif new_curr > config.max_curr:
            print("no change: max current")
        elif new_curr < config.min_curr:
            print("no change: min current")
        else:
            print("change current to:", new_curr)
            r = requests.get("http://" + config.openevse_ip + "/r?rapi=%24SC+" + str(new_curr))
            print(r.text)

        time.sleep(config.loop_sleep)
        sense.get_realtime()

def manualRun():
    t = Thread(target=senseloop)
    t.start()
    return "Started SenseLoop"

@app.route("/start")
def set_start_run():
    global runSenseLoop
    runSenseLoop = True
    return Response(manualRun(), mimetype="text/html")

@app.route("/stop")
def set_stop_run():
    global runSenseLoop
    runSenseLoop = False
    r = requests.get("http://" + config.openevse_ip + "/r?rapi=%24SC+" + str(config.max_curr))
    return "Stopped SenseLoop"

if __name__ == "__main__":
    app.run(host='0.0.0.0')

