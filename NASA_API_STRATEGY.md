# GeoPredict EWS: NASA API Decision & Architecture Strategy

**Document Purpose:** This document explains how GeoPredict uses its NASA Developer API key and why the chosen API-driven architecture is scientifically stronger than a custom-trained AI/ML model for a student project of this scope.

---

## 1. The NASA Developer API Key — What It Unlocks

GeoPredict has been issued an official NASA Developer API key from `api.nasa.gov`. This key is NOT for general searches — it is a cryptographic token that authorizes our application to directly query NASA's internal scientific databases in real time.

The key unlocks two extremely powerful endpoints specifically applicable to our **Landslide Early Warning System:**

---

### 1.1 NASA EONET — Earth Observatory Natural Event Tracker

**API Endpoint:**
```
GET https://eonet.gsfc.nasa.gov/api/v3/events?api_key=<YOUR_KEY>
```

**What it returns:** A real-time structured JSON feed of every natural disaster NASA's Earth observing satellites are actively tracking on the planet right now — severe storms, floods, wildfires, and more.

**Why it matters for landslides:** Heavy rainfall and severe storms are the **#1 scientific trigger** for landslides globally. If NASA's satellite network confirms an active severe storm system over Karnataka or Kerala, that is the most authoritative early warning signal possible.

**How we use it in the Dashboard:**
The GeoPredict dashboard queries this endpoint when a location is scanned. If a NASA-confirmed storm event is detected within proximity of the selected coordinates, the system displays:

> *"⚠️ NASA EONET ALERT: Active Severe Storm tracked over this region. Elevated landslide trigger probability."*

---

### 1.2 NASA Earth Imagery API — Landsat Satellite Photography

**API Endpoint:**
```
GET https://api.nasa.gov/planetary/earth/assets?lat=12.33&lon=75.80&dim=0.1&api_key=<YOUR_KEY>
```

**What it returns:** An actual, real-world satellite photograph from NASA's **Landsat 8** satellite of any coordinate on Earth.

**Why it matters for landslides:** Satellite imagery allows the system (and an operator viewing the dashboard) to visually confirm terrain conditions — deforestation on slopes, water-saturated dark soil patches, or post-rain cloud coverage — all of which are visual precursors to ground collapse.

**How we use it in the Dashboard:**
When an operator drops the map pin on a location (e.g., Wayanad, Coorg), the system fetches and displays a real NASA satellite photograph of that exact zone inside the dashboard panel. This transforms a data number into a **visual intelligence report**.

---

## 2. Approach Comparison: API Intelligence vs Custom AI/ML Model

This table is the key decision document for our project architecture strategy.

| Approach | What It Requires | Cost | Time to Build | Accuracy | Realistic for Project? |
|---|---|---|---|---|---|
| **Train YOLO on Satellite Imagery** | 10,000+ expert-labeled landslide satellite images, GPU server, months of training iterations | Very High | 4-6 months minimum | Unpredictable — can hallucinate | ❌ Not feasible |
| **Use Pre-Trained YOLO on Live Satellite Stream** | Real-time commercial satellite feed (e.g., Planet Labs, Maxar) | ₹2-5 Lakhs/month | 3+ months integration | High but expensive | ❌ Extremely expensive |
| **Collect & Label Our Own Dataset + Train Model** | Manually label thousands of images, annotate landslide boundaries, train classifier | Months of manual labor | 5-8 months | Low without large data | ❌ Insufficient data scale |
| **NASA LHASA ArcGIS API (Current Architecture)** | Only an internet connection — NASA runs the model | Free | Already implemented ✅ | Scientifically validated by NASA | ✅ Production ready |
| **NASA EONET Disaster Events Feed (New Key)** | NASA Developer API Key | Free | 1-2 hours | Real satellite ground truth | ✅ Highly achievable |
| **NASA Earth Imagery API for Visual Evidence** | NASA Developer API Key | Free | 2-3 hours | Real Landsat photography | ✅ Highly achievable |

---

## 3. Why the API Architecture is Scientifically Stronger

Training a custom YOLO model might seem more "advanced," but consider what we are actually doing:

> Instead of building our own algorithm to guess what NASA already knows, we pipe our queries **directly into NASA's supercomputers** and receive their verified, mission-critical output.

### The Science Behind Our Detection Pipeline

```
[User Drops Pin on Map]
         │
         ▼
[Step 1] NASA Earth Imagery API
         → Fetches real Landsat satellite photo of terrain
         → Visual confirmation: Is this steep? Is there deforestation?
         │
         ▼
[Step 2] OpenWeatherMap API
         → Fetches live 1-hour rainfall (mm) and humidity (%)
         → Determines: Is the ground currently being saturated?
         │
         ▼
[Step 3] Terrain Geofencing Engine (Local Python)
         → Are these coordinates within the Western Ghats, Himalayas, or Northeast?
         → Steep terrain + multiplier = exponentially higher risk
         │
         ▼
[Step 4] NASA EONET Active Events Check
         → Is NASA currently tracking a storm system near this location?
         → If YES → This is a live, confirmed trigger event
         │
         ▼
[Step 5] NASA LHASA ArcGIS Susceptibility API
         → Queries NASA's LHASA model for the exact pixel hazard value
         → Returns: Pixel Score > 0.8 = CRITICAL EVACUATION
         │
         ▼
[Final Output]
         → Landslide Susceptibility Index (0-100) rendered on Dashboard
         → Color-coded hazard zone overlays painted on GIS map
         → Emergency Dispatch Node arms SMS + Email notification system
```

---

## 4. Conclusion: The Correct Architecture Decision

For a project of this scope, the **hybrid API architecture** is not a compromise — it is the most correct engineering decision because:

1. **NASA's LHASA model** was built by a team of geologists and data scientists over multiple years using petabytes of satellite data. Our custom model could never match this accuracy.
2. **The NASA API key** provides institutional credibility. In a presentation, stating *"our system queries NASA's operational disaster server"* is far more powerful than *"we trained a neural network on 200 images."*
3. **The system is live and operational today.** A custom YOLO model would take months to reach a deployable state.

The correct path forward is to **deepen the NASA integration** using the newly acquired API key to add EONET disaster tracking and real satellite imagery to the dashboard — turning GeoPredict into a true multi-source geospatial intelligence platform.
