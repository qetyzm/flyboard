from flyboard import db, Base


board_flags = db.Table(
    'board_flags',
    db.Column('board_id', db.Integer, db.ForeignKey('board.id'), primary_key=True),
    db.Column('custom_flag_id', db.Integer, db.ForeignKey('custom_flag.id'), primary_key=True)
)


board_file_extensions = db.Table(
    'board_file_extensions',
    db.Column('board_id', db.Integer, db.ForeignKey('board.id'), primary_key=True),
    db.Column('file_extension_id', db.Integer, db.ForeignKey('file_extension.id'), primary_key=True)
)


class Stylesheet(Base):
    __tablename__ = 'stylesheet'
    name = db.Column(db.String(256), nullable=False, unique=True)
    style_content = db.Column(db.String(10000), nullable=False)


class CustomFlag(Base):
    __tablename__ = 'custom_flag'
    name = db.Column(db.String(256), nullable=False, unique=True)
    path = db.Column(db.String(256), nullable=False, unique=True)


class FileExtension(Base):
    __tablename__ = 'file_extension'
    extension = db.Column(db.String(4), nullable=False, unique=True)


class Board(Base):
    __tablename__ = 'board'
    uri = db.Column(db.String(64), nullable=False, unique=True)
    title = db.Column(db.String(96), nullable=False)
    min_files = db.Column(db.SmallInteger, nullable=False)
    max_files = db.Column(db.SmallInteger, nullable=False)
    file_required_for_post = db.Column(db.Boolean, nullable=False)
    default_poster_name = db.Column(db.String(96), nullable=False)
    tripcode_allowed = db.Column(db.Boolean, nullable=False)
    custom_name_allowed = db.Column(db.Boolean, nullable=False)
    embeds_allowed = db.Column(db.Boolean, nullable=False)
    ids_allowed = db.Column(db.Boolean, nullable=False)
    sage_allowed = db.Column(db.Boolean, nullable=False)
    sage_shown = db.Column(db.Boolean, nullable=False)
    max_pages = db.Column(db.Integer, nullable=False)
    archive_pages = db.Column(db.Integer, nullable=False)
    max_file_size_in_mbs = db.Column(db.SmallInteger, nullable=False)
    mute_not_original = db.Column(db.Boolean, nullable=False)
    extra_js = db.Column(db.String(1000000))
    extra_css = db.Column(db.String(1000000))
    animated_thumbnails = db.Column(db.Boolean, nullable=False)
    mute_videos = db.Column(db.Boolean, nullable=False)
    default_css = db.Column(db.Integer, db.ForeignKey('stylesheet.id'))
    show_country_flags = db.Column(db.Boolean, nullable=False)
    allowed_file_extensions = db.relationship(
        'FileExtension', secondary=board_file_extensions, 
        lazy='subquery', 
        backref=db.backref('boards', lazy=True))
    custom_flags = db.relationship(
        'CustomFlag', secondary=board_flags, 
        lazy='subquery', 
        backref=db.backref('boards', lazy=True))

    def __init__(
        self, 
        uri, 
        title, 
        min_files=1, 
        max_files=1, 
        file_required_for_post=False,
        default_poster_name="Anonymous",
        tripcode_allowed=False,
        custom_name_allowed=False,
        embeds_allowed=False,
        ids_allowed=False,
        sage_allowed=True,
        sage_shown=True,
        max_pages=10,
        archive_pages=5,
        max_file_size_in_mbs=10,
        mute_not_original=False,
        extra_js="",
        extra_css="",
        animated_thumbnails=False,
        mute_videos=True,
        show_country_flags=False):
        self.uri = uri
        self.title = title
        self.min_files = min_files
        self.max_files = max_files
        self.file_required_for_post = file_required_for_post
        self.default_poster_name = default_poster_name
        self.tripcode_allowed = tripcode_allowed
        self.custom_name_allowed = custom_name_allowed
        self.embeds_allowed = embeds_allowed
        self.ids_allowed = ids_allowed
        self.sage_allowed = sage_allowed
        self.sage_shown = sage_shown
        self.max_pages = max_pages
        self.archive_pages = archive_pages
        self.max_file_size_in_mbs = max_file_size_in_mbs
        self.mute_not_original = mute_not_original
        self.extra_js = extra_js
        self.extra_css = extra_css
        self.animated_thumbnails = animated_thumbnails
        self.mute_videos = mute_videos
        self.show_country_flags = show_country_flags
        self.allowed_file_extensions = []
        self.custom_flags = []
    
    def get_formatted_file_extensions(self):
        return ", ".join(list(map(lambda x: x.extension, self.allowed_file_extensions)))