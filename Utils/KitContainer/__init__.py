import tqdmLinguaUtil as tlu
import pandas as pd
from tqdm import tqdm
import sys

#print(sys.path)
#sys.path.append("C:\\Users\\lucky\\Documents\\COLLABORATION\\AirbnbWise\\Utils")
#sys.path.append("C:\\Users\\lucky\\Documents\\COLLABORATION\\AirbnbWise\\Utils\\KitContainer")
base_path = 'C:\\Users\\lucky\\Documents\\COLLABORATION\\AirbnbWise\\Tokyo_Airbnb\\yunyoung'
want_path = base_path + '\\translated_csv\\df2.csv'
df = pd.read_csv(want_path)

if __name__ == '__main__':
    source_lan = 'auto'
    target_lan = 'ko'
    ex = tlu.Translator(source = source_lan, target = target_lan)
    translated_comments = pd.DataFrame(columns=['kr_comments'])
    with tqdm(total=len(df)) as pbar:
        for index, row in df.iterrows():
            translated_text = ex.translate_text(row['comments'])
            translated_comments.loc[index] = [translated_text]
            pbar.update(1)
    df['kr_comments'] = translated_comments['kr_comments']
    df.to_csv('df2.csv', index=False)


#test = pd.read_csv('C:\\Users\\lucky\\Documents\\COLLABORATION\\AirbnbWise\\Tokyo_Airbnb\\yunyoung\\translated_csv\\test.csv')