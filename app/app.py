from flask import Flask
from flask import render_template
from flask import jsonify
from flask_caching import Cache
from util import get_mask_infos


config = {
    "DEBUG": True,  # some Flask specific configs
    "CACHE_TYPE": "simple",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300,
}
app = Flask(__name__)
# tell Flask to use the above defined config
app.config.from_mapping(config)
cache = Cache(app)
cache.init_app(app)


dir_to_be_watched = ["/app/templates"]


@app.route("/")
@cache.cached(timeout=120)
def mask_info():
    mask_infos = get_mask_infos()
    return render_template(
        "index.html", time=mask_infos[0].update_time, mask_infos=mask_infos
    )


@app.route("/api/v1.0/mask_infos", methods=["GET"])
def get_mask_infos():
    return jsonify({"mask_infs": {1: 2}})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", extra_files=dir_to_be_watched)
