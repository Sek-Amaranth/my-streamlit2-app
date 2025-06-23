import re
import requests

def extract_data_block(text, board_name):
    # แยกเฉพาะบล็อกของบอร์ดนี้
    pattern = rf"{board_name}(.*?)(MDB\d+|EMDB|$)"
    match = re.search(pattern, text, re.DOTALL)
    block = match.group(1) if match else ""

    def get(pattern):
        match = re.search(pattern, block)
        return match.group(1).strip() if match else ""

    return {
        "board": board_name,
        "voltageL1": get(r"Voltage effective L1 ([\d\.]+) V"),
        "voltageL2": get(r"Voltage effective L2 ([\d\.]+) V"),
        "voltageL3": get(r"Voltage effective L3 ([\d\.]+) V"),
        "voltL2L1": get(r"Voltage effective L2-L1 ([\d\.]+) V"),
        "voltL3L2": get(r"Voltage effective L3-L2 ([\d\.]+) V"),
        "voltL1L3": get(r"Voltage effective L1-L3 ([\d\.]+) V"),
        "currL1": get(r"Current effective L1 ([\d\.]+) A"),
        "currL2": get(r"Current effective L2 ([\d\.]+) A"),
        "currL3": get(r"Current effective L3 ([\d\.]+) A"),
        "currSum": get(r"Current effective Sum L1-L3 ([\d\.]+) A"),
        "powerL1": get(r"Active Power L1 ([\d\.]+) k[Ww]"),
        "powerL2": get(r"Active Power L2 ([\d\.]+) k[Ww]"),
        "powerL3": get(r"Active Power L3 ([\d\.]+) k[Ww]"),
        "powerSum": get(r"Active Power Sum L1-L3 ([\d\.]+) k[Ww]"),
        "freq": get(r"Frequency ([\d\.]+) Hz"),
        "energySum": get(r"Active Energy Sum L1-L3 ([\d\.]+) G[Ww]"),
        "consumedEnergy": get(r"Consumed Active Energy Sum .*? ([\d\.]+) G[Ww]h?")
    }


# 👉 ใช้ใน Streamlit
import streamlit as st
st.title("📊 MDB Data Extractor")

raw_text = st.text_area("Paste data here", height=300)

if st.button("📤 Send to Google Sheets"):
    for board in ["MDB1", "EMDB", "MDB2"]:
        data = extract_data_block(raw_text, board)
        response = requests.post(
            "https://script.google.com/macros/s/AKfycbxrNH8T-D-Fkwphrpy9TQQfJCxPsP7Du-bIbztjgiLVt6QXZEWxX7GCMKOxD8U_PTgitQ/exec",  # 🔁 ใส่ URL Web App ที่ได้จาก Apps Script
            json=data
        )
        if response.status_code == 200:
            st.success(f"✅ {board} sent to Google Sheets")
        else:
            st.error(f"❌ Failed to send {board}")
