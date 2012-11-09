import core.db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, UnicodeText

Base = declarative_base()

class TitleTest(Base):
    __tablename__ = "test_seo_titles"

    domain = Column(String(64), primary_key=True)
    url = Column(UnicodeText(255), primary_key=True)
    title = Column(UnicodeText)
    h1 = Column(UnicodeText)
