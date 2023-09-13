import pandas as pd
import numpy as np
from sklearn.preprocessing import RobustScaler

class InputDataProcessor:
    '''
    Author : 지은,
    데이터 전처리
    '''
    def __init__(self, df):
        self.df = df
        
    def totalNull(self):
        '''
        null 값 모두 0으로 채움
        '''
        self.df = self.df.fillna(0)
        return self.df

    def bathrooms(self):
        '''
        bathrooms 데이터 값 중 float 값만 추출
        bathrooms 중 'Half-bath' or 'Shared Half-bath' or 'Private' 은 0.5로 변환
        Private 과 Share 의 의미는 무시함
        '''
        self.df['bathrooms'] = self.df['bathrooms'].apply(lambda x: str(x).split()[0])
        self.df['bathrooms'] = self.df['bathrooms'].apply(lambda x: 0.5 if (x == 'Half-bath') or (x == 'Shared') or (x == 'Private') else float(x))
        return self.df
    
    def regionOneHot(self):
        '''
        지역 원핫인코딩
        '''
        regiondummy = pd.get_dummies(self.df['region'])
        self.df = pd.concat([self.df, regiondummy], axis=1)
        return self.df
    
    def processing(self):
        '''
        전체 전처리 작업 
        '''
        self.df = self.totalNull()
        self.df = self.bathrooms()
        self.df = self.regionOneHot()
        return self.df
    
#TODO : 평점, 침실 수, 침대 수, 지역, 가격, 수용 인원, 최소 숙박 수