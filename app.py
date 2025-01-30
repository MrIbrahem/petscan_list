from flask import Flask, request, render_template
from PetScanList import one_page, MakeTemplate
from urllib.parse import quote

app = Flask(__name__)


@app.route("/template", methods=["GET"])
def template():
    return render_template("template_form.html")


@app.route("/template_result", methods=["POST", "GET"])
def template_post():
    url = request.form.get("url")

    if not url:
        return render_template("template_form.html")

    result = MakeTemplate(url)

    return render_template("template.html", result=result)


@app.route("/update", methods=["GET"])
def update():
    title = request.args.get("title")
    encoded_title = quote(title)
    url = f"https://ar.wikipedia.org/wiki/{encoded_title}"

    if not title:
        return render_template("result.html", title=title, result="Title parameter is required", url=url), 400
    try:
        result = one_page(title)
    except Exception as e:
        return render_template("result.html", title=title, result=str(e), url=url), 400

    return render_template("result.html", title=title, result=result, url=url)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
