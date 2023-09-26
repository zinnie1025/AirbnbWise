import sentiword as st
import pandas as pd
from tqdm import tqdm
import os
import sys
import tensorflow as tf

physical_devices = tf.config.list_physical_devices('GPU')
if physical_devices:
    tf.config.experimental.set_memory_growth(physical_devices[0], enable=True)
if tf.config.list_physical_devices('GPU'):
    print("GPU가 사용 중입니다.")
else:
    print("GPU를 사용하지 않고 CPU를 사용 중입니다.")

path = 'C:\\Users\\lucky\\Documents\\COLLABORATION\\AirbnbWise\\Pipeline\\jieun'
rpath1 = os.path.join(path, 'total_translate_review.csv')
df = pd.read_csv(rpath1)

if __name__ == '__main__':
    ex = st.preSentiment(df)
    outText = ex.filteredTextoutput()
    #print(outText)
    
    ex2 = st.sentimentKiwi(filtered_comment=outText)  
    spaced_comments = ex2.spacingCorrection()  
    split_sentences = ex2.splitSentence(spaced_comments) 
    textTokendf = ex2.textTokenDataFrame(split_sentences) 
    print(textTokendf)
    