bought = holding_changes[holding_changes['DeltaRelative'] > 0].sort_values(by=['DeltaRelative'], ascending=False)
