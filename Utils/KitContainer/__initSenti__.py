import sentiword as st
import pandas as pd
from tqdm import tqdm
import os
import sys
import tensorflow as tf
import warnings
warnings.filterwarnings(action='ignore')
import ast

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
    # ex = st.preSentiment(df)
    # outdf = ex.removedata()
    # outsavePath = os.path.join(path, 'sentiment.csv')
    # outdf.to_csv(outsavePath)
    # outdf = ex.filteredTextoutput()
    outdf = pd.read_csv('C:\\Users\\lucky\\Documents\\COLLABORATION\\AirbnbWise\\Pipeline\\jieun\\sentiment.csv')
    
    ex2 = st.sentimentKiwi(filtered_comment=outdf)  
    # spaced_comments = ex2.spacingCorrection()  
    # split_sentences = ex2.splitSentence(spaced_comments) 
    # textTokendf = ex2.textTokenDataFrame(split_sentences)
    # textTokendf.to_csv(path, 'sentence_df.csv', index=False) 
    textTokendf = pd.read_csv('C:\\Users\\lucky\\Documents\\COLLABORATION\\AirbnbWise\\Pipeline\\jieun\\jieunsentence_df.csv')
    
    splitNVRdf = ex2.splitNVR(textTokendf) 
   
    ex3 = st.preVisualizationtext(splitNVRdf)
    #! 여기 부분 에러!!!
    nounsList = ex3.split_word('nouns')
    verbsList = ex3.split_word('verbs')
    radixList = ex3.split_word('radixs')
    
    nounsCounts = ex3.wordCount(nounsList)
    verbsCounts = ex3.wordCount(verbsList)
    radixCounts = ex3.wordCount(radixList)
    
    palettes = ['spring', 'summer', 'seismic','PuBu']
    font_path = 'C:/Windows/Fonts/malgun.ttf'
    save_path = os.path.join(path, 'wordcloud_verbs.png')
    ex4 = st.wordCloud(verbsCounts, font_path, 'Verbs Word Cloud', 'gnuplot2', save_path)
    
    sorted_verbs = sorted(verbsCounts.items(), key=lambda x: x[1], reverse=True)
    sorted_nouns = sorted(nounsCounts.items(), key=lambda x: x[1], reverse=True)
    sorted_radixs = sorted(radixCounts.items(), key=lambda x: x[1], reverse=True)
    
    ex5 = st.TreeMapGenerator()
    save_treemapPath = os.path.join(path, 'treemap_verb.png')
    save_treemapPath2 = os.path.join(path, 'treemap_nouns.png')
    save_treemapPath3 = os.path.join(path, 'treemap_radix.png')
    label1, counts1 = zip(*sorted_verbs)
    ex5.TreeMapGenerator(label1, counts1, 'Frequency verbs Treemap', save_treemapPath)
    label2, counts2 = zip(*sorted_nouns) 
    ex5.TreeMapGenerator(label2, counts2, 'Frequency nouns Treemap', save_treemapPath2)
    label3, counts3 = zip(*sorted_radixs) 
    ex5.TreeMapGenerator(label3, counts3, 'Frequency radixs Treemap', save_treemapPath3)
    