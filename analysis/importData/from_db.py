import pymysql
import pandas as pd


class FromDB:

    def __init__(self):
        self.conn = pymysql.connect(host='datain.co.kr'
                                    , user='datain'
                                    , password='wise15081508inc!@'
                                    , db='datain'
                                    , charset='utf8')

    def get_data(self):
        sql = """select userid, surveyidx, quizidx, quizinfo3, quizinfo4 from wise_survey_data where surveyidx = 1839 and userid = 'b0162';"""
        #         sql = "SHOW TABLES"
        curs = self.conn.cursor()
        curs.execute(sql)
        data = curs.fetchall()
        df = pd.DataFrame(data, columns=['userid', 'surveyidx', 'quizdix', 'quizinfo3', 'quizinfo4'])
        return df
