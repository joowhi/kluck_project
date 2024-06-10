import logging
import time
from django.core.mail import send_mail
from django.conf import settings
from .views import *

# 로깅 기본 설정: 로그 레벨, 로그 포맷, 파일 이름 등을 지정할 수 있습니다.
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='gpt_jobs.log')

# 이메일 전송 함수
def send_email(subject, message, recipient_list):
    try:
        # 지정된 백엔드를 사용하여 이메일을 보내는 Django 함수
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=recipient_list,
            fail_silently=False,
        )
        logging.info(f"이메일이 성공적으로 전송되었습니다. 수신자: {recipient_list}, 제목: {subject}")
        print("Email send successfully")
    except Exception as e:
        logging.info(f"이메일 전송 중 오류가 발생했습니다: {e}")
        print(f"Email send failed: {e}")

# 주요 작업 함수
def gpt_today_job():
    # request_ = None  # 필요한 경우 실제 request 객체를 제공해야 할 수도 있다.
    term = get_object_or_404(AdminSetting).term_date
    date = datetime.now() + timedelta(days=int(term))
    luck_date = date.strftime('%Y%m%d')

    # 성공 여부 scheduler_count 변수 설정.
    scheduler_count = 0
    
    try:
        Today = GptToday(luck_date)
        if Today.status_code == status.HTTP_200_OK:
            scheduler_count += 1
            logging.info("GptToday 작업이 실행되었습니다.")
        else:
            logging.info("GptToday 작업이 실행되지 않았습니다.")
    except Exception as e:
        logging.error(f"GptToday 작업 실행 중 예외가 발생했습니다: {e}")

    try:
        Star = GptStar(luck_date)
        if Star.status_code == status.HTTP_200_OK:
            scheduler_count += 2
            logging.info("GptStar 작업이 실행되었습니다.")
        else:
            logging.info("GptStar 작업이 실행되지 않았습니다.")
    except Exception as e:
        logging.error(f"GptStar 작업 실행 중 예외가 발생했습니다: {e}")

    try:
        Mbti = GptMbti(luck_date)
        if Mbti.status_code == status.HTTP_200_OK:
            scheduler_count += 4
            logging.info("GptMbti 작업이 실행되었습니다.")
        else:
            logging.info("GptMbti 작업이 실행되지 않았습니다.")
    except Exception as e:
        logging.error(f"GptMbti 작업 실행 중 예외가 발생했습니다: {e}")

    try:
        Zodiac = GptZodiac(luck_date)
        if Zodiac.status_code == status.HTTP_200_OK:
            scheduler_count += 8
            logging.info("GptZodiac 작업이 실행되었습니다.")
        else:
            logging.info("GptZodiac 작업이 실행되지 않았습니다.")
    except Exception as e:
        logging.error(f"GptZodiac 작업 실행 중 예외가 발생했습니다: {e}")

    # 스케줄러가 다 동작된 이후 메일 전송.
    print(scheduler_count)

    # 전부 다 작동시 success count 합 15, 이 외 일부만 작동시 해당 success count 확인하여 작동된 함수 유추 가능.
    if scheduler_count == 15:
        subject="Scheduler Success Perfectly"
        message="Scheduler 동작이 완벽하게 실행되었습니다."
    elif scheduler_count == 0:
        subject="Scheduler Fail"
        message="Scheduler 동작 중 오류가 발생했습니다. 또는, 이미 해당 일자 운세 데이터가 있습니다."
    else:
        subject="Scheduler Done"
        message=f"Scheduler 동작 중 일부가 실행되었습니다. result_count = {scheduler_count}"
        
    recipient_list=["j00whii@gmail.com"]

    send_email(subject, message, recipient_list)

gpt_today_job()