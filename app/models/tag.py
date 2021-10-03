from app.extensions import db


class Tag(db.Model):
    __tablename__ = 'tag'

    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.Integer, db.ForeignKey('company.id'))
    tag_ko = db.Column(db.String(200), unique=True, nullable=True)
    tag_en = db.Column(db.String(200), unique=True, nullable=True)
    tag_ja = db.Column(db.String(200), unique=True, nullable=True)

    def __init__(self, company, tag_ko, tag_en, tag_ja):
        self.company = company
        self.tag_ko = tag_ko
        self.tag_en = tag_en
        self.tag_ja = tag_ja

    def __repr__(self):
        return '<id %r>' % self.id

    @staticmethod
    def column_list():
        metadata = db.MetaData()
        table = db.Table('tag', metadata, autoload=True, autoload_with=db.engine)

        return table.columns.keys()
