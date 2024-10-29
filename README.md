# SkyNetDB

Welcome to SkyNetDB, a tool for exploring aircraft information. The site at [skynetdb.com](http://skynetdb.com) lets users search for aircraft details by N-number, Mode S Hex code, or registration number. We're continuously adding new features to improve the experience.

## Current Features

### Webpage

- **Aircraft Lookup**: Search for aircraft using N-number, Mode S Hex, or registration number.
- **Mobile Friendly and PWA Support**: The webpage is optimized for mobile devices and functions as a Progressive Web App (PWA) for easy access on all devices.

### Firefox Extension

- **Tar1090 Integration**: The Firefox extension (Chrome/Edge/Brave support in progress) integrates with sites running tar1090 or similar URLs ending with `/?icao="hex"`. It allows you to open the currently selected aircraft from a flight tracker directly in SkyNet, automatically displaying the relevant data.
- **Search Feature**: The extension also has a search function, letting you search by tail number, hex code, or registration directly from the extension. It will open a new tab with the data for that aircraft.
- **Temporary Installation**: Currently, you can add the extension via the debugging menu, with plans for listing in official extension stores.

### Discord Bot

- **Aircraft Lookup**: A bot for Discord that can look up aircraft information.
- **Active Development**: Still under development, with full-time availability planned after a stable release.

### API Integration

- **REST API**: SkyNetDB provides a public API that can be used to retrieve aircraft information programmatically. The API allows lookup by N-number, hex code, and other identifiers. Documentation is available at [skynetdb.com/docs](http://skynetdb.com/docs).
- **Rate Limiting**: API access is rate-limited to ensure fair usage and reliability for all users. Please refer to the documentation for specific rate limits and access guidelines.

### ChatGPT - SkyNet GPT

- **Custom Aircraft Lookup**: A custom GPT model designed specifically for looking up aircraft information and expanding on that information, providing deeper insights and answering detailed questions about aircraft data. [Access SkyNet GPT here](https://chatgpt.com/g/g-Yl0731HVv-skynet)

## What's Coming Next

- **Airframe & Engine Info**: Detailed airframe and engine data.
- **Enhanced Search**: Search by owner, aircraft type, and more.
- **Flight History**: Add flight history data for each aircraft, including recent routes and activity.
- **Discord Alerts**: Alerts via Discord for specific aircraft events, such as takeoff, landing, or specific hex codes.
- **Code Release**: Source code will be released after cleanup and testing.

## Technical Details

### SkyNet Database

SkyNetDB is built with **Python**, **FastAPI**, and uses **PostgreSQL** for data storage. API documentation is available at [skynetdb.com/docs](http://skynetdb.com/docs).

Deployment will be provided via **Docker Compose** to include everything needed for a full setup.

### Running the Firefox Extension

To install and run the Firefox extension temporarily:

1. Open Firefox and go to `about:debugging#/runtime/this-firefox`.
2. Select **Load Temporary Add-on**.
3. Navigate to the extensions folder and select the `manifest.json` file.

This will load the extension temporarily, and it will remain active until you restart Firefox. Permanent installation options will be available once the extension is listed in the official extension stores.

---

## Self Hosting SkyNetDB

Note: For Raspberry Pi 5 users, ARM64 version is available with the ":pi" tag.

### Running the SkyNetDB Database

The SkyNetDB database can be set up using the following steps:

1. **Start the PostgreSQL Database**: Use Docker Compose to start the PostgreSQL service with the following configuration:

   ```yaml
   docker-compose.yml
   version: '3.8'
   services:
     postgres:
       image: postgres:16.2
       container_name: skynet-db
       restart: always
       environment:
         POSTGRES_USER: skynet
         POSTGRES_PASSWORD: your_db_password
         PGDATA: /var/lib/postgresql/data/pgdata
       volumes:
         - your_mount_point:/var/lib/postgresql/data
       ports:
         - "0.0.0.0:5432:5432"
       healthcheck:
         test: ["CMD", "pg_isready", "-U", "skynet"]
         interval: 10s
         timeout: 5s
         retries: 5
   ```

   Replace `your_db_password` with your desired database password. This configuration will create a container named `skynet-db` that exposes port `5432` on your local machine.

2. **Create a `.env` File**: Before running the script to set up the database schema, create a `.env` file in the project directory with the following contents:

   ```
   user=skynet
   password=your_db_password
   host=host.docker.internal or the postgres server IP
   database_name=skynet
   ```

   This `.env` file is required for running the database setup script and should match the credentials used in the Docker Compose configuration.

3. **Run the Database Setup Script**: After the PostgreSQL container is up and running, execute the script [create_skynet_db.py](./database/create_skynet_db.py) to create the required tables:

   ```
   python create_skynet_db.py
   ```

   This script will use the credentials from the `.env` file to connect to the database and set up the necessary tables and schema for SkyNetDB.

---

### Populating the SkyNetDB Database

SkyNetDB can be enriched with a variety of data sources available in the [data_sources](./data_sources/) directory.

#### FAA Data

Begin by incorporating public data from the FAA using the instructions and scripts in the [faa_data](./data_sources/faa_data/readme.md).

#### Public APIs

You can further populate SkyNetDB with data from public APIs offered by flight tracking services such as [adsb.fi](https://adsb.fi/) and [airplanes.live](https://airplanes.live/). These services provide extensive information on tracked flights.

Refer to [Public_API's](./data_sources/public_apis/readme.md) for details on running `aircraft_api_logger.py` to log active flights.

#### ADS-B Receiver Data

If you have your own ADS-B receiver, you can use it to log flights directly into SkyNetDB. The relevant scripts and Docker setup for this will be available soon.



---

### Running the SkyNetDB Web App

The web app can be run using the following Docker Compose configuration:

```yaml
docker-compose.yml
version: '3.8'
services:
  skynet:
    image: registry.gitlab.com/codanaut/skynetdb/skynet
    container_name: skynet_webapp
    restart: always
    ports:
      - "5002:2222"
    healthcheck:
      test: ["CMD", "curl", "--fail", "http://localhost:2222/api"]
      interval: 30s
      timeout: 10s
      retries: 3
    environment:
      user: skynet
      password: your_db_password
      host: your_postgres_address
      database_name: skynet
```

Replace `your_db_password` with the appropriate database password. This configuration will create a container named `skynet_webapp`, exposing port `5002` on your local machine. Ensure that the database credentials are correct for the SkyNet web app to connect successfully.

---

We hope this README helps you get started with SkyNetDB! Feel free to contribute or report any issues you encounter. If you have any questions, please join our [Discord](https://discord.gg/VeURJbwtEk).

