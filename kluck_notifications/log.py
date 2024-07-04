import logging
import os

# Django 프로젝트의 루트 디렉토리 경로
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 푸시 알림 로그 설정
# logger instence 생성
push_logger = logging.getLogger('push_jobs')
# log level 설정
push_logger.setLevel(logging.INFO)
# 파일 핸들러 생성
file_path = os.path.join(BASE_DIR, 'logs/push_jobs.log')
file_handler = logging.FileHandler(file_path)
# 포맷 설정
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(funcName)s:%(lineno)s - %(message)s')
file_handler.setFormatter(formatter)


# 디바이스 토큰 로그 설정
# logger instence 생성
device_token_logger = logging.getLogger('device_token')
# log level 설정
device_token_logger.setLevel(logging.INFO)
# 파일 핸들러 생성
file_path = os.path.join(BASE_DIR, 'logs/device_token.log')
file_handler = logging.FileHandler(file_path)
# 포맷 설정
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(funcName)s:%(lineno)s - %(message)s')
file_handler.setFormatter(formatter)