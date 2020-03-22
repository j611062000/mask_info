import csv
import requests
import json
import yaml

HTML = """<!DOCTYPE html>
<html lang="en">

<head>
  <title>Bootstrap Example</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>
</head>

<body>

  <div class="container">
    <h2>口罩地圖</h2>
    <p>更新時間: {{time}}</p>
    <table class="table table-striped">
      <thead>
        <tr>
          <th>藥局名稱</th>
          <th>地址</th>
          <th>成人口罩庫存</th>
          <th>距離(km)</th>
          <th>電話</th>
        </tr>
      </thead>
      <tbody>

        {{mask_infos}}

      </tbody>
    </table>
  </div>

</body>

</html>"""


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


def get_MaskInfo_objs_by(mask_data_source_path, center, api_key):

    tmp = list()

    with open(mask_data_source_path) as source:
        mask_data_set = json.load(source)

        for data_set in mask_data_set["features"]:
            inventory = int(data_set["properties"]["mask_adult"])

            if "台北市信義區" in data_set["properties"]["address"] and inventory > 1:
                mask_info = init_MaskInfo_obj(data_set, center, api_key)

                if mask_info.distance < 5:
                    tmp.append(mask_info)
        return tmp


def render_html(html_snippet, HTML, time):
    final_html = HTML.replace("{{mask_infos}}", html_snippet)
    final_html = final_html.replace("{{time}}", time)

    return final_html


def render_mask_infos(mask_infos):
    html_snippet = ""

    for mask_info in mask_infos:
        html_snippet += """
        <tr>
            <td>{0}</td>
            <td><a href='http://maps.google.com/?q={1}'>{1}</a></td>
            <td>{2}</td>
            <td>{3}</td>
            <td>{4}</td>
        </tr>
        """.format(
            mask_info.phar_name,
            mask_info.address,
            mask_info.adult_mask,
            mask_info.distance,
            mask_info.phone
        )
    return html_snippet


def read_api_key(API_KEY_PATH):
    with open(API_KEY_PATH) as f:
        return yaml.load(f)["api_key"]


if __name__ == "__main__":
    config = read_config("/etc/config.yaml")
    MASK_DATA_SOURCE_PATH = config["MASK_DATA_SOURCE"]
    API_KEY = read_api_key(config["API_KEY_PATH"])
    CENTER = config["INIT_CENTER"]
    HTML_FILE_TARGET = config["HTML_FILE_TARGET"]

    maskInfos_objs = sorted(
        get_MaskInfo_objs_by(MASK_DATA_SOURCE_PATH, CENTER, API_KEY),
        key=lambda x: x.distance,
    )

    html_snippet = render_mask_infos(maskInfos_objs)
    time = maskInfos_objs[0].update_time
    final_html = render_html(html_snippet, HTML, time)

    with open(HTML_FILE_TARGET, "w") as f:
        f.write(final_html)
