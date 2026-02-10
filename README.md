# skylark-drone_OPS_agent
Drone Operations Coordinator AI Agent


# Skylark Drone Operations Coordinator

## Overview
This project is a Streamlit-based AI-assisted operations dashboard designed for Skylark Drones.  
It helps coordinate pilots, drones, and missions across multiple projects using live Google Sheets as the backend.

The system reduces manual coordination by providing real-time visibility, conflict detection, and assignment recommendations.

---

## Core Features

### 1. Pilot Roster Management
- View pilot availability, skills, certifications, and locations
- Update pilot status (Available / On Leave / Unavailable)
- Changes sync back to Google Sheets in real time

### 2. Mission Tracking & Assignment
- View all missions with requirements and priority
- Evaluate pilot suitability based on:
  - Availability
  - Skills
  - Certifications
  - Location
- Recommend the best pilot for a mission
- Assign pilots to missions with one click

### 3. Drone Inventory Management
- View drone availability, location, and deployment status
- Update drone status (Available / Deployed / In Maintenance)
- Maintenance warnings are flagged in the UI

### 4. Conflict Detection
- Skill and certification mismatch detection
- Pilot availability conflicts
- Location mismatches between pilot, drone, and mission
- Maintenance conflicts for drones

---

## Tech Stack
- Python
- Streamlit
- Google Sheets API
- gspread
- Google Cloud Service Accounts

---

## Architecture Overview
- `app.py`:  
  Handles UI, business logic, conflict detection, and assignments
- `sheets.py`:  
  Google Sheets integration layer (read/write operations)
- Google Sheets:  
  Acts as the live database for pilots, drones, and missions

---

## Deployment
- Hosted on **Streamlit Cloud**
- Connected to GitHub for continuous deployment
- Uses Streamlit Secrets for secure Google API authentication

---

## Limitations
- Date overlap conflicts are flagged but not auto-blocked
- Urgent reassignment logic is advisory, not automated
- Conversational interface is form-based rather than chat-based

---

## Future Improvements
- Full date-overlap enforcement
- Automated urgent reassignment workflows
- Chat-based conversational interface
- Audit log for historical assignments
