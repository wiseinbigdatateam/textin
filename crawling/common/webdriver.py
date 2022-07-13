from crawling import config
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class Webdriver:
    def __init__(self):
        # 크롬 드라이버 패스
        path = config.chromedriver_path
        # 크롬 드라이버 옵션
        options = Options()
        # 크롬 vpn확장 프로그램 설치 후 해당 창에서 디버그 모드로 열 때
        # # 포트 9222로 열어둔(VPN 확장프로그램 설치 및 로그인해 놓은) 크롬창에서 디버그 모드로 실행
        # # 9222포트로 크롬 실행 맥 터미널
        # # /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 --user-data-dir="/ChromeProfile"
        # # 윈도우 실행창
        # # C:\Program Files (x86)\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:/ChromeTEMP"
        # # 혹은
        # # C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:/ChromeTEMP"
        # chrome_options.add_experimental_option('debuggerAddress', '127.0.0.1:9222')
        # options.add_argument("--headless") # 크롬창이 열리지 않음
        options.add_argument("--no-sandbox")  # GUI를 사용할 수 없는 환경에서 설정. linux, docker 등
        options.add_argument("--disable-gpu")  # GUI를 사용할 수 없는 환경에서 설정. linux, docker 등
        options.add_argument(f"--window-size={1920, 1920}")
        options.add_argument('Content-Type=application/json; charset=utf-8')
        options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15")
        self.driver = webdriver.Chrome(executable_path=path, options=options)
        self.driver.implicitly_wait(3)  # 웹 자원 로드 위해 3초 대기