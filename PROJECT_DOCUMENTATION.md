# GeoPredict: Early Warning System Documentation

Welcome to the technical documentation for **GeoPredict**, a professional, AI-powered Early Warning System (EWS) designed for landslide disaster prevention. This system integrates satellite data fusion and temporal telemetry to provide real-time risk assessment and automated alerts.

---

## 🚀 1. Project Overview

**GeoPredict** is a state-of-the-art landslide prediction platform. It leverages a **Dual-Engine AI Architecture** to analyze environmental risks from both spatial (satellite imagery) and temporal (ground-level telemetry) perspectives.

- **Objective**: To minimize the loss of life and property through predictive intelligence and automated early warnings.
- **Value Proposition**: High-tech command center interface, secure authenticated access, and dual-layer risk assessment engines.

---

## 🛠️ 2. Technology Stack

### Backend
- **Framework**: FastAPI (Python) - High-performance asynchronous API framework.
- **Database**: MySQL - Relational database for persistent storage of users, profiles, and alert history.
- **ORM**: SQLAlchemy - SQL Toolkit and Object-Relational Mapper.
- **Security**: JWT (JSON Web Tokens) for authentication, Bcrypt for password hashing.
- **Communication**: SMTP for secure Email OTP (One-Time Password) verification.
- **AI Modules (Simulated/Proposed)**: 
  - **XGBoost**: For temporal telemetry analysis (Rainfall, Slope Angle, Soil Saturation).
  - **YOLO (You Only Look Once)**: For spatial object detection (landslide slip detection in satellite imagery).

### Frontend
- **Library**: React 19 (Vite) - Modern, lightning-fast frontend development.
- **Styling**: Tailwind CSS 4.0 - Utility-first CSS for premium, responsive designs.
- **Animations**: Framer Motion - Smooth transitions and high-end micro-animations.
- **Icons**: Lucide React - Clean, modern vector icons.
- **State Management**: React Context API (AuthContext) - Secure handling of user sessions.
- **Networking**: Axios - For robust API communication.

---

## 🏗️ 3. Backend Architecture (Modules)

The backend is organized into **6 core modules**:

1.  **`main.py`**: The entry point. Handles application startup, CORS configuration, and core API routes for temporal and spatial predictions.
2.  **`auth.py`**: Manages the complete authentication lifecycle, including user registration, OTP generation/validation via email, and login.
3.  **`database.py`**: Configures the SQLAlchemy engine and provides database session management.
4.  **`models.py`**: Defines the database schema using SQLAlchemy models (`User`, `Profile`, `OTP`).
5.  **`profile.py`**: Handles user profile management, including updates and admin-level user discovery.
6.  **`security.py`**: Contains core security utilities such as password hashing and JWT token creation/decryption.

---

## 🎨 4. Frontend Architecture (Modules)

The frontend is built with a focused, component-based architecture:

### 📄 Pages
- **Landing**: A premium "Command Center" introduction showcasing system capabilities.
- **Login / Register**: Secure entry points for users.
- **Dashboard**: The primary operational interface showing real-time risk scores and telemetry.
- **Profile**: User-specific settings and preferences management.
- **Admin**: A dedicated view for system administrators to manage users (Restricted Access).
- **Home**: Authenticated user landing area.

### 🧩 Components
- **Navbar**: Dynamic navigation that adjusts based on authentication state.
- **ProtectedRoute**: A higher-order component that secures routes, ensuring only authenticated users can access the dashboard.

---

## ⚙️ 5. Requirements & Working Details

### System Requirements
- **Software**:
  - Python 3.9 or higher.
  - Node.js 18+ (for Vite/React).
  - MySQL Server 8.0+.
  - Modern Browser (Chrome, Firefox, Safari, Edge).
- **Environment Variables**:
  - `DATABASE_URL`: Connection string for MySQL.
  - `SECRET_KEY`: For JWT signing.
  - `SMTP_USER` & `SMTP_PASSWORD`: For email functionalities.

### Operational Workflow
1.  **Data Acquisition**: The system accepts telemetry data (Rainfall, Slope Angle, etc.) or satellite imagery uploads.
2.  **Dual-Engine Inference**:
    - **Temporal Engine**: Analyzes ground-level sensor data to calculate a risk score (0-100).
    - **Spatial Engine**: Processes satellite images to detect physical landslide slips using object detection.
3.  **Risk Dissemination**: Based on the calculated risk, the system categorizes the threat:
    - `0-30`: SAFE
    - `31-50`: WATCH
    - `51-75`: WARNING
    - `76-100`: CRITICAL EVACUATION
4.  **User Dashboard**: Displays interactive charts, risk meters, and live alerts for the user.

---

## 🔒 6. Security Features
- **Email OTP Verification**: Every new account must be verified via a unique 6-digit code sent to the registered email.
- **JWT Session Management**: Tokens are used to secure every sensitive API request.
- **Role-Based Access Control (RBAC)**: Distinguishes between standard users and system administrators.

---

*GeoPredict — Predictive Intelligence for Disaster Prevention.*
