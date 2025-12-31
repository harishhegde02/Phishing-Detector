# 🛡️ SecureSentinel

**Your Autonomous Defense Layer Against Social Engineering & Phishing Attacks**

SecureSentinel is an AI-powered security platform that protects you from phishing, social engineering, and malicious websites in real-time. It combines machine learning, heuristic analysis, and behavioral monitoring to provide multi-layered protection across your browsing experience.

---

## 🎯 What Does SecureSentinel Do?

SecureSentinel analyzes every website you visit and gives it a **Risk Score** from 0% (Safe) to 100% (Dangerous). Based on this score, you'll see:

- 🟢 **Green Badge** (0-40%): Safe to browse
- 🟡 **Yellow Badge** (41-70%): Moderate risk - be cautious
- 🔴 **Red Badge** (71-100%): High risk - dangerous site

### Where You'll See Protection:
1. **Search Results**: Badges appear next to links in Google, Brave, and other search engines
2. **Dashboard**: Monitor all browsing activity and manually block/unblock sites
3. **Real-time Blocking**: Automatic blocking of extremely dangerous sites

---

## 📦 Project Structure

```
DTLshit/
├── backend/              # FastAPI server (AI detection engine)
├── my-app/              # Next.js dashboard (activity monitoring)
├── extension-clean/     # Chrome extension (real-time protection)
├── models/              # ML models and vectorizers
├── ext_data/            # Training datasets
└── README.md           # This file
```

---

## 🚀 Quick Start

### 1. Start the Backend Server
```bash
python start_server_v3.py
```
The backend will run on `http://127.0.0.1:8002`

### 2. Start the Dashboard
```bash
cd my-app
npm run dev
```
The dashboard will open at `http://localhost:3000`

### 3. Install the Chrome Extension
1. Open Chrome and go to `chrome://extensions/`
2. Enable "Developer mode"
3. Click "Load unpacked"
4. Select the `extension-clean` folder

---

## 🛡️ The 6 Defense Layers

SecureSentinel uses a multi-layered defense approach:

### 1. 🔍 **Behavioral Baseline**
Monitors normal website behavior patterns. If a site acts suspiciously (unusual permissions, strange redirects), it's flagged.

### 2. ⏰ **Temporal Analysis**
Detects psychological pressure tactics like "Act now!" or "Your account will be deleted in 2 hours" - classic phishing strategies.

### 3. 🧠 **Neural Detection**
Core AI engine trained on 1.2M+ samples. Analyzes URL patterns, domain structure, and content in milliseconds.

### 4. 🛡️ **Cognitive Shield**
Identifies manipulation tactics:
- **Authority**: "Official FBI Warning"
- **Fear**: "Security Breach Detected"
- **Impersonation**: Fake Google/Bank login pages

### 5. ⚡ **Quantum Defense** (Heuristic Overrides)
Instant protection for known threats:
- Piracy sites (Tamilrockers, 123Movies)
- Suspicious TLDs (.xyz, .top, .tk)
- Bypass tools (proxy, unscrambler)

### 6. 🌐 **Sentinel Mesh**
Keeps your extension, backend, and dashboard perfectly synchronized.

---

## 📊 How It Works (Technical Overview)

```
User Opens Website
        ↓
Extension Sends URL to Backend
        ↓
Backend Processes:
  1. Check Whitelist (safe_patterns)
  2. Check Heuristic Overrides
  3. Check Database Blocklist
  4. Run ML Model (SGD Classifier)
        ↓
Return Risk Score (0.0 - 1.0)
        ↓
Extension Shows Badge (Green/Yellow/Red)
        ↓
Dashboard Logs Activity
```

---

## 📚 Detailed Documentation

- [Backend Documentation](./backend/README.md) - API endpoints and ML models
- [Dashboard Documentation](./my-app/README.md) - Frontend features and deployment
- [Extension Documentation](./extension-clean/README.md) - How the extension works
- [Features Deep Dive](./FEATURES.md) - Detailed explanation of all 6 defense layers
- [User Guide](./USER_GUIDE.md) - Step-by-step usage instructions
- [Developer Guide](./DEVELOPER_GUIDE.md) - Contributing and extending

---

## 🔧 Key Features

### For End Users:
- ✅ Real-time phishing detection on search results
- ✅ Visual risk indicators (colored badges)
- ✅ Manual block/unblock from dashboard
- ✅ Activity history and analytics
- ✅ Zero configuration required

### For Administrators:
- ✅ Centralized monitoring dashboard
- ✅ Activity insights and statistics
- ✅ Manual intervention (block/unblock domains)
- ✅ Export telemetry data

### For Developers:
- ✅ REST API for threat detection (`/api/v1/detect`)
- ✅ Extensible heuristic rules
- ✅ Model retraining pipeline
- ✅ Open-source ML models

---

## 🗃️ Database Schema

SecureSentinel uses SQLite for persistence:

- **scan_results**: All analyzed URLs with risk scores
- **blocked_domains**: Manually blocked domains
- **allowed_domains**: Whitelisted trusted domains

---

## 🔒 Privacy & Security

- ✅ All analysis happens locally (no third-party services)
- ✅ Database stored locally on your machine
- ✅ No personal data collected or shared
- ✅ Open-source and auditable

---

## 🐛 Troubleshooting

### Extension Not Working?
1. Reload the extension at `chrome://extensions/`
2. Check that the backend is running on port 8002
3. Clear the extension cache

### Dashboard Not Loading?
1. Verify backend is running: `http://127.0.0.1:8002/docs`
2. Check browser console for errors
3. Restart the Next.js dev server

### Backend Errors?
1. Check database path: `backend/app/sql_app.db`
2. Verify all dependencies: `pip install -r requirements.txt`
3. Check server logs for detailed errors

---

## 📄 License

This project is for educational and personal use.

---

## 🤝 Support

For issues or questions, refer to the detailed documentation in each component folder.
