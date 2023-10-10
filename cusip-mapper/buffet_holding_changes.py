from datetime import datetime

import pandas as pd

def calculate_holding_changes(df):
    date_2023_06_30 = datetime.strptime('2023-06-30', '%Y-%m-%d').date()
    date_2023_03_31 = datetime.strptime('2023-03-31', '%Y-%m-%d').date()

    holdings_changes = "NaN"
    holding_changes = []

    subset = df[df['PeriodOfReport']==date_2023_06_30]

    # mask_1 = select holdings for 2023-03-31 period
    mask_1 = df['PeriodOfReport']==date_2023_03_31

    for index, holding_2023_06_30 in subset.iterrows():
        # mask_2 = select holdings with same NameOfIssuer
        mask_2 = df['CUSIP']==holding_2023_06_30['CUSIP']
        # merge both masks
        holdings_2023_03_31 = df[(mask_1 & mask_2)]

        if len(holdings_2023_03_31) != 0:
            holding_2023_03_31 = holdings_2023_03_31.iloc[0]

            share_delta_absolute = holding_2023_06_30['Shares'] - holding_2023_03_31['Shares']
            share_delta_relative = (share_delta_absolute / holding_2023_03_31['Shares']) * 100
            shares_2023_06_30 = holding_2023_06_30['Shares']
            shares_2023_03_31 = holding_2023_03_31['Shares']

        else:
            # holding didn't exist in 2023-03-31 filing
            share_delta_absolute = holding_2023_06_30['Shares']
            share_delta_relative = 100
            shares_2023_06_30 = holding_2023_06_30['Shares']
            shares_2023_03_31 = 0

        holding_changes.append((holding_2023_06_30['CUSIP'],
                                holding_2023_06_30['Ticker'],
                                holding_2023_06_30['SecurityName'],
                                shares_2023_03_31,
                                shares_2023_06_30,
                                share_delta_absolute,
                                share_delta_relative))

    holding_changes = pd.DataFrame(holding_changes, columns =['CUSIP',
                                                              'Ticker',
                                                              'SecurityName',
                                                              'Shares2023_03_31',
                                                              'Shares2023_06_30',
                                                              'DeltaAbsolute',
                                                              'DeltaRelative'])
    return holding_changes

