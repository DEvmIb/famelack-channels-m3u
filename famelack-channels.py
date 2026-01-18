import os
import sys
import json
from pathlib import Path

try:
    m3u_dach = "#EXTM3U\n"
    m3u_all = "#EXTM3U\n"
    num_dach = 1
    num_all = 1
    if not os.path.isdir("m3u"):
        os.makedirs("m3u", exist_ok=True)
    if os.path.isdir("famelack-channels/channels/raw/countries"):
        for file in Path("famelack-channels/channels/raw/countries").glob("*.json"):
            if not file.is_file():
                continue
            country = file.stem
            print(country)
            m3u = "#EXTM3U\n"

            num = 1
            with open(
                f"famelack-channels/channels/raw/countries/{country}.json", "r"
            ) as f:
                try:
                    data = json.load(f)
                except:
                    print(f"json error: {file.stem}")
                    continue
                for channel in data:
                    if len(channel["iptv_urls"]):
                        m3u += f'#EXTINF:0001 tvg-id="{channel["nanoid"]}" tvg-chno="{num}" group-title="famelack ({file.stem}) [{channel["country"]}] [{channel["isGeoBlocked"]}]" tvg-logo="", {channel["name"]}\n'
                        m3u += f'{channel["iptv_urls"][0]}\n'
                        m3u_all += f'#EXTINF:0001 tvg-id="{channel["nanoid"]}" tvg-chno="{num_all}" group-title="famelack ({file.stem}) [{channel["country"]}] [{channel["isGeoBlocked"]}]" tvg-logo="", {channel["name"]}\n'
                        m3u_all += f'{channel["iptv_urls"][0]}\n'
                        if country == "de" or country == "ad" or country == "ch":
                            m3u_dach += f'#EXTINF:0001 tvg-id="{channel["nanoid"]}" tvg-chno="{num_dach}" group-title="famelack ({file.stem}) [{channel["country"]}] [{channel["isGeoBlocked"]}]" tvg-logo="", {channel["name"]}\n'
                            m3u_dach += f'{channel["iptv_urls"][0]}\n'
                            num_dach += 1
                        num += 1
                        num_all += 1
            with open(f"m3u/{file.stem}.m3u", "w") as f:
                f.write(m3u)
        with open(f"m3u/_dach.m3u", "w") as f:
            f.write(m3u_dach)
        with open(f"m3u/_all.m3u", "w") as f:
            f.write(m3u_all)
        sys.exit(0)
    else:
        print("famelack-channels folder missing")
        sys.exit(1)
except Exception as e:
    print("error processing files", e)
    sys.exit(1)
