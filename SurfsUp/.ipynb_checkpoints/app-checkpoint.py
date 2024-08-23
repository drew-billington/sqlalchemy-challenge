# Import the dependencies.
import datetime as dt
import numpy as np

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################

# reflect an existing database into a new model
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine)

# reflect the tables
# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session (engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    return(
        f"Welcome to the Hawaii Climate Analysis API<br/>",
        f"Available Routes:<br/>",
        f"/api/v1.0/precipitation<br/>",
        f"/api/v1.0/stations<br/>",
        f"/api/v1.0/tobs<br/>",
        f"/api/v1.0/temp/start<br/>",
        f"/api/v1.0/temp/end<br/>",
        f"<p>'start' and 'end' date should be in the format MMDDYYYY.</p>",
    )
@app.route("/api/v1.0/precipitation")
def precipitation ():
    prev_year = dt.date(2017,8,23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).all()
    
    session.close()

    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)

if __name__ == "main":
    app.run(debug=True)