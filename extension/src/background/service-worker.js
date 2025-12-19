const API_BASE_URL = "http://localhost:8000/api/v1";

/**
 * Strips sensitive query parameters from URLs before analysis
 */
function sanitizeURL(url) {
    try {
        const urlObj = new URL(url);
        return `${urlObj.hostname}${urlObj.pathname}`;
    } catch (e) {
        return url;
    }
}

/**
 * Logic for risk analysis with persistent caching
 */
async function handleRiskCheck(payload, sendResponse) {
    const { text, url } = payload;
    const sanitizedUrl = url ? sanitizeURL(url) : null;

    if (sanitizedUrl) {
        const cached = await chrome.storage.local.get(sanitizedUrl);
        if (cached[sanitizedUrl]) {
            console.log("[SecureSentinel] Cache hit:", sanitizedUrl);
            sendResponse({ success: true, data: cached[sanitizedUrl] });
            return;
        }
    }

    try {
        console.log("[SecureSentinel] Fetching analysis for:", sanitizedUrl || "text");
        const response = await fetch(`${API_BASE_URL}/analyze`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text: text || url }),
        });

        if (!response.ok) throw new Error(`API error: ${response.status}`);

        const data = await response.json();
        console.log("[SecureSentinel] API Success:", data.max_risk_score);
        
        if (sanitizedUrl) {
            await chrome.storage.local.set({ 
                [sanitizedUrl]: { ...data, timestamp: Date.now() } 
            });
        }

        sendResponse({ success: true, data });
    } catch (error) {
        console.error("[SecureSentinel] Backend unreachable:", error);
        sendResponse({ success: false, error: error.message });
    }
}

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    console.log("[SecureSentinel] Msg:", message.type);

    if (message.type === "CHECK_RISK") {
        handleRiskCheck(message.payload, sendResponse);
        return true; 
    }

    if (message.type === "GET_CACHED_RESULT") {
        const sanitized = sanitizeURL(message.payload.url);
        chrome.storage.local.get(sanitized).then(result => {
            sendResponse({ result: result[sanitized] || null });
        });
        return true;
    }
});

console.log("[SecureSentinel] Service Worker Active.");
