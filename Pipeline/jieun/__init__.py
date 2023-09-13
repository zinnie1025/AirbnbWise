import Preprocessing as pp
import pandas as pd
import numpy as np


if __name__ == "__main__":
    df = pd.read_csv("/Users/genie/Documents/COLLABORATION/AirbnbWise/Pipeline/user_10000db.csv")
    ex = pp.InputDataProcessor(df)
    output = ex.processing()
    output.drop(columns=['region'],inplace=True)
    output.to_csv("/Users/genie/Documents/COLLABORATION/AirbnbWise/Pipeline/preprocessed_user_10000db.csv", index=False)