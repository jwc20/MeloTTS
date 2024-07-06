import requests
from datetime import datetime
from pprint import pprint
import json

start_time = datetime.now()

output_directory = "./outputs/"


def send():
    url = "http://127.0.0.1:8000/api/synthesize/"

    txt1 = "1번. 또 파이썬은 순수한 프로그램 언어로&서의 기능 외에도 ;다른 언어로 쓰인 모듈들을 연결하는 접착&제 언어로써 자주 이용된다. 실제 파이썬은 많은 상용 응용 프로그램에서 스크립트 언어로 채용되고 있다+. 도움말 문서도 정리가 잘 되어 있으며, 유니코드 문자열을 지원해서 다양한 언어의 문자 처리에도 능하다."
    txt2 = ";2번. 파이썬에서는 들여쓰기를 사용해서 블록을 구분하는 독;특한 문법을 채용하고 있다.&& 이 문법은 파이썬에 익숙한 사용자나 기존 프로그래밍 언어에서 들여쓰+기의 중요성을 높;이 평가하는 사용자에게는+ 잘 받아들여지고 있지만;, 다른 언어의 사용자에게서는 프로그래머의 코딩 스타일을 제한한다는 비판도 많다."
    txt3 = "3번. 파이썬은 1980년대 말 고안되어 네덜란드 CWI의 귀도 반 로섬이 ;1989년 12월 구현하기 시작하였다. 이는 역시 SETL에서 영감을 받은 ABC 언어의 후계로서 +예외 처리가 가능하고, 아메바 OS와 연동이 가능;하였다. 반 로섬은 파이썬의 주 저자로 계속 중심적 역할을 맡아 파이썬의 방향을 결정하여, 파이썬 공동체로부터 '자선 종신 이사'의 칭호를 부여받았다. 이 같은 예;로는 리눅스의 리누스 토발즈 등이 있다.;"

    txt_arr = [txt1, txt2, txt3]

    current_datetime = datetime.now()
    date_format = current_datetime.strftime("%Y%m%d%H%M%S")
    date_format = date_format + str(current_datetime.microsecond)

    for i, t in enumerate(txt_arr):
        data = {"languageCode": "ko-KR", "name": "ko-KR-Standard-B", "text": str(t)}
        try:
            response = requests.post(url, data=json.dumps(data), verify=False)
            response.raise_for_status()

            with open(output_directory + "melo_" + date_format + "_" + str(i) + ".txt", "a") as the_file:
                the_file.write(response.text)

        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
        except ValueError as e:
            print(f"JSON parsing error: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

    # single text
    # data = {
    #     "languageCode": "ko-KR",
    #     "name": "ko-KR-Standard-B",
    #     "text": str(txt1)
    # }
    # try:
    #     response = requests.post(url, data=json.dumps(data), verify=False)
    #     response.raise_for_status()
    #     # print(response)
    #     # rsp = response.text
    #     # pprint(rsp)

    #     with open('somefile.txt', 'a') as the_file:
    #         the_file.write(response.text)

    # except requests.exceptions.RequestException as e:
    #     print(f"Request error: {e}")
    # except ValueError as e:
    #     print(f"JSON parsing error: {e}")
    # except Exception as e:
    #     print(f"An error occurred: {e}")

    # data = {
    #     "voice": {
    #         "languageCode": "ko-KR",
    #         "name": "ko-KR-Standard-B"
    #     },
    #     "input": {
    #         "ssml":txt1
    #     },
    #     "audioConfig":{"audioEncoding":"mp3",
    #         "effectsProfileId":"telephony-class-application"
    #     }
    # }


if __name__ == "__main__":
    send()
    print(f"Elapsed time: {datetime.now() - start_time}")
