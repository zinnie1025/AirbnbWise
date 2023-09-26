import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")
import os
import re
from tqdm import tqdm

#from kiwipiepy import Kiwi
from itertools import chain
from collections import Counter

import matplotlib.pyplot as plt
from wordcloud import WordCloud
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
import plotly.express as px
class preSentiment:
    '''
    text 준비
    '''
    def __init__(self, df):
        self.df = df
        
    def removedata(self):
        self.df = self.df.dropna(subset=['kr_comments'])
        self.df = self.df.drop_duplicates(['listing_id','reviewer_id', 'comments', 'date'], keep='first').reset_index(drop=True)
        return self.df
    
    def processComment(self, text):
        '''
        한글 제외한 텍스트 제거
        작은 따옴표 제거
        양쪽 공백 제거
        '''
        comment = re.sub(r'[^가-힣 ]', ' ', text)
        comment = comment.replace("'", '')
        comment = ' '.join(comment.split())
        return comment
            
    def filteredTextoutput(self):
        '''
        번역 데이터 텍스트 전처리 후
        '''
        self.df = self.removedata()
        self.df['kr_comments'] = self.df['kr_comments'].apply(self.processComment)
        filtered_comment = self.df['kr_comments'].tolist()
        return filtered_comment
    

class sentimentKiwi:
    def __init__(self, filtered_comment = None):
        self.filtered_comment = filtered_comment
        self.kiwi = Kiwi(model_type='sbg', typos='basic', typo_cost_threshold=2.5)
        
    def spacingCorrection(self):
        '''
        텍스트 띄어쓰기 교정
        #! 여기 왜 오래걸리지????
        '''
        space_comments = []
        with tqdm(total=len(self.filtered_comment)) as pbar:
            for comment in self.filtered_comment:
                space_comment = self.kiwi.space(comment, reset_whitespace=True)
                space_comments.append(space_comment)
                pbar.update(1)
        return space_comments
    
    def splitSentence(self, space_comments):
        '''
        여러 문장으로 구성된 텍스트 분리
        '''
        split_result = self.kiwi.split_into_sents(space_comments)
        split_result = list(split_result)
        return split_result        
    
    def textTokenDataFrame(self, split_result):
        '''
        text와 token을 분리해서 데이터 프레임 생성
        '''
        text = []
        token = []
        with tqdm(total=len(split_result)) as pbar:
            for comment in split_result:
                text.extend([sentence[0] for sentence in comment])
                token.extend([sentence[3] for sentence in comment])
                pbar.update(1)
        sentence_df = pd.DataFrame(
            {
                'text' : text,
                'token' : token
            }
        )
        return sentence_df
    
    def splitNVR(self, sentence_df):
        '''
        명사, 동사, 어근 분리
        nouns : 명사 -> NNG : 일반 명사, NNP : 고유 명사
        neg_verb: 부정 동사 -> VCN : 부정 동사
        verb : 동사 -> VA : 형용사, VV : 동사, VX : 보조 용언(시제, 높임말)
        radix : 어근 
        '''
        nouns = []
        verbs = []
        neg_verbs = []
        radixs = []

        for morphs in sentence_df['token']:
            nouns.append([(noun[0], noun[1]) for noun in morphs if noun[1] in ['NNG', 'NNP']])
            neg_verbs.append([morphs for noun in morphs if noun[1] in ['VCN']])
            verbs.append([(verb[0]+'다', verb[1]) for verb in morphs if verb[1] in ['VA', 'VV', 'VX']])
            radixs.append([(verb[0], verb[1]) for verb in morphs if verb[1] in ['XR']])

        sentence_df['verbs'] = verbs
        sentence_df['nouns'] = nouns
        sentence_df['radixs'] = radixs
        return sentence_df
    
class preVisualizationtext:
    '''
    wordCloud 텍스트 준비
    '''
    def __init__(self, sentence_df):
        self.sentence_df = sentence_df
        
    def splitWord(self, row):
        wordList = [word[0] for words in self.sentence_df[row] for word in words]
        return wordList
    
    def wordCount(self, wordList):
        word_counts = Counter(wordList)
        return word_counts

class wordCloud:
    '''
    visualization
    '''
    def generate_word_cloud(self, data, font_path, title, color=None, save_path=None):
        wordcloud = WordCloud(width=800, height=400,
                            max_words=200,
                            scale=2,
                            random_state=42,
                            background_color='white',
                            colormap = color,
                            font_path=font_path).generate_from_frequencies(data)
        if save_path:
            wordcloud.to_file(save_path)

class TreeMapGenerator:
    '''
    TreeMap visualization
    '''
    def __init__(self, df):
        self.df = df
        
    def TreeMap(self, labels, values, title, save_treemapPath=None):
        fig = go.Figure(go.Treemap(
            labels=labels[:30],
            parents=[''] * len(labels[:30]),
            values=values,
            texttemplate="%{label}<br>%{value}",
            hoverinfo='label+value',
        ))

        fig.update_layout(
            title=title,
            margin=dict(l=10, r=10, t=40, b=10)
        )
        # fig.show()

        # if save_treemapPath:
        #     fig.write_image(save_treemapPath)
