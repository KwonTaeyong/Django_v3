import pandas
import xmltodict
from datetime import date
import json

def mss():  # 중소벤처기업부
    # https://www.data.go.kr/iim/api/selectAPIAcountView.do
    # https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15113297#/API%20%EB%AA%A9%EB%A1%9D/getbizList_v2

    today = date.today().strftime("%Y-%m-%d")

    base_uri = "https://apis.data.go.kr/1421000/mssBizService_v2/getbizList_v2"
    params = {
        "serviceKey": "dtV7zrWSbf4WJZo8cp52dgUvXsRx8OqBXcs3OkrzAVqnNLQ/3e1fAHeLjvsFywbOCM5TCQcOwCkHD8vGDr0dBQ==",
        "pageNo": "1",
        "numOfRows": "1000",
        "startDate": "2024-03-01",
        "endDate": today
    }

    res_xml = session.get(url=base_uri, params=params)
    res_dict = xmltodict.parse(res_xml.text)

    res_parse = res_dict['response']['body']['items']['item']

    df = pandas.DataFrame(res_parse)

    df = df.rename(columns={
        'itemId': 'sourceId',
        'viewUrl': 'sourceUrl',
        'dataContents': 'contents',
        'applicationStartDate': 'pStDt',
        'applicationEndDate': 'pEdDt',
        'writerPosition': 'hostOrg',
        'writerName': 'hostName',
        'writerPhone': 'hostPhone',
        'writerEmail': 'hostEmail'
    })

    df = df[[
        'sourceId',
        'sourceUrl',
        'title',
        'contents',
        'pStDt',
        'pEdDt',
        'hostOrg',
        'hostName',
        'hostPhone',
        'hostEmail'
    ]]

    df['sourceOrg'] = '중소벤처기업부'

    url = 'http://127.0.0.1:8000/gongo/upload/'

    records = df.to_dict(orient='records')
    for record in records:
        x = session.post(url, data=record)
        print(x.text)
        break


if __name__ == '__main__':
    import requests

    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }
    session.headers.update(headers)

    mss()
