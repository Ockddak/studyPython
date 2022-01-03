"""

    https://www.data.go.kr/data/15044713/openapi.do 표제부 데이터 받기
    카카오로 정제후 받기

"""

import requests  # lib 설치
import json  # lib 설치
import pandas as pd  # lib 설치
import chardet
from collections import defaultdict
from urllib.request import urlopen
from urllib.parse import urlencode, unquote, quote_plus
import xmltodict

# api 연결 및 데이터 불러오기 주소 -> 좌표 및 주소정제
def getLatLng(addr):
    url = 'https://dapi.kakao.com/v2/local/search/address.json?query=' + addr
    headers = {"Authorization": "Kakao API key"}
    result = json.loads(str(requests.get(url, headers=headers).text))

    if result['meta']['total_count'] != 0:
        if result['documents'][0]['address'] is not None:
            match_first = result['documents'][0]['address']

        else:
            return None
    else:
        return None

    return match_first['b_code'], match_first['main_address_no'], match_first['sub_address_no']

# 파일불러오기
fileName = "csv 파일 불러오기"
file_enc = open(fileName, 'rb').read()
result = chardet.detect(file_enc)
charenc = result['encoding']

df = pd.read_csv(fileName, encoding=charenc)

Addr_df = pd.DataFrame(columns=list(df.columns) + ['sigunguCd', 'bjdongCd', 'bun', 'ji'])
Addr_row = defaultdict()


ge_title_col = ['rnum', 'platPlc', 'platGbCd', 'mgmBldrgstPk', 'regstrGbCd', 'regstrGbCdNm',
                'regstrKindCd', 'regstrKindCdNm', 'newOldRegstrGbCd', 'newOldRegstrGbCdNm', 'newPlatPlc', 'bldNm', 'splotNm', 'block',
                'lot', 'bylotCnt', 'naRoadCd', 'naBjdongCd', 'naUgrndCd', 'naMainBun', 'naSubBun', 'platArea', 'archArea', 'bcRat', 'totArea',
                'vlRatEstmTotArea', 'vlRat', 'mainPurpsCd', 'mainPurpsCdNm', 'etcPurps', 'hhldCnt', 'fmlyCnt', 'mainBldCnt', 'atchBldCnt', 'atchBldArea',
                'totPkngCnt', 'indrMechUtcnt', 'indrMechArea', 'oudrMechUtcnt', 'oudrMechArea', 'indrAutoUtcnt', 'indrAutoArea', 'oudrAutoUtcnt', 'oudrAutoArea',
                'pmsDay', 'stcnsDay', 'useAprDay', 'pmsnoYear', 'pmsnoKikCd', 'pmsnoKikCdNm', 'pmsnoGbCd', 'pmsnoGbCdNm', 'hoCnt', 'engrGrade', 'engrRat', 'engrEpi',
                'gnBldGrade', 'gnBldCert', 'itgBldGrade', 'itgBldCert', 'crtnDay' ]

ge_title_df = pd.DataFrame(columns = ['sigunguCd', 'bjdongCd', 'bun', 'ji'] + ge_title_col)


build_row = defaultdict()
dup_check = defaultdict()
suc = 0
fail = 0
for n in range(df.shape[0]) :
    Addr_row['상호'] = df.loc[n,'상호']
    Addr_row['주소'] = df.loc[n,'주소']
    kakao_res = getLatLng(df.loc[n,'주소'])


    if kakao_res is not None :

        sigunguCd = kakao_res[0][:5]
        bjdongCd = kakao_res[0][5:]
        bun = kakao_res[1]
        ji = kakao_res[2]

        Addr_row['sigunguCd'] = sigunguCd
        Addr_row['bjdongCd'] = bjdongCd
        Addr_row['bun'] = bun
        Addr_row['ji'] = ji
        if ''.join(map(str,kakao_res)) not in dup_check:
            dup_check[''.join(map(str,kakao_res))] = ''
            build_row['sigunguCd']          = sigunguCd
            build_row['bjdongCd']           = bjdongCd
            build_row['bun']                = bun
            build_row['ji']                 = ji

            while len(bun) < 4 :
                bun = '0' + bun
            while len(ji) < 4 :
                ji = '0' + ji

            print(sigunguCd ,bjdongCd, bun, ji)

            serviceKey = 'wk52r5dzJE%2B%2FE1%2FNlTeXny1gQsMPvFhodPk7aIb6Dm%2FI4nN4MJhEqRN9uAxsH5P7HbvEeD%2BHHFmC8TGr6RIp0A%3D%3D'

            url = f'http://apis.data.go.kr/1613000/BldRgstService_v2/getBrRecapTitleInfo?serviceKey={serviceKey}&'
            queryParams = urlencode({quote_plus('sigunguCd'): sigunguCd,
                                     quote_plus('bjdongCd'): bjdongCd,
                                     quote_plus('bun'): bun,
                                     quote_plus('ji'): ji})

            url2 = url + queryParams
            response = urlopen(url2)
            results = response.read().decode("utf-8")
            results_to_json = xmltodict.parse(results)
            data = json.loads(json.dumps(results_to_json))
            try :

                count = int(data['response']['body']['totalCount'])
                print(count)

                if count > 0 :
                    items = data['response']['body']['items']['item']
                    if count != 1:
                        for item_n in range(len(items)):
                            for i in items[item_n].keys():
                                build_row[i] = items[item_n][i]

                    else:
                        for i in items.keys():
                            build_row[i] = items[i]

                    ge_title_df = ge_title_df.append(build_row, ignore_index=True)
            except :
                fail += 1
                for col in ge_title_col:
                    build_row[col] = ''
                ge_title_df = ge_title_df.append(build_row, ignore_index=True)
                pass

    else :
        Addr_row['sigunguCd'] = None
        Addr_row['bjdongCd'] = None
        Addr_row['bun'] = None
        Addr_row['ji'] = None

    Addr_df = Addr_df.append(Addr_row, ignore_index=True)

Addr_df.to_csv('D:/Addr_df.csv', encoding='euc-kr')
