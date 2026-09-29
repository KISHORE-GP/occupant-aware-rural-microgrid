# Occupant-Aware Demand-Response Planner for a Rural Microgrid

An occupant-aware demand-response (DR) planning system for rural microgrids that balances peak-demand reduction, electricity tariffs, and microgrid capacity against occupant comfort ranges, opt-out choices, essential safety loads, and social equity.

---

## 🚀 Key Features

- **Two Objective Modes**: Mode 1 — Peak Reduction Mode (prioritizes peak demand shaving) vs Mode 2 — Comfort Mode (prioritizes thermal comfort and minimal disruption).
- **Explicit Hard & Soft Constraints**: Protects essential safety loads (HC-1), respects active occupant opt-outs (HC-2), enforces thermal safe bounds (HC-3), and penalizes comfort drift and load shift inconvenience.
- **Simple Baseline Comparison**: Benchmark naive controller that curtails flexible loads during peak hours without occupant awareness.
- **Fail-Safe Fallback Engine**: Detects missing occupancy telemetry and switches to `FALLBACK MODE — Conservative Operation`.
- **Authorised Operator Override**: Allows operators to approve, reject, or override recommendations with role-based logging.
- **Multi-Lingual UI**: Native dictionary-based language switcher supporting **English** and **தமிழ் (Tamil)**.

---

## 📂 File Structure

The project strictly follows a minimal 8-file structure:

```text
project/
├── app.py              # Streamlit dashboard interface
├── planner.py          # Planning decision logic, baseline, explanations & fallback
├── constraints.py      # Hard & soft constraints validation & penalty logic
├── data.csv            # Primary 30-day synthetic microgrid dataset
├── experiment.ipynb    # Experimental evaluation notebook
├── requirements.txt    # Minimal project dependencies
├── README.md           # Instructions and documentation
└── docs/
    └── final_report.md # Comprehensive final project report & presentation outline
```

---

## 💻 Installation & Setup

1. Clone or open the repository.
2. Install minimal dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## ⚡ How to Run the Application

Launch the Streamlit interactive dashboard:

```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`.

---

## 🧪 How to Run the Experiment Notebook

Launch Jupyter and run the evaluation notebook:

```bash
jupyter notebook experiment.ipynb
```

---

## 🔄 Example Operational Workflow

1. Open `app.py` dashboard.
2. View current microgrid state (Total demand, Peak demand, Tariff, Occupancy, Essential vs Flexible load breakdown).
3. Select Objective Mode: **Peak Reduction Mode** or **Comfort Mode**.
4. Review recommended load actions (`RUN`, `SHIFT`, `CURTAIL`, `DO NOTHING`) with plain-language explanations.
5. Test failure scenarios (Missing Occupancy -> Fallback mode activation; Active Opt-Out -> Exclusion; Comfort Conflict -> Bound protection).
6. Perform operator overrides if local operational changes are required.
7. Compare Baseline vs Occupant-Aware results in the comparative metrics table.
