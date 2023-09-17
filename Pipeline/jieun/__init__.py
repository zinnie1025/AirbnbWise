import inputPreprocessing as ip
import reviewPreprocessing as rp
import pandas as pd
import numpy as np
import sys
import warnings
warnings.filterwarnings(action='ignore')
#print(sys.executable)

if __name__ == "__main__":
    base_path = '/Users/genie/Documents/COLLABORATION/AirbnbWise/Pipeline/'
    df = pd.read_csv(base_path + 'csv/user_totaldb.csv')
    ex = ip.InputDataProcessor(df)
    output = ex.processing()
    output.drop(columns=['region'],inplace=True)
    output.to_csv(base_path + 'csv/preprocessed_user_totaldb.csv', index=False)
    
    review = pd.read_csv(base_path + 'csv/150000_review.csv')
    ex2 = rp.ReviewDataProcessor(review)
    reviewoutput = ex2.processing()
    reviewoutput.drop(columns=['neighbourhood_cleansed', 'comments'],inplace=True)
    reviewoutput.to_csv(base_path + 'csv/150000_preprocessed_review.csv', index=False, encoding='utf-8')