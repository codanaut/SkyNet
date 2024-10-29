# SkyNetDB - FAA Data

FAA\_Data is a tool that fetches the latest FAA data dump, converts it to an SQLite3 database for processing, and uploads it to the main SkyNet database. It can also update existing data records efficiently.

## How to run
Running the script `master-update.py` will download the newest data to an SQLite database, where it will then be processed and uploaded to the SkyNet PostgreSQL database. To run this script, use the same `.env` file you created earlier and then execute the following command:

```
python master-update.py
```


## master-updater.py

This script is the main component for fetching and downloading the latest FAA data, as well as updating the database accordingly.

## Additional Scripts

### download_faa_data_to_sqlite_db

This script downloads the FAA data and imports it into an SQLite database.

### sqlite-postgres.py

This script processes the aircraft data from the SQLite3 database and uploads it to the PostgreSQL database.

## Support Files

### country-codes.json

Contains mappings of US FIPS codes to their respective counties.

### state_abbr_to_incits_code.json

Maps state abbreviations to INCITS codes.

### state_abbr_to_name.json

Maps state abbreviations to full state names.

