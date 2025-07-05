# app/ui.py

import streamlit as st
import pandas as pd
from app.decoder import decode_can_log
import matplotlib.pyplot as plt
import plotly.graph_objects as go

def render_ui():
    st.sidebar.subheader("📁 Upload Files")
    asc_file = st.sidebar.file_uploader("Upload .asc file", type=["asc"])
    dbc_file = st.sidebar.file_uploader("Upload .dbc file", type=["dbc"])

    if asc_file and dbc_file:
        st.sidebar.success("Both files uploaded successfully! 🎉")
        with st.spinner("🔄 Decoding CAN log..."):
            df_decoded, error_msg = decode_can_log(asc_file, dbc_file)

        if error_msg:
            st.error(error_msg)
            return None
        else:
            st.success(f"✅ Decoded {len(df_decoded)} messages.")
            signal_columns = [col for col in df_decoded.columns if '.' in col and col != 'timestamp']
            unique_messages = {col.split('.')[0] for col in signal_columns}
            st.info(f"📦 Detected {len(unique_messages)} messages, {len(signal_columns)} signals.")
            with st.expander("🔍 Preview Decoded Data"):
                st.dataframe(df_decoded.head(10))
            return df_decoded
    else:
        st.sidebar.info("Upload both files to continue.")
        return None

def render_message_signal_selector_multi(df_final):
    st.markdown("### 🔍 Select Messages and Signals to Plot")

    signal_columns = [col for col in df_final.columns if '.' in col and col != 'timestamp']

    # Build message-to-signal mapping
    message_to_signals = {}
    for col in signal_columns:
        msg, signal = col.split('.', 1)
        message_to_signals.setdefault(msg, []).append(signal)

    # Select multiple messages
    selected_msgs = st.multiselect("📨 Select Messages", sorted(message_to_signals.keys()))

    # Flatten signals from selected messages
    selected_signals = []
    for msg in selected_msgs:
        for sig in message_to_signals.get(msg, []):
            selected_signals.append(f"{msg}.{sig}")

    # Let user optionally filter down signals
    final_signals = st.multiselect("📈 Select Signals to Plot", selected_signals)

    return final_signals

import io

def plot_multiple_signals(df, signal_list):
    st.markdown("### 📊 Multi-Signal Plot")

    if df.empty or not signal_list:
        st.warning("⚠️ No valid data to plot.")
        return

    fig = go.Figure()

    for signal in signal_list:
        if signal not in df.columns:
            st.warning(f"⚠️ Signal '{signal}' not found in DataFrame.")
            continue

        signal_series = df[['timestamp', signal]].dropna()
        if signal_series.empty:
            st.warning(f"⚠️ Signal '{signal}' has no valid data.")
            continue

        # Extract .value if NamedSignalValue
        try:
            if isinstance(signal_series[signal].iloc[0], object):
                signal_series[signal] = signal_series[signal].apply(lambda x: x.value)
        except:
            pass

        fig.add_trace(go.Scatter(
            x=signal_series['timestamp'],
            y=signal_series[signal],
            mode='lines+markers',
            name=signal,
            line=dict(width=2),
            marker=dict(size=4)
        ))

    fig.update_layout(
        title="Selected Signals Over Time",
        xaxis_title=dict(text="Timestamp (s)", font=dict(size=14, family="Arial Black")),
        yaxis_title=dict(text="Signal Value", font=dict(size=14, family="Arial Black")),
        template="plotly_white",
        height=500,
        margin=dict(l=60, r=40, t=60, b=60),
        hoverlabel=dict(
            font_size=12,
            font_family="Arial",
            namelength=-1
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    st.plotly_chart(fig, use_container_width=True)