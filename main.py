import json
import os
import argparse

import requests
from reamber.osu.OsuMap import OsuMap
from reamber.osu.OsuHit import OsuHit

parser = argparse.ArgumentParser(description='osu!mania rate changer.')
parser.add_argument("rate", type=float)
parser.add_argument("-od", help="Change the od to [value]", type=int)
parser.add_argument("-nsv", help="Removes all the SVs in a map", action='store_true')
parser.add_argument("-nln", help="Removes all the LNs in a map", action='store_true')
args = parser.parse_args()

r = requests.get('http://127.0.0.1:24050/json')
jsons = json.loads(r.text)['menu']['bm']['path']

SONG_FOLDER = json.loads(r.text)['settings']['folders']['songs']
FOLDER = f"{SONG_FOLDER}\\{jsons['folder']}\\"
RATE = float(args.rate)

m = OsuMap.read_file(FOLDER + jsons['file'])
m_ = m.rate(RATE)

if args.rate != 1.0:
    m_.version = f"{m_.version} {RATE}x {round(m_.bpms[0].bpm, 1)}bpm"
    m_.audio_file_name = f"{jsons['audio'][:-4]} {RATE}.mp3"
    os.system(
        f'ffmpeg -i "{FOLDER + jsons["audio"]}" -filter_complex [0:a]atempo={RATE}[s0] -map [s0] "{FOLDER + m_.audio_file_name}"')

filename = f"{FOLDER + jsons['file'][:-4]} {RATE}"

if args.od is not None:
    m_.overall_difficulty = args.od
    m_.version += f" OD {args.od}"
    filename += f" od{args.od}"

if args.nsv is True:
    m_.svs = m_.svs[:0]
    m_.bpms = m_.bpms[:1]
    m_.version += " NSV"
    filename += " NSV"

if args.nln is True:
    for ln in m_.holds:
        m_.hits = m_.hits.append(OsuHit(ln.offset, int(ln.column)))
    m_.holds.df = m_.holds.df[:0]
    m_.version += " NLN"
    filename += " NLN"


filename += ".osu"
m_.write_file(filename)
