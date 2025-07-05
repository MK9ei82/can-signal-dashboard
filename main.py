import streamlit as st
from app.ui import (
    render_ui,
    render_message_signal_selector_multi,
    plot_multiple_signals
)

st.set_page_config(page_title="AutoSignalViz", layout="wide")

def main():
    st.title("🚗 AutoSignalViz")
    with st.expander("ℹ️ About this App", expanded=False):
        st.markdown("""
        This dashboard helps engineers analyze CAN logs by:
        - Uploading `.asc` (CAN log) and `.dbc` (database) files
        - Decoding CAN messages and signals
        - Selecting and plotting multiple signals for comparison
        - Exporting signal plots as PNG images

        🚀 Built for cloud-accessible debugging, visualization, sharing without tool/license dependency.
        """)
        st.markdown("👩‍💻 **Co-Created with AI by Komal Krishna Maddali**")


    # 👇 Create tabs
    tabs = st.tabs(["📁 Upload & Decode", "📈 Plot Signals", "ℹ️ About"])

    with tabs[0]:
        st.markdown("Upload your `.asc` CAN log and corresponding `.dbc` file to decode signals.")
        st.session_state['df_final'] = render_ui()  # ⬅️ Store in session state

    with tabs[1]:
        df_final = st.session_state.get('df_final')
        if df_final is not None:
            selected_signals = render_message_signal_selector_multi(df_final)
            if selected_signals:
                plot_multiple_signals(df_final, selected_signals)
        else:
            st.warning("Please upload files and decode the log in the first tab.")

    with tabs[2]:
        st.markdown("""
        ### ℹ️ About This Tool
        This dashboard allows you to:
        - Upload CAN log files (`.asc`), matching database files (`.dbc`)
        - Decode raw CAN messages into meaningful signals
        - Select and visualize multiple signals on a time-series plot
        - Export the plots as PNG images

        Co-Created with AI using Python, Streamlit, Plotly. Ideal for quick diagnostics, validation reviews, analysis.
        """)

if __name__ == "__main__":
    main()
