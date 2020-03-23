from flask import Flask
from flask import render_template
from util import update_mask_info

app = Flask(__name__)

dir_to_be_watched = ["/app/templates"]


@app.route("/")
def mask_info():
    maskInfos_objs = update_mask_info()
    return render_template(
        "index.html", time=maskInfos_objs[0].update_time, mask_infos=maskInfos_objs
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", extra_files=dir_to_be_watched)
