from flask import Flask, request, jsonify, render_template, send_from_directory
from PetScanList import one_page

app = Flask(__name__)


@app.route("/update", methods=["GET"])
def update():
    title = request.args.get("title")
    result = one_page(title)
    url = f"https://ar.wikipedia.org/wiki/{title}"
    return render_template("result.html", title=title, result=result, url=url)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/autocomplete.js", methods=["GET"])
def autocomplete_js():
    return send_from_directory("static", "autocomplete.js")


if __name__ == "__main__":
    app.run(debug=True)
