# Import the dependencies.
import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup.0/
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
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
        f"Date range options 2010-01-01 to 2017-08-23<br/>"
        f"To use api below enter date at end of api with format /yyyymmdd<br/>"
        f"/api/v1.0/startonly/<start><br/>"
        f"To specify both start and end dates, enter with format /YYYYmmddYYYYmmdd<br/>"
        f"/api/v1.0/<startday><end>"

    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return 12-months of precipitation as json"""

    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Query results from 12-month precipitation analysis"""
    # Query 12 months
    results = session.query(Measurement.date, Measurement.prcp).\
            filter(Measurement.date <= '2017-08-23').\
            filter(Measurement.date > '2016-08-23').\
            order_by(Measurement.date).all()
    
    session.close()

    # Create a dictionary from the row data and append to a list of measurements
    all_precip = []
    for date, prcp in results:
        precip_dict = {}
        precip_dict["date"] = date
        precip_dict["prcp"] = prcp
        all_precip.append(precip_dict)

    ### above creates a list of dictionaries

    return jsonify(all_precip)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a JSON list of stations from dataset"""
    # Query all stations
    results = session.query(Station.station).all()

    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)



@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return dates and temps of most-active station previous year"""
    # Query most active station
    results = session.query(Measurement.date, Measurement.tobs).\
            filter(Measurement.date <= '2017-08-23').\
            filter(Measurement.date > '2016-08-23').\
            filter(Measurement.station == 'USC00519281').all()

    session.close()

    # Convert list of tuples into normal list
    dates_temps = list(np.ravel(results))

    return jsonify(dates_temps)



@app.route("/api/v1.0/startonly/<start>")
def temps(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Calculate min temp, avg tem, and max temp for start date selected""" 
    """Query temps by date range"""

    sel = [func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)]

    start = dt.datetime.strptime(start, "%Y%m%d")

    start_temps = session.query(*sel).filter(Measurement.date >= start).filter(Measurement.date <= 20170823).all()
   
    session.close()

    all_temps = list(np.ravel(start_temps))

    return jsonify(all_temps)


@app.route("/api/v1.0/<startday><end>")
def tempsstartend(startday):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Calculate min temp, avg tem, and max temp for start and end dates selected""" 
    """Query temps by date range"""

    sel = [func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)]

    startday = dt.datetime.strptime(startday, "%Y%m%d")
    end = dt.datetime.strptime(end, "%Y%m%d")

    startend_temps = session.query(*sel).filter(Measurement.date >= startday).filter(Measurement.date <= end).all()
   
    session.close()

    alltemps = list(np.ravel(startend_temps))

    return jsonify(alltemps)


if __name__ == "__main__":
    app.run(debug=True)