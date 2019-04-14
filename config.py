#!/usr/bin/env python3
import os

debug = True
max_curr = os.getenv('AMP_MAX', 40)
min_curr = os.getenv('AMP_MIN', 12)
sense_user = "email@email.com"
sense_pass = "password"
openevse_ip = "1.1.1.1"