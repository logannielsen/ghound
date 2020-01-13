import sqlalchemy


from sqlalchemy import create_engine, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship 
from sqlalchemy import Column, Integer, String, DateTime

engine = create_engine('sqlite:///:here:', echo=True)
Base = declarative_base()
Session = sessionmaker()
Session.configure(bind=engine)
sess = Session()

race_greyhound_association_table = Table('race_greyhound_association', Base.metadata,
    Column('greyhound', Integer, ForeignKey('greyhound.id')),
    Column('race', Integer, ForeignKey('race.id'))
)

class GreyhoundTable(Base):
    #future features
    #trainer = Column(String)
    # status = Column(String)
    # owner = Column(String)
    # sex = Column(String)
    # colour = Column(String)
    # whelped = Column(DateTime)
    # state = Column(String)
    # sire = Column(String)
    # dam = Column(String)
    # breeder = Column(String)
    # litter = Column(String)
    # dna_reg = Column(String)
    # stud_sire = Column(String)
    # vic_greys = Column(String)
    __tablename__ = 'greyhound'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    races = relationship("RaceTable", secondary=race_greyhound_association_table,
                                back_populates="greyhounds")
    race_stats = relationship("RaceStatsTable")

    def __repr__(self):
        return "<Greyhound(name='%s')>" % (
                            self.name)


class TrackTable(Base):
    __tablename__ = 'track'

    id = Column(Integer, primary_key=True)
    track_name = Column(String, ForeignKey('racehound_stats.track'), nullable=False)
    race = relationship("RaceTable", uselist=False, back_populates="track")

    def __repr__(self):
        return "<Greyhound(track_name='%s')>" % (
                            self.track_name)


class RaceTable(Base):
    __tablename__ = 'race'

    id = Column(Integer, primary_key=True, autoincrement=True)
    track_id = Column(Integer, ForeignKey('track.id'), nullable = False)
    date = Column(DateTime, ForeignKey('racehound_stats.date'), nullable=False)
    race_number = Column(Integer, ForeignKey('racehound_stats.race_number'), nullable = False)
    greyhounds = relationship("GreyhoundTable", secondary=race_greyhound_association_table,
                                back_populates="races")
    track = relationship("TrackTable", back_populates="race")


class RaceStatsTable(Base):
    __tablename__ = 'racehound_stats'

    id = Column(Integer, primary_key=True)
    greyhound_id = Column(Integer, ForeignKey('greyhound.id'))
    race_number = Column(Integer)
    date = Column(DateTime)
    track = Column(String)
    distance = Column(Integer)
    weight = Column(Integer)
    time = Column(Integer)
    bon = Column(Integer)
    margin = Column(Integer)
    split_1 = Column(Integer)
    pir = Column(Integer)
    Comment = Column(String)
    grade = Column(String)
    sp = Column(Integer)
    hcap = Column(Integer)

