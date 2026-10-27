// SHE SHIELD - Main Client Application Logic

document.addEventListener("DOMContentLoaded", () => {
  const locationInput = document.getElementById("location-input");
  const dateInput = document.getElementById("date-input");
  const timeInput = document.getElementById("time-input");
  const planForm = document.getElementById("plan-form");
  const submitBtn = document.getElementById("submit-btn");
  const autocompleteList = document.getElementById("autocomplete-list");
  const resultsContainer = document.getElementById("results-container");

  // Pre-fill today's date if empty
  if (dateInput && !dateInput.value) {
    const today = new Date().toISOString().split("T")[0];
    dateInput.value = today;
  }

  // Pre-fill default time if empty (current local time)
  if (timeInput && !timeInput.value) {
    const now = new Date();
    const hh = String(now.getHours()).padStart(2, "0");
    const mm = String(now.getMinutes()).padStart(2, "0");
    timeInput.value = `${hh}:${mm}`;
  }

  // 1. Time Preset Chips
  const timeChips = document.querySelectorAll(".chip-btn");
  timeChips.forEach(chip => {
    chip.addEventListener("click", () => {
      timeChips.forEach(c => c.classList.remove("active"));
      chip.classList.add("active");
      const chosenTime = chip.getAttribute("data-time");
      if (chosenTime && timeInput) {
        timeInput.value = chosenTime;
      }
    });
  });

  // 2. Autocomplete Suggestions
  let debounceTimer = null;
  if (locationInput && autocompleteList) {
    locationInput.addEventListener("input", (e) => {
      clearTimeout(debounceTimer);
      const query = e.target.value.trim();
      if (query.length < 2) {
        autocompleteList.innerHTML = "";
        autocompleteList.style.display = "none";
        return;
      }

      debounceTimer = setTimeout(async () => {
        try {
          const res = await fetch(`/api/autocomplete?q=${encodeURIComponent(query)}`);
          if (res.ok) {
            const data = await res.json();
            renderAutocomplete(data.matches || []);
          }
        } catch (err) {
          console.warn("Autocomplete fetch failed:", err);
        }
      }, 200);
    });

    document.addEventListener("click", (e) => {
      if (!locationInput.contains(e.target) && !autocompleteList.contains(e.target)) {
        autocompleteList.style.display = "none";
      }
    });
  }

  function renderAutocomplete(items) {
    if (!items.length) {
      autocompleteList.innerHTML = "";
      autocompleteList.style.display = "none";
      return;
    }
    autocompleteList.innerHTML = items.map(item => `
      <li class="autocomplete-item" data-name="${item.name}">
        <span>📍 <strong>${item.name}</strong></span>
        <span class="dist-badge">${item.district}</span>
      </li>
    `).join("");
    autocompleteList.style.display = "block";

    autocompleteList.querySelectorAll(".autocomplete-item").forEach(el => {
      el.addEventListener("click", () => {
        locationInput.value = el.getAttribute("data-name");
        autocompleteList.style.display = "none";
      });
    });
  }

  // 3. Form Submission
  if (planForm) {
    planForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const location = locationInput.value.trim();
      const date = dateInput.value;
      const time = timeInput.value;

      if (!location) {
        alert("Please enter a destination in Kerala.");
        return;
      }

      setLoading(true);

      try {
        const response = await fetch("/api/predict", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ location, date, time })
        });

        const data = await response.json();
        if (!response.ok || !data.success) {
          alert(data.error || "Could not generate advisory for this location.");
          setLoading(false);
          return;
        }

        renderResults(data.result);
        if (typeof updateMap === "function") {
          updateMap(data.result.location, data.result.nearby_police_stations);
        }
      } catch (err) {
        console.error("Advisory error:", err);
        alert("Server communication error. Please try again.");
      } finally {
        setLoading(false);
      }
    });
  }

  function setLoading(isLoading) {
    if (!submitBtn) return;
    if (isLoading) {
      submitBtn.disabled = true;
      submitBtn.innerHTML = `<span>⏳ Evaluating verified safety metrics...</span>`;
    } else {
      submitBtn.disabled = false;
      submitBtn.innerHTML = `<span>🛡️ Assess Travel Safety & Comfort</span>`;
    }
  }

  function renderResults(res) {
    if (!resultsContainer) return;

    const adv = res.advisory;
    const loc = res.location;
    const sch = res.travel_schedule;
    const crime = res.crime_context;

    const badgeClass = adv.badge_color === "safe" ? "badge-safe" :
                       adv.badge_color === "cautious" ? "badge-cautious" : "badge-unsafe";
    const scoreColorClass = adv.badge_color === "safe" ? "score-safe" :
                            adv.badge_color === "cautious" ? "score-cautious" : "score-unsafe";

    resultsContainer.innerHTML = `
      <!-- 1. Advisory Banner -->
      <div class="advisory-badge-card ${badgeClass}">
        <div class="advisory-title-group">
          <div style="display:flex;align-items:center;gap:8px;margin-bottom:6px;">
            <span style="font-size:12px;text-transform:uppercase;letter-spacing:1.5px;color:var(--gold-primary);font-weight:700;">
              Pre-Travel Assessment
            </span>
            <span style="font-size:11px;background:rgba(255,255,255,0.1);padding:2px 8px;border-radius:12px;">
              ${loc.district_name} District
            </span>
          </div>
          <h3>${adv.category}</h3>
          <p>${adv.summary}</p>
        </div>
        <div class="score-display">
          <div class="score-number ${scoreColorClass}">${adv.score}</div>
          <div class="score-denom">/100</div>
        </div>
      </div>

      <!-- 2. Actionable Recommendations -->
      <div class="glass-card">
        <h4 style="font-size:17px;font-weight:700;color:#fff;margin-bottom:14px;display:flex;align-items:center;gap:8px;">
          <span>💡</span> Recommended Travel Precautions
        </h4>
        <ul style="list-style:none;display:flex;flex-direction:column;gap:10px;">
          ${adv.recommendations.map(r => `
            <li style="display:flex;align-items:flex-start;gap:10px;font-size:14.5px;color:#e2e8f0;">
              <span style="color:var(--gold-primary);font-weight:bold;">✔</span>
              <span>${r}</span>
            </li>
          `).join("")}
        </ul>
      </div>

      <!-- 3. Indicators Grid -->
      <div class="indicator-grid">
        ${adv.contributing_factors.map(f => `
          <div class="indicator-card">
            <div class="indicator-header">
              <span>${f.factor}</span>
              <span class="indicator-score">${f.score}/100</span>
            </div>
            <div class="indicator-bar">
              <div class="indicator-fill" style="width:${f.score}%;background:${
                f.score >= 75 ? 'var(--safe-green)' : f.score >= 50 ? 'var(--cautious-yellow)' : 'var(--unsafe-red)'
              }"></div>
            </div>
            <div class="indicator-detail">${f.detail}</div>
          </div>
        `).join("")}
      </div>

      <!-- 4. Verified Official Crime Context -->
      ${crime ? `
        <div class="glass-card" style="border-left:4px solid var(--cyan-accent);">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;flex-wrap:wrap;gap:8px;">
            <h4 style="font-size:16px;color:#fff;display:flex;align-items:center;gap:8px;">
              <span>📊</span> Official Crime Context (${crime.district} District)
            </h4>
            <span style="font-size:11px;color:var(--cyan-accent);border:1px solid rgba(56,189,248,0.3);padding:2px 8px;border-radius:12px;">
              Kerala Police SCRB Verified
            </span>
          </div>
          <div style="display:grid;grid-template-columns:repeat(auto-fit, minmax(160px,1fr));gap:16px;margin-bottom:12px;">
            <div style="background:rgba(0,0,0,0.3);padding:12px;border-radius:8px;">
              <span style="font-size:11px;color:var(--text-muted);display:block;">Latest Annual Total</span>
              <strong style="font-size:18px;color:#fff;">${crime.latest_annual_crimes.toLocaleString()} cases</strong>
            </div>
            <div style="background:rgba(0,0,0,0.3);padding:12px;border-radius:8px;">
              <span style="font-size:11px;color:var(--text-muted);display:block;">Rate per Lakh Females</span>
              <strong style="font-size:18px;color:var(--gold-primary);">${crime.rate_per_lakh_females}</strong>
            </div>
            <div style="background:rgba(0,0,0,0.3);padding:12px;border-radius:8px;">
              <span style="font-size:11px;color:var(--text-muted);display:block;">Public Space Crimes Rate</span>
              <strong style="font-size:18px;color:#fff;">${crime.public_space_crime_rate} / lakh</strong>
            </div>
            <div style="background:rgba(0,0,0,0.3);padding:12px;border-radius:8px;">
              <span style="font-size:11px;color:var(--text-muted);display:block;">State Risk Bracket</span>
              <strong style="font-size:18px;color:#fff;">${crime.relative_risk_category}</strong>
            </div>
          </div>
          <p style="font-size:12px;color:var(--text-dim);margin:0;">
            Source: Kerala Police Crime Against Women Portal & NCRB. 
            Statistics reflect administrative district totals; they provide broad regional context and must not be interpreted as street-level incident predictions.
          </p>
        </div>
      ` : ''}

      <!-- 5. Nearby Mapped Police Stations -->
      <div class="glass-card">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">
          <h4 style="font-size:16px;color:#fff;display:flex;align-items:center;gap:8px;">
            <span>🛡️</span> Nearby Mapped Police Stations
          </h4>
          <span style="font-size:12px;color:var(--text-muted);">
            Emergency Call Button Active
          </span>
        </div>
        <div class="ps-list">
          ${res.nearby_police_stations.map(ps => `
            <div class="ps-item">
              <div class="ps-info">
                <h5>${ps.name} ${ps.is_women_cell ? '<span style="color:#ec4899;font-size:11px;">(Women Cell)</span>' : ''}</h5>
                <p>📍 ${ps.district} District &bull; ${ps.jurisdiction_type} &bull; <strong>${ps.distance_km} km away</strong></p>
              </div>
              <div class="ps-action">
                <a href="tel:${ps.phone}">📞 Call Station</a>
              </div>
            </div>
          `).join("")}
        </div>
        <p style="font-size:11.5px;color:var(--text-dim);margin-top:12px;">
          * Note: Mapped stations show confirmed facility locations and linear proximity. In Kerala, jurisdiction is defined by designated police station areas, not purely by nearest geographic point.
        </p>
      </div>
    `;

    // Scroll gently to results
    resultsContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  // Auto trigger default location on /plan load (Chengannur)
  if (planForm && locationInput && !locationInput.value) {
    locationInput.value = "Chengannur";
    // Trigger planForm submit after a brief delay so map is ready
    setTimeout(() => {
      planForm.dispatchEvent(new Event("submit"));
    }, 400);
  }
});
