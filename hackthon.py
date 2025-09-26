import streamlit as st
import pandas as pd
import hashlib
import time
import json

# ----------------------------
# Blockchain classes
# ----------------------------

class Block:
    def __init__(self, data, previous_hash):
        self.timestamp = time.time()
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = f"{self.timestamp}{self.data}{self.previous_hash}".encode()
        return hashlib.sha256(block_string).hexdigest()


class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block("Genesis Block", "0")

    def add_block(self, data):
        previous_hash = self.chain[-1].hash
        block = Block(data, previous_hash)
        self.chain.append(block)

    def get_last_co2(self):
        for block in reversed(self.chain):
            if isinstance(block.data, dict) and "co2_kg" in block.data:
                return block.data["co2_kg"]
        return 0

    def get_chain(self):
        return [{
            "Index": i,
            "Timestamp": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(block.timestamp)),
            "Data": block.data,
            "Hash": block.hash,
            "Previous Hash": block.previous_hash
        } for i, block in enumerate(self.chain)]


# ----------------------------
# Eco recommendations
# ----------------------------

def eco_recommendations(co2):
    tips = []
    if co2 > 1000:
        tips.append("Your emissions are quite high. Consider reducing travel or using renewable energy.")
    elif co2 > 500:
        tips.append("Try to optimize your energy use and consider eco-friendly transport options.")
    else:
        tips.append("Great job! Keep maintaining low emissions.")
    return tips


# ----------------------------
# Load dataset
# ----------------------------

@st.cache_data
def load_data():
    df = pd.read_csv('global_co2_emissions.csv')  # update path as needed
    return df


df = load_data()

# ----------------------------
# Streamlit UI
# ----------------------------

st.title("🌱 GreenTrack with Global CO₂ Emissions Dataset")

countries = df['Country'].unique()
selected_country = st.selectbox("Select Country", countries)

years = df['Year'].unique()
selected_year = st.selectbox("Select Year", years)

record = df[(df['Country'] == selected_country) & (df['Year'] == selected_year)]

if record.empty:
    st.warning("No data available for this selection.")
else:
    co2_emissions = float(record['Total CO2 Emissions (kt)'].values[0])
    co2_kg = co2_emissions * 1000  # kt → kg

    st.write(f"CO₂ Emissions for {selected_country} in {selected_year}: *{co2_kg:,.0f} kg*")

    if 'blockchain' not in st.session_state:
        st.session_state.blockchain = Blockchain()

    if st.button("Add Record to Blockchain"):
        last_co2 = st.session_state.blockchain.get_last_co2()
        reduction = max(last_co2 - co2_kg, 0)
        tokens = reduction * 0.01

        data = {
            "country": selected_country,
            "year": selected_year,
            "co2_kg": co2_kg,
            "tokens_earned": tokens,
            "timestamp": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        }
        st.session_state.blockchain.add_block(data)
        st.success(f"Record added! Tokens earned: {tokens:.2f}")

    # ----------------------------
    # Eco tips
    # ----------------------------
    st.subheader("Eco Recommendations")
    for tip in eco_recommendations(co2_kg):
        st.write(f"• {tip}")

    # ----------------------------
    # Blockchain Records
    # ----------------------------
    st.subheader("Blockchain Records")
    chain = st.session_state.blockchain.get_chain()
    for block in chain:
        st.write(block)

    # ----------------------------
    # Download Blockchain Records
    # ----------------------------
    st.subheader("📥 Export Blockchain Records")

    # Convert to DataFrame (for CSV)
    df_chain = pd.DataFrame(chain)

    # CSV download
    csv_data = df_chain.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Download as CSV",
        data=csv_data,
        file_name="blockchain_records.csv",
        mime="text/csv"
    )

    # JSON download
    json_data = json.dumps(chain, indent=4)
    st.download_button(
        label="⬇️ Download as JSON",
        data=json_data,
        file_name="blockchain_records.json",
        mime="application/json"
    )
