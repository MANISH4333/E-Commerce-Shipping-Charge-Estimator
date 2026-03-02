/**
 * JumboTails — Frontend Application Logic
 *
 * Handles API calls to the FastAPI backend for:
 * 1. Finding the nearest warehouse (GET /api/v1/warehouse/nearest)
 * 2. Calculating shipping charge (GET /api/v1/shipping-charge)
 * 3. Combined calculator (POST /api/v1/shipping-charge/calculate)
 *
 * All API calls include error handling with user-friendly messages.
 */

// ═══════════════════════════════════════════════════════════════
//  CONFIGURATION
// ═══════════════════════════════════════════════════════════════

const API_BASE = '';  // Same origin — served by FastAPI

// ═══════════════════════════════════════════════════════════════
//  UTILITY FUNCTIONS
// ═══════════════════════════════════════════════════════════════

/**
 * Show a DOM element by removing the 'hidden' class.
 * @param {HTMLElement} el
 */
function show(el) {
    el.classList.remove('hidden');
}

/**
 * Hide a DOM element by adding the 'hidden' class.
 * @param {HTMLElement} el
 */
function hide(el) {
    el.classList.add('hidden');
}

/**
 * Format a number as Indian Rupees.
 * @param {number} amount
 * @returns {string} Formatted currency string
 */
function formatRupees(amount) {
    return `₹ ${amount.toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
}

/**
 * Display an error message in the given error panel.
 * @param {HTMLElement} errorEl - The error panel element
 * @param {string} message - Error message to display
 */
function showError(errorEl, message) {
    errorEl.textContent = message;
    show(errorEl);
}

/**
 * Generic fetch wrapper with error handling.
 * @param {string} url - API endpoint URL
 * @param {object} options - Fetch options
 * @returns {Promise<object>} Parsed JSON response
 * @throws {Error} With user-friendly message
 */
async function apiFetch(url, options = {}) {
    const response = await fetch(url, {
        headers: { 'Content-Type': 'application/json' },
        ...options,
    });

    const data = await response.json();

    if (!response.ok) {
        // FastAPI returns { detail: "..." } for HTTP errors
        const message = data.detail || `Request failed with status ${response.status}`;
        throw new Error(message);
    }

    return data;
}

// ═══════════════════════════════════════════════════════════════
//  1. COMBINED CALCULATOR
// ═══════════════════════════════════════════════════════════════

const combinedForm = document.getElementById('combinedForm');
const combinedResult = document.getElementById('combinedResult');
const combinedError = document.getElementById('combinedError');
const combinedLoader = document.getElementById('combinedLoader');
const combinedBtn = document.getElementById('combinedBtn');
const combinedCharge = document.getElementById('combinedCharge');
const combinedWhId = document.getElementById('combinedWarehouseId');
const combinedWhLoc = document.getElementById('combinedWarehouseLoc');

combinedForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    hide(combinedResult);
    hide(combinedError);
    show(combinedLoader);
    combinedBtn.disabled = true;

    try {
        const sellerId = document.getElementById('combined-seller').value;
        const productId = document.getElementById('combined-product').value;
        const customerId = document.getElementById('combined-customer').value;
        const deliverySpeed = document.getElementById('combined-speed').value;

        // Validate all fields are selected
        if (!sellerId || !productId || !customerId) {
            throw new Error('Please select all fields before calculating.');
        }

        const data = await apiFetch(`${API_BASE}/api/v1/shipping-charge/calculate`, {
            method: 'POST',
            body: JSON.stringify({
                sellerId: parseInt(sellerId),
                productId: parseInt(productId),
                customerId: parseInt(customerId),
                deliverySpeed: deliverySpeed,
            }),
        });

        // Populate results
        combinedCharge.textContent = formatRupees(data.shippingCharge);
        combinedWhId.textContent = `Warehouse #${data.nearestWarehouse.warehouseId}`;

        const loc = data.nearestWarehouse.warehouseLocation;
        combinedWhLoc.textContent = `Lat: ${loc.lat}  ·  Long: ${loc.long}`;

        show(combinedResult);
    } catch (err) {
        showError(combinedError, err.message);
    } finally {
        hide(combinedLoader);
        combinedBtn.disabled = false;
    }
});

// ═══════════════════════════════════════════════════════════════
//  2. NEAREST WAREHOUSE
// ═══════════════════════════════════════════════════════════════

const warehouseForm = document.getElementById('warehouseForm');
const warehouseResult = document.getElementById('warehouseResult');
const warehouseError = document.getElementById('warehouseError');
const warehouseLoader = document.getElementById('warehouseLoader');
const warehouseBtn = document.getElementById('warehouseBtn');

warehouseForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    hide(warehouseResult);
    hide(warehouseError);
    show(warehouseLoader);
    warehouseBtn.disabled = true;

    try {
        const sellerId = document.getElementById('wh-seller').value;
        const productId = document.getElementById('wh-product').value;

        if (!sellerId || !productId) {
            throw new Error('Please select both seller and product.');
        }

        const params = new URLSearchParams({ sellerId, productId });
        const data = await apiFetch(`${API_BASE}/api/v1/warehouse/nearest?${params}`);

        // Populate results
        document.getElementById('whResultId').textContent = `#${data.warehouseId}`;
        document.getElementById('whResultLat').textContent = `Lat: ${data.warehouseLocation.lat}`;
        document.getElementById('whResultLng').textContent = `Long: ${data.warehouseLocation.long}`;

        show(warehouseResult);
    } catch (err) {
        showError(warehouseError, err.message);
    } finally {
        hide(warehouseLoader);
        warehouseBtn.disabled = false;
    }
});

// ═══════════════════════════════════════════════════════════════
//  3. SHIPPING CHARGE
// ═══════════════════════════════════════════════════════════════

const shippingForm = document.getElementById('shippingForm');
const shippingResult = document.getElementById('shippingResult');
const shippingError = document.getElementById('shippingError');
const shippingLoader = document.getElementById('shippingLoader');
const shippingBtn = document.getElementById('shippingBtn');

shippingForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    hide(shippingResult);
    hide(shippingError);
    show(shippingLoader);
    shippingBtn.disabled = true;

    try {
        const warehouseId = document.getElementById('sh-warehouse').value;
        const customerId = document.getElementById('sh-customer').value;
        const productId = document.getElementById('sh-product').value;
        const deliverySpeed = document.getElementById('sh-speed').value;

        if (!warehouseId || !customerId || !productId) {
            throw new Error('Please select warehouse, customer, and product.');
        }

        const params = new URLSearchParams({ warehouseId, customerId, productId, deliverySpeed });
        const data = await apiFetch(`${API_BASE}/api/v1/shipping-charge?${params}`);

        // Populate result
        document.getElementById('shippingCharge').textContent = formatRupees(data.shippingCharge);

        show(shippingResult);
    } catch (err) {
        showError(shippingError, err.message);
    } finally {
        hide(shippingLoader);
        shippingBtn.disabled = false;
    }
});

// ═══════════════════════════════════════════════════════════════
//  SMOOTH NAV SCROLL
// ═══════════════════════════════════════════════════════════════

document.querySelectorAll('.nav-link').forEach((link) => {
    link.addEventListener('click', function (e) {
        // Update active state
        document.querySelectorAll('.nav-link').forEach((l) => l.classList.remove('active'));
        this.classList.add('active');
    });
});

// ═══════════════════════════════════════════════════════════════
//  HEALTH CHECK ON LOAD
// ═══════════════════════════════════════════════════════════════

(async function healthCheck() {
    try {
        await apiFetch(`${API_BASE}/api/health`);
        console.log('✅ API is online');
    } catch {
        console.warn('⚠️  API health check failed — backend may not be running');
    }
})();
