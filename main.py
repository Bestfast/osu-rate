import json
import os
import sys

import requests
from reamber.osu.OsuMap import OsuMap

r = requests.get('http://127.0.0.1:24050/json')
jsons = json.loads(r.text)['menu']['bm']['path']

SONG_FOLDER = json.loads(r.text)['settings']['folders']['songs']
FOLDER = f"{SONG_FOLDER}\\{jsons['folder']}\\"
RATE = float(sys.argv[1])

m = OsuMap.readFile(FOLDER + jsons['file'])
m.rate(RATE, True)

for offset in m.bpms:
    offset.bpm *= RATE

m.version = f"{m.version} {RATE}x {round(int(m.bpms[0].bpm), 1)}bpm"
m.audioFileName = jsons['audio'][:-4] + "{}.mp3".format(RATE)
m.writeFile(FOLDER + jsons['file'][:-4] + " {}.osu".format(RATE))

os.system(f'ffmpeg -i "{FOLDER + jsons["audio"]}" -filter_complex [0:a]atempo={RATE}[s0] -map [s0] "{FOLDER + m.audioFileName}"')