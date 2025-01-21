let map; // Declare map variable outside the function to keep its state
var randomHex = '';

document.addEventListener("DOMContentLoaded", function() {
    // Check for URL parameters on page load and fetch data if present
    handleUrlParameters();

    // Only run get_count if the 'count' element exists
    if (document.getElementById("count")) {
        get_count();
    }

    // Only run fetchAircraftInfo if the 'hexInput' element exists
    if (document.getElementById("hexInput")) {
        setupEnterKeyListener();
        //fetchRandomAircraft();
        loadRandomAircraftFromLocal();
    }

    // You can add other conditional checks here depending on the page's requirements
});

function handleUrlParameters() {
    const urlParams = new URLSearchParams(window.location.search);
    const inputCode = urlParams.get('icao') || urlParams.get('tail') || urlParams.get('reg') || urlParams.get('search');

    if (inputCode) {
        document.getElementById("hexInput").value = inputCode; // Set the input field value
        fetchAircraftInfo(); // Fetch aircraft info based on the URL parameter
    }
}

// Search for aircraft
async function fetchAircraftInfo() {
    //clear existing info
    document.getElementById("aircraftInfo").style.display = "none";
    document.getElementById("error").style.display = "none";
    // Show the loading spinner
    showLoadingSpinner();

    var inputCode = document.getElementById("hexInput").value.trim();
    if (!inputCode) {
        //inputCode = 'a34890'; // Default HEX code
        inputCode = randomHex;
    }

    let apiUrl = `/api/lookup/${inputCode}`;


    try {
        const response = await fetch(apiUrl);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
    
        const aircraftData = await response.json();
    
        // Check if aircraftData contains the expected field (like 'hex')
        if (!aircraftData.hex) {
            throw new Error('No valid aircraft data found');
        }
    
        // If the aircraftData contains valid data, proceed to display it
        displayAircraftInfo(aircraftData);
    
    } catch (error) {
        console.error('Failed to fetch aircraft data:', error);
        document.getElementById("error-ac-hex").textContent = inputCode;
        document.getElementById("error").style.display = "block";
        window.history.replaceState(null, '', '/');
    } finally {
        // Hide the loading spinner
        hideLoadingSpinner();
    }
    
}

//Random Aircraft
async function fetchRandomAircraft() {
    document.getElementById("aircraftInfo").style.display = "none";
    document.getElementById("error").style.display = "none";
    //document.getElementById("loadingSpinner").style.display = "flex";
    showLoadingSpinner();

    let apiUrl = `/api/random`;
    try {
        const response = await fetch(apiUrl);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const aircraftData = await response.json();
        //console.log(aircraftData.hex)
        document.getElementById("hexInput").value = aircraftData.hex;
        displayAircraftInfo(aircraftData);
    } catch (error) {
        console.error('Failed to fetch aircraft data:', error);
        alert(`Failed to fetch random aircraft`, error);
    }
    //document.getElementById("loadingSpinner").style.display = "none";
    hideLoadingSpinner();
}

// Display the info
function displayAircraftInfo(data) {
    window.history.replaceState(null, '', `/?icao=${data.hex}`);

    // set description
    if (data.description == null) {
        var description = data.aircraft_manufacturer + " " + data.aircraft_model
    } else {
        var description = data.description
        
    }

    // hide if no flight
    if (data.flight == null) {
        document.getElementById("flight").style.display = "none";
    }

    // hide if no category
    if (data.category == null) {
        document.getElementById("full_category").style.display = "none";
    }
    
    // FLight Details
    document.getElementById("flight").textContent = "Flight: " + data.flight;
    document.getElementById("registration").textContent = "Registration: " + data.registration;
    document.getElementById("hex").textContent = "Mode S: " + data.hex;
    document.getElementById("description").textContent = "Plane: " + description;
    //document.getElementById("year").textContent = "Year: " + data.year_mfr;
    document.getElementById("full_category").textContent = "Category: " + data.category + " - " + data.category_description;
    document.getElementById("owner").textContent = "Owner: " + data.owner;
    document.getElementById("country").textContent = "Country: " + data.country;
    
    // Aircraft Specs
    document.getElementById("aircraft_manufacturer").textContent = data.aircraft_manufacturer;
    document.getElementById("aircraft_model").textContent = data.aircraft_model;
    document.getElementById("number_seats").textContent = data.number_seats;
    document.getElementById("number_engines").textContent = data.number_engines;

    // Engine Specs
    document.getElementById("engine_manufacturer").textContent = data.engine_manufacturer;
    document.getElementById("engine_model").textContent = data.engine_model;
    document.getElementById("type_engine").textContent = data.type_engine;
    document.getElementById("type_aircraft").textContent = data.type_aircraft;
    document.getElementById("serial_number").textContent = data.serial_number;
    document.getElementById("year_mfr").textContent = data.year_mfr;

    // Registration
    document.getElementById("registered-owner").textContent = data.owner;
    document.getElementById("type_registrant").textContent = data.type_registrant;
    document.getElementById("street").textContent = data.street;
    document.getElementById("city").textContent = data.city;
    document.getElementById("county").textContent = data.county;
    document.getElementById("state").textContent = data.state;
    
    document.getElementById("alt_baro").textContent = "Barometric Altitude: " + data.alt_baro + " ft";
    document.getElementById("alt_geom").textContent = "Geometric Altitude: " + data.alt_geom + " ft";
    document.getElementById("ground_speed").textContent = "Ground Speed: " + data.ground_speed + " knots";
    document.getElementById("ias").textContent = "Indicated Airspeed: " + data.ias + " knots";
    document.getElementById("tas").textContent = "True Airspeed: " + data.tas + " knots";
    document.getElementById("mach").textContent = "Mach: " + data.mach;
    document.getElementById("wind_dir").textContent = "Wind Direction: " + data.wind_dir + "°";
    document.getElementById("wind_speed").textContent = "Wind Speed: " + data.wind_speed + " knots";
    document.getElementById("oat").textContent = "Outside Air Temperature: " + data.oat + "°C";
    document.getElementById("tat").textContent = "Total Air Temperature: " + data.tat + "°C";
    document.getElementById("track").textContent = "Track: " + data.track + "°";
    document.getElementById("track_rate").textContent = "Track Rate: " + data.track_rate + "°/min";
    document.getElementById("roll").textContent = "Roll: " + data.roll + "°";
    document.getElementById("mag_heading").textContent = "Magnetic Heading: " + data.mag_heading + "°";
    document.getElementById("true_heading").textContent = "True Heading: " + data.true_heading + "°";
    document.getElementById("baro_rate").textContent = "Barometric Rate: " + data.baro_rate + " ft/min";
    document.getElementById("geom_rate").textContent = "Geometric Rate: " + data.geom_rate + " ft/min";
    document.getElementById("squawk").textContent = "Squawk: " + data.squawk;
    document.getElementById("emergency").textContent = "Emergency: " + data.emergency;
    //document.getElementById("category").textContent = "Category: " + data.category;
    //document.getElementById("category_description").textContent = "Category Description: " + data.category_description;
    document.getElementById("nav_qnh").textContent = "QNH: " + data.nav_qnh + " hPa";
    document.getElementById("nav_altitude_mcp").textContent = "MCP Altitude: " + data.nav_altitude_mcp + " ft";
    document.getElementById("nav_heading").textContent = "Nav Heading: " + data.nav_heading + "°";
    document.getElementById("nav_modes").textContent = "Nav Modes: " + data.nav_modes;
    document.getElementById("latitude").textContent = "Latitude: " + data.latitude;
    document.getElementById("longitude").textContent = "Longitude: " + data.longitude;
    document.getElementById("nic").textContent = "NIC: " + data.nic;
    document.getElementById("rc").textContent = "RC: " + data.rc;
    //document.getElementById("seen_pos").textContent = "Seen Position: " + data.seen_pos + " s";
    document.getElementById("version").textContent = "Version: " + data.version;
    document.getElementById("nic_baro").textContent = "NIC Baro: " + data.nic_baro;
    document.getElementById("nac_p").textContent = "NAC P: " + data.nac_p;
    document.getElementById("nac_v").textContent = "NAC V: " + data.nac_v;
    document.getElementById("sil").textContent = "SIL: " + data.sil;
    document.getElementById("sil_type").textContent = "SIL Type: " + data.sil_type;
    document.getElementById("gva").textContent = "GVA: " + data.gva;
    document.getElementById("sda").textContent = "SDA: " + data.sda;
    document.getElementById("alert").textContent = "Alert: " + data.alert;
    document.getElementById("spi").textContent = "SPI: " + data.spi;
    document.getElementById("mlat").textContent = "MLAT: " + data.mlat;
    document.getElementById("tisb").textContent = "TISB: " + data.tisb;
    document.getElementById("messages").textContent = "Messages: " + data.messages;
    //document.getElementById("seen").textContent = "Seen: " + data.seen + " s";
    document.getElementById("rssi").textContent = "RSSI: " + data.rssi;
    document.getElementById("distance").textContent = "Distance: " + data.distance + " nmi";
    document.getElementById("direction").textContent = "Direction: " + data.direction + "°";
    document.getElementById("dbFlags").textContent = "DB Flags: " + data.dbFlags;
    document.getElementById("source_type").textContent = "Source Type: " + data.source_type;
    document.getElementById("current_receiver_location").textContent = "Receiver Location: " + data.current_receiver_location;
    document.getElementById("last_seen").textContent = "Last Seen: " + data.last_updated;
    
    
    if (data.source_type == null) {
        document.getElementById("adsb").style.display = "none";
        document.getElementById("last_updated").textContent = "Last Updated: " + data.last_updated;
    } else {
        // Show the element if source_type is not null
        document.getElementById("adsb").style.display = "block";  // Or whatever display value you need (e.g., "inline", "flex")
    }

    // If manufacturer data
    if (data.aircraft_manufacturer == null) {
        document.getElementById("aircraft-specs").style.display = "none";
        document.getElementById("year").style.display = "block";
        document.getElementById("year").textContent = "Year: " + data.year_mfr;
        document.getElementById("last_updated").textContent = "Last Updated: " + data.last_updated;
    } else {
        // Show the element if source_type is not null
        document.getElementById("aircraft-specs").style.display = "block";  // Or whatever display value you need (e.g., "inline", "flex")
        document.getElementById("year").style.display = "none";
    }

    if (data.type_registrant == null) {
        document.getElementById("aircraft-registration").style.display = "none";
    } else {
        // Show the element if source_type is not null
        document.getElementById("aircraft-registration").style.display = "block";  // Or whatever display value you need (e.g., "inline", "flex")
    }
    
    
    if (data.image) {
        // Hide the image and set a blank source to avoid flashing the old image
        document.getElementById("img").style.display = "none";
        document.getElementById("img").src = ""; // Clear the image source to avoid flashing
    
        // Load the new image
        document.getElementById("img").src = data.image;
        document.getElementById("img").alt = "Aircraft Image";
    
        // Once the new image is fully loaded, show the image and the aircraft info box
        document.getElementById("img").onload = function() {
            document.getElementById("img").style.display = "block";
        };
    } else {
        document.getElementById("img").src = "";
        document.getElementById("img").style.display = "none"; // Hide the image element
    }

    //route
    if (data.flight) {
        lookupRoute(data.flight)
            .then(routeData => {
                if (routeData && routeData._airports && routeData._airports.length > 0) {
                    document.getElementById("flight").style.display = "block";
                    const routeElement = document.getElementById("route");
                    routeElement.style.display = "block"; // Show the route block
    
                    // Construct the route display dynamically
                    let routeHTML = `<p>Route: ${routeData._airport_codes_iata || 'Unknown'}</p>`;
                    routeHTML += `<p>Origin: ${routeData._airports[0].name || 'Unknown'} (${routeData._airports[0].iata || 'Unknown'})</p>`;
    
                    // Add stops if there are more than two airports
                    if (routeData._airports.length > 2) {
                        for (let i = 1; i < routeData._airports.length - 1; i++) {
                            routeHTML += `<p>Layover: ${routeData._airports[i].name || 'Unknown'} (${routeData._airports[i].iata || 'Unknown'})</p>`;
                        }
                    }
    
                    // Add the destination
                    const lastAirport = routeData._airports[routeData._airports.length - 1];
                    routeHTML += `<p>Destination: ${lastAirport.name || 'Unknown'} (${lastAirport.iata || 'Unknown'})</p>`;
    
                    // Update the route element
                    routeElement.innerHTML = routeHTML;
                } else {
                    // Hide the route block if no data is found
                    document.getElementById("route").style.display = "none";
                }
            })
            .catch(error => {
                console.error("Error fetching route data:", error);
                // Hide the route block on error
                document.getElementById("route").style.display = "none";
            });
    } else {
        // Hide the route block if no flight information is available
        document.getElementById("route").style.display = "none";
    }
    
    

    //Display the data again
    document.getElementById("aircraftInfo").style.display = "block";
       
    if (data.latitude && data.longitude) {
        // Check if map is already initialized
        document.getElementById("map").style.display = "block";
        if (!map) {
            map = L.map('map').setView([data.latitude, data.longitude], 6);

            L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            }).addTo(map);
        } else {
            // If map is already initialized, just set the view to new coordinates
            map.setView([data.latitude, data.longitude], 7);
        }

        // Define a custom icon (airplane icon)
        var airplaneIcon = L.icon({
            iconUrl: '/img/plane-icon.png',  // URL to your airplane icon image
            iconSize: [32, 32],  // size of the icon
            iconAnchor: [16, 16],  // point of the icon which will correspond to marker's location
            popupAnchor: [0, -16]  // point from which the popup should open relative to the iconAnchor
        });

        // Clear previous markers
        if (map._layers) {
            for (let i in map._layers) {
                if (map._layers[i]._icon) {
                    map.removeLayer(map._layers[i]);
                }
            }
        }

        // Add a marker with the custom icon to the map
        L.marker([data.latitude, data.longitude], { icon: airplaneIcon, rotationAngle: data.track }).addTo(map)
            .bindPopup(`<b>Altitude: ${data.alt_baro} ft <br>Speed: ${data.ground_speed} knots`)
            .openPopup();
        
        // Calculate receiver's location based on aircraft's location, distance, and direction
        let receiverLocation = calculateDestination(
            data.latitude, 
            data.longitude, 
            data.distance,  // Use dynamic distance
            (data.direction + 180) % 360  // Adjusting direction for the reverse bearing
        );

        // Define a custom icon for the receiver (radio icon)
        var radioIcon = L.icon({
            iconUrl: '/img/broadcast-tower-solid.png',  // URL to your radio icon image
            iconSize: [32, 32],  // size of the icon
            iconAnchor: [16, 16],  // point of the icon which will correspond to marker's location
            popupAnchor: [0, -16]  // point from which the popup should open relative to the iconAnchor
        });

        // Add a marker for the receiver location
        L.marker([receiverLocation.latitude, receiverLocation.longitude], { icon: radioIcon }).addTo(map)
        .bindPopup(`<b>Receiver Location</b>`);
    }else {
        // Hide the map if latitude or longitude data are missing
        document.getElementById('map').style.display = 'none';
        //Display the data again
        document.getElementById("aircraftInfo").style.display = "block";
    }
    

        
}// main close

// Fetch data from the '/count' endpoint
async function get_count(){
    document.getElementById("loadingSpinner-little").style.display = "inline-flex";
    fetch('/api/count')
    .then(response => {
        // Check if the request was successful
        if (!response.ok) {
        throw new Error('Network response was not ok');
        }
        return response.json(); // Parse JSON response
    })
    .then(data => {
        // Get the count from the response data
        const count = data.count.toLocaleString();
        // Update the DOM element with the ID 'count' to display the count
        document.getElementById("loadingSpinner-little").style.display = "none";
        document.getElementById("count").textContent = count + " Aircraft Logged";
    })
    .catch(error => {
        // Handle any errors that occur during the fetch operation
        console.error('There was a problem with the fetch operation:', error);
        document.getElementById("count").textContent = "Error loading count";
    });
}



// Function to handle 'Enter' key press on the input field
function setupEnterKeyListener() {
    var input = document.getElementById("hexInput");

    if (input) {
        input.addEventListener("keypress", function(event) {
            if (event.key === "Enter") {
                event.preventDefault();
                document.getElementById("inputBTN").click();
            }
        });
    }
}


async function loadRandomAircraftFromLocal() {
    let jsonUrl = 'aircraft.json'; // Replace with the correct path to your local JSON file
    try {
        const response = await fetch(jsonUrl);
        if (!response.ok) {
            throw new Error('Failed to load local hexes file');
        }
        const data = await response.json();
        const hexArray = data.hexes;
        randomHex = hexArray[Math.floor(Math.random() * hexArray.length)];
        document.getElementById("hexInput").placeholder = randomHex;
    } catch (error) {
        console.error('Failed to load local hexes:', error);
        alert('Failed to load random aircraft from local list');
    }
}

function calculateDestination(lat, lon, distance, bearing) {
    const R = 6371; // Radius of the Earth in kilometers
    const bearingRad = bearing * Math.PI / 180; // Convert bearing to radians

    // Convert distance from nautical miles to kilometers
    const distanceKm = distance * 1.852; // 1 nmi = 1.852 km
    const distanceRatio = distanceKm / R; // Convert distance to radians

    const latRad = lat * Math.PI / 180;
    const lonRad = lon * Math.PI / 180;

    const newLat = Math.asin(Math.sin(latRad) * Math.cos(distanceRatio) +
        Math.cos(latRad) * Math.sin(distanceRatio) * Math.cos(bearingRad));

    const newLon = lonRad + Math.atan2(Math.sin(bearingRad) * Math.sin(distanceRatio) * Math.cos(latRad),
        Math.cos(distanceRatio) - Math.sin(latRad) * Math.sin(newLat));

    return {
        latitude: newLat * 180 / Math.PI,
        longitude: newLon * 180 / Math.PI
    };
}

// Spinner Stuff


// Function to select a random message
function getRandomLoadingMessage() {
    return fetch('loadingmessages.json')
        .then(response => response.json())
        .then(data => {
            const loadingMessages = data.loadingMessages;
            const randomIndex = Math.floor(Math.random() * loadingMessages.length);
            return loadingMessages[randomIndex];
        })
        .catch(() => "Loading... Please Wait"); // Fallback message if there's an error
}


// Update the loading message in the HTML
function showLoadingSpinner() {
    const loadingSpinner = document.getElementById("loadingSpinner");
    const spinnerMessageElement = document.getElementById("spinnermessage");
    getRandomLoadingMessage().then(message => {
        spinnerMessageElement.innerHTML = `${message}`;
    });
    document.getElementById("details").style.display = "block";
    loadingSpinner.classList.remove("hidden");
    document.getElementById("spinner").style.display = "flex";
    spinnerMessageElement.style.display = "block";
}

// Hide the loading spinner (when appropriate)
function hideLoadingSpinner() {
    const loadingSpinner = document.getElementById("loadingSpinner");
    document.getElementById("spinner").style.display = "none";
    document.getElementById("spinnermessage").style.display = "none";
    
}

async function lookupRoute(callsign) {
    if (!callsign || typeof callsign !== "string") {
        console.error("Invalid callsign provided.");
        return null;
    }

    // Extract the first two characters of the callsign
    const prefix = callsign.substring(0, 2);

    // Construct the URL
    const url = `https://vrs-standing-data.adsb.lol/routes/${prefix}/${callsign}.json`;

    try {
        // Fetch the data from the URL
        const response = await fetch(url);

        // Check if the response is ok (status 200)
        if (response.ok) {
            const data = await response.json();
            console.log(data);
            return data;
        } else if (response.status === 404) {
            // Return null if the resource is not found
            console.warn(`Route not found for callsign: ${callsign}`);
            return null;
        } else {
            console.error(`Failed to fetch route: ${response.status}`);
            return null;
        }
    } catch (error) {
        console.error(`Error fetching route for callsign ${callsign}:`, error);
        return null;
    }
}
