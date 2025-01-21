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
