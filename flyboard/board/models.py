from flyboard import db, Base


class Board(Base):
    __tablename__ = 'board'
    uri = db.Column(db.String(64), nullable=False, unique=True)
    title = db.Column(db.String(96), nullable=False)
    description = db.Column(db.String(128), nullable=False)