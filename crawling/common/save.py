import os


def save_to_csv(path, name, exist_df, exist_state, results_df, state):
    # 기존 데이터프레임과 새로 크롤링한 데이터프레임 결합
    result_df = exist_df.append(results_df, ignore_index=False)

    # 기존 진행중 파일 삭제
    exist_file = f'{path}{name}_{exist_state}.csv'
    if os.path.isfile(exist_file):
        if exist_state != 1:
            print(f"미완료 파일 : {exist_file} 삭제.")
            os.remove(exist_file)

    # 결합한 데이터 프레임 저장
    results_csv = result_df.to_csv(f'{path}{name}_{state}.csv', encoding='utf-8')
    print(f'{path}{name}_{state}.csv 가 저장 완료 되었습니다.')

    return f'{path}{name}_{state}.csv'