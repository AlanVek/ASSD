import pandas as pd
import numpy as np
import os

def gen_data() -> tuple[np.array, list[pd.DataFrame], list[pd.DataFrame]]:
    real = np.arange(1, 13) * 5/12
    dfs_adc : list[pd.DataFrame] = []
    dfs_dac : list[pd.DataFrame] = []
    for file in os.listdir('VADC'): dfs_adc.append(pd.read_csv('VADC/' + file))
    for file in os.listdir('VDAC'): dfs_dac.append(pd.read_csv('VDAC/' + file))

    return real, dfs_dac, dfs_adc

def gen_table() -> pd.DataFrame:
    real, dfs_dac, dfs_adc = gen_data()

    for i in range(len(dfs_adc)):
        dfs_adc[i] = dfs_adc[i].replace('SLO', 0).replace('SHI', 1)

    out_dac = np.array([dfs_dac[i]['VDAC'][200] for i in range(len(dfs_dac))])
    cols = dfs_adc[0].columns[1:]
    out_adc = np.array([''.join(list(map(str, dfs_adc[i][cols].loc[2]))) for i in range(len(dfs_adc))])

    df = pd.DataFrame(np.vstack((real.round(3), out_adc, out_dac)).T, columns = ['Real [V]', 'Bits ADC', 'Output DAC [V]'])
    return df


if __name__ == '__main__':
    df = gen_table()

    # with open('Table_Latex.txt', 'wt') as file:
    #     file.write(df.to_latex(index = False, column_format='|c|c|c|'))

    print((df['Real [V]'].to_numpy().astype(float) - df['Output DAC [V]'].to_numpy().astype(float)).mean())