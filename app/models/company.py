from app.extensions import db
from app.models.tag import Tag


class Company(db.Model):
    __tablename__ = 'company'

    id = db.Column(db.Integer, primary_key=True)
    company_ko = db.Column(db.String(80), unique=True, nullable=True)
    company_en = db.Column(db.String(80), unique=True, nullable=True)
    company_ja = db.Column(db.String(80), unique=True, nullable=True)

    def __init__(self, company_ko, company_en, company_ja):
        self.company_ko = company_ko
        self.company_en = company_en
        self.company_ja = company_ja

    def __repr__(self):
        return f'<Company({self.id}, {self.company_ko}, {self.company_en}, {self.company_ja})>'

    @staticmethod
    def column_list():
        metadata = db.MetaData()
        table = db.Table('company', metadata, autoload=True, autoload_with=db.engine)

        return table.columns.keys()

    def add_column(self, company_list, tag_list):
        for data in company_list:
            sql = f"""
                ALTER TABLE company
                ADD {data} VARCHAR( 80 ) NULL DEFAULT NULL;
            """
            self.session.execute(sql)

        for data in tag_list:
            sql = f"""
                ALTER TABLE tag
                ADD {data} VARCHAR( 80 ) NULL DEFAULT NULL;
            """
            self.session.execute(sql)

        db.session.commit()

    def get_tag(self):
        filters = {"company": self.id}
        tag = db.session.query(Tag).filter_by(**filters).first()

        return tag
