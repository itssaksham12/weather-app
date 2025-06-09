from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

Base = declarative_base()

class WeatherRecord(Base):
    __tablename__ = 'weather_records'

    id = Column(Integer, primary_key=True)
    city = Column(String)
    temperature = Column(String)
    description = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

# Database setup
engine = create_engine('sqlite:///weather.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()