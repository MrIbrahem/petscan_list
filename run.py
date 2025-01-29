from flask import Flask, request, jsonify
from PetScanList import one_page

app = Flask(__name__)

@app.route("/", methods=["GET"])
def signup():
    data = request.json
    # ---
    title = data.get("title")
    result = one_page(title)
    # ---
    return jsonify({"message": result}), 201


if __name__ == "__main__":
    app.run(debug=True)
