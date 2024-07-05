import firebase_admin # Firebase Admin SDK 사용
from firebase_admin import credentials # 서비스 계정 키를 사용하여 Firebase Admin SDK 인증
from firebase_admin import messaging # FCM 메시지 생성 및 전송
from datetime import datetime, timedelta
from .models import DeviceToken
from luck_messages.models import LuckMessage
import logging
import os

# Django 프로젝트의 루트 디렉토리 경로
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 푸시 로거 가져오기
push_logger = logging.getLogger('push_jobs')

# firebase adminsdk 초기화
cred_path = os.path.join(BASE_DIR, 'kluck_notifications/kluck-firebase.json')
try:
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred) # 초기화 한번만
    push_logger.info("Firebase Admin SDK 초기화 성공")
except Exception as e:
    push_logger.error(f"Firebase Admin SDK 초기화 실패: {e}")
    raise

# push 보내는 함수
def send_push_notifications():
    try:
        # DB에서 디바이스 토큰 가져오기
        registration_tokens = list(DeviceToken.objects.values_list('token', flat=True))

        # 오늘 날짜 가져오기
        today = datetime.now().strftime("%Y%m%d")
        # DB에서 오늘의 운세 메시지 가져오기
        today_luck_msg = LuckMessage.objects.filter(luck_date=today, category='today').first()

        # 오늘의 운세 메시지가 존재한다면 푸시 알림 보내기
        if today_luck_msg:
            title = '오늘의 운세'
            body = today_luck_msg.luck_msg
        else:
            title = '오늘의 운세'
            body = '새벽 공기처럼 맑고 상쾌한 기운이 가득하길.🍃✨ 마음 가득 행복이 채워지는 날 되세요.🌷'
            push_logger.info(f"오늘의 운세 메시지가 존재하지 않습니다. today_luck_msg: {today_luck_msg} => 임의의 내용 작성: {body}")
            
        # 푸시 알림 (notification -> 백그라운드)
        message = messaging.MulticastMessage( # 여러 기기에 메시지 전송
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            # Android 알림 설정
            android=messaging.AndroidConfig(
                # 알림 유효 시간 == 1시간 (알림 유지)
                ttl=timedelta(seconds=3600),
                # 알림 우선 순위 == 일반
                priority='normal',
                # 알림 아이콘 설정
                notification=messaging.AndroidNotification(
                    icon='https://exodus-web.gcdn.ntruss.com/static/appicon_512_512.png',
                    sound='default',
                )
            ),
            tokens = registration_tokens, # 여러 개의 등록 토큰 리스트
        )

        # Firebase로 푸시 알림 전송
        response = messaging.send_multicast(message)
        push_logger.info(f"푸시 알림 발송 성공. Response: 'title' = {title}, 'body' = {body}")
    
    except Exception as e:
        push_logger.error(f"푸시 알림 전송 중 오류 발생: {e}")
