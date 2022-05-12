from preprocess import preprocess
from es import from_es

if __name__ == "__main__":
    ps = preprocess.Preprocessor()
    keywords = ['경기도', '석촌', '아파트', '부동산', '서울']
    save_df = ps.start_preprocess('mecab', [1,2,3,4,6], keywords)
