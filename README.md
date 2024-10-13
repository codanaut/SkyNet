# SkyNet Project Overview

Welcome to SkyNet, a tool for exploring aircraft information. The site at [skynet.codanaut.com](http://skynet.codanaut.com) lets users search for aircraft details by N-number, Mode S Hex code, or registration number. We're continuously adding new features to improve the experience.

## Current Features

### Webpage
- **Aircraft Lookup**: Search for aircraft using N-number, Mode S Hex, or registration number.

### Firefox Extension
- **Tar1090 Integration**: Firefox extension (Chrome/Edge support in progress) integrates with sites running tar1090 or similar URLs ending with `/ ?icao="hex"`.
- **Temporary Installation**: Currently, add via the debugging menu, with plans for listing in official extension stores.

### Discord Bot
- **Aircraft Lookup**: A bot for Discord that can look up aircraft information.
- **Active Development**: Still under development, with full-time availability planned after a stable release.

## What's Coming Next
- **Airframe & Engine Info**: Detailed airframe and engine data.
- **Enhanced Search**: Search by owner, aircraft type, and more.
- **Code Release**: Source code will be released after cleanup and testing.

## Technical Details
SkyNet is built with **Python**, **FastAPI**, and uses **PostgreSQL** for data storage. API documentation is available at [skynet.codanaut.com/docs](http://skynet.codanaut.com/docs).

Deployment will be provided via **Docker Compose** to include everything needed for a full setup.

Check out the site and let us know what you think!