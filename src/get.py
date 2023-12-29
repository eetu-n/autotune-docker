import requests
import json

url = 'https://nightscout.eahs.xyz/api/v2/profile.json'

ns_profile = requests.get(url).json()[0]['store']['baseline']

ns_basal = ns_profile['basal']
basal_profile = []
for i in range(len(ns_basal)):
    minutes = 0
    if i < len(ns_basal) - 1:
        minutes = (ns_basal[i + 1]['timeAsSeconds'] - ns_basal[i]['timeAsSeconds']) / 60
    else:
        minutes = (86400 - ns_basal[i]['timeAsSeconds']) / 60
    basal_profile.append({
        'minutes': int(minutes),
        'rate': round(ns_basal[i]['value'], 2),
        'start': ns_basal[i]['time'] + ':00',
        'i': int(i)
    })

ns_isf = ns_profile['sens']
sensitivity = 0
for i in range(len(ns_isf)):
    seconds = 0
    if i < len(ns_isf) - 1:
        seconds = (ns_isf[i + 1]['timeAsSeconds'] - ns_isf[i]['timeAsSeconds'])
    else:
        seconds = (86400 - ns_isf[i]['timeAsSeconds'])
    sensitivity += (seconds * ns_isf[i]['value'])

sensitivity = sensitivity / 86400

ns_carb = ns_profile['carbratio']
carb_ratio = 0
for i in range(len(ns_carb)):
    seconds = 0
    if i < len(ns_carb) - 1:
        seconds = (ns_carb[i + 1]['timeAsSeconds'] - ns_carb[i]['timeAsSeconds'])
    else:
        seconds = (86400 - ns_carb[i]['timeAsSeconds'])
    carb_ratio += (seconds * ns_carb[i]['value'])

carb_ratio = carb_ratio / 86400

oref_profile = {
  "min_5m_carbimpact": 8.0,
  "dia": ns_profile['dia'],
  "basalprofile": basal_profile,
  "isfProfile": {
    "sensitivities": [{
        "i": 0,
        "start": "00:00:00",
        "sensitivity": round(sensitivity * 18, 2),
        "offset": 0,
        "x": 0,
        "endOffset": 1440
    }]
  },
  "carb_ratio": round(carb_ratio, 2),
  "autosens_max": 1.2,
  "autosens_min": 0.7
}

with open('/openaps/settings/profile.json', 'w') as f:
    json.dump(oref_profile, f)

