import numpy as np
import plotly.graph_objects as go
from CoolProp.CoolProp import PropsSI

import refrigerationMain

df_axv, df_txv, df_ctv = refrigerationMain.df_axv, refrigerationMain.df_txv, refrigerationMain.df_ctv

# Filter AXV at 15 psig
axv15 = df_axv[df_axv["Suction Pressure (psig)"] == 15].iloc[0]

# Define the four cycle state points
# 1: before throttling valve
# 2: evap inlet
# 3: evap outlet
# 4: cond inlet
state_points = {
    "Cond Outlet": ("T1 [K]", "P1 [Pa]"),
    "Evap Inlet":  ("T2 [K]", "P2 [Pa]"),
    "Evap Outlet": ("T4 [K]", "P3 [Pa]"),
    "Cond Inlet":  ("T5 [K]", "P4 [Pa]")
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
labels = list(cycle.keys()) + ["Cond Outlet"]
cycle_s = [cycle[l]["s"] for l in labels]
cycle_h = [cycle[l]["h"] for l in labels]
cycle_T = [cycle[l]["T"] for l in labels]

# get true bounds for R12
Ttriple = PropsSI("Ttriple","",0,"",0,"R12")
Tcrit   = PropsSI("Tcrit","",0,"",0,"R12") - 1e-3
eps     = 1e-3

T_dom   = np.linspace(Ttriple, Tcrit - eps, 400)
sL      = [PropsSI("S","T",T,"Q",0,"R12")/1000 for T in T_dom]
hL      = [PropsSI("H","T",T,"Q",0,"R12")/1000 for T in T_dom]
sV      = [PropsSI("S","T",T,"Q",1,"R12")/1000 for T in T_dom]
hV      = [PropsSI("H","T",T,"Q",1,"R12")/1000 for T in T_dom]

# Mollier (h-s) diagram
fig_hs = go.Figure()
fig_hs.add_trace(go.Scatter(x=sL, y=hL, mode="lines", name="Sat. Liquid", line=dict(dash="dash")))
fig_hs.add_trace(go.Scatter(x=sV, y=hV, mode="lines", name="Sat. Vapor", line=dict(dash="dash")))
fig_hs.add_trace(go.Scatter(x=cycle_s, y=cycle_h, mode="lines+markers", name="Cycle",
                            marker=dict(symbol="circle", size=8), line=dict(color="black")))
fig_hs.update_layout(
    title="Mollier Diagram (h–s) for Pressure Regulated Expander at 15 psig",
    xaxis_title="Entropy [kJ/kg·K]", yaxis_title="Enthalpy [kJ/kg]",
    legend=dict(
        x=0.01,
        y=0.99,
        xanchor='left',
        yanchor='top',
        bgcolor='rgba(255,255,255,0.5)'
    )
)
fig_hs.show()

# Temperature–Entropy (T-s) diagram
fig_ts = go.Figure()
fig_ts.add_trace(go.Scatter(x=sL, y=T_dom, mode="lines", name="Sat. Liquid", line=dict(dash="dash")))
fig_ts.add_trace(go.Scatter(x=sV, y=T_dom, mode="lines", name="Sat. Vapor", line=dict(dash="dash")))
fig_ts.add_trace(go.Scatter(x=cycle_s, y=cycle_T, mode="lines+markers", name="Cycle",
                           marker=dict(symbol="circle", size=8), line=dict(color="black")))

# Mark coolant (air) inlet temperature (T8) -- assuming this is ambient temp??
T_cool = axv15["T8 [K]"]
fig_ts.add_trace(go.Scatter(
    x=[0, max(cycle_s)],
    y=[T_cool, T_cool],
    mode="lines", name="Coolant (Air) Inlet T", line=dict(color="green", dash="dot")
))

fig_ts.update_layout(
    title="T–s Diagram for Pressure Regulated Expander at 15 psig",
    xaxis_title="Entropy [kJ/kg·K]", yaxis_title="Temperature [K]",
    legend=dict(
        x=0.01,        # 1% from left
        y=0.99,        # 99% from bottom
        xanchor="left",
        yanchor="top",
        bgcolor="rgba(255,255,255,0.5)"
    )
)
fig_ts.show()


### thermally controlled data ###
# If df_txv has a 'Configuration' column, you can filter by name:
txv_high_high = df_txv[df_txv["Configuration"] == 1].iloc[0] # both fans high
txv_high_low  = df_txv[df_txv["Configuration"] == 2].iloc[0] # condenser fan low, evap fan high

def compute_cycle(hrow):
    """Given a single-row Series hrow, return lists (s, h, T) closing back to Comp Outlet."""
    cycle_s, cycle_h, cycle_T = [], [], []
    # go through each corner
    for name,(Tkey,Pkey) in state_points.items():
        T = hrow[Tkey]
        P = hrow[Pkey]
        s = PropsSI("S","T",T,"P",P,"R12")/1000
        h = PropsSI("H","T",T,"P",P,"R12")/1000
        cycle_s.append(s)
        cycle_h.append(h)
        cycle_T.append(T)
    # close the loop by appending the first point again
    cycle_s.append(cycle_s[0])
    cycle_h.append(cycle_h[0])
    cycle_T.append(cycle_T[0])
    return cycle_s, cycle_h, cycle_T

# Compute for both cases
s_hh, h_hh, T_hh = compute_cycle(txv_high_high)
s_hl, h_hl, T_hl = compute_cycle(txv_high_low)

# Plot Mollier (h–s) for both configurations ---
fig_hs = go.Figure()
fig_hs.add_trace(go.Scatter(x=sL, y=hL, mode="lines", name="Sat. Liquid", line=dict(dash="dash")))
fig_hs.add_trace(go.Scatter(x=sV, y=hV, mode="lines", name="Sat. Vapor", line=dict(dash="dash")))

# TXV: both fans high
fig_hs.add_trace(go.Scatter(x=s_hh, y=h_hh, mode="lines+markers", name="Fans High",
                            marker=dict(symbol="circle",size=6), line=dict(color="black")))

# TXV: evap high, cond low
fig_hs.add_trace(go.Scatter(x=s_hl, y=h_hl, mode="lines+markers", name="Cond Low, Evap High",
                            marker=dict(symbol="square",size=6), line=dict(color="brown")))

fig_hs.update_layout(
    title="Mollier Diagram (h-s) with Thermally Controlled Expander at Different Fan Configurations",
    xaxis_title="Entropy [kJ/kg·K]", yaxis_title="Enthalpy [kJ/kg]",
    legend=dict(orientation="h", x=0.5, y=1.02, xanchor="center", yanchor="bottom")
)
fig_hs.show()


# Plot Temperature–Entropy (T–s) for both configurations ---
fig_ts = go.Figure()
fig_ts.add_trace(go.Scatter(x=sL, y=T_dom, mode="lines", name="Sat. Liquid", line=dict(dash="dash")))
fig_ts.add_trace(go.Scatter(x=sV, y=T_dom, mode="lines", name="Sat. Vapor", line=dict(dash="dash")))

# TXV cycles
fig_ts.add_trace(go.Scatter(x=s_hh, y=T_hh, mode="lines+markers", name="Fans High",
                            marker=dict(symbol="circle",size=6), line=dict(color="black")))
fig_ts.add_trace(go.Scatter(x=s_hl, y=T_hl, mode="lines+markers", name="Cond Low, Evap High",
                            marker=dict(symbol="square",size=6), line=dict(color="brown")))

# Coolant (air) inlet = T8 [K] on both rows
T_cool_hh = txv_high_high["T8 [K]"]
T_cool_hl = txv_high_low ["T8 [K]"]

# horizontal lines at each coolant temp
fig_ts.add_trace(go.Scatter(
    x=[0, max(cycle_s)], y=[T_cool_hh, T_cool_hh],
    mode="lines", name="Coolant Inlet Temp (Fans High)", line=dict(color="green", dash="dot")
))
fig_ts.add_trace(go.Scatter(
    x=[0, max(cycle_s)], y=[T_cool_hl, T_cool_hl],
    mode="lines", name="Coolant Inlet Temp (Cond Low, Evap High)",  line=dict(color="orange",dash="dot")
))

fig_ts.update_layout(
    title="T–s Diagram with Thermally Controlled Expander at Different Fan Configurations",
    xaxis_title="Entropy [kJ/kg·K]", yaxis_title="Temperature [K]",
    legend=dict(orientation="h", x=0.5, y=1.02, xanchor="center", yanchor="bottom")
)
fig_ts.show()


### Capillary Tube Data ###

# Helper to compute P (kPa) and v (m3/kg) arrays closing the loop
def cycle_pv(row):
    P_list, v_list = [], []
    for name,(Tkey,Pkey) in state_points.items():
        T = row[Tkey]
        P = row[Pkey]
        rho = PropsSI("D","T",T,"P",P,"R12")      # density [kg/m3]
        v = 1.0 / rho                            # specific volume [m3/kg]
        P_list.append(P/1000)                      # convert Pa -> kPa
        v_list.append(v)
    # close the loop:
    P_list.append(P_list[0])
    v_list.append(v_list[0])
    return P_list, v_list

# Extract each CTV configuration by name
ctv_bh = df_ctv[df_ctv["Configuration"] == 11].iloc[0] # both high
ctv_hl = df_ctv[df_ctv["Configuration"] == 10].iloc[0] # evap high, condense low
ctv_lh = df_ctv[df_ctv["Configuration"] == 1].iloc[0] # evap low, condense high

p_bh, v_bh = cycle_pv(ctv_bh)
p_hl, v_hl = cycle_pv(ctv_hl)
p_lh, v_lh = cycle_pv(ctv_lh)

# Sweep through two‐phase region
T_dom = np.linspace(Ttriple, Tcrit, 400)
P_dom = [PropsSI("P","T",T,"Q",0,"R12")/1000 for T in T_dom]  # Pa→kPa
vL_dom = [1/PropsSI("D","T",T,"Q",0,"R12") for T in T_dom]   # sat. liquid
vV_dom = [1/PropsSI("D","T",T,"Q",1,"R12") for T in T_dom]   # sat. vapor

# compute your cycle’s v-limits:
v_all = v_bh + v_hl + v_lh
vmin, vmax = min(v_all), max(v_all)

vL_arr = np.array(vL_dom)
vV_arr = np.array(vV_dom)
P_arr  = np.array(P_dom)

# mask the dome curves:
maskL = (vL_arr >= vmin*0.9) & (vL_arr <= vmax*1.1)
maskV = (vV_arr >= vmin*0.9) & (vV_arr <= vmax*1.1)

# plotting
fig_pv = go.Figure()

fig_pv.add_trace(go.Scatter(
    x=np.array(vL_dom)[maskL], y=np.array(P_dom)[maskL],
    mode="lines", name="Sat. Liquid", line=dict(dash="dash", color="blue")
))
fig_pv.add_trace(go.Scatter(
    x=np.array(vV_dom)[maskV], y=np.array(P_dom)[maskV],
    mode="lines", name="Sat. Vapor", line=dict(dash="dash", color="red")
))

# both fans high
fig_pv.add_trace(go.Scatter(
    x=v_bh, y=p_bh,
    mode="lines+markers", name="Both High",
    line=dict(color="black"),
    marker=dict(symbol="circle", size=6)
))

# evap high, cond low
fig_pv.add_trace(go.Scatter(
    x=v_hl, y=p_hl,
    mode="lines+markers", name="Evap High, Cond Low",
    line=dict(color="green"),
    marker=dict(symbol="square", size=6)
))

# evap low, cond high
fig_pv.add_trace(go.Scatter(
    x=v_lh, y=p_lh,
    mode="lines+markers", name="Evap Low, Cond High",
    line=dict(color="orange"),
    marker=dict(symbol="diamond", size=6)
))

fig_pv.update_layout(
    title="P–v Diagram with Capillary Tube Expander at Different Fan Settings",
    xaxis=dict(range=[vmin*0.9, vmax*1.1]),
    xaxis_title="Specific Volume v [m³/kg]",
    yaxis_title="Pressure P [kPa]",
    legend=dict(orientation="h", x=0.5, y=1.02, xanchor="center"),
    margin=dict(t=80)
)
fig_pv.show()