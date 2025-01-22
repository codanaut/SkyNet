// Conversion constants
const KNOTS_TO_MPH = 1.15078;
const MACH_TO_MPH = 767.269; // Approximate for Mach 1 at sea level

// Input elements
const knotsInput = document.getElementById('knots');
const machInput = document.getElementById('mach');
const mphInput = document.getElementById('mph');

// Conversion functions
function knotsToOthers(knots) {
    const mph = knots * KNOTS_TO_MPH;
    const mach = mph / MACH_TO_MPH;
    return { mph, mach };
}

function machToOthers(mach) {
    const mph = mach * MACH_TO_MPH;
    const knots = mph / KNOTS_TO_MPH;
    return { mph, knots };
}

function mphToOthers(mph) {
    const knots = mph / KNOTS_TO_MPH;
    const mach = mph / MACH_TO_MPH;
    return { knots, mach };
}

// Event listeners
knotsInput.addEventListener('input', () => {
    const knots = parseFloat(knotsInput.value) || 0;
    const { mph, mach } = knotsToOthers(knots);
    mphInput.value = mph.toFixed(2);
    machInput.value = mach.toFixed(4);
});

machInput.addEventListener('input', () => {
    const mach = parseFloat(machInput.value) || 0;
    const { mph, knots } = machToOthers(mach);
    mphInput.value = mph.toFixed(2);
    knotsInput.value = knots.toFixed(2);
});

mphInput.addEventListener('input', () => {
    const mph = parseFloat(mphInput.value) || 0;
    const { knots, mach } = mphToOthers(mph);
    knotsInput.value = knots.toFixed(2);
    machInput.value = mach.toFixed(4);
});



// Celsius and Fahrenheit inputs
const celsiusInput = document.getElementById('celsius');
const fahrenheitInput = document.getElementById('fahrenheit');

// Conversion functions for temperature
function celsiusToFahrenheit(celsius) {
    return (celsius * 9/5) + 32;
}

function fahrenheitToCelsius(fahrenheit) {
    return (fahrenheit - 32) * 5/9;
}

// Event listeners for temperature inputs
celsiusInput.addEventListener('input', () => {
    const celsius = parseFloat(celsiusInput.value) || 0;
    const fahrenheit = celsiusToFahrenheit(celsius);
    fahrenheitInput.value = fahrenheit.toFixed(2);
});

fahrenheitInput.addEventListener('input', () => {
    const fahrenheit = parseFloat(fahrenheitInput.value) || 0;
    const celsius = fahrenheitToCelsius(fahrenheit);
    celsiusInput.value = celsius.toFixed(2);
});


// Pressure inputs
const inHgInput = document.getElementById('inHg');
const hPaInput = document.getElementById('hPa');

// Conversion functions for pressure
function inHgToHPa(inHg) {
    return inHg * 33.8639;
}

function hPaToInHg(hPa) {
    return hPa / 33.8639;
}

// Event listeners for pressure inputs
inHgInput.addEventListener('input', () => {
    const inHg = parseFloat(inHgInput.value) || 0;
    const hPa = inHgToHPa(inHg);
    hPaInput.value = hPa.toFixed(2);
});

hPaInput.addEventListener('input', () => {
    const hPa = parseFloat(hPaInput.value) || 0;
    const inHg = hPaToInHg(hPa);
    inHgInput.value = inHg.toFixed(2);
});
