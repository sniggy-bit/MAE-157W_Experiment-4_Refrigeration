import pandas as pd

# Define file paths
file_axv = "Refrigeration Data  - AXV CSV.csv"
file_txv = "Refrigeration Data  - TXV CSV.csv"
file_ctv = "Refrigeration Data  - CTV CSV.csv"

# Define consistent column names
columns = [
    "Suction Pressure (psig)", "T1 [C]", "T2 [C]", "T3 [C]", "T4 [C]", "T5 [C]", "T6 [C]",
    "T7 [C]", "T8 [C]", "T10 [C]", "P1 [psi]", "P2 [psi]", "P3 [psi]", "P4 [psi]",
    "Evap [A]", "Comp [A]", "Cond [A]", "Voltage [V]", "Flow Rate [lb/min]"
]


# Function to clean and convert one dataset
def clean_data(file, config_type):
    if config_type == 'AXV':
        columns = [
            "Suction Pressure (psig)", "T1 [C]", "T2 [C]", "T3 [C]", "T4 [C]", "T5 [C]", "T6 [C]",
            "T7 [C]", "T8 [C]", "T10 [C]", "P1 [psi]", "P2 [psi]", "P3 [psi]", "P4 [psi]",
            "Evap [A]", "Comp [A]", "Cond [A]", "Voltage [V]", "Flow Rate [lb/min]"
        ]
    else:
        columns = [
            "Configuration", "T1 [C]", "T2 [C]", "T3 [C]", "T4 [C]", "T5 [C]", "T6 [C]",
            "T7 [C]", "T8 [C]", "T10 [C]", "P1 [psi]", "P2 [psi]", "P3 [psi]", "P4 [psi]",
            "Evap [A]", "Comp [A]", "Cond [A]", "Voltage [V]", "Flow Rate [lb/min]"
        ]

    df = pd.read_csv(file, header=None, names=columns)

    for col in df.columns:
        if '[C]' in col:
            df[col.replace('[C]', '[K]')] = df[col] + 273.15
        if '[psi]' in col:
            df[col.replace('[psi]', '[Pa]')] = df[col] * 6894.76

    return df

df_axv = clean_data(file_axv, config_type='AXV')
df_txv = clean_data(file_txv, config_type='TXV')
df_ctv = clean_data(file_ctv, config_type='CTV')
