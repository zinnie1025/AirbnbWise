import contents as ct
import pandas as pd
import numpy as np

# import sys
# print(sys.path)
if __name__ == "__main__":
    df = pd.read_csv("/Users/genie/Documents/COLLABORATION/AirbnbWise/Pipeline/user_db.csv")
    ex = ct.InputDataProcessor(df)
    output = ex.processing()
    output.drop(columns=['region'],inplace=True)
    output.to_csv("/Users/genie/Documents/COLLABORATION/AirbnbWise/Pipeline/preprocessed_user_db.csv", index=False)