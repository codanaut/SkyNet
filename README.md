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
- **Mobile App**: A mobile version of SkyNet is in early planning to allow easy lookups and alerts directly from your phone.
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

### Running the SkyNetDB Database

The main SkyNet web app relies on the SkyNet database. To set up the SkyNet database, follow the steps below: (Coming soon)

### Running the SkyNetDB Web App

Note: For running on the Raspberry Pi 5, there is an ARM64 version available using the same image but with the `:pi` tag.

It can easily be run using the following Docker Compose file:

```yaml
docker-compose.yml
version: '3.8'

services:
  skynet:
    image: registry.gitlab.com/codanaut/skynetdb/skynet
    container_name: skynet
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

Replace `your_db_password` with the appropriate database password. This setup will create a container named `skynet`, exposing port `5002` on your local machine. Ensure that the database is accessible with the correct credentials to allow the SkyNet web app to connect.

