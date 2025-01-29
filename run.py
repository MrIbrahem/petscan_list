from flask import Flask, request, jsonify, render_template
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


if __name__ == "__main__":
    app.run(debug=True)
