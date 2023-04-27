# Import the dependencies.

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
from flask import Flask, jsonify
import datetime as dt
import numpy as np

#################################################
# Database Setup
#################################################


# reflect an existing database into a new model
# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precip():
    return 'hello'

@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.id, Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()
    all_stations = []
    for id, station, name, latitude, longitude, elevation in results:
        station_dict = {}
        station_dict['id'] = id
        station_dict['station'] = station
        station_dict['name'] = name
        station_dict['latitude'] = latitude
        station_dict['longitude'] = longitude
        station_dict['elevation'] = elevation
        all_stations.append(station_dict)
    
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def temps():
    one_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    activity = session.query(Measurement.station, func.count(Measurement.station)).\
    group_by(Measurement.station).\
    order_by(func.count(Measurement.station).desc())

    most_active = activity.first()[0]

    temp_data = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.station == most_active).\
    filter(Measurement.date >= one_year).all()

    all_temps = []
    for date, tobs in temp_data:
        temp_dict = {}
        temp_dict['date'] = date
        temp_dict['temp'] = tobs
        all_temps.append(temp_dict)
    # list(np.ravel(temp_data))
    
    return jsonify(all_temps)

@app.route("/api/v1.0/<start>")
def temp_range_start():
    return 'hello'

@app.route("/api/v1.0/<start>/<end>")
def temp_range_start_end():
    return 'hello'


if __name__ == '__main__':
    app.run(debug=True)