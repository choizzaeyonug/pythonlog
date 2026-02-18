import requests
import datetime
import json
import sys


#네이버 API
naver_client_id = ""
naver_client_secret= ""


#카카오 정보
kakao_rest_api_key = ""
kakao_client_secret = ""
kakao_refresh_token = ""

#액세스 토큰 재발급
def refresh_access_token():
    url = "https://kauth.kakao.com/oauth/token"

    data = {
        "grant_type":"refresh_token",
        "client_id":kakao_rest_api_key.strip(),
        "client_secret":kakao_client_secret.strip(),
        "refresh_token":kakao_refresh_token.strip()
    }

    response = requests.post(url, data=data)

    print("토큰 응답 코드:",response.status_code)
    print("토큰 응답 내용:",response.text)

    if response.status_code !=200:
        print("토큰 재발급 실패")
        return None
    
    token_data = response.json()

    if "access_token" not in token_data:
        print("access_token 없음")
        return None
    
    print("액세스 토큰 재발급 성공")
    return token_data["access_token"]


#네이버 뉴스 가져오기
def get_news(keyword):
    url="https://openapi.naver.com/v1/search/news.json"

    headers = {
        "X-Naver-Client-Id":naver_client_id,
        "X-Naver-Client-Secret":naver_client_secret
    }

    params = {
        "query":keyword,
        "display":5,
        "sort":"date"
    }

    response = requests.get(url,headers=headers,params=params)

    if response.status_code != 200:
        print("네이버 API 오류:",response.text)
        return []
    
    return response.json().get("items",[])

        
#메세지 생성
def make_message(news_items,keyword):
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    message = f"[{today}] {keyword} 최신 뉴스\n\n"

    for item in news_items:
        title = item["title"].replace("<b>","").replace("</b>","")
        link = item["link"]
        message +=f"-{title}\n{link}\n\n"

    return message[:990]

#카카오 전송
def send_kakao(access_token,message):
    url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/x-www-form-urlencoded;charset=utf-8"
    }

    template = {
        "object_type": "text",
        "text": message,
        "link": {
            "web_url": "https://www.naver.com"
        }
    }
    

    data = {
        "template_object": json.dumps(template)
    }

    res = requests.post(url, headers=headers, data=data)

    print("카카오 응답 코드:", res.status_code)
    print("카카오 응답 내용:", res.text)

    if res.status_code == 200:
        print("카카오 전송 성공")
    else:
        print("카카오 전송 실패")


#실행

if __name__ == "__main__":
    
    keyword = "주식"

    access_token = refresh_access_token()

    if not access_token:
        print("프로그램 종료")
        sys.exit()

    news_items = get_news(keyword)

    if not news_items:
        print("뉴스 없음")
        sys.exit()

    message = make_message(news_items,keyword)
    send_kakao(access_token,message)