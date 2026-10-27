// SHE SHIELD Interactive Map Engine (Leaflet integration)

let sheMap = null;
let destinationMarker = null;
let policeStationLayer = null;
let proximityCircles = [];

function initMap(lat = 9.3176, lon = 76.6112, zoom = 13) {
  const mapElement = document.getElementById('advisory-map');
  if (!mapElement) return;

  // Check if Leaflet L is available
  if (typeof L === 'undefined') {
    mapElement.innerHTML = `
      <div style="display:flex;height:100%;align-items:center;justify-content:center;color:#94a3b8;flex-direction:column;gap:10px;text-align:center;padding:20px;">
        <p>⚠️ Interactive Leaflet map library loading...</p>
        <p style="font-size:12px;">Displaying verified coordinates: Latitude ${lat}, Longitude ${lon}</p>
      </div>
    `;
    return;
  }

  if (sheMap) {
    sheMap.setView([lat, lon], zoom);
    return;
  }

  try {
    sheMap = L.map('advisory-map', {
      zoomControl: true,
      scrollWheelZoom: true
    }).setView([lat, lon], zoom);

    // OpenStreetMap Tile Layer with attribution
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright" target="_blank">OpenStreetMap</a> contributors | SHE SHIELD'
    }).addTo(sheMap);

    policeStationLayer = L.layerGroup().addTo(sheMap);
  } catch (err) {
    console.warn("Map initialization error:", err);
  }
}

function updateMap(locationData, nearbyStations = []) {
  if (typeof L === 'undefined') return;
  if (!sheMap) {
    initMap(locationData.lat, locationData.lon, 13);
  }

  const lat = locationData.lat;
  const lon = locationData.lon;

  sheMap.setView([lat, lon], 13);

  // 1. Clear previous layers
  if (destinationMarker) {
    sheMap.removeLayer(destinationMarker);
  }
  if (policeStationLayer) {
    policeStationLayer.clearLayers();
  }
  proximityCircles.forEach(c => sheMap.removeLayer(c));
  proximityCircles = [];

  // 2. Custom Destination Pin
  const destIcon = L.divIcon({
    className: 'custom-dest-pin',
    html: `
      <div style="
        background: #d4af37;
        width: 22px;
        height: 22px;
        border-radius: 50%;
        border: 3px solid #0c0a17;
        box-shadow: 0 0 15px rgba(212,175,55,0.8);
        display: flex;
        align-items: center;
        justify-content: center;
        color: #0c0a17;
        font-size: 11px;
        font-weight: 800;
      ">★</div>
    `,
    iconSize: [22, 22],
    iconAnchor: [11, 11]
  });

  destinationMarker = L.marker([lat, lon], { icon: destIcon })
    .addTo(sheMap)
    .bindPopup(`
      <div style="color:#0c0a17;font-family:sans-serif;min-width:180px;">
        <h4 style="margin:0 0 4px 0;font-size:14px;color:#0f172a;">📍 ${locationData.name}</h4>
        <p style="margin:0;font-size:12px;color:#475569;">Selected Destination</p>
        <p style="margin:4px 0 0 0;font-size:11px;color:#64748b;">Coord: ${lat.toFixed(4)}, ${lon.toFixed(4)}</p>
      </div>
    `)
    .openPopup();

  // 3. Proximity Buffer Circles (2 km immediate response, 5 km standard range)
  const circle2km = L.circle([lat, lon], {
    radius: 2000,
    color: '#d4af37',
    weight: 1,
    dashArray: '4, 4',
    fillColor: '#d4af37',
    fillOpacity: 0.05
  }).addTo(sheMap);

  const circle5km = L.circle([lat, lon], {
    radius: 5000,
    color: '#38bdf8',
    weight: 1,
    dashArray: '6, 6',
    fillColor: '#38bdf8',
    fillOpacity: 0.03
  }).addTo(sheMap);

  proximityCircles.push(circle2km, circle5km);

  // 4. Plot Nearby Police Stations
  nearbyStations.forEach(ps => {
    const isWomenCell = ps.is_women_cell;
    const pinColor = isWomenCell ? '#ec4899' : '#3b82f6';
    const pinLabel = isWomenCell ? '♀' : '🛡️';

    const psIcon = L.divIcon({
      className: 'custom-ps-pin',
      html: `
        <div style="
          background: ${pinColor};
          width: 24px;
          height: 24px;
          border-radius: 6px;
          border: 2px solid #ffffff;
          box-shadow: 0 0 10px ${pinColor};
          display: flex;
          align-items: center;
          justify-content: center;
          color: #ffffff;
          font-size: 12px;
        ">${pinLabel}</div>
      `,
      iconSize: [24, 24],
      iconAnchor: [12, 12]
    });

    const marker = L.marker([ps.lat, ps.lon], { icon: psIcon });
    marker.bindPopup(`
      <div style="color:#0c0a17;font-family:sans-serif;min-width:200px;">
        <div style="display:flex;align-items:center;gap:6px;margin-bottom:4px;">
          <span style="font-size:14px;">${pinLabel}</span>
          <h4 style="margin:0;font-size:13.5px;color:#0f172a;">${ps.name}</h4>
        </div>
        <p style="margin:2px 0;font-size:12px;color:#475569;">
          <strong>Distance:</strong> ${ps.distance_km} km from destination
        </p>
        <p style="margin:2px 0;font-size:12px;color:#475569;">
          <strong>Jurisdiction:</strong> ${ps.jurisdiction_type}
        </p>
        <p style="margin:6px 0 0 0;font-size:12px;">
          <a href="tel:${ps.phone}" style="
            display:inline-block;
            background:#10b981;
            color:white;
            padding:3px 8px;
            border-radius:4px;
            text-decoration:none;
            font-weight:600;
            font-size:11px;
          ">📞 Call ${ps.phone}</a>
        </p>
      </div>
    `);

    policeStationLayer.addLayer(marker);
  });
}
