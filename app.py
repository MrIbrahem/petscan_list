from flask import Flask, request, render_template, jsonify
from urllib.parse import quote
from PetScanList import one_page, MakeTemplate, valid_wikis, valid_projects, get_all_pages

app = Flask(__name__)


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


@app.route("/wiki_pages", methods=["GET"])
def get_wiki_pages():
    lang = request.args.get("lang")
    project = request.args.get("project")
    # ---
    if not lang or not project:
        return jsonify([])
    # ---
    pages = get_all_pages(lang, project)
    # ---
    return jsonify(pages)


@app.route("/pages", methods=["GET"])
def get_pages():
    project = request.args.get("project")
    lang = request.args.get("lang")
    # ---
    if lang and project:
        pages = get_all_pages(lang, project)
        return render_template("pages.html", pages=pages, lang=lang, project=project), 200
    # ---
    return render_template("pages.html", wikis=valid_projects), 200


@app.route("/template", methods=["POST", "GET"])
def template():
    url = request.form.get("url")

    if not url:
        return render_template("template_form.html")

    # Validate and sanitize the URL
    if not is_valid_petscan_url(url):
        return render_template("template_form.html", url=url, tt="invalid_url")
    try:
        result = MakeTemplate(url, request.form)
    except Exception as e:
        return render_template("template_form.html", url=url, tt="unexpected_error", tt1=str(e)), 400

    return render_template("template_form.html", result=result, url=url)


@app.route("/update", methods=["GET"])
def update():
    title = request.args.get("title")
    wiki = request.args.get("wiki")
    encoded_title = quote(title)
    url = f"https://{wiki}/wiki/{encoded_title}"
    # ---
    if wiki not in valid_wikis:
        return render_template("result.html", title=title, url=url, result_class="danger", tt="wiki_not_supported", tt1=wiki), 400
    # ---
    result_class = ""
    # ---
    if not title:
        return render_template("result.html", title=title, url=url, result_class="danger", tt="title_required"),

    # result, result_class = one_page(title, wiki)

    try:
        result1, result_class = one_page(title, wiki)
        return render_template("result.html", title=title, url=url, result_class=result_class, tt=result1, tt1=""), 200

    except ValueError as ve:
        return render_template("result.html", title=title, url=url, result_class="danger", tt="value_error", tt1=str(ve)), 400

    except ConnectionError as ce:
        return render_template("result.html", title=title, url=url, result_class="danger", tt="connection_error", tt1=str(ce)), 400

    except Exception as e:
        return render_template("result.html", title=title, url=url, result_class="danger", tt="unexpected_error", tt1=str(e)), 400


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", wikis=valid_wikis)


@app.route("/tutorials", methods=["GET"])
def tutorials():
    return render_template("tutorials.html", wikis=valid_wikis)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("error.html", tt="invalid_url", error=str(e)), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template("error.html", tt="unexpected_error", error=str(e)), 500


if __name__ == "__main__":
    app.run(debug=True)
