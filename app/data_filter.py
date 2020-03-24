import json
import yaml

from util import read_config
from util import read_api_key


def filter_by_center(center, source_file_path):
    tmp = {
        "type": "FeatureCollection",
        "features": []
    }
    with open(source_file_path, encoding="utf-8") as f:
        raw_data = json.load(f)
        for pharmacy in raw_data["features"]:
            if center[:7] in pharmacy["properties"]["address"]:
                tmp["features"].append(pharmacy)

        return tmp


def main():
    config = read_config("/etc/config.yaml")
    MASK_DATA_SOURCE_PATH = config["MASK_DATA_SOURCE"]
    CENTER = config["INIT_CENTER"]
    FILTERED_DATA_SOURCE_PATH = config["FILTERED_DATA_SOURCE"]

    with open(FILTERED_DATA_SOURCE_PATH, "w", encoding="utf-8") as f:

        json.dump(filter_by_center(CENTER, MASK_DATA_SOURCE_PATH),
                  f, indent=4)


if __name__ == "__main__":
    main()
