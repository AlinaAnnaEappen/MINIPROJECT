/**
 * SHE SHIELD – Main Client Controller
 * Handles location autocomplete, journey planning form submission,
 * and clean advisory rendering.
 */

document.addEventListener("DOMContentLoaded", function () {
  const planForm = document.getElementById("plan-form");
  const locationInput = document.getElementById("location-input");
  const dateInput = document.getElementById("date-input");
  const timeInput = document.getElementById("time-input");
  const autocompleteList = document.getElementById("autocomplete-list");
  const submitBtn = document.getElementById("submit-btn");
  const resultsContainer = document.getElementById("results-container");

  // 1. Initialize default date to today and time to 21:30 (night default)
  if (dateInput && !dateInput.value) {
    const today = new Date().toISOString().split("T")[0];
    dateInput.value = today;
  }

  if (timeInput && !timeInput.value) {
    timeInput.value = "21:30";
  }

  // Preset time buttons
  const timeChips = document.querySelectorAll(".time-presets .preset-btn");
  timeChips.forEach(btn => {
    btn.addEventListener("click", () => {
      timeChips.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      if (timeInput) {
        timeInput.value = btn.getAttribute("data-time");
      }
    });
  });

  // 2. Autocomplete location search
  let debounceTimeout = null;
  if (locationInput && autocompleteList) {
    locationInput.addEventListener("input", function () {
      const query = this.value.trim();
      clearTimeout(debounceTimeout);

      if (query.length < 2) {
        autocompleteList.innerHTML = "";
        autocompleteList.style.display = "none";
        return;
      }

      debounceTimeout = setTimeout(async () => {
        try {
          const res = await fetch(`/api/autocomplete?q=${encodeURIComponent(query)}`);
          if (res.ok) {
            const data = await res.json();
            renderAutocomplete(data.matches || []);
          }
        } catch (e) {
          console.error("Autocomplete error:", e);
        }
      }, 150);
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
      <li class="autocomplete-entry" data-name="${item.name}">
        <span class="entry-name">${item.name}</span>
        <span class="entry-district">${item.district}</span>
      </li>
    `).join("");
    autocompleteList.style.display = "block";

    autocompleteList.querySelectorAll(".autocomplete-entry").forEach(el => {
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
        console.error("Advisory calculation error:", err);
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
      submitBtn.innerHTML = `<span>Evaluating regional data & facilities...</span>`;
    } else {
      submitBtn.disabled = false;
      submitBtn.innerHTML = `<span>Generate Travel Advisory</span>`;
    }
  }

  function renderResults(res) {
    if (!resultsContainer) return;

    const adv = res.advisory;
    const loc = res.location;
    const sch = res.travel_schedule;
    const crime = res.crime_context;
    const stn = res.nearest_police_station;

    const statusBadgeClass = adv.badge_color === "safe" ? "status-safe" :
                             adv.badge_color === "cautious" ? "status-cautious" : "status-elevated";

    resultsContainer.innerHTML = `
      <!-- Advisory Overview Banner -->
      <div class="card result-card ${statusBadgeClass}">
        <div class="advisory-top-bar">
          <div>
            <span class="advisory-location-tag">${loc.district_name} District &bull; ${loc.name}</span>
            <h2 class="advisory-category">${adv.category}</h2>
          </div>
          <div class="score-pill">
            <span class="score-val">${adv.score}</span>
            <span class="score-label">Index Score</span>
          </div>
        </div>
        <p class="advisory-summary">${adv.summary}</p>
      </div>

      <!-- Actionable Travel Guidance -->
      <div class="card guidance-card">
        <h3 class="card-heading">Practical Travel Guidance</h3>
        <ul class="guidance-list">
          ${adv.recommendations.map(r => `
            <li>
              <span class="guidance-bullet">&#10003;</span>
              <span>${r}</span>
            </li>
          `).join("")}
        </ul>
      </div>

      <!-- Verified District Crime Context -->
      ${crime ? `
        <div class="card crime-context-card">
          <div class="crime-header-flex">
            <div>
              <h3 class="card-heading">Regional Crime Context (${crime.district} District)</h3>
              <p class="crime-subhead">Official Kerala Police State Crime Records Bureau (SCRB)</p>
            </div>
            <span class="data-tag">Verified SCRB Data</span>
          </div>

          <div class="crime-stats-row">
            <div class="stat-box">
              <span class="stat-num">${crime.latest_annual_crimes.toLocaleString()}</span>
              <span class="stat-caption">Annual Reported Crimes</span>
            </div>
            <div class="stat-box">
              <span class="stat-num">${crime.rate_per_lakh_females}</span>
              <span class="stat-caption">Per Lakh Females</span>
            </div>
            <div class="stat-box">
              <span class="stat-num">${crime.public_space_crime_rate}</span>
              <span class="stat-caption">Public Space Rate</span>
            </div>
            <div class="stat-box">
              <span class="stat-num">${crime.relative_risk_category}</span>
              <span class="stat-caption">Statewide Benchmark</span>
            </div>
          </div>
          <p class="crime-disclaimer-note">
            Statistics represent administrative district totals to establish broad regional context. They do not predict individual incidents at specific street corners.
          </p>
        </div>
      ` : ''}

      <!-- Nearby Mapped Police Stations -->
      <div class="card police-stations-card">
        <div class="card-header-flex">
          <div>
            <h3 class="card-heading">Nearest Police Stations</h3>
            <p class="card-subhead">Confirmed facility locations with direct telephone lines</p>
          </div>
          <span class="data-tag">Direct Emergency Access</span>
        </div>

        <div class="station-list">
          ${res.nearby_police_stations.map(ps => `
            <div class="station-row">
              <div class="station-details">
                <h4 class="station-name">
                  ${ps.name}
                  ${ps.is_women_cell ? '<span class="women-cell-tag">Women Desk</span>' : ''}
                </h4>
                <p class="station-meta">
                  ${ps.district} District &bull; <strong>${ps.distance_km} km away</strong>
                </p>
              </div>
              <div class="station-dialer">
                <a href="tel:${ps.phone}" class="btn-call">
                  <span>Call ${ps.phone}</span>
                </a>
              </div>
            </div>
          `).join("")}
        </div>
        <p class="station-note">
          Mapped stations reflect geographic proximity. In Kerala, official response is governed by designated jurisdictional boundaries.
        </p>
      </div>
    `;

    // Smooth scroll to results
    resultsContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  // 4. Handle pre-filled query parameter from URL (e.g. ?q=Kochi from Home page)
  const urlParams = new URLSearchParams(window.location.search);
  const qParam = urlParams.get('q');
  if (qParam && locationInput) {
    locationInput.value = qParam;
    setTimeout(() => {
      if (planForm) {
        planForm.dispatchEvent(new Event("submit"));
      }
    }, 350);
  } else if (planForm && locationInput && !locationInput.value) {
    // Default initial query: Chengannur
    locationInput.value = "Chengannur";
    setTimeout(() => {
      if (planForm) {
        planForm.dispatchEvent(new Event("submit"));
      }
    }, 350);
  }
});
