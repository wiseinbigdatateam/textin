from ctrl_data import DataDict

if __name__ == "__main__":
    test = DataDict()
    keywords = ['경기도', '석촌', '아파트', '부동산', '서울']
    save_df = test.start_preprocess([1,2,3,4,6], keywords)
