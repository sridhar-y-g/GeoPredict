# GeoPredict: Landslide Disaster Prevention Network
## Technical Architecture & Operations Manual

This document outlines the current state of the GeoPredict platform, explicitly detailing **what** technologies are used, **why** they were chosen, **how** they are implemented, and exactly **how the system operates** end-to-end.

---

## 1. What is Currently Used (The Tech Stack)

### Frontend (Command Center Interface)
*   **React.js (via Vite):** The core framework driving the user interface.
*   **TailwindCSS & Custom CSS:** Used for all styling. Tailwind provides rapid utility classes, while `index.css` handles the advanced "Glassmorphism" properties (translucent blurring) and complex `@keyframes` animations (pulsing radars, glowing elements).
*   **React-Leaflet (`leaflet`):** An advanced Geographic Information System (GIS) mapping library.
*   **Lucide-React:** Provides pristine, highly-legible SVG icons used throughout the dashboard.
*   **Framer Motion:** Used on the Landing page and specific Modals for physics-based spring animations.

### Backend (Telemetry Processing Engine)
*   **Python & FastAPI:** The core backend routing framework, chosen for its extreme speed and built-in Data Validation (Pydantic).
*   **Uvicorn:** The lightning-fast ASGI server that runs the Python application.
*   **Requests:** Handles server-to-server outbound calls to retrieve weather data.
*   **OpenWeatherMap API:** The live environmental data provider.
*   **OpenStreetMap (Nominatim) API:** The geocoding system used when a user inputs a text city instead of GPS coordinates.

---

## 2. Why is it Used?

*   **FastAPI over Django/Flask:** In early warning systems, millisecond-level responsiveness is critical. FastAPI is significantly faster than standard Python frameworks and auto-documents itself via Swagger, letting us seamlessly pass GPS coordinates back and forth.
*   **React-Leaflet over Google Maps:** Google Maps requires a paid API key and credit card. Leaflet is 100% open-source, allowing us to build the "Basemap Gallery" using free, military-grade tilesets (from CartoDB and OpenTopoMap) with absolutely zero recurring costs.
*   **Glassmorphism UI (Cyber Aesthetic):** Landslide data can be visually overwhelming. By using heavy background blur, deep dark slate colors, and bright neon accents, the platform mimics high-end government aerospace software (like the GSI Bhusanket). This makes critical alerts (Red/Crimson) instantly visible to the operator.
*   **Live Sensor Data vs Simulated Data:** The initial prototype used fake random numbers. By switching to the OpenWeatherMap API, the platform now relies on actual meteorological ground-truth. If it is raining directly over Wayanad in the real world right now, the dashboard dial will immediately spike.

---

## 3. How is it Used (Architecture Layout)

*   **`main.py` (The Brain):** Houses the primary endpoint `/api/predict/location-risk`. It accepts JSON payloads containing either a `city_name` or strict `lat`/`lng` coordinates.
*   **`Dashboard.jsx` (The Eyes):** Maps out the data. It contains an array of `BASEMAPS` holding 10 reliable map feed URLs and paints an SVG dial using trigonometric CSS (`stroke-dashoffset`) to visualize danger.
*   **`Profile.jsx` (The Credentials):** A secure enclave where the operator manages contact overrides (Email/SMS) ensuring any critical dashboard alerts correspond to valid emergency broadcast channels.

---

## 4. How the System Works (End-to-End Flow)

When an operator launches the GeoPredict system, the following automated chain reaction occurs:

1.  **Operator Access:** 
    The operator logs in. The frontend dynamically checks authentication state and routes them safely to the Dashboard.
2.  **Target Acquisition (3 Methods):**
    *   *Auto-Lock*: On first load, the browser requests the operator's physical GPS location.
    *   *Manual Search*: The user types a region (e.g., "Munnar") into the search bar.
    *   *Map Drag*: The user clicks and drags the central Map Pin crosshair to a physical mountain range.
3.  **Data Ingestion:**
    The React frontend securely transmits those targets to the FastAPI backend. If the target is a text string, the backend uses the Nominatim API to secretly translate "Munnar" into strict GPS Coordinates `[10.0889, 77.0595]`.
4.  **Environmental Evaluation:**
    FastAPI instantly asks OpenWeatherMap for the atmospheric conditions at `[10.0889, 77.0595]`. It retrieves total Rainfall (mm) and Ground Saturation/Humidity (%).
5.  **Risk Algorithms:**
    The backend computes a mathematical heuristic. If rainfall is high and humidity is saturated above 75%, the ground is prone to physical collapse. It generates a "Landslide Susceptibility Index" score from 1-100.
6.  **Visual Render & Evac:**
    The payload is fired back to the dashboard. The SVG dials spin up to match the math. The Leaflet Map physically `flyTo()` animates across the globe to the coordinates, immediately drawing a 4000-meter translucent Red/Green risk ring over the terrain.
    *   *Critical Trigger*: If the mathematical score breaks the "WARNING" threshold, React intercepts the render and forcefully throws an animated, deep-red `<AlertModal />` onto the screen indicating an immediate Evacuation Protocol.
