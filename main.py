import json
import os
import sys

import requests
from reamber.osu.OsuMap import OsuMap

r = requests.get('http://127.0.0.1:24050/json')
json = json.loads(r.text)['menu']['bm']['path']

SONG_FOLDER = 'E:\\Games\\osu!\\Songs\\'
FOLDER = SONG_FOLDER + json['folder'] + '\\'
RATE = float(sys.argv[1])

m = OsuMap.readFile(FOLDER + json['file'])
m.rate(RATE, True)

for offset in m.bpms:
    offset.bpm = offset.bpm * RATE

m.version = m.version + " {}x".format(RATE)
m.audioFileName = json['audio'][:-4] + "{}.mp3".format(RATE)
m.writeFile(FOLDER + json['file'][:-4] + " {}.osu".format(RATE))

os.system(f'ffmpeg -i "{FOLDER + json["audio"]}" -filter_complex [0:a]atempo={RATE}[s0] -map [s0] "{FOLDER + m.audioFileName}"') # TODO: Don't use os.system+ffmpeg