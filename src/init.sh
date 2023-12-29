#!/bin/bash

python3 /get.py

cp /openaps/settings/profile.json /openaps/settings/pumpprofile.json
cp /openaps/settings/profile.json /openaps/settings/autotune.json

oref0-autotune --dir=/openaps --ns-host="https://nightscout.eahs.xyz" --start-date="2023-10-16"

cat /openaps/settings/autotune.json

