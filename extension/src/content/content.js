/**
 * SecureSentinel Content Script
 * Observes DOM changes and injects risk badges.
 */

console.log("[SecureSentinel] Content script active on:", window.location.href);

/**
 * Injects a risk badge next to an element
 * Uses Shadow DOM to isolate styles
 */
function injectBadge(element, score) {
    if (element.dataset.sentinelChecked === "injected") return;
    element.dataset.sentinelChecked = "injected";

    const container = document.createElement("span");
    container.className = "sentinel-badge-anchor";
    container.style.cssText = `
        display: inline-flex !important;
        vertical-align: middle !important;
        margin-left: 6px !important;
        align-items: center !important;
        justify-content: center !important;
        transform: translateY(-1px) !important;
        height: 1em !important;
        width: 1em !important;
    `;

    const shadow = container.attachShadow({ mode: "open" });
    const color = score > 0.8 ? "#f43f5e" : score > 0.6 ? "#f59e0b" : "#10b981";
    const label = score > 0.8 ? "High Risk" : score > 0.6 ? "Suspicious" : "Likely Safe";

    shadow.innerHTML = `
    <style>
      :host {
        display: inline-flex;
        vertical-align: middle;
      }
      .badge {
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background-color: ${color};
        box-shadow: 0 0 4px ${color}66;
        cursor: pointer;
        border: 1.5px solid white;
        transition: transform 0.2s;
        flex-shrink: 0;
      }
      .badge:hover {
        transform: scale(1.3);
      }
    </style>
    <div class="badge" title="SecureSentinel: ${label} (${Math.round(score * 100)}%)"></div>
  `;

    // Try to find the title element inside the link to append next to
    const titleElement = element.querySelector("h3, .title, [class*='title']") || element;
    
    // If we found a specific title element, append to it so it stays with the text
    // Otherwise append to the anchor itself
    if (titleElement !== element) {
        titleElement.style.display = "inline"; // Ensure title doesn't force block to keep badge on same line
        titleElement.appendChild(container);
    } else {
        element.appendChild(container);
    }
    
    console.log(`[SecureSentinel] Badge injected inline for: ${element.hostname}`);
}

function scanLinks() {
    // Target common search result link patterns
    const links = document.querySelectorAll("a[href^='http']:not([data-sentinel-checked])");
    if (links.length > 0) console.log(`[SecureSentinel] Scanning ${links.length} potential triggers...`);

    links.forEach(link => {
        const url = link.href;
        if (url.includes(window.location.hostname) || url.length > 300) {
            link.dataset.sentinelChecked = "skipped";
            return;
        }

        chrome.runtime.sendMessage({
            type: "CHECK_RISK",
            payload: { url }
        }, (response) => {
            if (chrome.runtime.lastError) {
                console.error("[SecureSentinel] Communication Error:", chrome.runtime.lastError.message);
                return;
            }
            
            if (response && response.success) {
                console.log("[SecureSentinel] Analysis received for:", url);
                injectBadge(link, response.data.max_risk_score);
            } else {
                console.warn("[SecureSentinel] Analysis failed for:", url, response?.error);
            }
        });
    });
}

// Aggressive initial scans
[500, 1500, 3000].forEach(ms => setTimeout(scanLinks, ms));

const observer = new MutationObserver(() => {
    if (window.scanTimeout) clearTimeout(window.scanTimeout);
    window.scanTimeout = setTimeout(scanLinks, 300);
});
observer.observe(document.body, { childList: true, subtree: true });
