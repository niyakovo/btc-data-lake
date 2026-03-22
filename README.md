# 🌊 BTC Data Lake & Analyzer API

A microservice for automated data ingestion, storage, and visual analysis of historical Bitcoin (BTC/USDT) prices. Built using a Producer-Consumer architecture with an interactive File Explorer dashboard.

## 🚀 Core Features
* **ETL Pipeline (`watchdog`):** Automated monitoring of the local file storage (`/data_lake`). Upon the arrival of new `.csv` files, the system instantly parses them, handles time-series duplicates, and writes unique records to the SQLite database.
* **Interactive Dashboard:** A built-in frontend (Client-Side Rendering) that acts as a File Explorer. Users can select specific datasets from the data lake and plot them dynamically on a Chart.js graph.
* **REST API (`FastAPI`):** Fast on-demand access to file metadata and aggregated time-series data from selected batches.
* **Event-Driven WebSockets:** Real-time broadcasting of file system events. When the Producer saves a new file, all connected web clients instantly see the new file appear in their Explorer without refreshing the page.
* **Data Producer (`requests`):** An independent scraper script that automatically fetches live prices from the public Binance API and generates structured CSV files.

## 🛠 Tech Stack
* **Language:** Python 3.x
* **Backend Framework:** FastAPI, Uvicorn
* **Database & ORM:** SQLite, SQLAlchemy
* **Data Validation:** Pydantic
* **Frontend:** HTML5, JavaScript (Fetch API), Chart.js
* **Additional Libraries:** Watchdog (File System monitoring), WebSockets, Requests

---

## ⚙️ Installation & Usage

**1. Clone the repository:**
```bash
git clone [https://github.com/niyakovo/btc-data-lake.git](https://github.com/niyakovo/btc-data-lake.git)
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
*The server will start at `http://127.0.0.1:8000`.*
* **Dashboard:** Open `http://127.0.0.1:8000/dashboard` in your browser to use the Data Lake Analyzer.
* **Docs:** The interactive API documentation (Swagger UI) is available at `http://127.0.0.1:8000/docs`.

**4. Run the Binance data scraper (Producer):**
Open a **new terminal window**, activate the virtual environment, and run the scraper script:
```bash
python binance_scraper.py
```
*This script will fetch the BTC price from Binance every 10 seconds and save new `.csv` files into the `data_lake` folder, triggering the ETL pipeline and updating the Dashboard in real-time.*

---

## 📡 API Endpoints

### Frontend
* `GET /dashboard`
  * **Description:** Serves the interactive HTML interface (File Explorer & Chart).

### HTTP / REST
* `GET /api/files`
  * **Description:** Returns a sorted list of all available `.csv` files currently in the Data Lake.
* `POST /api/files/data`
  * **Description:** Accepts a JSON payload with an array of selected filenames (`{"files": ["file1.csv", "file2.csv"]}`) and returns the aggregated, time-sorted price data from those specific files.

### WebSockets
* `WS /api/btc/stream`
  * **Description:** WebSocket connection for receiving real-time file system events. 
  * **Payload Example:** `{"type": "new_file", "filename": "btc_142530.csv"}`