from . import db

class Property(db.Model):
   
    __tablename__ = 'properties'

    id = db.Column(db.Integer, primary_key=True, autoincrement =True)
    title = db.Column(db.String(100))
    num_bedrooms = db.Column(db.Integer)
    description = db.Column(db.String(250))
    num_bathrooms = db.Column(db.Integer)
    location = db.Column(db.String(200))
    price = db.Column(db.Integer)
    property_type = db.Column(db.String(20))
    photo = db.Column(db.String(20))
    
    def __init__(self, title, description, num_bedrooms, num_bathrooms, price, property_type, location, photo):
        self.title = title
        self.num_bedrooms = num_bedrooms
        self.description = description
        self.num_bathrooms = num_bathrooms
        self.location = location
        self.price = price
        self.property_type = property_type
        self.photo = photo
        