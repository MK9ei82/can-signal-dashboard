# 🚗 CAN Signal Dashboard
This Streamlit app visualizes and analyzes decoded signals from CAN logs. Upload your `.asc` and `.dbc` files to:

- Decode messages and signals
- Select multiple signals from different messages
- Plot and compare signals over time
- Export plots as PNG

## 💡 Use Case
Useful for embedded software engineers, test/validation teams, and diagnostics engineers who need to analyze CAN data remotely or without licensed tools.

## 📦 Built With
- Python
- Streamlit
- cantools
- python-can
- Plotly

## 🏁 How to Run

```bash
git clone https://github.com/your-username/can-dashboard.git
cd can-dashboard
pip install -r requirements.txt
streamlit run main.py
