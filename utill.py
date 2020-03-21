import csv
import requests
import json
import yaml

HTML = """
<!DOCTYPE html>
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
      </tr>
    </thead>
    <tbody>
    
    {{mask_infos}}
     
    </tbody>
  </table>
</div>

</body>
</html>

"""


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


def get_distance(target_addr, HOME):
    distance = (
        "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins="
        + HOME
        + "&destinations="
        + target_addr
        + "&key="
        + API_KEY
    )
    distance_str = json.loads(requests.get(distance).text)["rows"][0]["elements"][0][
        "distance"
    ]["text"]

    distance_km = round(float(distance_str.split(" ")[0]) * 1.61, 2)
    return distance_km


def to_MaskInfo(data_set):
    distance = get_distance(data_set[2], HOME)

    return MaskInfo(
        data_set[1], data_set[2], data_set[3], data_set[4], distance, data_set[-1]
    )


def get_valid_mask_info():

    tmp = list()

    with open(SOURCE) as source:
        csv_reader = csv.reader(source)

        for data_set in list(csv_reader)[1:]:  # skip header
            inventory = int(data_set[4])

            if "臺北市信義區" in data_set[2] and inventory > 1:
                mask_info = to_MaskInfo(data_set)

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
        </tr>
        """.format(
            mask_info.phar_name,
            mask_info.address,
            mask_info.adult_mask,
            mask_info.distance,
        )
    return html_snippet


mask_infos = sorted(get_valid_mask_info(), key=lambda x: x.distance)
html_snippet = render_mask_infos(mask_infos)
time = mask_infos[0].update_time
final_html = render_html(html_snippet, HTML, time)

with open(HTML_FILE_TARGET, "w") as f:
    f.write(final_html)
