# Import Dependencies
import sqlalchemy
import numpy as np
import datetime as dt
from datetime import datetime, timedelta
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# sqlite setup
engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station

# start of Flask App
app = Flask(__name__)

# Home Page
# Lists all options
@app.route("/")
def home():
    return ("<h1>Seth Newbill Weather Page</h1><br>"
            f"<h2>Please copy and paste one of the options below to the end of the url above.</h2><br>"
            f"<h3>/api/v1.0/precipitation</h3><br>"
            f"<h3>/api/v1.0/stations</h3><br>"
            f"<h3>/api/v1.0/tobs</h3><br>"
            f"To retrieve the recorded minimum, average, and maximum temperatures since a specific date<br>"
            f"add a date in YYYY-MM-DD format at the end of this url and copy it to the url above.<br>"
            f"<h3>/api/v1.0/</h3><br>"
            f"To retrieve the recorded minimum, average, and maximum temperatures between two specific dates<br>"
            f"add a start and end date in YYYY-MM-/YYYY-MM-DD format at the end of this url and copy it to the url above.<br>"
            f"<h3>/api/v1.0/</h3><br>"
             )

# Precipitation page
# Query precipitation data a year from the last recorded entry
# add query results to dictionary
# display on page as json
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    datetime_obj = datetime.strptime(date[0], "%Y-%m-%d")
    yearAgo = datetime_obj - timedelta(days=365)
    precip = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > yearAgo).all()
    
    dates = {}
    for date, prcp in precip:
        dates[date] = prcp
    return jsonify(dates)


# stations page
# query the station
# return on page as json
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    stations = session.query(Station.station, Station.name).all()
    stationlist = list(np.ravel(stations))
    return jsonify(stationlist)

# tobs page
# Query tobs data a year from the last recorded entry
# display on page as json
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    datetime_obj = datetime.strptime(date[0], "%Y-%m-%d")
    yearAgo = datetime_obj - timedelta(days=365)
    tobs = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date > yearAgo).all()
    tobslist = list(np.ravel(tobs))
    return jsonify(tobslist)

# start date page
# allow user to add a date to the end of url
# return min, avg, and max temp since that date
@app.route("/api/v1.0/<start>")
def start(start):
    session = Session(engine)
    startList = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    return jsonify(startList)

# start and end date page
# allow user to add a start and end date to end of url
# return min, avg, and max temp between those dates
@app.route("/api/v1.0/<start>/<end>")
def startEnd(start, end):
    session = Session(engine)
    startEndList = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    return jsonify(startEndList)

if __name__ == "__main__":
    app.run(debug=True)