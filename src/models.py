from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

    class People(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(50), nullable=False, default="N/A")
        eye_color = db.Column(db.String(15), nullable=True, default="N/A")
        hair_color = db.Column(db.String(15), nullable=True, default="N/A")
        home_world = db.Column(db.String(50), nullable=True, default="N/A")
        gender = db.Column(db.String(20), nullable=True, default="N/A")
        height = db.Column(db.String(20), nullable=True, default="N/A")
        weight = db.Column(db.String(20), nullable=True, default="N/A")
        skin_color = db.Column(db.String(20), nullable=True, default="N/A")
        date_of_birth = db.Column(db.String(25), nullable=True, default="N/A")

    def __repr__(self):
        return '<Character %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "eye_color": self.eye_color,
            "hair_color": self.hair_color,
            "home_world": self.home_world,
            "gender": self.gender,
            "height": self.height,
            "weight": self.weight,
            "skin_color": self.skin_color,
            "date_of_birth": self.date_of_birth
        }

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    planet_name = db.Column(db.String(60), nullable=False)
    orbital_period = db.Column(db.String(50), nullable=True)
    rotation_period = db.Column(db.String(50), nullable=True)
    diameter = db.Column(db.String(60), nullable=True)
    climate = db.Column(db.String(80), nullable=True)
    land = db.Column(db.String(80), nullable=True)
    gravity = db.Column(db.String(120), nullable=True)
    population = db.Column(db.String(100), nullable=True)
    species_that_inhabit_the_planet = db.Column(db.String(120), nullable=True
    )

    def __repr__(self):
        return '<Planet %r>' % self.planet_name

    def serialize(self):
        return {
            "id": self.id,
            "planet_name": self.planet_name,
            "orbital_period": self.orbital_period,
            "rotation_period": self.rotation_period,
            "diameter": self.diameter,
            "climate": self.climate,
            "land": self.land,
            "gravity": self.gravity,
            "population": self.population,
            "species_that_inhabit_the_planet": self.species_that_inhabit_the_planet
        }


class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("User", backref="favorite")
    people_id = db.Column(db.Integer, db.ForeignKey("people.id"), nullable=False)
    people = db.relationship("People", backref="favorite")
    planet_id = db.Column(db.Integer, db.ForeignKey("planet.id"), nullable=False)
    planet = db.relationship("Planet", backref="favorite")

    def __repr__(self):
        return '<Favorite %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "people_id": self.people_id,
            "planet_id": self.planet_id
        }