from server import db


# Model for a University
class University(db.DynamicDocument):
    title = db.StringField()
    uid = db.IntField()

    # TODO
    # comments = db.ListField(db.StringField())

    def to_json(self):
        return {"title": self.name,
                "uid": self.uid,
                "comments": ''}


# Model for a Professor
class Professor(db.DynamicDocument):
    name = db.StringField()
    pid = db.IntField()
    dept = db.StringField()
    no_ratings = db.IntField()
    rating_class = db.StringField()
    overall_rating = db.StringField()
    comments = db.ListField(db.StringField())
    university = db.ReferenceField(University)

    def to_json(self):
        return {"name": self.name,
                "uni": self.university.title,
                "pid": self.pid,
                "comments": self.comments}


# Model for Ratings TODO
class Ratings(db.DynamicDocument):
    test: db.StringField()
