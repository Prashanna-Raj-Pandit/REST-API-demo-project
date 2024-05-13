from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
import random

app = Flask(__name__)
API = 'e0984fkjdnad98qhrkh'


# CREATE DB
class Base(DeclarativeBase):
    pass


# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# cafe TABLE Configuration
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)

    def to_dict(
            self):  # This is a dictionary comprehension function created inside the Cafe class definition. It will be used to turn rows into a dictionary before sending it to jsonify.

        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


# HTTP GET - Read Record
@app.route("/random")
def get_random_cafe():
    result = db.session.execute(db.select(Cafe))
    all_cafe = result.scalars().all()
    random_cafe = random.choice(all_cafe)
    return jsonify(cafe={"name": random_cafe.name,
                         "map_url": random_cafe.map_url,
                         "img_url": random_cafe.img_url,
                         "location": random_cafe.location,
                         "seats": random_cafe.seats,
                         "coffee_price": random_cafe.coffee_price,

                         "amenities": {
                             "can_take_calls": random_cafe.can_take_calls,
                             "has_toilet": random_cafe.has_toilet,
                             "has_wifi": random_cafe.has_wifi,
                             "has_sockets": random_cafe.has_sockets,
                         }

                         }
                   )


@app.route("/all")
def get_all_cafe():
    result = db.session.execute(db.select(Cafe).order_by(Cafe.name))
    all_cafes = result.scalars().all()
    return jsonify(cafe=[cafe.to_dict() for cafe in all_cafes])


@app.route("/search")
def search():
    querry_location = request.args.get("loc")
    result = db.session.execute(db.select(Cafe).where(Cafe.location == querry_location))
    all_cafe = result.scalars().all()
    if all_cafe:
        return jsonify(cafe=[cafe.to_dict() for cafe in all_cafe])
    else:
        return jsonify(error="Sorry we didn't find any cafe at requested location")


# HTTP POST - Create Record
## inorder to add a cafe record u have to create a form to get inputs from user
# HTTP PUT/PATCH - Update Record

# Updating the price of a cafee based on a particular id:
# http://127.0.0.1:5000/update-price/CAFE_ID?new_price=£5.67
@app.route("/update-price/<int:cafe_id>", methods=["PATCH"])
def patch_new_price(cafe_id):
    new_price = request.args.get("new_price")
    cafe = db.session.get(Cafe, cafe_id)
    # cafe = db.session.execute(db.select(Cafe).where(Cafe.id == cafe_id)).scalar()
    if cafe:
        cafe.coffee_price = new_price
        db.session.commit()
        ## Just add the code after the jsonify method. 200 = Ok
        return jsonify(response={"success": "Successfully updated the price."}), 200
    else:
        # 404 = Resource not found
        return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database."}), 404


# HTTP DELETE - Delete Record

@app.route('/report-closed/<int:cafe_id>', methods=['DELETE'])
def delete_cafe(cafe_id):
    api_key = request.args.get('api_key')
    if api_key == API:
        cafe_to_delete = db.session.execute(db.select(Cafe).where(Cafe.id == cafe_id)).scalar()
        db.session.delete(cafe_to_delete)
        db.session.commit()
        return jsonify(response={"success": "Successfully deleted the cafe"}), 200
    else:
        return jsonify(response={"Not Authorized:""you are not allowed to make this change"}), 403


if __name__ == '__main__':
    app.run(debug=True)
