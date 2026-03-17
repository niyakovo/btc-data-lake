# 🌊 BTC Data Lake & Real-Time API

A microservice for automated data ingestion, storage, and real-time broadcasting of historical Bitcoin (BTC/USDT) prices. Built using a Producer-Consumer architecture.

## 🚀 Core Features
* **ETL Pipeline (`watchdog`):** Automated monitoring of the local file storage (`/data_lake`). Upon the arrival of new `.csv` files, the system instantly parses them, handles time-series duplicates, and writes unique records to the database.
* **Storage (`SQLite` + `SQLAlchemy`):** Reliable storage of financial time-series data with proper time-based indexing for fast querying.
* **REST API (`FastAPI`):** Fast on-demand access to historical data.
* **Real-Time Stream (`WebSockets`):** Instant broadcasting of new price updates to all connected clients immediately after database insertion.
* **Data Producer (`requests`):** An independent scraper script that automatically fetches live prices from the public Binance API and generates CSV files.

## 🛠 Tech Stack
* **Language:** Python 3.x
* **Backend Framework:** FastAPI, Uvicorn
* **Database & ORM:** SQLite, SQLAlchemy
* **Data Validation:** Pydantic
* **Additional Libraries:** Watchdog (File System monitoring), WebSockets, Requests

---

## ⚙️ Installation & Usage

**1. Clone the repository:**
```bash
git clone https://github.com/niyakovo/btc-data-lake.git
cd btc-data-lake
```

**2. Create a virtual environment and install dependencies:**
```bash
python -m venv env

# Activation for Windows:
env\Scripts\activate
# Activation for Linux/MacOS:
source env/bin/activate

# Install required packages
python -m pip install -r requirements.txt
```

**3. Run the main server (Consumer / API):**
```bash
uvicorn main:app --reload
```
*The server will start at `http://127.0.0.1:8000`. The interactive API documentation (Swagger UI) is available at `http://127.0.0.1:8000/docs`.*

**4. Run the Binance data scraper (Producer):**
Open a **new terminal window**, activate the virtual environment, and run the scraper script:
```bash
python binance_scraper.py
```
*This script will fetch the BTC price from Binance every 10 seconds and save new `.csv` files into the `data_lake` folder, triggering the entire ETL pipeline.*

---

## 📡 API Endpoints

### HTTP / REST
* `GET /api/btc/history`
  * **Description:** Returns historical price data.
  * **Query Parameters:** `limit` (int, default 100) — Limits the number of returned records (ordered by most recent).

### WebSockets
* `WS /api/btc/stream`
  * **Description:** WebSocket connection for receiving real-time price updates.

#### 🧪 Quick WebSocket Testing in Browser
Open any webpage in your browser, press `F12` to open the Developer Console, and execute the following JavaScript code:
```javascript
let ws = new WebSocket("ws://127.0.0.1:8000/api/btc/stream");
ws.onopen = () => console.log("✅ Connected to BTC Stream!");
ws.onmessage = (event) => console.log("📈 New BTC Price:", JSON.parse(event.data));
```