# SkyNet Data Sources - Public API's

One option to get aircraft data is to load it from some of the public api's available for aircraft tracking. While this project isn't focused on realtime aircraft tracking, we can still get semi-recent location data to provide with the rest of the aircraft data. 


## Setup

Create a .env file and fill in the matching data

```env
user=skynet
password=your-db-password
host=localhost or postgres ip
database_name=skynet
api=adsbfi or airplaneslive
```

Run `aircraft_api_logger.py` with the .env in the same folder.
```
python aircraft_api_logger.py
```

This will create the DB if it does not exist, and then start uploading data from each location in the `locations` database. By default it seeds five locations to get things started. 

NOTE: while this will create the DB for SkyNet it's suggested that you run `create_skynet_db.py` from [Running the SkyNetDB Database](../../README.md#running-the-skynetdb-database) first. 



Optional: Run `seed-locations.py` to add a number of popular airports from around the world. 