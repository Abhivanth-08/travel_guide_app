# Smart Travel Guide Mobile Application

This is the Smart Travel Guide monorepo containing a full-stack React Native Expo mobile application and a FastAPI backend with MongoDB.

## Features
- JWT Authentication (Register/Login)
- MongoDB integration (Places, Users, Itineraries)
- Offline-ready basic architecture (AsyncStorage)
- Connected Mobile UI built with React Native Expo
- Local API configuration (`10.0.2.2` mapping for Android Emulators)
- Seeded database with demo points of interest.
- AI Recommendations (Groq API, falling back to Demo Mode when no key is present)
- APK building capability via Expo prebuild + gradle.

## Architecture
- **Backend**: FastAPI + MongoDB (motor) + Groq AI
- **Mobile**: React Native + Expo + Axios + React Navigation

## Prerequisites
- Node.js & npm
- Python 3.10+
- MongoDB instance (Local or Atlas)
- Java 17 / Android SDK (for building the APK locally)

## Backend Setup
1. `cd backend`
2. `python -m venv venv`
3. Activate venv: `.\venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Mac/Linux)
4. `pip install -r requirements.txt`
5. Copy `.env.example` to `.env` and fill in secrets (like `GROQ_API_KEY`).

### Running the Backend
1. Start the database (Ensure MongoDB is running on localhost:27017 or update `.env`).
2. Run the seed script to populate demo places:
   `python seed.py`
3. Start the FastAPI server:
   `uvicorn app.main:app --host 0.0.0.0 --port 8000`

## Mobile App Setup
1. `cd mobile`
2. `npm install`

### Running the Mobile App
During development:
1. `npx expo start`
2. Press 'a' to run on an Android emulator or scan the QR code using Expo Go.

## Generating the APK
To generate a standalone installable Android APK:
1. `cd mobile`
2. `npx expo prebuild --platform android`
3. `cd android`
4. `.\gradlew assembleDebug`
5. The generated APK will be located at:
   `mobile/android/app/build/outputs/apk/debug/app-debug.apk`

## Demo Procedure
1. Ensure the backend is running (`uvicorn ...`).
2. Launch the mobile app (or install the generated APK).
3. Tap "Register" and create an account.
4. Tap "Login" using the newly created credentials.
5. You will see the Home Dashboard. (Additional screens like Map and AI Chat are stubbed out for future expansion but the core auth flow is connected end-to-end to the real backend).
