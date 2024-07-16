import firebase_admin # Firebase Admin SDK 사용
from firebase_admin import credentials # 서비스 계정 키를 사용하여 Firebase Admin SDK 인증
from firebase_admin import messaging # FCM 메시지 생성 및 전송
from datetime import datetime, timedelta
from .models import DeviceToken
from luck_messages.models import LuckMessage
import logging
import os
import time

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

# Android push 보내는 함수
def send_push_android():
    try:
        # DB에서 Android 디바이스 모든 토큰 가져오기
        android_registration_tokens_all = list(DeviceToken.objects.filter(device_os='android').values_list('token', flat=True))

        #푸시 분산 발송용 리스트 생성
        android_registration_tokens = []
        #한번에 푸시 발송 할 수량 설정
        push_cnt = 1
        #푸시를 발송하는 단위 시간
        push_term = 6

        #전체 토큰을 발송량에 따라 분산 저장
        for i in range(0, len(android_registration_tokens_all), push_cnt):
            temp = android_registration_tokens_all[i:i+push_cnt]
            android_registration_tokens.append(temp)

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

        for i in range(0, len(android_registration_tokens)):
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
                    # 알림 우선 순위 == 높음
                    priority='high',
                    # 알림 아이콘 설정
                    notification=messaging.AndroidNotification(
                        icon='https://exodus-web.gcdn.ntruss.com/static/appicon_512_512.png',
                        sound='default',
                    )
                ),
                tokens = android_registration_tokens[0][i], # 여러 개의 등록 토큰 리스트
            )

            # Firebase로 푸시 알림 전송
            response = messaging.send_multicast(message)
            push_logger.info(f"Android 푸시 알림 발송 성공. Response_num[{i}]: 'title' = {title}, 'body' = {body}")

            time.sleep(push_term)

    except Exception as e:
        push_logger.error(f"Android 푸시 알림 전송 중 오류 발생: {e}")


# IOS push 보내는 함수
def send_push_ios():
    try:
        # DB에서 IOS 디바이스 토큰 가져오기
        ios_registration_tokens = list(DeviceToken.objects.filter(device_os='ios').values_list('token', flat=True))

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
            # IOS 알림 설정 (APNs, Apple Push Notification Service)
            apns=messaging.APNSConfig(
                headers={
                    'apns-push-type': 'background', # 알림 유형 == 백그라운드
                    'apns-sound': 'default',
                    'apns-priority': '10', # 알림 우선순위 == 높음(10)
                },
                payload=messaging.APNSPayload( # Android의 data 설정 역할 (alert으로 뜨는 정보)
                    aps=messaging.Aps(
                        content_available=True,
                    ),
                ),
            ),
            tokens = ios_registration_tokens, # 여러 개의 등록 토큰 리스트
        )

        # Firebase로 푸시 알림 전송
        response = messaging.send_multicast(message)
        push_logger.info(f"IOS 푸시 알림 발송 성공. Response: 'title' = {title}, 'body' = {body}")
    
    except Exception as e:
        push_logger.error(f"IOS 푸시 알림 전송 중 오류 발생: {e}")