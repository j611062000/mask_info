from flask import Flask
from flask import render_template
from flask_caching import Cache
from util import get_mask_infos


app = Flask(__name__)

dir_to_be_watched = ["/app/templates"]


@app.route("/")
@cache.cached(timeout=120)
def mask_info():
    mask_infos = get_mask_infos()
    return render_template(
        "index.html", time=mask_infos[0].update_time, mask_infos=mask_infos
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", extra_files=dir_to_be_watched)
