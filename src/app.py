"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route("/peoples", methods=["GET"])
def get_peoples():
    peoples = People.query.all()
    serialized_peoples = [people.serialize() for people in peoples]
    return jsonify({"data": serialized_peoples})


@app.route("/people/<int:id>", methods=["GET"])
def get_people(id):
    people = People.query.filter_by(id = id).one_or_none()
    return jsonify({"data": people.serialize()})


@app.route("/planets", methods=["GET"])
def get_planets():
    planets = Planet.query.all()
    serialized_planets = [planet.serialize() for planet in planets]
    return jsonify({"data": serialized_planets})


@app.route("/planet/<int:id>", methods=["GET"])
def get_planet(id):
    planet = Planet.query.filter_by(id = id).one_or_none()
    return jsonify({"data": planet.serialize()})


@app.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    serialized_users = [user.serialize() for user in users]
    return jsonify({"data": serialized_users})


@app.route("/users/favorites", methods=["GET"])
def get_list_favorites():
    list_favorites = Favorite.query.all()
    serialized_list_favorites = [favorite.serialize() for favorite in list_favorites]
    return jsonify({"data": serialized_list_favorites})

@app.route("/favorite/people/<int:people_id>", methods=["POST"])
def add_personaje_favorito(people_id):
    body = request.JSON
    people_id = body.get("people_id", None)
    user_id = body.get("user_id", None)
    if not people_id:
        return {"error": "Todos los campos requeridos"}, 400
    favorite_exists = Favorite.query.filter_by(user_id=body_user_id, people_id=body_people_id).first()
    if favorite_exists:
        return {"error": f"El personaje ya existe {body_user_id, body_people_id}"}, 400
    new_favorites = Favorite(user_id=body_user_id, people_id=body_people_id)
    db.session.add(new_favorites)

    try:
        db.session.comit()
        return jsonify({"msg": "Se creo exitosamente"}), 201
    except Exception as error:
        db.session.rollback()
        return jsonify({"error": error})


@app.route("/favorite/planet/<int:planet_id>", methods=["POST"])
def add_planeta_favorito(planet_id):
    body = request.JSON
    planet_id = body.get("planet_id", None)
    user_id = body.get("user_id", None)
    if not planet_id:
        return {"error": "Todos los campos son requeridos"}, 400
    favorite_exists = Favorite.query.filter_by(user_id=body_user_id, planet_id=body_planet_id).first()
    if favorite_exists:
        return {"error": f"El planeta ya existe {body_user_id, body_planet_id}"}, 400
    new_favorites = Favorite(user_id=body_user_id, planet_id=body_planet_id)
    db.session.add(new_favorites)

    try:
        db.session.commit()
        return jsonify({"msg": "Se agrego el planeta a favoritos"}), 201
    except Exception as error:
        db.session.rollback()
        return jsonify({"error": error})

@app.route("/favorite/people/<int:people_id>/<int:user_id>", methods=["DELETE"])
def delete_favorite_people(people_id, user_id):
    favorite_delete = Favorite.query.filter_by(people_id=people_id, user_id=user_id).first()
    if not favorite_delete:
        return {"error": "Este personaje no existe en favoritos"}, 400
    db.session.delete(favorite_delete)
    try:
        db.session.commit()
        return {"msg": "El personaje favorito fue eliminado con exito"}, 200
    except Exception as error:
        db.session.rollback()
        return jsonify({"error": error})


@app.route("/favorite/planet/<int:planet_id>/<int:user_id>", methods=["DELETE"])
def delete_favorite_planet(planet_id, user_id):
    favorite_delete = Favorite.query.filter_by(planet_id=planet_id, user_id=user_id).first()
    if not favorite_delete:
        return {"error": "Este planeta no existe en favoritos"}, 400
    db.session.delete(favorite_delete)
    try:
        db.session.commit()
        return {"msg": "El planeta favorito fue eliminado exitosamente"}, 200
    except Exception as error:
        db.session.rollback()
        return jsonify({"error": error})


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
