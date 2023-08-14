# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
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
        f"To use api below enter date at end of api with format yyyy-mm-dd<br/>"
        f"/api/v1.0/<start><end>"

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



@app.route("/api/v1.0/<start>")
def temps(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Calculate min temp, avg tem, and max temp for dates selected, 
    or a 404 if not."""
    """Query temps by date range"""

    start_temps = session.query(Measurement.date, Measurement.tobs).\
            filter(Measurement.date <= '2017-08-23').\
            filter(Measurement.date >= start).\
            order_by(Measurement.date).all()
   

    session.close()
    tmin = "0"
    tmax = "0"
    tavg = "0"

    # for tobs in 

    # temp_all = [start_temps["tmin": {func.min(Measurement.tobs)}, "tavg": {func.avg(Measurement.tobs)}, "tmax": {func.max(Measurement.tobs)}]]
    # print (temp_all)
    all_temps = []

    # for temps in start_temps:
    #     all_temps.append(temps)
    #     func.min = tmin[all_temps]
    #     func.avg = tavg[all_temps]
    #     func.max = tmax[all_temps]

    tmin = session.query(func.min(Measurement.tobs))

    session.close()

    # Create a dictionary from the row data and append to a list of measurements
    # all_temps = []
    # for date, tobs in start_temps:
    #     temps_dict = {}
    #     temps_dict["day"] = date
    #     temps_dict["tobs"] = tobs
    #     all_temps.append(temps_dict)
    # Create a dictionary from the specified data 
    # temperature = []
    # for tobs in start_temps:
    #     temps_dict = {}
    #     temps_dict["tmin"] = func.min(Measurement.tobs)
    #     temps_dict["tavg"] = func.avg(Measurement.tobs)
    #     temps_dict["tmax"] = func.max(Measurement.tobs)
    #     temperature.append(temps_dict)

    # print(temperature)

    # return jsonify(tmin_tavg_tmax)

    # return jsonify({'tmin': tmin})

    # return jsonify({"error": "Date not found."}), 404


if __name__ == "__main__":
    app.run(debug=True)