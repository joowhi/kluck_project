from django.utils import timezone
from datetime import datetime, timedelta
from .scheduler import gpt_today_job
from .models import GptPrompt
from admin_settings.models import AdminSetting
import logging
import pytz

# gpt ai 로거
gpt_ai_logger = logging.getLogger('gpt_ai_jobs')

# GPT AI를 이용해 운세 받아오기
def gpt_ai_cron_job():
    """
    매분마다 관리자 페이지에서 설정한 term_time과 현재 시각(한국 기준)을 비교한 후,
    현재 시각이 term_time과 같으면 '현재 일자(한국 기준) + term_date'일자의 운세를 gpt ai를 통해 받아온다.
    """
    
    # DB에서 term_time, term_date 가져오기
    try:
        term_time = AdminSetting.objects.first().term_time
        # # 숫자 네자리를 문자열로 변환하여 분리
        # scheduler_time_str = str(scheduler_time).zfill(4)  # 네자리로 맞추기 위해 zfill 사용
        # hour = int(scheduler_time_str[:2])  # 앞 두 자리
        # minute = int(scheduler_time_str[2:])  # 뒤 두 자리
    except AttributeError:
        term_time = "0110"  # 기본값 오전 1시 10분
        
    # 현재 시각
    current_time = datetime.now(pytz.timezone('Asia/Seoul'))
    # 현재 시각과 push_time 같은 형식으로 맞추기
    current_time_str = current_time.strftime('%H%M')

    # 현재 시각과 term_time이 같으면 gpt ai에게 질문 전송.
    if current_time_str == term_time:
        try:
            gpt_today_job()
            gpt_ai_logger.info(f"현재 시각: {current_time_str} | 발송 시간: {term_time} => Gpt AI가 동작할 시간입니다.")
        except Exception as e:
            gpt_ai_logger.error(f"Gpt AI 작동 중 오류 발생: {e}")
    else:
        gpt_ai_logger.info(f"현재 시각: {current_time_str} | 발송 시간: {term_time} => Gpt AI가 동작할 시간이 아닙니다.")