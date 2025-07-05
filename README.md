# 🚗 CAN Signal Dashboard

A clean and interactive Streamlit app to decode and visualize CAN bus signals from `.asc` logs using `.dbc` files.  
Perfect for remote diagnostics, validation reviews, or embedded systems debugging.

---

## 📌 Features
- Upload `.asc` + `.dbc` to decode CAN messages
- Select multiple messages and signals to plot together
- Interactive, responsive Plotly charts
- Download plots as PNG images
- Helpful UI with tabs for Upload, Plot, and About sections

---

## 🧰 Stack
Built with:
- Python
- Streamlit
- Plotly
- cantools & python-can
- pandas

---

## 🚀 How to Run Locally

```bash
git clone https://github.com/MK9ei82/can-signal-dashboard.git
cd can-signal-dashboard
pip install -r requirements.txt
streamlit run main.py
