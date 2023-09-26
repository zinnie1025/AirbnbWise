import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")
import os
import re
from tqdm import tqdm
from kiwipiepy import Kiwi

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
        split_result = self.kiwi.split_into_sentences(space_comments)
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

        sentence_df = pd.DataFrame(
            {
                'text' : text,
                'token' : token
            }
        )
        return sentence_df