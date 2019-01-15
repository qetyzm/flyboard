from flyboard import db, Base


class Board(Base):
    __tablename__ = 'board'
    uri = db.Column(db.String(64), nullable=False, unique=True)
    title = db.Column(db.String(96), nullable=False)
    min_files = db.Column(db.SmallInteger, nullable=False)
    max_files = db.Column(db.SmallInteger, nullable=False)
    file_required_for_post = db.Column(db.Boolean, nullable=False)
    embeds_allowed = db.Column(db.Boolean, nullable=False)
    ids_allowed = db.Column(db.Boolean, nullable=False)
    sage_allowed = db.Column(db.Boolean, nullable=False)
    sage_shown = db.Column(db.Boolean, nullable=False)
    max_pages = db.Column(db.Integer, nullable=False)
    archive_pages = db.Column(db.Integer, nullable=False)
    max_file_size_in_mbs = db.Column(db.SmallInteger, nullable=False)
    allowed_file_extensions = db.Column(db.String(200), nullable=False)
    mute_not_original = db.Column(db.Boolean, nullable=False)
    extra_js = db.Column(db.String(10000))
    extra_css = db.Column(db.String(10000))