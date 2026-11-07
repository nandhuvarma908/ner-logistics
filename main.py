"""
FastAPI Backend Service
Smart Logistics & Accessibility Intelligence Platform for North Eastern Region (NER)
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid

app = FastAPI(
    title="NER Smart Logistics & Accessibility Intelligence API",
    version="1.0.0",
    description="SIH Prototype backend providing GIS intelligence, AI risk prediction, real-time GPS tracking, and offline incident sync."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory mock store for rapid SIH demonstration
INCIDENTS_DB = []
ALERTS_DB = [
    {
        "id": "alt-001",
        "level": "CRITICAL",
        "title": "Sonapur Tunnel (NH-6) High Landslide Alert",
        "message": "Continuous heavy rainfall (>160mm) detected in East Jaintia Hills. Soil saturation threshold breached. Heavy freight advised to halt or reroute.",
        "affected_corridor": "NH-6 (Meghalaya - Silchar Lifeline)",
        "timestamp": datetime.utcnow().isoformat()
    },
    {
        "id": "alt-002",
        "level": "WARNING",
        "title": "Brahmaputra Flood Spillover Advisory",
        "message": "Water levels near Kaziranga NH-37 approaching critical markers. 20 km/h speed restrictions enforced.",
        "affected_corridor": "NH-37 (Guwahati - Jorhat)",
        "timestamp": datetime.utcnow().isoformat()
    }
]

class RoutePredictionRequest(BaseModel):
    origin: str = Field(..., example="Guwahati")
    destination: str = Field(..., example="Silchar")
    weather_condition: Optional[str] = "HEAVY_MONSOON"
    cargo_priority: Optional[str] = "EMERGENCY_MEDICAL"

class IncidentReport(BaseModel):
    client_offline_id: Optional[str] = None
    reporter_name: str
    incident_type: str
    severity: str
    highway_code: str
    nearest_landmark: str
    description: str
    latitude: float
    longitude: float
    photo_url: Optional[str] = None

@app.get("/")
def root():
    return {
        "status": "online",
        "platform": "NER Accessibility Intelligence Platform",
        "coverage": ["Assam", "Meghalaya", "Arunachal Pradesh", "Nagaland", "Manipur", "Mizoram", "Tripura", "Sikkim"],
        "endpoints": ["/api/v1/gis/corridors", "/api/v1/predict/route-risk", "/api/v1/incidents", "/api/v1/fleet/live", "/api/v1/alerts"]
    }

@app.get("/api/v1/gis/corridors")
def get_corridors():
    """Returns key NER National Highway corridors with real-time risk scores."""
    return [
        {
            "id": "cor-nh6",
            "highway": "NH-6",
            "name": "Guwahati - Shillong - Silchar Lifeline",
            "length_km": 313.5,
            "status": "HIGH_RISK",
            "risk_score": 78.4,
            "critical_chokepoints": ["Sonapur Tunnel", "Khliehriat Ghat", "Barapani"],
            "recommended_bypass": "NH-27 via Doboka - Lumding - Haflong"
        },
        {
            "id": "cor-nh27",
            "highway": "NH-27",
            "name": "Doboka - Lumding - Haflong Alternate Bypass",
            "length_km": 360.0,
            "status": "MODERATE_RISK",
            "risk_score": 42.0,
            "critical_chokepoints": ["Jatinga Valley", "Mahur Ghat"],
            "recommended_bypass": None
        },
        {
            "id": "cor-nh37",
            "highway": "NH-37",
            "name": "Guwahati - Nagaon - Jorhat - Dibrugarh",
            "length_km": 435.0,
            "status": "NORMAL",
            "risk_score": 24.5,
            "critical_chokepoints": ["Kaziranga Corridor", "Kaliabor"],
            "recommended_bypass": None
        },
        {
            "id": "cor-nh2",
            "highway": "NH-2",
            "name": "Dimapur - Kohima - Senapati - Imphal",
            "length_km": 205.0,
            "status": "HIGH_RISK",
            "risk_score": 71.5,
            "critical_chokepoints": ["Zubza Sinking Zone", "Mao Gate"],
            "recommended_bypass": "Silchar - Jiribam - Imphal (NH-37 New)"
        },
        {
            "id": "cor-nh10",
            "highway": "NH-10",
            "name": "Siliguri - Sevoke - Singtam - Gangtok",
            "length_km": 114.0,
            "status": "HIGH_RISK",
            "risk_score": 84.0,
            "critical_chokepoints": ["Paglajhora Slide", "Teesta Bazaar"],
            "recommended_bypass": "Via Lava - Algarah - Reshi Alternate"
        }
    ]

@app.post("/api/v1/predict/route-risk")
def predict_route_risk(req: RoutePredictionRequest):
    """
    AI Route Risk prediction engine returning primary route, safe alternate routes,
    ETA adjustments, and SHAP explainability.
    """
    if req.origin.lower() == "guwahati" and req.destination.lower() == "silchar":
        return {
            "origin": "Guwahati",
            "destination": "Silchar",
            "primary_route": {
                "name": "Primary: Via NH-6 (GS Road & Sonapur Tunnel)",
                "distance_km": 313.5,
                "base_eta_hours": 7.5,
                "risk_adjusted_eta_hours": 12.8,
                "risk_score": 78.4,
                "status": "HIGH_RISK",
                "hazard_reason": "High landslide vulnerability at Sonapur Tunnel (36.5 deg slope + 185mm 48h rain)",
                "shap_explainability": {
                    "Rainfall Intensity & Saturation": 36.4,
                    "Steep Ghat Slope": 26.2,
                    "Historical Landslide Frequency": 21.0,
                    "River Proximity": 10.5,
                    "Road Surface Quality": 5.9
                }
            },
            "safer_alternate_route": {
                "name": "Recommended Alternate: Via NH-27 (Doboka - Lumding - Haflong Bypass)",
                "distance_km": 362.0,
                "base_eta_hours": 8.8,
                "risk_adjusted_eta_hours": 9.4,
                "risk_score": 38.5,
                "status": "SAFE_VIABLE",
                "risk_reduction_pct": 50.8,
                "recommended_for": ["EMERGENCY_MEDICAL", "PERISHABLE", "HEAVY_FREIGHT"]
            }
        }
    else:
        return {
            "origin": req.origin,
            "destination": req.destination,
            "primary_route": {
                "name": f"Corridor {req.origin} -> {req.destination}",
                "distance_km": 240.0,
                "base_eta_hours": 5.5,
                "risk_adjusted_eta_hours": 6.2,
                "risk_score": 32.0,
                "status": "MODERATE_RISK"
            },
            "safer_alternate_route": None
        }

@app.post("/api/v1/incidents")
def report_incident(incident: IncidentReport):
    """
    Endpoint for field officers to sync geo-tagged incident reports.
    Supports offline sync tokens.
    """
    report_dict = incident.dict()
    report_dict["id"] = str(uuid.uuid4())
    report_dict["timestamp"] = datetime.utcnow().isoformat()
    report_dict["status"] = "VERIFIED"
    INCIDENTS_DB.append(report_dict)

    # Automatically generate alert if critical
    if incident.severity.upper() in ["HIGH", "CRITICAL"]:
        ALERTS_DB.insert(0, {
            "id": f"alt-{len(ALERTS_DB)+1}",
            "level": "CRITICAL",
            "title": f"New Field Incident: {incident.incident_type} on {incident.highway_code}",
            "message": f"{incident.nearest_landmark}: {incident.description}. Road passable status compromised.",
            "affected_corridor": incident.highway_code,
            "timestamp": datetime.utcnow().isoformat()
        })

    return {
        "success": True,
        "message": "Incident synced successfully with central dispatch",
        "incident_id": report_dict["id"],
        "client_offline_id": incident.client_offline_id
    }

@app.get("/api/v1/incidents")
def list_incidents():
    return INCIDENTS_DB

@app.get("/api/v1/alerts")
def get_alerts():
    return ALERTS_DB
