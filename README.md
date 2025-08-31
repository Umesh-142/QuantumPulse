# ⚛️ Quantum Data Generator

<p align="center">
  <img src="[https://via.placeholder.com/1200x300?text=Quantum+Data+Generator](https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.nist.gov%2Fcybersecurity%2Fwhat-quantum-cryptography&psig=AOvVaw2V6gfX5lto4T8SJBW_mLSi&ust=1756727599969000&source=images&cd=vfe&opi=89978449&ved=0CBUQjRxqFwoTCID--M3-tI8DFQAAAAAdAAAAABAE)" alt="Banner: Quantum Data Generator">
</p>

<p align="center">
  AI-generated synthetic quantum datasets with a professional, responsive UI. Configure Rabi oscillations, T1/T2 decay, and Bell correlations; visualize, validate, and export JSON/CSV.
</p>

<p align="center">
  <!-- Tech Badges -->
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/FastAPI-0.108+-009688?style=for-the-badge&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/Streamlit-1.29+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" />
  <img src="https://img.shields.io/badge/Plotly-5.18-3F4F75?style=for-the-badge&logo=plotly&logoColor=white" />
  <img src="https://img.shields.io/badge/NumPy-1.26-013243?style=for-the-badge&logo=numpy&logoColor=white" />
  <img src="https://img.shields.io/badge/Pandas-2.1-150458?style=for-the-badge&logo=pandas&logoColor=white" />
</p>

<p align="center">
  <a href="#overview">Overview</a> •
  <a href="#features">Features</a> •
  <a href="#quickstart">Quickstart</a> •
  <a href="#usage">Usage</a> •
  <a href="#api">API</a> •
  <a href="#screenshots">Screenshots</a> •
  <a href="#troubleshooting">Troubleshooting</a> •
  <a href="#roadmap">Roadmap</a> •
  <a href="#contributing">Contributing</a> •
  <a href="#license">License</a>
</p>

---

## 🚀 Overview

**Quantum Data Generator** is a **FastAPI + Streamlit** application that produces realistic synthetic quantum experiment datasets. It simulates Rabi oscillations, T1/T2 decay, and Bell correlations with configurable noise, shot counts, and time grids. Results are visualized with interactive **Plotly charts** and exported in **JSON/CSV** formats — complete with metadata and reproducibility.

**Use Cases:**

* 📚 Teaching quantum concepts without hardware
* 🤖 Generating datasets for ML/QML experiments
* 🔍 Validating analysis pipelines with controlled noise
* ⚡ Rapid prototyping of experimental UIs

---

## ✨ Features

* **🔬 Experiments**

  * Rabi Oscillations (two-level system with decay)
  * T1/T2 Decay (relaxation + coherence)
  * Bell State Correlations (CHSH violation, entanglement realism)

* **🎛️ Controls**

  * Shots, noise, time range, step size, drive frequency, θ (Bell), random seed

* **📊 Visualizations**

  * Interactive plots for time-series, counts, correlations

* **✅ Validation**

  * Fit/error metrics (MSE, estimated periods, CHSH value)

* **💾 Export**

  * JSON (with metadata)
  * CSV (flattened measurement data)

* **🖥️ UX**

  * Responsive Streamlit UI, presets (low/high noise), tooltips, progress indicators

* **♻️ Reproducibility**

  * Parameters + seed echoed back in all responses

---

## 🛠️ Tech Stack

* **Backend**: FastAPI, NumPy
* **Frontend**: Streamlit, Plotly, HTML/CSS
* **Data**: Pandas (tabular views & CSV export)
* **Runtime**: Python 3.11+

---

## 📂 Project Structure

```bash
quantum-data-generator/
├── backend/
│   ├── main.py              # FastAPI server
│   ├── quantum_simulator.py # Physics-inspired data generators
│   └── requirements.txt
├── frontend/
│   ├── app.py               # Streamlit UI
│   ├── static/
│   │   ├── style.css        # (Optional) Extra styles
│   │   └── script.js        # (Optional) Extra scripts
│   └── requirements.txt
└── README.md
```

---

## ⚡ Quickstart

### 1️⃣ Clone the repo

```bash
git clone https://github.com/yourusername/quantum-data-generator.git
cd quantum-data-generator
```

### 2️⃣ Backend (FastAPI)

```bash
cd backend
python -m venv venv
```

**Activate venv**

* Windows: `venv\Scripts\activate`
* macOS/Linux: `source venv/bin/activate`

```bash
pip install -r requirements.txt
python main.py
```

* API: [http://localhost:8000](http://localhost:8000)
* Docs: [http://localhost:8000/docs](http://localhost:8000/docs)

### 3️⃣ Frontend (Streamlit)

```bash
cd ../frontend
python -m venv venv
```

**Activate venv**

* Windows: `venv\Scripts\activate`
* macOS/Linux: `source venv/bin/activate`

```bash
pip install -r requirements.txt
streamlit run app.py
```

* App: [http://localhost:8501](http://localhost:8501)

---

## 🎮 Usage

1. Choose experiment type (Rabi / T1-T2 / Bell)
2. Configure parameters (noise, shots, frequency/θ, seed, etc.)
3. Click **Generate** to synthesize data
4. Explore **plots, metrics, CHSH value** (Bell)
5. Export as **JSON or CSV**

👉 Tip: For Bell violation (CHSH > 2), try `noise ~0.02–0.05` with `shots ≥ 10k`.

---

## 🔗 API Endpoints

**Base URL:** `http://localhost:8000`

* `GET /` → Health check
* `POST /generate/rabi`
* `POST /generate/decay`
* `POST /generate/bell`

**All responses include:**

```json
{
  "experiment_type": "...",
  "parameters": {...},
  "measurements": [...],
  "statistics": {...},
  "metadata": {...}
}
```

---

## 🖼️ Screenshots

<p align="center">
  <img src="https://via.placeholder.com/900x450?text=Main+Interface" alt="Main UI" />
</p>

<p align="center">
  <img src="https://via.placeholder.com/900x450?text=Rabi+Oscillation+Visualization" alt="Rabi Results" />
</p>

<p align="center">
  <img src="https://via.placeholder.com/900x450?text=Bell+Correlation+and+CHSH" alt="Bell Results" />
</p>

> Replace placeholders with actual app screenshots.

---

## 🛠️ Troubleshooting

* **Python 3.12 distutils error** → Prefer Python 3.11 or update `setuptools`
* **Streamlit `use_container_width` warning** → Use `width='stretch'`
* **Frontend cannot reach backend** → Ensure FastAPI is running on port 8000
* **Data mismatch** → Inspect `/docs` OpenAPI schema

---

## 🗺️ Roadmap

* 🤖 LLM Assistant

  * Natural-language parameter suggestions
  * Auto-generated experiment summaries
* 🔬 New Experiments (Ramsey, randomized benchmarking)
* 📂 Dataset gallery with presets and versioning

---

## 🤝 Contributing

1. Fork the repo
2. Create a feature branch

   ```bash
   git checkout -b feat/amazing-idea
   ```
3. Commit changes

   ```bash
   git commit -m "feat: add amazing idea"
   ```
4. Push the branch

   ```bash
   git push origin feat/amazing-idea
   ```
5. Open a Pull Request 🚀

---

## 📜 License

MIT License — see [LICENSE](LICENSE).

---

## 🙌 Acknowledgments

* [FastAPI](https://fastapi.tiangolo.com), [Streamlit](https://streamlit.io), [Plotly](https://plotly.com), [NumPy](https://numpy.org), [Pandas](https://pandas.pydata.org)
* Educators & researchers promoting open quantum tooling
* Built with ❤️ for GenAI coursework and demos
