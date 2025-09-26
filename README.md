
# 🌱 GreenTrack: CO₂ Emissions Tracker with Blockchain

GreenTrack is an interactive **Streamlit app** that helps visualize **global CO₂ emissions**,  
provides **eco-recommendations**, and records emission data on a simple **blockchain** for transparency.  
You can also **download blockchain records** as CSV or JSON for further analysis.

---

## 🚀 Features
- 📊 Select a **country** and **year** to view CO₂ emissions from the dataset.
- 🔗 Add records to a blockchain (with timestamps + cryptographic hash).
- 🪙 Earn tokens when CO₂ emissions decrease compared to previous records.
- 🌍 Eco-friendly recommendations based on CO₂ levels.
- 🧾 View blockchain history directly in the app.
- 📥 **Export blockchain records** as CSV or JSON.

---

## 🛠️ Tech Stack
- **Python 3.9+**
- [Streamlit](https://streamlit.io/) — interactive dashboard
- **Pandas** — data processing
- **Hashlib** — cryptographic hashing (blockchain)
- **Time / JSON** — timestamps and export

---

## 📂 Project Structure
- │── app.py # Main Streamlit application
- │── global_co2_emissions.csv # Dataset file (must be downloaded separately)
- │── requirements.txt # Python dependencies
- │── README.md # Project documentation
- │── .gitignore # Ignore unnecessary files


## ▶️ Usage
- **Run the app with**
- streamlit run app.py

