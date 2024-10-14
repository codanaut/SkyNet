document.getElementById("parse-url").addEventListener("click", function () {
  // Get the current tab URL
  chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
    const url = new URL(tabs[0].url);
    const params = new URLSearchParams(url.search);
    let icao = params.get("icao");

    // If ICAO code is not found in the query params, try extracting from the path
    if (!icao && url.hostname.includes("flightaware.com")) {
      const pathSegments = url.pathname.split("/");
      const flightIndex = pathSegments.indexOf("flight");
      if (flightIndex !== -1 && flightIndex + 1 < pathSegments.length) {
        icao = pathSegments[flightIndex + 1];
      }
    }

    if (icao) {
      const newUrl = `https://skynet.codanaut.com/?icao=${icao}`;
      chrome.tabs.create({ url: newUrl });
    } else {
      alert("No ICAO code or flight identifier found in the current URL.");
    }
  });
});

document.getElementById("open-url").addEventListener("click", function () {
  const icao = document.getElementById("icao-input").value;
  if (icao) {
    const newUrl = `https://skynet.codanaut.com/?icao=${icao}`;
    chrome.tabs.create({ url: newUrl });
  } else {
    alert("Please enter an ICAO code.");
  }
});

function applyTheme(theme) {
  if (theme === 'dark') {
    // Apply dark theme styles dynamically
    document.body.style.backgroundColor = '#363434';
    document.body.style.color = 'white';
    // Update any other elements if necessary
  } else {
    // Apply light theme styles dynamically
    document.body.style.backgroundColor = 'white';
    document.body.style.color = 'black';
  }
}

function setThemeBasedOnPreference() {
  if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
    applyTheme('dark');
  } else {
    applyTheme('light');
  }
}

// Listen for changes in system color scheme preference
window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', setThemeBasedOnPreference);

// Apply the theme initially when the page loads
setThemeBasedOnPreference();