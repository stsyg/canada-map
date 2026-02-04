"""
Canada Map POI Demo - Flask Application
Demonstrates how to use the self-hosted TileServer GL with Python
"""

from flask import Flask, jsonify, render_template_string
from dataclasses import dataclass
from typing import List
import os
import json

app = Flask(__name__)

# TileServer GL URLs
# TILESERVER_URL is for internal container-to-container communication
# TILESERVER_PUBLIC_URL is for browser/client access (served in HTML)
TILESERVER_URL = os.environ.get("TILESERVER_URL", "http://localhost:8080")
TILESERVER_PUBLIC_URL = os.environ.get("TILESERVER_PUBLIC_URL", "http://localhost:8080")


@dataclass
class POI:
    """Point of Interest with location and metadata"""
    name: str
    description: str
    latitude: float
    longitude: float
    flag: str  # Flag emoji or icon identifier
    country: str
    country_code: str = ""  # ISO 2-letter country code for flag images
    category: str = "army"  # army, navy, air, special


# Comprehensive military installations data
# Sources: Public government websites, Wikipedia
POIS: List[POI] = [
    # ============================================
    # CANADA - ARMY
    # ============================================
    POI(
        name="CFB Petawawa",
        description="Home of 2 Canadian Mechanized Brigade Group, 4th Canadian Division Support Base",
        latitude=45.8972,
        longitude=-77.2819,
        flag="🇨🇦",
        country="Canada",
        country_code="ca",
        category="army"
    ),
    POI(
        name="CFB Edmonton",
        description="Home of 1 Canadian Mechanized Brigade Group, 3rd Canadian Division HQ",
        latitude=53.4972,
        longitude=-113.4636,
        flag="🇨🇦",
        country="Canada",
        country_code="ca",
        category="army"
    ),
    POI(
        name="CFB Gagetown",
        description="Largest military base in Canada, Combat Training Centre",
        latitude=45.7500,
        longitude=-66.4500,
        flag="🇨🇦",
        country="Canada",
        country_code="ca",
        category="army"
    ),
    POI(
        name="CFB Valcartier",
        description="Home of 5 Canadian Mechanized Brigade Group, 2nd Canadian Division",
        latitude=46.9000,
        longitude=-71.5000,
        flag="🇨🇦",
        country="Canada",
        country_code="ca",
        category="army"
    ),
    POI(
        name="CFB Shilo",
        description="Artillery training center, Royal Regiment of Canadian Artillery",
        latitude=49.8333,
        longitude=-99.6333,
        flag="🇨🇦",
        country="Canada",
        country_code="ca",
        category="army"
    ),
    POI(
        name="CFB Wainwright",
        description="Canadian Manoeuvre Training Centre, major training area",
        latitude=52.8333,
        longitude=-110.8667,
        flag="🇨🇦",
        country="Canada",
        country_code="ca",
        category="army"
    ),
    POI(
        name="CFB Suffield",
        description="British Army Training Unit Suffield (BATUS), large training area",
        latitude=50.2667,
        longitude=-111.1833,
        flag="🇨🇦",
        country="Canada",
        country_code="ca",
        category="army"
    ),
    POI(
        name="CFB Kingston",
        description="Canadian Forces Base, home to multiple army schools",
        latitude=44.2333,
        longitude=-76.5000,
        flag="🇨🇦",
        country="Canada",
        country_code="ca",
        category="army"
    ),
    POI(
        name="CFB Borden",
        description="Largest training base in Canada, multiple schools",
        latitude=44.2708,
        longitude=-79.9128,
        flag="🇨🇦",
        country="Canada",
        country_code="ca",
        category="army"
    ),
    
    # ============================================
    # CANADA - NAVY
    # ============================================
    POI(
        name="CFB Esquimalt",
        description="Pacific Fleet HQ, Maritime Forces Pacific (MARPAC)",
        latitude=48.4322,
        longitude=-123.4139,
        flag="🇨🇦",
        country="Canada",
        country_code="ca",
        category="navy"
    ),
    POI(
        name="CFB Halifax",
        description="Atlantic Fleet HQ, Maritime Forces Atlantic (MARLANT)",
        latitude=44.6667,
        longitude=-63.5833,
        flag="🇨🇦",
        country="Canada",
        country_code="ca",
        category="navy"
    ),
    POI(
        name="HMCS Naden",
        description="Naval training establishment, Pacific coast",
        latitude=48.4319,
        longitude=-123.4186,
        flag="🇨🇦",
        country="Canada",
        country_code="ca",
        category="navy"
    ),
    POI(
        name="Fleet Diving Unit Atlantic",
        description="Naval diving and EOD unit, Halifax",
        latitude=44.6700,
        longitude=-63.5700,
        flag="🇨🇦",
        country="Canada",
        country_code="ca",
        category="navy"
    ),
    
    # ============================================
    # CANADA - AIR FORCE
    # ============================================
    POI(
        name="CFB Trenton",
        description="8 Wing, main air transport hub, CC-130 Hercules, CC-177 Globemaster",
        latitude=44.1189,
        longitude=-77.5281,
        flag="🇨🇦",
        country="Canada",
        country_code="ca",
        category="air"
    ),
    POI(
        name="CFB Cold Lake",
        description="4 Wing, CF-18 fighter jet base, Air Weapons Evaluation",
        latitude=54.4050,
        longitude=-110.2794,
        flag="🇨🇦",
        country="Canada",
        country_code="ca",
        category="air"
    ),
    POI(
        name="CFB Bagotville",
        description="3 Wing, CF-18 operations, NORAD alert facility",
        latitude=48.3306,
        longitude=-70.9964,
        flag="🇨🇦",
        country="Canada",
        country_code="ca",
        category="air"
    ),
    POI(
        name="CFB Comox",
        description="19 Wing, maritime patrol, CP-140 Aurora, SAR",
        latitude=49.7108,
        longitude=-124.8867,
        flag="🇨🇦",
        country="Canada",
        country_code="ca",
        category="air"
    ),
    POI(
        name="CFB Greenwood",
        description="14 Wing, maritime patrol, CP-140 Aurora",
        latitude=44.9844,
        longitude=-64.9169,
        flag="🇨🇦",
        country="Canada",
        country_code="ca",
        category="air"
    ),
    POI(
        name="CFB Winnipeg",
        description="17 Wing, 1 Canadian Air Division HQ, training center",
        latitude=49.9100,
        longitude=-97.2400,
        flag="🇨🇦",
        country="Canada",
        country_code="ca",
        category="air"
    ),
    POI(
        name="CFB Moose Jaw",
        description="15 Wing, NATO Flying Training Canada, CT-156 Harvard II",
        latitude=50.3303,
        longitude=-105.5592,
        flag="🇨🇦",
        country="Canada",
        country_code="ca",
        category="air"
    ),
    POI(
        name="CFB North Bay",
        description="22 Wing, NORAD operations center, underground complex",
        latitude=46.3500,
        longitude=-79.4167,
        flag="🇨🇦",
        country="Canada",
        country_code="ca",
        category="air"
    ),
    POI(
        name="CFB Goose Bay",
        description="5 Wing, NATO tactical training, forward operating base",
        latitude=53.3192,
        longitude=-60.4258,
        flag="🇨🇦",
        country="Canada",
        country_code="ca",
        category="air"
    ),
    POI(
        name="CFS Alert",
        description="Signals intelligence station, northernmost military base",
        latitude=82.5018,
        longitude=-62.3481,
        flag="🇨🇦",
        country="Canada",
        country_code="ca",
        category="air"
    ),
    POI(
        name="CFS Leitrim",
        description="Communications Security Establishment signals station",
        latitude=45.3500,
        longitude=-75.6167,
        flag="🇨🇦",
        country="Canada",
        country_code="ca",
        category="air"
    ),
    
    # ============================================
    # CANADA - SPECIAL FORCES
    # ============================================
    POI(
        name="JTF2 Headquarters",
        description="Joint Task Force 2, Tier 1 special operations unit",
        latitude=45.4600,
        longitude=-75.8800,
        flag="🇨🇦",
        country="Canada",
        country_code="ca",
        category="special"
    ),
    POI(
        name="CSOR Base",
        description="Canadian Special Operations Regiment, Petawawa",
        latitude=45.9000,
        longitude=-77.2500,
        flag="🇨🇦",
        country="Canada",
        country_code="ca",
        category="special"
    ),
    POI(
        name="427 SOAS",
        description="427 Special Operations Aviation Squadron, Petawawa",
        latitude=45.9100,
        longitude=-77.2600,
        flag="🇨🇦",
        country="Canada",
        country_code="ca",
        category="special"
    ),
    
    # ============================================
    # USA - ARMY (presence in Canada/near border)
    # ============================================
    POI(
        name="Fort Drum",
        description="10th Mountain Division, near Canadian border",
        latitude=44.0500,
        longitude=-75.7667,
        flag="🇺🇸",
        country="USA",
        country_code="us",
        category="army"
    ),
    POI(
        name="Joint Base Lewis-McChord",
        description="I Corps HQ, near Vancouver BC",
        latitude=47.0867,
        longitude=-122.5797,
        flag="🇺🇸",
        country="USA",
        country_code="us",
        category="army"
    ),
    POI(
        name="Fort Wainwright",
        description="US Army Alaska, Fairbanks",
        latitude=64.8300,
        longitude=-147.6500,
        flag="🇺🇸",
        country="USA",
        country_code="us",
        category="army"
    ),
    
    # ============================================
    # USA - NAVY
    # ============================================
    POI(
        name="Naval Station Everett",
        description="Carrier Strike Group, Puget Sound",
        latitude=47.9856,
        longitude=-122.2278,
        flag="🇺🇸",
        country="USA",
        country_code="us",
        category="navy"
    ),
    POI(
        name="Naval Base Kitsap",
        description="Submarine base, Trident ballistic missiles",
        latitude=47.7178,
        longitude=-122.7328,
        flag="🇺🇸",
        country="USA",
        country_code="us",
        category="navy"
    ),
    POI(
        name="Naval Station Norfolk (HQ)",
        description="Largest naval base in the world, fleet operations",
        latitude=36.9461,
        longitude=-76.3156,
        flag="🇺🇸",
        country="USA",
        country_code="us",
        category="navy"
    ),
    
    # ============================================
    # USA - AIR FORCE
    # ============================================
    POI(
        name="Thule Air Base",
        description="US Space Force, NORAD early warning, Greenland",
        latitude=76.5311,
        longitude=-68.7033,
        flag="🇺🇸",
        country="USA",
        country_code="us",
        category="air"
    ),
    POI(
        name="Elmendorf-Richardson",
        description="Joint Base, 11th Air Force, F-22 Raptors",
        latitude=61.2500,
        longitude=-149.8000,
        flag="🇺🇸",
        country="USA",
        country_code="us",
        category="air"
    ),
    POI(
        name="Eielson AFB",
        description="354th Fighter Wing, F-35A Lightning II",
        latitude=64.6656,
        longitude=-147.1019,
        flag="🇺🇸",
        country="USA",
        country_code="us",
        category="air"
    ),
    POI(
        name="Clear Space Force Station",
        description="Ballistic missile early warning system",
        latitude=64.2917,
        longitude=-149.1917,
        flag="🇺🇸",
        country="USA",
        country_code="us",
        category="air"
    ),
    POI(
        name="Peterson SFB",
        description="NORAD/USNORTHCOM HQ, Colorado Springs",
        latitude=38.8236,
        longitude=-104.7003,
        flag="🇺🇸",
        country="USA",
        country_code="us",
        category="air"
    ),
    POI(
        name="Cheyenne Mountain SFS",
        description="NORAD Alternate Command Center, underground complex",
        latitude=38.7436,
        longitude=-104.8469,
        flag="🇺🇸",
        country="USA",
        country_code="us",
        category="air"
    ),
    
    # ============================================
    # USA - SPECIAL FORCES
    # ============================================
    POI(
        name="Fort Liberty (Bragg)",
        description="US Army Special Operations Command, Delta Force",
        latitude=35.1392,
        longitude=-78.9967,
        flag="🇺🇸",
        country="USA",
        country_code="us",
        category="special"
    ),
    POI(
        name="Naval Special Warfare Command",
        description="US Navy SEALs HQ, Coronado",
        latitude=32.6833,
        longitude=-117.1833,
        flag="🇺🇸",
        country="USA",
        country_code="us",
        category="special"
    ),
    POI(
        name="Dam Neck",
        description="SEAL Team Six (DEVGRU), Virginia Beach",
        latitude=36.8167,
        longitude=-75.9667,
        flag="🇺🇸",
        country="USA",
        country_code="us",
        category="special"
    ),
    
    # ============================================
    # UK - ARMY
    # ============================================
    POI(
        name="BATUS",
        description="British Army Training Unit Suffield, Alberta",
        latitude=50.2833,
        longitude=-111.2000,
        flag="🇬🇧",
        country="UK",
        country_code="gb",
        category="army"
    ),
    POI(
        name="Catterick Garrison",
        description="Largest British Army garrison, North Yorkshire",
        latitude=54.3833,
        longitude=-1.6333,
        flag="🇬🇧",
        country="UK",
        country_code="gb",
        category="army"
    ),
    POI(
        name="Aldershot Garrison",
        description="Home of the British Army, Hampshire",
        latitude=51.2500,
        longitude=-0.7667,
        flag="🇬🇧",
        country="UK",
        country_code="gb",
        category="army"
    ),
    
    # ============================================
    # UK - NAVY
    # ============================================
    POI(
        name="HMNB Portsmouth",
        description="Home of the Royal Navy, Queen Elizabeth carriers",
        latitude=50.8000,
        longitude=-1.1000,
        flag="🇬🇧",
        country="UK",
        country_code="gb",
        category="navy"
    ),
    POI(
        name="HMNB Clyde",
        description="Trident submarine base, Scotland",
        latitude=55.9833,
        longitude=-4.8333,
        flag="🇬🇧",
        country="UK",
        country_code="gb",
        category="navy"
    ),
    POI(
        name="HMNB Devonport",
        description="Largest naval base in Western Europe, Plymouth",
        latitude=50.3833,
        longitude=-4.1833,
        flag="🇬🇧",
        country="UK",
        country_code="gb",
        category="navy"
    ),
    
    # ============================================
    # UK - AIR FORCE
    # ============================================
    POI(
        name="RAF Coningsby",
        description="Typhoon FGR4, Quick Reaction Alert",
        latitude=53.0936,
        longitude=-0.1661,
        flag="🇬🇧",
        country="UK",
        country_code="gb",
        category="air"
    ),
    POI(
        name="RAF Lossiemouth",
        description="Typhoon, P-8 Poseidon maritime patrol",
        latitude=57.7056,
        longitude=-3.3392,
        flag="🇬🇧",
        country="UK",
        country_code="gb",
        category="air"
    ),
    POI(
        name="RAF Marham",
        description="F-35B Lightning II, UK stealth fighter base",
        latitude=52.6483,
        longitude=0.5506,
        flag="🇬🇧",
        country="UK",
        country_code="gb",
        category="air"
    ),
    POI(
        name="RAF Brize Norton",
        description="Air Mobility Force, C-17 Globemaster, A400M",
        latitude=51.7500,
        longitude=-1.5833,
        flag="🇬🇧",
        country="UK",
        country_code="gb",
        category="air"
    ),
    POI(
        name="RAF Lakenheath",
        description="USAF in UK, F-15E Strike Eagles, F-35A",
        latitude=52.4092,
        longitude=0.5611,
        flag="🇬🇧",
        country="UK",
        country_code="gb",
        category="air"
    ),
    
    # ============================================
    # UK - SPECIAL FORCES
    # ============================================
    POI(
        name="SAS Headquarters",
        description="22 Special Air Service Regiment, Hereford",
        latitude=52.0567,
        longitude=-2.7150,
        flag="🇬🇧",
        country="UK",
        country_code="gb",
        category="special"
    ),
    POI(
        name="SBS Headquarters",
        description="Special Boat Service, Poole",
        latitude=50.7167,
        longitude=-1.9833,
        flag="🇬🇧",
        country="UK",
        country_code="gb",
        category="special"
    ),
    POI(
        name="SFSG Base",
        description="Special Forces Support Group, St Athan",
        latitude=51.4050,
        longitude=-3.4400,
        flag="🇬🇧",
        country="UK",
        country_code="gb",
        category="special"
    ),
    
    # ============================================
    # NATO - HEADQUARTERS & COMMANDS
    # ============================================
    POI(
        name="NATO HQ Brussels",
        description="North Atlantic Treaty Organization Headquarters",
        latitude=50.8792,
        longitude=4.4281,
        flag="🔵",
        country="NATO",
        country_code="nato",
        category="army"
    ),
    POI(
        name="SHAPE",
        description="Supreme Headquarters Allied Powers Europe, Mons",
        latitude=50.5033,
        longitude=3.9678,
        flag="🔵",
        country="NATO",
        country_code="nato",
        category="army"
    ),
    POI(
        name="Allied Joint Force Command Norfolk",
        description="JFC Norfolk, Atlantic operations",
        latitude=36.9461,
        longitude=-76.2892,
        flag="🔵",
        country="NATO",
        country_code="nato",
        category="navy"
    ),
    POI(
        name="MARCOM Northwood",
        description="Allied Maritime Command, UK",
        latitude=51.6167,
        longitude=-0.4167,
        flag="🔵",
        country="NATO",
        country_code="nato",
        category="navy"
    ),
    POI(
        name="AIRCOM Ramstein",
        description="Allied Air Command, Germany",
        latitude=49.4369,
        longitude=7.6003,
        flag="🔵",
        country="NATO",
        country_code="nato",
        category="air"
    ),
    POI(
        name="NATO AWACS Geilenkirchen",
        description="E-3A Sentry AWACS aircraft base, Germany",
        latitude=50.9617,
        longitude=6.0428,
        flag="🔵",
        country="NATO",
        country_code="nato",
        category="air"
    ),
    POI(
        name="NSHQ Mons",
        description="NATO Special Operations Headquarters",
        latitude=50.4500,
        longitude=3.9500,
        flag="🔵",
        country="NATO",
        country_code="nato",
        category="special"
    ),
]


# HTML template with MapLibre GL JS
MAP_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Military Installations Map</title>
    <script src="https://unpkg.com/maplibre-gl@4.0.0/dist/maplibre-gl.js"></script>
    <link href="https://unpkg.com/maplibre-gl@4.0.0/dist/maplibre-gl.css" rel="stylesheet" />
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }
        #map { position: absolute; top: 0; bottom: 0; width: 100%; }
        
        .sidebar {
            position: absolute;
            top: 10px;
            left: 10px;
            background: white;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
            max-width: 350px;
            max-height: calc(100vh - 40px);
            overflow-y: auto;
            z-index: 1000;
        }
        
        .sidebar h2 { margin-bottom: 5px; font-size: 18px; }
        .sidebar p { font-size: 12px; color: #666; margin-bottom: 10px; }
        
        .filters {
            background: #f8f9fa;
            padding: 12px;
            border-radius: 6px;
            margin-bottom: 12px;
        }
        .filters h3 { font-size: 13px; margin-bottom: 8px; color: #333; }
        .filter-section { margin-bottom: 10px; }
        .filter-section:last-child { margin-bottom: 0; }
        .filter-label { font-size: 11px; font-weight: 600; color: #666; margin-bottom: 4px; display: block; }
        .filter-options { display: flex; flex-wrap: wrap; gap: 4px; }
        .filter-option {
            display: flex;
            align-items: center;
            padding: 4px 8px;
            background: white;
            border: 1px solid #ddd;
            border-radius: 4px;
            cursor: pointer;
            font-size: 11px;
            transition: all 0.2s;
        }
        .filter-option:hover { border-color: #999; }
        .filter-option.active { background: #e3f2fd; border-color: #2196f3; }
        .filter-option input { display: none; }
        .filter-option img { width: 16px; height: 12px; margin-right: 4px; border-radius: 1px; }
        .filter-option .icon { margin-right: 4px; font-size: 12px; }
        
        .stats { font-size: 11px; color: #666; margin-bottom: 8px; padding: 6px 10px; background: #f0f0f0; border-radius: 4px; }
        
        .poi-list { list-style: none; max-height: 300px; overflow-y: auto; }
        .poi-item {
            padding: 8px;
            margin: 4px 0;
            background: #f5f5f5;
            border-radius: 5px;
            cursor: pointer;
            transition: background 0.2s;
            font-size: 12px;
            display: flex;
            align-items: center;
        }
        .poi-item:hover { background: #e0e0e0; }
        .poi-item.hidden { display: none; }
        .poi-flag { width: 20px; height: 15px; margin-right: 8px; border-radius: 2px; object-fit: cover; }
        .poi-name { font-weight: 600; flex: 1; }
        .poi-category { 
            font-size: 9px; 
            padding: 2px 5px; 
            border-radius: 3px; 
            text-transform: uppercase;
            font-weight: 600;
            margin-left: 6px;
        }
        .cat-army { background: #c8e6c9; color: #2e7d32; }
        .cat-navy { background: #bbdefb; color: #1565c0; }
        .cat-air { background: #e1bee7; color: #7b1fa2; }
        .cat-special { background: #ffccbc; color: #d84315; }
        
        .legend {
            margin-top: 12px;
            padding-top: 12px;
            border-top: 1px solid #ddd;
        }
        .legend h3 { font-size: 12px; margin-bottom: 6px; }
        
        .maplibregl-popup-content {
            padding: 15px;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            min-width: 200px;
        }
        .popup-header { display: flex; align-items: center; margin-bottom: 8px; }
        .popup-flag { width: 40px; height: 30px; border-radius: 4px; margin-right: 10px; object-fit: cover; box-shadow: 0 1px 3px rgba(0,0,0,0.2); }
        .popup-title { font-size: 15px; font-weight: 600; }
        .popup-meta { display: flex; align-items: center; gap: 8px; margin-bottom: 8px; }
        .popup-country { color: #666; font-size: 12px; }
        .popup-cat { font-size: 10px; padding: 2px 6px; border-radius: 3px; text-transform: uppercase; font-weight: 600; }
        .popup-desc { font-size: 13px; line-height: 1.4; color: #333; }
        .popup-coords { font-size: 11px; color: #999; margin-top: 8px; }
    </style>
</head>
<body>
    <div id="map"></div>
    
    <div class="sidebar">
        <h2>🎖️ Military Installations</h2>
        <p>Allied Forces Bases - Canada, USA, UK & NATO</p>
        
        <div class="filters">
            <h3>🔍 Filter Markers</h3>
            
            <div class="filter-section">
                <span class="filter-label">By Country</span>
                <div class="filter-options" id="country-filters">
                    <label class="filter-option active" data-filter="country" data-value="ca">
                        <input type="checkbox" checked>
                        <img src="https://flagcdn.com/w40/ca.png"> Canada
                    </label>
                    <label class="filter-option active" data-filter="country" data-value="us">
                        <input type="checkbox" checked>
                        <img src="https://flagcdn.com/w40/us.png"> USA
                    </label>
                    <label class="filter-option active" data-filter="country" data-value="gb">
                        <input type="checkbox" checked>
                        <img src="https://flagcdn.com/w40/gb.png"> UK
                    </label>
                    <label class="filter-option active" data-filter="country" data-value="nato">
                        <input type="checkbox" checked>
                        <img src="https://upload.wikimedia.org/wikipedia/commons/3/37/Flag_of_NATO.svg"> NATO
                    </label>
                </div>
            </div>
            
            <div class="filter-section">
                <span class="filter-label">By Branch</span>
                <div class="filter-options" id="category-filters">
                    <label class="filter-option active" data-filter="category" data-value="army">
                        <input type="checkbox" checked>
                        <span class="icon">🪖</span> Army
                    </label>
                    <label class="filter-option active" data-filter="category" data-value="navy">
                        <input type="checkbox" checked>
                        <span class="icon">⚓</span> Navy
                    </label>
                    <label class="filter-option active" data-filter="category" data-value="air">
                        <input type="checkbox" checked>
                        <span class="icon">✈️</span> Air Force
                    </label>
                    <label class="filter-option active" data-filter="category" data-value="special">
                        <input type="checkbox" checked>
                        <span class="icon">🎯</span> Special Forces
                    </label>
                </div>
            </div>
        </div>
        
        <div class="stats" id="stats">Loading...</div>
        
        <ul class="poi-list" id="poi-list"></ul>
        
        <div class="legend">
            <h3>Category Colors</h3>
            <div style="display:flex;gap:8px;flex-wrap:wrap;font-size:11px;">
                <span class="poi-category cat-army">Army</span>
                <span class="poi-category cat-navy">Navy</span>
                <span class="poi-category cat-air">Air</span>
                <span class="poi-category cat-special">Special</span>
            </div>
        </div>
    </div>

    <script>
        const TILESERVER_URL = '{{ tileserver_public_url }}';
        let allPois = [];
        let markers = [];
        let activeFilters = {
            country: ['ca', 'us', 'gb', 'nato'],
            category: ['army', 'navy', 'air', 'special']
        };
        
        // Initialize map with wider bounds to show UK and Europe
        const map = new maplibregl.Map({
            container: 'map',
            style: TILESERVER_URL + '/styles/osm-bright/style.json',
            center: [-50.0, 55.0],
            zoom: 2.5
        });

        map.addControl(new maplibregl.NavigationControl());
        map.addControl(new maplibregl.ScaleControl());
        
        // Setup filter event listeners
        document.querySelectorAll('.filter-option').forEach(option => {
            option.addEventListener('click', function() {
                const checkbox = this.querySelector('input');
                checkbox.checked = !checkbox.checked;
                this.classList.toggle('active', checkbox.checked);
                
                const filterType = this.dataset.filter;
                const value = this.dataset.value;
                
                if (checkbox.checked) {
                    if (!activeFilters[filterType].includes(value)) {
                        activeFilters[filterType].push(value);
                    }
                } else {
                    activeFilters[filterType] = activeFilters[filterType].filter(v => v !== value);
                }
                
                applyFilters();
            });
        });
        
        function applyFilters() {
            let visibleCount = 0;
            
            markers.forEach((item, index) => {
                const poi = allPois[index];
                const countryMatch = activeFilters.country.includes(poi.country_code);
                const categoryMatch = activeFilters.category.includes(poi.category);
                const visible = countryMatch && categoryMatch;
                
                // Toggle marker visibility
                item.marker.getElement().style.display = visible ? 'block' : 'none';
                
                // Toggle list item visibility
                const listItem = document.querySelector(`[data-poi-index="${index}"]`);
                if (listItem) {
                    listItem.classList.toggle('hidden', !visible);
                }
                
                if (visible) visibleCount++;
            });
            
            // Update stats
            document.getElementById('stats').textContent = `Showing ${visibleCount} of ${allPois.length} installations`;
        }
        
        function getFlagUrl(countryCode) {
            if (countryCode === 'nato') {
                return 'https://upload.wikimedia.org/wikipedia/commons/3/37/Flag_of_NATO.svg';
            }
            return `https://flagcdn.com/w80/${countryCode}.png`;
        }

        // Fetch POIs from API
        async function loadPOIs() {
            try {
                const response = await fetch('/api/pois');
                allPois = await response.json();
                
                const poiList = document.getElementById('poi-list');
                
                allPois.forEach((poi, index) => {
                    // Create custom marker element with flag image
                    const el = document.createElement('div');
                    el.className = 'marker';
                    el.style.width = '28px';
                    el.style.height = '21px';
                    el.style.cursor = 'pointer';
                    el.style.borderRadius = '3px';
                    el.style.boxShadow = '0 2px 4px rgba(0,0,0,0.3)';
                    el.style.border = '2px solid white';
                    el.style.overflow = 'hidden';
                    el.style.backgroundImage = `url(${getFlagUrl(poi.country_code)})`;
                    el.style.backgroundSize = 'cover';
                    el.style.backgroundPosition = 'center';
                    
                    // Create popup
                    const popup = new maplibregl.Popup({ offset: 25 })
                        .setHTML(`
                            <div class="popup-header">
                                <img class="popup-flag" src="${getFlagUrl(poi.country_code)}">
                                <div class="popup-title">${poi.name}</div>
                            </div>
                            <div class="popup-meta">
                                <span class="popup-country">${poi.country}</span>
                                <span class="popup-cat cat-${poi.category}">${poi.category}</span>
                            </div>
                            <div class="popup-desc">${poi.description}</div>
                            <div class="popup-coords">📍 ${poi.latitude.toFixed(4)}, ${poi.longitude.toFixed(4)}</div>
                        `);
                    
                    // Add marker to map
                    const marker = new maplibregl.Marker({ element: el })
                        .setLngLat([poi.longitude, poi.latitude])
                        .setPopup(popup)
                        .addTo(map);
                    
                    // Store marker reference for filtering
                    markers.push({ marker, poi });
                    
                    // Add to sidebar list
                    const li = document.createElement('li');
                    li.className = 'poi-item';
                    li.dataset.poiIndex = index;
                    li.innerHTML = `
                        <img class="poi-flag" src="${getFlagUrl(poi.country_code)}">
                        <span class="poi-name">${poi.name}</span>
                        <span class="poi-category cat-${poi.category}">${poi.category}</span>
                    `;
                    li.onclick = () => {
                        map.flyTo({
                            center: [poi.longitude, poi.latitude],
                            zoom: 8,
                            duration: 1500
                        });
                        marker.togglePopup();
                    };
                    poiList.appendChild(li);
                });
                
                // Apply initial filters and update stats
                applyFilters();
                
            } catch (error) {
                console.error('Error loading POIs:', error);
            }
        }

        map.on('load', loadPOIs);
    </script>
</body>
</html>
"""


@app.route('/')
def index():
    """Serve the main map page"""
    return render_template_string(MAP_TEMPLATE, tileserver_public_url=TILESERVER_PUBLIC_URL)


@app.route('/api/pois')
def get_pois():
    """API endpoint to get all POIs as JSON"""
    return jsonify([
        {
            'name': poi.name,
            'description': poi.description,
            'latitude': poi.latitude,
            'longitude': poi.longitude,
            'flag': poi.flag,
            'country': poi.country,
            'country_code': poi.country_code,
            'category': poi.category
        }
        for poi in POIS
    ])


@app.route('/api/pois/<country>')
def get_pois_by_country(country: str):
    """API endpoint to get POIs filtered by country"""
    filtered = [poi for poi in POIS if poi.country.lower() == country.lower()]
    return jsonify([
        {
            'name': poi.name,
            'description': poi.description,
            'latitude': poi.latitude,
            'longitude': poi.longitude,
            'flag': poi.flag,
            'country': poi.country,
            'country_code': poi.country_code,
            'category': poi.category
        }
        for poi in filtered
    ])


@app.route('/api/pois/region/<region>')
def get_pois_by_region(region: str):
    """
    API endpoint to get POIs by region (bounding box)
    Regions: ontario, bc, alberta, arctic
    """
    regions = {
        'ontario': {'min_lat': 41.0, 'max_lat': 57.0, 'min_lon': -95.0, 'max_lon': -74.0},
        'bc': {'min_lat': 48.0, 'max_lat': 60.0, 'min_lon': -139.0, 'max_lon': -114.0},
        'alberta': {'min_lat': 49.0, 'max_lat': 60.0, 'min_lon': -120.0, 'max_lon': -110.0},
        'arctic': {'min_lat': 66.0, 'max_lat': 84.0, 'min_lon': -141.0, 'max_lon': -52.0},
    }
    
    if region.lower() not in regions:
        return jsonify({'error': f'Unknown region. Valid: {list(regions.keys())}'}), 400
    
    bounds = regions[region.lower()]
    filtered = [
        poi for poi in POIS
        if bounds['min_lat'] <= poi.latitude <= bounds['max_lat']
        and bounds['min_lon'] <= poi.longitude <= bounds['max_lon']
    ]
    
    return jsonify([
        {
            'name': poi.name,
            'description': poi.description,
            'latitude': poi.latitude,
            'longitude': poi.longitude,
            'flag': poi.flag,
            'country': poi.country,
            'country_code': poi.country_code,
            'category': poi.category
        }
        for poi in filtered
    ])


@app.route('/api/health')
def health():
    """Health check endpoint"""
    import requests
    try:
        resp = requests.get(f"{TILESERVER_URL}/health", timeout=5)
        tileserver_ok = resp.status_code == 200
    except:
        tileserver_ok = False
    return jsonify({
        'status': 'ok' if tileserver_ok else 'degraded',
        'tileserver_internal': TILESERVER_URL,
        'tileserver_public': TILESERVER_PUBLIC_URL,
        'tileserver_healthy': tileserver_ok
    })


if __name__ == '__main__':
    print(f"""
╔════════════════════════════════════════════════════════════╗
║  Canada Map POI Demo                                       ║
║  ─────────────────────────────────────────────────────────║
║  Map UI:     http://localhost:5000                         ║
║  POI API:    http://localhost:5000/api/pois                ║
║  TileServer: {TILESERVER_URL:<40} ║
╚════════════════════════════════════════════════════════════╝
    """)
    app.run(host='0.0.0.0', port=5000, debug=True)
