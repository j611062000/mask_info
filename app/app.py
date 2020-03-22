from flask import Flask
from flask import render_template
from util import update_mask_info

app = Flask(__name__)

dir_to_be_watched = ["/app/templates"]


@app.route("/")
def mask_info():
    update_mask_info()
    return render_template("mask_infos.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", extra_files=dir_to_be_watched)

