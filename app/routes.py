import random
from flask import Blueprint, jsonify, request, render_template
from .extensions import db
from .models import Cafe

api = Blueprint("api", __name__)

API_KEY_FOR_DELETION = "TopSecretAPI"

def to_bool(v):
    return str(v).strip().lower() in ("1", "true", "yes", "y", "on")

@api.route("/")
def home():
    return render_template("index.html")

@api.route("/random", methods=["GET"])
def get_random_cafe():
    cafes = db.session.execute(db.select(Cafe)).scalars().all()
    if not cafes:
        return jsonify(error="No cafes found"), 404
    cafe = random.choice(cafes)
    return jsonify(cafe=cafe.to_dict()), 200

@api.route("/all", methods=["GET"])
def get_all_cafes():
    cafes = db.session.execute(db.select(Cafe)).scalars().all()
    return jsonify(cafes=[c.to_dict() for c in cafes]), 200

@api.route("/search", methods=["GET"])
def search_cafe():
    location = request.args.get("loc")
    if not location:
        return jsonify(error="Missing query parameter: loc"), 400

    cafes = db.session.execute(
        db.select(Cafe).where(Cafe.location == location)
    ).scalars().all()

    return jsonify(cafes=[c.to_dict() for c in cafes]), 200

@api.route("/add", methods=["POST"])
def add_cafe():
    # Supports either JSON body or form data
    data = request.get_json(silent=True) or request.form

    required = ["name", "map_url", "img_url", "location", "seats",
                "has_toilet", "has_wifi", "has_sockets", "can_take_calls"]
    missing = [k for k in required if data.get(k) in (None, "")]
    if missing:
        return jsonify(error=f"Missing fields: {', '.join(missing)}"), 400

    new_cafe = Cafe(
        name=data.get("name"),
        map_url=data.get("map_url"),
        img_url=data.get("img_url"),
        location=data.get("location"),
        seats=data.get("seats"),
        has_toilet=to_bool(data.get("has_toilet")),
        has_wifi=to_bool(data.get("has_wifi")),
        has_sockets=to_bool(data.get("has_sockets")),
        can_take_calls=to_bool(data.get("can_take_calls")),
        coffee_price=data.get("coffee_price")
    )
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(message="Cafe added", cafe=new_cafe.to_dict()), 201

@api.route("/update-price/<int:cafe_id>", methods=["PATCH"])
def update_price(cafe_id):
    # Accept price via query param or JSON
    new_price = request.args.get("new_price")
    if not new_price:
        payload = request.get_json(silent=True) or {}
        new_price = payload.get("coffee_price")

    if not new_price:
        return jsonify(error="Provide new_price (query) or coffee_price (JSON)"), 400

    cafe = db.session.execute(
        db.select(Cafe).where(Cafe.id == cafe_id)
    ).scalar_one_or_none()

    if cafe is None:
        return jsonify(error="Cafe not found"), 404

    cafe.coffee_price = new_price
    db.session.commit()
    return jsonify(message="Price updated", cafe=cafe.to_dict()), 200

@api.route("/report-closed/<int:cafe_id>", methods=["DELETE"])
def delete_cafe(cafe_id):
    api_key = request.args.get("api-key")
    if api_key != API_KEY_FOR_DELETION:
        return jsonify(error="Invalid API key"), 403

    cafe = db.session.execute(
        db.select(Cafe).where(Cafe.id == cafe_id)
    ).scalar_one_or_none()

    if cafe is None:
        return jsonify(error="Cafe not found"), 404

    db.session.delete(cafe)
    db.session.commit()
    return jsonify(message="Cafe deleted", cafe=cafe.to_dict()), 200
