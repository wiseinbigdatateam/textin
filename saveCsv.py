import os
import pandas as pd


def df_save_csv(data, filename, state, exist_df):
    if os.path.isfile(f"{filename}_0.csv"):
        result_df = exist_df.append(pd.Series(data, index=exist_df.columns), ignore_index=True)
        # 기존 진행중 파일 삭제
        os.remove(f"{filename}_0.csv")
        # 결합한 데이터 프레임 저장
        result_df.to_csv(f'{filename}_{state}.csv', encoding='utf-8')
        # print("기존 파일")
        # with open(filename, 'a') as url_csv:
        #     data.to_csv(url_csv, header=False)
        # url_csv.close()
        # print(f"{filename}에 추가 끝")

    else:
        data.to_csv(f"{filename}_{state}.csv", encoding='utf-8')
        print(f"{filename}_{state} 저장")

    return f"{filename}_{state}.csv"