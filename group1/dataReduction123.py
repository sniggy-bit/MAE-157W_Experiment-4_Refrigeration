import numpy as np
import plotly.express as px
from CoolProp.CoolProp import PropsSI

import refrigerationMain

df_axv, df_txv, df_ctv = refrigerationMain.df_axv, refrigerationMain.df_txv, refrigerationMain.df_ctv

# Filter AXV at 15 psig
axv15 = df_axv[df_axv["Suction Pressure (psig)"] == 15].iloc[0]

# Define the four cycle state points
state_points = {
    "Evap Inlet":  ("T2 [K]", "P2 [Pa]"),
    "Evap Outlet": ("T3 [K]", "P2 [Pa]"),
    "Cond Inlet":  ("T5 [K]", "P1 [Pa]"),
    "Cond Outlet": ("T4 [K]", "P3 [Pa]")
}

# Compute h (kJ/kg) and s (kJ/kg K) at each point
cycle = {}
for name, (Tcol, Pcol) in state_points.items():
    T = axv15[Tcol]
    P = axv15[Pcol]
    h = PropsSI("H", "T", T, "P", P, "R12") / 1000
    s = PropsSI("S", "T", T, "P", P, "R12") / 1000
    cycle[name] = {"T": T, "P": P, "h": h, "s": s}

# Close cycle loop
labels = list(cycle.keys()) + ["Evap Inlet"]
cycle_s = [cycle[l]["s"] for l in labels]
cycle_h = [cycle[l]["h"] for l in labels]
cycle_T = [cycle[l]["T"] for l in labels]

# Generate saturation dome
T_min, T_max = min(cycle_T)-20, max(cycle_T)+20
T_dom = np.linspace(T_min, T_max, 300)
sL = [PropsSI("S","T",T,"Q",0,"R12")/1000 for T in T_dom]
hL = [PropsSI("H","T",T,"Q",0,"R12")/1000 for T in T_dom]
sV = [PropsSI("S","T",T,"Q",1,"R12")/1000 for T in T_dom]
hV = [PropsSI("H","T",T,"Q",1,"R12")/1000 for T in T_dom]

# Mollier (h-s) diagram
fig_hs = go.Figure()
fig_hs.add_trace(go.Scatter(x=sL, y=hL, mode="lines", name="Sat. Liquid", line=dict(dash="dash")))
fig_hs.add_trace(go.Scatter(x=sV, y=hV, mode="lines", name="Sat. Vapor", line=dict(dash="dash")))
fig_hs.add_trace(go.Scatter(x=cycle_s, y=cycle_h, mode="lines+markers", name="Cycle",
                            marker=dict(symbol="circle", size=8), line=dict(color="black")))
fig_hs.update_layout(
    title="Mollier Diagram (h–s) for AXV @ 15 psig",
    xaxis_title="Entropy [kJ/kg·K]", yaxis_title="Enthalpy [kJ/kg]",
    legend=dict(x=0.7, y=0.2)
)
fig_hs.show()

# Temperature–Entropy (T-s) diagram
fig_ts = go.Figure()
fig_ts.add_trace(go.Scatter(x=sL, y=T_dom, mode="lines", name="Sat. Liquid", line=dict(dash="dash")))
fig_ts.add_trace(go.Scatter(x=sV, y=T_dom, mode="lines", name="Sat. Vapor", line=dict(dash="dash")))
fig_ts.add_trace(go.Scatter(x=cycle_s, y=cycle_T, mode="lines+markers", name="Cycle",
                           marker=dict(symbol="circle", size=8), line=dict(color="black")))

# Mark coolant (air) inlet temperature (T10)
T_cool = axv15["T10 [K]"]
fig_ts.add_trace(go.Scatter(
    x=[min(sL), max(sL)], y=[T_cool, T_cool],
    mode="lines", name="Coolant Inlet T", line=dict(color="green", dash="dot")
))

fig_ts.update_layout(
    title="T–s Diagram for AXV @ 15 psig",
    xaxis_title="Entropy [kJ/kg·K]", yaxis_title="Temperature [K]",
    legend=dict(x=0.7, y=0.2)
)
fig_ts.show()