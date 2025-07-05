# app/decoder.py

import cantools
import can
import pandas as pd
import io
import tempfile

def decode_can_log(asc_file, dbc_file):
    # Save DBC file to temp path
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".dbc") as temp_dbc:
            temp_dbc.write(dbc_file.read())
            dbc_path = temp_dbc.name
        db = cantools.database.load_file(dbc_path)
    except Exception as e:
        return None, f"❌ Failed to load DBC: {e}"

    # Read ASC log
    try:
        raw_msgs = []
        asc_text = io.StringIO(asc_file.read().decode("utf-8"))
        for msg in can.ASCReader(asc_text):
            raw_msgs.append({
                'timestamp': msg.timestamp,
                'arbitration_id': msg.arbitration_id,
                'data': msg.data.hex()
            })
        if not raw_msgs:
            return None, "⚠️ No messages found in ASC log."

        df_raw = pd.DataFrame(raw_msgs)
    except Exception as e:
        return None, f"❌ Failed to read ASC log: {e}"

    # Decode using DBC
    decoded_rows = []
    for _, row in df_raw.iterrows():
        try:
            raw_data = bytes.fromhex(row['data'])
            msg_def = db.get_message_by_frame_id(row['arbitration_id'])
            decoded = msg_def.decode(raw_data)
            decoded_prefixed = {f"{msg_def.name}.{k}": v for k, v in decoded.items()}
            decoded_prefixed['timestamp'] = row['timestamp']
            decoded_rows.append(decoded_prefixed)
        except Exception:
            continue

    if not decoded_rows:
        return None, "⚠️ No signals were decoded from the log."

    df_decoded = pd.DataFrame(decoded_rows)
    return df_decoded, None
