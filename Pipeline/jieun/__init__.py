import preprocessing as pp
import pandas as pd
import numpy as np
import sys
print(sys.executable)

if __name__ == "__main__":
    df = pd.read_csv("/Users/genie/Documents/COLLABORATION/AirbnbWise/Pipeline/csv/user_totaldb.csv")
    ex = pp.InputDataProcessor(df)
    output = ex.processing()
    output.drop(columns=['region'],inplace=True)
    output.to_csv("/Users/genie/Documents/COLLABORATION/AirbnbWise/Pipeline/csv/preprocessed_user_totaldb.csv", index=False)