import refrigerationMain
from CoolProp.CoolProp import PropsSI
import pandas as pd

### DATA REDUCTION 4 ###########################################################################

df_axv = refrigerationMain.df_axv
df_txv = refrigerationMain.df_txv

results = []

# AXV @ 15 psig
row_axv = df_axv[df_axv["Suction Pressure (psig)"] == 15].iloc[0]

T2, T3 = row_axv["T2 [K]"], row_axv["T3 [K]"]
P2, P3 = row_axv["P2 [Pa]"], row_axv["P3 [Pa]"]
m_dot = row_axv["Flow Rate [lb/min]"] * 0.453592 / 60  # lb/min to kg/s
W_dot = row_axv["Comp [A]"] * row_axv["Voltage [V]"]   # Electrical power

h2 = PropsSI("H", "T", T2, "P", P2, "R12")
h3 = PropsSI("H", "T", T3, "P", P3, "R12")

Q_in = m_dot * (h3 - h2)
COP = (h3 - h2) / (W_dot / m_dot)

results.append({
    "Expander": "AXV",
    "Condition": "15 psig",
    "COP": round(COP, 2),
    "Refrigeration Capacity (kW)": round(Q_in / 1000, 3)
})

# TXV Configs
for i, label in enumerate(["Both Fans High", "Evap High, Cond Low"]):
    row_txv = df_txv.iloc[i]

    T2, T3 = row_txv["T2 [K]"], row_txv["T3 [K]"]
    P2, P3 = row_txv["P2 [Pa]"], row_txv["P3 [Pa]"]
    m_dot = row_txv["Flow Rate [lb/min]"] * 0.453592 / 60
    W_dot = row_txv["Comp [A]"] * row_txv["Voltage [V]"]

    h2 = PropsSI("H", "T", T2, "P", P2, "R12")
    h3 = PropsSI("H", "T", T3, "P", P3, "R12")

    Q_in = m_dot * (h3 - h2)
    COP = (h3 - h2) / (W_dot / m_dot)

    results.append({
        "Expander": "TXV",
        "Condition": label,
        "COP": round(COP, 2),
        "Refrigeration Capacity (kW)": round(Q_in / 1000, 3)
    })

# Display Results
df_results = pd.DataFrame(results)
print("\n### COP and Refrigeration Capacity for AXV & TXV (Data Reduction 4) ###")
print(df_results.to_string(index=False))

### DATA REDUCTION 5 ###########################################################################

superheat_results = []

# Loop through test conditions
for i, label in enumerate(["Both Fans High", "Evap High, Cond Low"]):
    row_txv = df_txv.iloc[i]
    
    T3 = row_txv["T3 [K]"]           # Actual temp after evaporator
    P3 = row_txv["P3 [Pa]"]          # Suction pressure

    # Get saturation temperature at suction pressure (saturated vapor)
    T_sat = PropsSI("T", "P", P3, "Q", 1, "R12")

    # Superheat = actual vapor temp - saturation temp
    superheat = T3 - T_sat

    superheat_results.append({
        "Condition": label,
        "T3 (K)": round(T3, 2),
        "T_sat (K)": round(T_sat, 2),
        "Superheat (K)": round(superheat, 2)
    })

# Display table
df_superheat = pd.DataFrame(superheat_results)
print("\n### TXV Superheat Results (Data Reduction 5) ###")
print(df_superheat.to_string(index=False))

### DATA REDUCTION 6 ###########################################################################

import plotly.express as px

axv_results = []

# Loop through each pressure value
for p_suction in sorted(df_axv["Suction Pressure (psig)"].unique()):
    row = df_axv[df_axv["Suction Pressure (psig)"] == p_suction].iloc[0]

    T2, T3 = row["T2 [K]"], row["T3 [K]"]
    P2, P3 = row["P2 [Pa]"], row["P3 [Pa]"]
    m_dot = row["Flow Rate [lb/min]"] * 0.453592 / 60
    W_dot = row["Comp [A]"] * row["Voltage [V]"]

    try:
        h2 = PropsSI("H", "T", T2, "P", P2, "R12")
        h3 = PropsSI("H", "T", T3, "P", P3, "R12")

        Q_in = m_dot * (h3 - h2)
        COP = (h3 - h2) / (W_dot / m_dot)

        axv_results.append({
            "Suction Pressure (psig)": p_suction,
            "COP": round(COP, 2),
            "Refrigeration Capacity (kW)": round(Q_in / 1000, 3)
        })
    
    except Exception as e:
        print(f"Error at {p_suction} psig: {e}")
        continue

# Convert results to DataFrame
df_axv_results = pd.DataFrame(axv_results)

# Print results table
print("\n### COP and Refrigeration Capacity vs. Suction Pressure (AXV) ###")
print(df_axv_results.to_string(index=False))

# Plot COP vs suction pressure
fig_cop = px.scatter(df_axv_results, x="Suction Pressure (psig)", y="COP",
                     title="COP vs. Suction Pressure (AXV)",
                     labels={"COP": "Coefficient of Performance"})
fig_cop.update_traces(mode="lines+markers")
fig_cop.show()

# Plot RC vs suction pressure
fig_qin = px.scatter(df_axv_results, x="Suction Pressure (psig)", y="Refrigeration Capacity (kW)",
                     title="Refrigeration Capacity vs. Suction Pressure (AXV)",
                     labels={"Refrigeration Capacity (kW)": "Cooling Capacity (kW)"})
fig_qin.update_traces(mode="lines+markers")
fig_qin.show()