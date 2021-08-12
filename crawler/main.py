from requests import Session
from requests.adapters import HTTPAdapter
from dotenv import load_dotenv


import os
import pandas as pd
from lxml import html
from tqdm import tqdm
import pymysql
## 사용변수 설정


load_dotenv(verbose=True)

## session 설정
session = Session()
session.mount("https://", HTTPAdapter(max_retries=3))
URL = 'https://work.mma.go.kr/caisBYIS/search/byjjecgeomsaek.do'
POST_DATA = {
    'al_eopjong_gbcd': '21101,21102,21103,21201,21202,21301,21401,21402,21501,21502,21503,21504,21505,21601,22101,23101,23201,23202,24101,25101,26101',
    'eopjong_gbcd_list': '21101,21102,21103,21201,21202,21301,21401,21402,21501,21502,21503,21504,21505,21601,22101,23101,23201,23202,24101,25101,26101',
    'eopjong_gbcd': 2,
    'pageUnit': 1000,
    'pageIndex': 1
}
def convert_str_int(data):
    r1 = int(data['현역배정인원'].replace('명', ''))
    r2 = int(data['보충역배정인원'].replace('명', ''))
    r3 = int(data['현역편입인원'].replace('명', ''))
    r4 = int(data['보충역편입인원'].replace('명', ''))
    r5 = int(data['현역복무인원'].replace('명', ''))
    r6 = int(data['보충역복무인원'].replace('명', ''))
    return pd.Series((r1,r2,r3,r4,r5,r6))

def create_lat_lon(data): # 위경도 데이터 추출 with kakaoAPI
    address = data['주소']
    # print(address)
    if address == '':
        return pd.Series((None, None))
    url = 'https://dapi.kakao.com/v2/local/search/address.json'
    params = {'query' : address}
    headers = {'Authorization' : 'KakaoAK '+ os.getenv('KAKAO_API_KEY')}
    response = session.get(url, headers=headers, params=params)
    data = response.json()
    # print(address, data)
    if(data['meta']['total_count'] != 0):
        result = data['documents'][0]
    else:
        address = address.split()[:-1]
        params = {'query' : address}
        response = session.get(url, headers=headers, params=params)
        data = response.json()
        result = data['documents'][0]
    return pd.Series((result['y'], result['x']))

if __name__ == '__main__':
    
    conn = pymysql.connect(
                    host=os.getenv('MYSQL_HOST'),
                    port=int(os.getenv('MYSQL_PORT')), 
                    user=os.getenv('MYSQL_USER'),
                    passwd=os.getenv('MYSQL_PASSWORD'),
                    db=os.getenv('MYSQL_DATABASE'),
                    charset='utf8')
    print(os.getenv('MYSQL_HOST'),os.getenv('MYSQL_PORT'),os.getenv('MYSQL_USER'),os.getenv('MYSQL_PASSWORD'))
    cursor = conn.cursor()
    cursor.execute('''DROP table if exists %s''' % os.getenv('MYSQL_DATABASE'))
    ## create table
    sql = open('create_table.sql').read()
    cursor.execute(sql)

    for i,page_num in enumerate(range(10)):
        POST_DATA['pageIndex'] = i+1
        res = session.post(URL, data=POST_DATA) # retry 정책 필요
        root = html.fromstring(res.text)
        urls = ['https://work.mma.go.kr'+ i for i in root.xpath('//tbody/tr/th/a/@href')]
        
        if not urls: # url 이 존재하지 않으면
            print('==== 데이터 파싱 / db 업데이트 완료 ====')
            break
        results = []
        for iurl in tqdm(urls):
            res_detail = session.get(iurl)
            root_detail = html.fromstring(res_detail.text)
            header = [i.text_content() for i in root_detail.xpath('//table/tbody/tr/th')]
            body = [i.text_content() for i in root_detail.xpath('//table/tbody/tr/td')]
            results.append(pd.DataFrame(list(zip(header, body)), columns=['header','body']).set_index('header').to_dict().get('body', None))
        
        df = pd.DataFrame(results)
        df[['현역배정인원','보충역배정인원','현역편입인원','보충역편입인원','현역복무인원','보충역복무인원']] = df.apply(convert_str_int, axis=1) # int 형으로 변환
        
        print('====위경도 추출====')
        df[['latitude', 'longitude']] = df.apply(create_lat_lon, axis=1) # 위경도 추출
        
        df.columns = ['name', 'address', 'phone', 'fax', 'eopjong','product','scale','research_field','a_number','r_number',
                        'a_enlistment_in','r_enlistment_in','a_service','r_service', 'latitude','longitude'
                        ] # column 명 세팅
        df.to_csv('data/{}.csv'.format(i), index=False)

        for idx, row in df.iterrows():
            print(row)
            data = row.to_dict()
            placeholders = ', '.join(['%s'] * len([key for key,val in data.items() if val is not None ])) # dict 값이 None 인 경우 제외
            columns = ', '.join(key for key,val in data.items() if val is not None)
            
            ## insert query 준비
            sql = "INSERT INTO  %s ( %s ) VALUES ( %s );" % (os.getenv('MYSQL_DATABASE'), columns, placeholders)
            
            a = list(data.values())
            value = [i for i in a if i is not None]
            r = cursor.execute(sql, value)
            
            conn.commit()
        print('INSERT FINISH \n NUMBER : {}'.format(idx+1))
