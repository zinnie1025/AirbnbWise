import tqdmLinguaUtil as tlu
import pandas as pd
from tqdm import tqdm
import sys

#print(sys.path)
#sys.path.append("C:\\Users\\lucky\\Documents\\COLLABORATION\\AirbnbWise\\Utils")
#sys.path.append("C:\\Users\\lucky\\Documents\\COLLABORATION\\AirbnbWise\\Utils\\KitContainer")

df = pd.read_csv('/Users/genie/Documents/COLLABORATION/AirbnbWise/Pipeline/filtered_data/filtered_data4.csv')

if __name__ == '__main__':
    source_lan = 'auto'
    target_lan = 'ko'
    ex = tlu.Translator(source = source_lan, target = target_lan)
    translated_comments = pd.DataFrame(columns=['kr_comments'])
        
    with tqdm(total=len(df)) as pbar:
        for index, row in df.iterrows():
            try:
                translated_text = ex.translate_text(row['comments'])
                translated_comments.loc[index] = [translated_text]
                pbar.update(1)
            except:
                print(f'{index}error')
                pass
    df['kr_comments'] = translated_comments['kr_comments']
    df.to_csv('/Users/genie/Documents/COLLABORATION/AirbnbWise/Pipeline/translated_data/transdf4.csv', index=False)


#test = pd.read_csv('C:\\Users\\lucky\\Documents\\COLLABORATION\\AirbnbWise\\Tokyo_Airbnb\\yunyoung\\translated_csv\\test.csv')
#! want_path, df_to_csv 숫자 변경
#! 글자수가 5000개 이상이면 번역 불가능하므로 예외처리