import pickle
import pandas as pd
import streamlit as st

# 1. Saved model load karo (jo notebook mein model.pkl bana tha)
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

months = ["January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"]

st.title("WasteWeave")
st.write("Order ki details daalein, model act_shrink% predict karega.")

# 2. User se inputs lo
month = st.selectbox("Month", months)
req_fabric = st.number_input("Req_Finish_Fabrics", value=10000)
allowance = st.number_input("Fabric_Allowance", value=7.0)
beam_len = st.number_input("Rec_Beam_length(yds)", value=3000.0)
shrink_allow = st.number_input("Shrink_allow", value=12.5)
warp = st.selectbox("warp_count", ["40", "50", "double"])
weft = st.number_input("weft_count", value=40)
epi = st.number_input("epi", value=110)
ppi = st.number_input("ppi", value=80)

# 3. Button dabane par prediction
if st.button("Predict"):
    # training jaisi encoding
    month_number = months.index(month)          # Ordinal: January = 0, February = 1 ...
    warp_40 = 1 if warp == "40" else 0          # One-hot: 3 columns, ek 1 baqi 0
    warp_50 = 1 if warp == "50" else 0
    warp_double = 1 if warp == "double" else 0

    # columns ka naam aur tarteeb bilkul training jaisa
    row = pd.DataFrame([[month_number, req_fabric, allowance, beam_len,
                         shrink_allow, weft, epi, ppi,
                         warp_40, warp_50, warp_double]],
                       columns=["Month", "Req_Finish_Fabrics", "Fabric_Allowance",
                                "Rec_Beam_length(yds)", "Shrink_allow", "weft_count",
                                "epi", "ppi", "warp_count_40", "warp_count_50",
                                "warp_count_double"])

    result = model.predict(row)[0]
    st.success(f"Predicted act_shrink%: {result:.2f} %")