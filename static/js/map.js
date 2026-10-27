// SHE SHIELD Interactive Map Engine (Leaflet integration)

let sheMap = null;
let destinationMarker = null;
let policeStationLayer = null;
let proximityCircles = [];

function initMap(lat = 9.3176, lon = 76.6112, zoom = 13) {
  const mapElement = document.getElementById('advisory-map');
  if (!mapElement) return;

  if (typeof L === 'undefined') {
    mapElement.innerHTML = `
      <div style="display:flex;height:100%;align-items:center;justify-content:center;color:#4d5c53;flex-direction:column;gap:10px;text-align:center;padding:20px;">
        <p>Interactive Map is loading...</p>
        <p style="font-size:12px;">Coordinates: Latitude ${lat}, Longitude ${lon}</p>
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

    // Warm, highly readable OpenStreetMap CartoDB Positron / OSM tiles
    L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
      maxZoom: 19,
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright" target="_blank">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/">CARTO</a>'
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

  // 2. Custom Destination Pin (Warm Terracotta)
  const destIcon = L.divIcon({
    className: 'custom-dest-pin',
    html: `
      <div style="
        background: #c26738;
        width: 24px;
        height: 24px;
        border-radius: 50%;
        border: 2px solid #ffffff;
        box-shadow: 0 2px 8px rgba(0,0,0,0.25);
        display: flex;
        align-items: center;
        justify-content: center;
        color: #ffffff;
        font-size: 11px;
        font-weight: 700;
      ">&#9733;</div>
    `,
    iconSize: [24, 24],
    iconAnchor: [12, 12]
  });

  destinationMarker = L.marker([lat, lon], { icon: destIcon })
    .addTo(sheMap)
    .bindPopup(`
      <div style="color:#1c2a22;font-family:'Plus Jakarta Sans',sans-serif;min-width:180px;padding:4px;">
        <h4 style="margin:0 0 4px 0;font-size:14px;color:#1c2a22;font-weight:700;">${locationData.name}</h4>
        <p style="margin:0;font-size:12px;color:#4d5c53;">Selected Destination</p>
        <p style="margin:4px 0 0 0;font-size:11px;color:#78867d;">${lat.toFixed(4)}, ${lon.toFixed(4)}</p>
      </div>
    `)
    .openPopup();

  // 3. Proximity Buffer Circles (2 km immediate response, 5 km standard range)
  const circle2km = L.circle([lat, lon], {
    radius: 2000,
    color: '#c26738',
    weight: 1.5,
    dashArray: '4, 4',
    fillColor: '#c26738',
    fillOpacity: 0.04
  }).addTo(sheMap);

  const circle5km = L.circle([lat, lon], {
    radius: 5000,
    color: '#2d6a4f',
    weight: 1.5,
    dashArray: '6, 6',
    fillColor: '#2d6a4f',
    fillOpacity: 0.02
  }).addTo(sheMap);

  proximityCircles.push(circle2km, circle5km);

  // 4. Plot Nearby Police Stations
  nearbyStations.forEach(ps => {
    const isWomenCell = ps.is_women_cell;
    const pinColor = isWomenCell ? '#9d4edd' : '#2d6a4f';

    const psIcon = L.divIcon({
      className: 'custom-ps-pin',
      html: `
        <div style="
          background: ${pinColor};
          width: 22px;
          height: 22px;
          border-radius: 4px;
          border: 2px solid #ffffff;
          box-shadow: 0 2px 6px rgba(0,0,0,0.2);
          display: flex;
          align-items: center;
          justify-content: center;
          color: #ffffff;
          font-size: 11px;
          font-weight: 700;
        ">&#9873;</div>
      `,
      iconSize: [22, 22],
      iconAnchor: [11, 11]
    });

    const marker = L.marker([ps.lat, ps.lon], { icon: psIcon });
    marker.bindPopup(`
      <div style="color:#1c2a22;font-family:'Plus Jakarta Sans',sans-serif;min-width:200px;padding:4px;">
        <h4 style="margin:0 0 4px 0;font-size:13.5px;color:#1c2a22;font-weight:700;">${ps.name}</h4>
        <p style="margin:2px 0;font-size:12px;color:#4d5c53;">
          <strong>Distance:</strong> ${ps.distance_km} km away
        </p>
        <p style="margin:2px 0;font-size:12px;color:#4d5c53;">
          <strong>District:</strong> ${ps.district}
        </p>
        <p style="margin:8px 0 0 0;">
          <a href="tel:${ps.phone}" style="
            display:inline-block;
            background:#2d6a4f;
            color:white;
            padding:4px 10px;
            border-radius:4px;
            text-decoration:none;
            font-weight:600;
            font-size:11.5px;
          ">Call ${ps.phone}</a>
        </p>
      </div>
    `);

    policeStationLayer.addLayer(marker);
  });
}
