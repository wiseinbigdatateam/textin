import os


def df_save_csv(data, filename):
    if os.path.isfile(filename):
        print("기존 파일")
        with open(filename, 'a') as url_csv:
            data.to_csv(url_csv, header=False)
        url_csv.close()
        print(f"{filename}에 추가 끝")

    else:
        df_csv = data.to_csv(filename, encoding='utf-8')
        print(f"{filename} 저장")

    return filename