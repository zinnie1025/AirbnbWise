import pandas as pd
import numpy as np

class ReviewDataProcessor:
    def __init__(self, df):
        self.df = df
        
    def regionOneHot(self):
        '''
        지역 원핫인코딩
        'neighbourhood_cleansed'칼럼
        '''
        regiondummy = pd.get_dummies(self.df['neighbourhood_cleansed'])
        self.df = pd.concat([self.df, regiondummy], axis=1)
        return self.df
    
    def price(self):
        '''
        숫자만 추출
        '''
        self.df['price'] = self.df['price'].apply(lambda x: str(x).replace('$', '').replace(',', ''))
        return self.df
    
    def hostIdType(self):
        '''
        host_id object -> integer
        '''
        self.df['host_id'] = pd.to_numeric(self.df['host_id'], errors='coerce')
        self.df['host_id'] = self.df['host_id'].fillna(0)
        self.df['host_id'] = self.df['host_id'].astype(int)
        return self.df
    
    def reviewerIdType(self):
        '''
        reviewer_id object -> integer
        '''
        self.df['reviewer_id'] = pd.to_numeric(self.df['reviewer_id'], errors='coerce')
        self.df['reviewer_id'] = self.df['reviewer_id'].fillna(0)
        self.df['reviewer_id'] = self.df['reviewer_id'].astype(int)
        return self.df
    
    def datetimeType(self):
        '''
        날짜 타입 datetime 변경
        '''
        self.df['first_review'] = pd.to_datetime(self.df['first_review'])
        self.df['last_review'] = pd.to_datetime(self.df['last_review'])
        self.df['date'] = pd.to_datetime(self.df['date'])
        return self.df
    
    def processing(self):
        '''
        전체 전처리 작업
        '''
        self.df = self.regionOneHot()
        self.df = self.price()
        self.df = self.hostIdType()
        self.df = self.reviewerIdType()
        self.df = self.datetimeType()
        return self.df