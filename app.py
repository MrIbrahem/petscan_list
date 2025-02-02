from flask import Flask, request, render_template, jsonify
from urllib.parse import quote
from PetScanList import one_page, MakeTemplate
from PetScanList import valid_wikis
from PetScanList.I18n import get_translations

app = Flask(__name__)

translations = get_translations()


def is_valid_petscan_url(url: str) -> bool:
    """
    Checks if the given URL is a valid PetScan URL.

    A valid PetScan URL starts with either https://petscan.wmflabs.org/ or https://petscan.wmcloud.org/.

    Args:
        url: The URL to validate.

    Returns:
        True if the URL is a valid PetScan URL, False otherwise.
    """
    urls = ["https://petscan.wmflabs.org", "https://petscan.wmcloud.org"]
    return any(url.startswith(u) for u in urls)


@app.route("/wikis", methods=["GET"])
def get_valid_wikis():
    return jsonify(valid_wikis)


@app.route("/template", methods=["POST", "GET"])
def template():
    url = request.form.get("url")

    if not url:
        return render_template("template_form.html")

    # Validate and sanitize the URL
    if not is_valid_petscan_url(url):
        return render_template("template_form.html", error=translations["invalid_url"], url=url)
    try:
        result = MakeTemplate(url)
    except Exception as e:
        error = translations["unexpected_error"].format(error=str(e))
        return render_template("template_form.html", error=error, url=url), 400

    return render_template("template_form.html", result=result, url=url)


@app.route("/update", methods=["GET"])
def update():
    title = request.args.get("title")
    wiki = request.args.get("wiki")
    encoded_title = quote(title)
    url = f"https://{wiki}/wiki/{encoded_title}"
    # ---
    if wiki not in valid_wikis:
        error = translations["wiki_not_supported"].format(wiki=wiki)
        return render_template("result.html", title=title, result=error, url=url, result_class="danger"), 400
    # ---
    result_class = ""
    # ---
    if not title:
        return render_template("result.html", title=title, result=translations["title_required"], url=url, result_class="danger"), 400
    try:
        result, result_class = one_page(title, wiki)

    except ValueError as ve:
        error = translations["value_error"].format(error=str(ve))
        return render_template("result.html", title=title, result=error, url=url, result_class="danger"), 400

    except ConnectionError as ce:
        error = translations["connection_error"].format(error=str(ce))
        return render_template("result.html", title=title, result=error, url=url, result_class="danger"), 400

    except Exception as e:
        error = translations["unexpected_error"].format(error=str(e))
        return render_template("result.html", title=title, result=error, url=url, result_class="danger"), 400

    return render_template("result.html", title=title, result=result, url=url, result_class=result_class)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", wikis=valid_wikis)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("error.html", title=translations["invalid_url"], error=str(e)), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template("error.html", title=translations["unexpected_error"], error=str(e)), 500


if __name__ == "__main__":
    app.run(debug=True)
