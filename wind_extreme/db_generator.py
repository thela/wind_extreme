from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float

from sqlalchemy.orm import relationship, declarative_base

from logger import getgglogger

Base = declarative_base()

logger = getgglogger(__name__)


class FileData(Base):
    __tablename__ = 'file_data'

    id = Column(Integer, primary_key=True)
    filename = Column(String(length=30))
    hash_digest = Column(String(length=64), unique=True)

    windextreme_table = relationship("WindExtreme", back_populates="related_file")

    def __repr__(self):
        return f"FileData(id={self.id!r}, filename={self.filename!r}, hash_digest={self.hash_digest!r})"


class MetaData(Base):
    __tablename__ = 'data_metadata'

    id = Column(Integer, primary_key=True)

    instrument_model = Column(String(length=30))
    serial = Column(String(length=30))
    location = Column(String(length=30))
    firmware_rev = Column(String(length=30))
    software_rev = Column(String(length=30))

    windextreme_table = relationship("WindExtreme", back_populates="metadata_related")

    def __repr__(self):
        model_fields = ['id', 'instrument_model', 'serial', 'location', 'firmware_rev', 'software_rev']
        return f"MetaData(id={self.id!r}" + \
            ', '.join([f'{item}={getattr(self, item)!r}' for item in model_fields]) +\
        ")"


class WindExtreme(Base):
    __tablename__ = 'windextreme'

    id = Column(Integer, primary_key=True)
    datetime = Column(DateTime, nullable=False)
    file_data = Column(Integer, ForeignKey('file_data.id'))
    data_metadata = Column(Integer, ForeignKey('data_metadata.id'))

    speed = Column(Float)
    direction = Column(Integer)
    state = Column(Integer)

    related_file = relationship("FileData", back_populates="windextreme_table")
    metadata_related = relationship("MetaData", back_populates="windextreme_table")

    def as_dict(self):
        columns = ['speed', 'direction', 'state']
        return {c: getattr(self, c) for c in columns}

    def __repr__(self):
        return f"EDM264_L(id={self.id!r}, datetime={self.datetime!r})"
