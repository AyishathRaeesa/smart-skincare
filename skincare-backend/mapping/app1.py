from flask import Flask, jsonify, request
from mapping import recommendations

app = Flask(__name__, static_folder='static')  # Do NOT put image paths here

@app.route("/recommendations", methods=["GET"])
def get_recommendations():
    condition = request.args.get("condition")
    if not condition:
        return jsonify({"error": "Please provide a condition parameter"}), 400

    images = recommendations.get(condition, [])
    if not images:
        return jsonify({"error": f"No recommendations found for '{condition}'"}), 404

    return jsonify({"condition": condition, "images": images})

if __name__ == "__main__":
    app.run(debug=True)
