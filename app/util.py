import csv
import requests
import json
import yaml


class MaskInfo:
    def __init__(self, phar_name, address, phone, adult_mask, distance, update_time):
        self.phar_name = phar_name
        self.address = address
        self.phone = phone
        self.adult_mask = adult_mask
        self.update_time = update_time
        self.distance = distance

    def is_city(self, city):
        if city in self.address:
            return True
        else:
            return False


def read_config(config_file_path):
    with open(config_file_path) as f:
        config_data = yaml.load(f)
        return config_data


def get_distance(target_addr, center, api_key):
    distance = (
        "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins="
        + center
        + "&destinations="
        + target_addr
        + "&key="
        + api_key
    )
    distance_str = json.loads(requests.get(distance).text)["rows"][0]["elements"][0][
        "distance"
    ]["text"]

    distance_km = round(float(distance_str.split(" ")[0]) * 1.61, 2)
    return distance_km


def init_MaskInfo_obj(data_set, center, api_key):
    distance = get_distance(data_set["properties"]["address"], center, api_key)

    return MaskInfo(
        data_set["properties"]["name"],
        data_set["properties"]["address"],
        data_set["properties"]["phone"],
        data_set["properties"]["mask_adult"],
        distance,
        data_set["properties"]["updated"],
    )


def get_MaskInfo_objs_by(mask_data_source_path, center, api_key, interest_area):

    tmp = list()

    with open(mask_data_source_path) as source:
        mask_data_set = json.load(source)

        for data_set in mask_data_set["features"]:
            inventory = int(data_set["properties"]["mask_adult"])

            if interest_area in data_set["properties"]["address"] and inventory > 1:
                mask_info = init_MaskInfo_obj(data_set, center, api_key)

                if mask_info.distance < 5:
                    tmp.append(mask_info)
        return tmp


def read_api_key(API_KEY_PATH):
    with open(API_KEY_PATH) as f:
        return yaml.load(f)["api_key"]


def get_confirmed_numbers():
    url = "https://pomber.github.io/covid19/timeseries.json"
    data = json.loads(requests.get(url).text)["Taiwan*"]
    confirmed_today = int(data[-1]["confirmed"]) - int(data[-2]["confirmed"])
    total_confirmed = int(data[-1]["confirmed"])
    return confirmed_today, total_confirmed


def get_mask_infos():
    config = read_config("/etc/config.yaml")
    MASK_DATA_SOURCE_PATH = config["MASK_DATA_SOURCE"]
    API_KEY = read_api_key(config["API_KEY_PATH"])
    CENTER = config["INIT_CENTER"]
    INTEREST_AREA = "台北市信義區"

    maskInfos_objs = sorted(
        get_MaskInfo_objs_by(MASK_DATA_SOURCE_PATH, CENTER, API_KEY, INTEREST_AREA),
        key=lambda x: x.distance,
    )

    return maskInfos_objs


if __name__ == "__main__":
    print(get_confirmed_today())
