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

    # if data.shape[1] == 2:
    #     if os.path.isfile(filename):
    #         print("url 기존 파일")
    #         with open(filename, 'a') as url_csv:
    #             data.to_csv(url_csv, header=False)
    #         url_csv.close()
    #         print("url 추가 끝")
    #
    #     else:
    #         df_csv = data.to_csv(filename, encoding='utf-8')
    #         print(f"{filename} 저장")
    #         return filename
    #
    # else:
    #     if os.path.isfile(filename):
    #         print("기존 파일 감지")
    #         with open(filename, 'a') as w_csv:
    #             print("기존 파일에 추가")
    #             data.to_csv(w_csv, header=False)
    #             w_csv.close()
    #             return print("추가 끝")
    #     else:
    #         df_csv = data.to_csv(filename, encoding='utf-8')
    #         print(f"{filename} 저장")
    #     return filename