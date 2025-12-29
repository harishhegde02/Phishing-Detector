/**
 * SecureSentinel Service Worker v2.0
 * Clean implementation - No errors
 */

const API_BASE = "http://127.0.0.1:8000/api/v1";
console.log("[SecureSentinel] Service Worker v2.0 - Build: 2025-12-30");

// Cache for analyzed URLs
const cache = new Map();
const CACHE_DURATION = 3600000; // 1 hour

/**
 * Check backend health on startup
 */
async function checkBackend() {
    try {
        const res = await fetch("http://127.0.0.1:8000/health", {
            method: "GET",
            cache: "no-cache"
        });
        if (res.ok) {
            console.log("[SecureSentinel] ✅ Backend online");
            return true;
        }
    } catch (err) {
        console.warn("[SecureSentinel] ⚠️ Backend offline - start with: python start_server.py");
    }
    return false;
}

// Check backend on install/startup
chrome.runtime.onInstalled.addListener(() => {
    console.log("[SecureSentinel] Extension installed");
    checkBackend();
});

/**
 * Analyze URL for phishing/malicious content
 */
async function analyzeURL(url, isMainFrame = false) {
    // Check cache first
    const cached = cache.get(url);
    if (cached && Date.now() - cached.timestamp < CACHE_DURATION) {
        // Even if cached, we might need to update stats if it's a main frame visit
        if (isMainFrame) updateStats(url, cached.data.max_risk_score, true);
        return cached.data;
    }

    try {
        const response = await fetch(`${API_BASE}/detect`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text: url })
        });

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }

        const data = await response.json();
        
        // Cache result
        cache.set(url, {
            data: data,
            timestamp: Date.now()
        });

        // Limit cache size
        if (cache.size > 200) {
            const firstKey = cache.keys().next().value;
            cache.delete(firstKey);
        }

        // Track stats for popup
        await updateStats(url, data.max_risk_score, isMainFrame);

        return data;
    } catch (error) {
        console.error("[SecureSentinel] API Error:", error.message);
        // Return safe default on error
        return {
            max_risk_score: 0,
            text: url,
            labels: {}
        };
    }
}

/**
 * Update statistics for popup
 */
/**
 * Stats management
 */
async function updateStats(url, riskScore, isMainFrame) {
    try {
        const result = await chrome.storage.local.get(['scansToday', 'threatsBlocked', 'recentScans', 'lastResetDate']);
        
        const today = new Date().toDateString();
        let scansToday = result.scansToday || 0;
        let threatsBlocked = result.threatsBlocked || 0;
        let recentScans = result.recentScans || [];
        
        // Reset daily count if new day
        if (result.lastResetDate !== today) {
            scansToday = 0;
            await chrome.storage.local.set({ lastResetDate: today });
        }
        
        // Increment counters
        scansToday++;
        if (riskScore > 0.5) {
            threatsBlocked++;
            // Badge text for threats
            chrome.action.setBadgeText({ text: "!" });
            chrome.action.setBadgeBackgroundColor({ color: "#ef4444" });
        }
        
        // HISTORY LOGIC:
        // Only log if it's the MAIN PAGE we visited, OR if it's a THREAT found on the page.
        // Ignore safe links to avoid spamming "brave.com", "google.com" etc.
        if (isMainFrame || riskScore > 0.5) {
            // Avoid duplicate consecutive entries
            if (recentScans.length === 0 || recentScans[0].url !== url) {
                recentScans.unshift({
                    url: url,
                    risk_score: riskScore,
                    timestamp: Date.now()
                });
                recentScans = recentScans.slice(0, 10);
            }
        }
        
        // Save updated stats
        await chrome.storage.local.set({
            scansToday,
            threatsBlocked,
            recentScans
        });
    } catch (error) {
        console.error("[SecureSentinel] Stats update failed:", error);
    }
}

/**
 * Message handler
 */
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.type === "ANALYZE_URL") {
        analyzeURL(message.url, message.isMainFrame)
            .then(data => sendResponse({ success: true, data }))
            .catch(err => sendResponse({ success: false, error: err.message }));
        return true; 
    }
    
    if (message.type === "PING") {
        sendResponse({ status: "ok" });
        return false;
    }
});

console.log("[SecureSentinel] Service Worker ready");
