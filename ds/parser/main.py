from helpers import ParserHelper
from utils import YandexParser
import time
import pandas as pd

if __name__ == '__main__':
    time_start = time.time()
    id_ya = [i for i in pd.read_csv("ds/data/collected_ids.csv")["0"]]
    print(id_ya)
    
    df_parsed = pd.DataFrame()
    
    for i, id in enumerate(id_ya):
        print(f"{i}/{len(id_ya)}")
        parser = YandexParser(int(id))
        df_parsed[id] = pd.Series(parser.parse(company_id=id))
        
        df_parsed.to_csv("df_parsed_all.csv")
        # df_parsed = pd.DataFrame()
        
        # df_parsed = pd.json_normalize(df_parsed)
        # print(df_parsed)
        # ParserHelper.write_json_txt(parser.parse(company_id=id_ya, dataframe=df_parsed), 'result_all.json')
    
    # df_parsed.to_csv("df_parsed_all.csv")
        
    print(f"Время работы: {time.time() - time_start}")

