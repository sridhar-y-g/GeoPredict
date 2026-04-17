# GeoPredict EWS: Full System Architecture & Detection Logic

This document serves as the master technical blueprint for the **GeoPredict Early Warning System (EWS)**. It details exactly how the application is architected, how the various external APIs interface with local algorithms, and precisely how a landslide is detected.

---

## 1. Executive Summary

GeoPredict is not a standard web application; it is a **geospatial intelligence aggregator**. The system operates by collecting live coordinates from a user, piping them through a rapid succession of meteorological and geological APIs, and applying heuristic algorithms to output a real-time Landslide Susceptibility Index (0-100) and actionable evacuation protocols.

---

## 2. The Core Detection Algorithm

Landslides cannot be predicted by a single metric. They require a catastrophic intersection of vulnerable topography and severe weather. When an operator drops a pin on the `Dashboard` map, the backend `main.py` triggers the following sequential algorithm:

### Step 2.1: Topographical Geofencing (Local Python Logic)
Before relying on external APIs, the Python backend executes a strict coordinate bounds check. It intercepts the user's `latitude` and `longitude` and determines if the region fundamentally supports landslides.
*   **The Code:** Bounding box arrays in `predict_location_risk` (`main.py`).
*   **The Logic:** If the coordinates intersect `8.0 < lat < 21.0` and `73.0 < lng < 77.5`, the engine flags the region as the `WESTERN GHATS`. 
*   **The Impact:** Recognizing a high-altitude mountain range immediately adds a core base-multiplier to the risk score, as steep terrain is a prerequisite for ground collapse.

### Step 2.2: Live Meteorological Telemetry (OpenWeatherMap)
A steep mountain only collapses when the soil liquifies. We must determine the current atmospheric saturation.
*   **The Integration:** Python fires a secure HTTPS request using the `OPENWEATHER_API_KEY`.
*   **The Extraction:** The algorithm specifically hunts for `weather_data["rain"]["1h"]` (live precipitation over the last 60 minutes) and `weather_data["main"]["humidity"]` (air moisture, serving as a proxy for topsoil saturation).
*   **The Impact:** If rainfall exceeds 0mm and humidity crosses 85%, the mathematical model exponentially inflates the risk score by interpreting the ground as maximally saturated.

### Step 2.3: Global Susceptibility Intersection (NASA LHASA)
To finalize the prediction, GeoPredict queries the highest authority: NASA's supercomputers.
*   **The Integration:** Python connects directly to the NASA Center for Climate Simulation via the Disasters ArcGIS MapServer (`maps.disasters.nasa.gov.../identify`).
*   **The Extraction:** We request the precise Global Precipitation Measurement (GPM) fused `{Pixel Value}` for that exact coordinate.
*   **The Impact:** If NASA's neural network returns a hazard pixel > 0.8, the system immediately overrides all local mathematics and declares a `CRITICAL EVACUATION` state.

### Step 2.4: The Fallback Heuristic
NASA servers frequently undergo maintenance. To ensure our Early Warning System never fails during a presentation or real-life storm, GeoPredict features a hardened fail-safe.
*   If NASA times out, Python catches the error and executes a local heuristic formula using the data gathered in Steps 2.1 and 2.2 (`base_risk += rainfall_1h * 18.5`).
*   This ensures the dashboard always displays a highly accurate, calculated mathematical risk score regardless of external government server uptime.

---

## 3. Technology Stack Mapping (Where to find the code)

GeoPredict utilizes a strict separation of concerns, heavily dividing the frontend GIS visuals from the backend processing engine.

### 3.1 Frontend Operations (The GIS Engine)
**Framework:** React + Vite + TailwindCSS
**Core File:** `frontend/src/pages/Dashboard.jsx`
*   **Interactive Mapping:** We use `react-leaflet` (`<MapContainer>`, `<TileLayer>`) to render the global viewport.
*   **Hazard Overlays:** Found in the `HA_OVERLAYS` array, we programmatically draw massive translucent `<Circle>` vectors mapped to exact coordinates (e.g., Wayanad, Kedarnath, Assam) to visually demonstrate color-coded (Red/Orange/Yellow) threat zones across all of India.
*   **Live UI State:** Framer Motion handles the smooth animations while React's `useEffect` hooks strictly govern the network telemetry handshakes.

### 3.2 Backend Processing (The Neural Router)
**Framework:** Python + FastAPI + Requests
**Core File:** `backend/main.py`
*   **Uvicorn ASGI:** Acts as the lightning-fast web server routing traffic.
*   **The Brain:** The `/api/predict/location-risk` endpoint serves as the central circulatory system, performing the OpenWeather grabs, NASA ArcGIS requests, and running the `terrain_type` Geofence calculations mentioned in Section 2.

### 3.3 Authorization & Notification Network (The Dispatch Node)
**Framework:** SQLAlchemy + Python `smtplib` + JWT
**Core Files:** `backend/auth.py` && `backend/security.py`
*   **Authentication:** When a Commander requests clearance, `security.py` uses `passlib.bcrypt` to cryptographically shred and hash their password before saving it to SQLite.
*   **Emergency Dispatch:** `auth.py` houses the `send_otp_email()` function. It connects to Google's SMTP network over Port 587 using Secure App Passwords, generating and dispatching high-end HTML `MIMEMultipart` emails. This infrastructure is what arms the Dashboard's "Emergency Dispatch Node" for mass casualty alerts.

### 3.4 Data Persistence
**Framework:** SQLite / SQLAlchemy
**Core Files:** `backend/database.py` && `backend/models.py`
*   Uses a fully relational ORM structure to store Commander accounts, OTP verification hashes, and Profile telemetry settings dynamically.
