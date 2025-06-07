import os
import requests
from datetime import datetime
import time
import logging
from flask import current_app

logger = logging.getLogger(__name__)

def transcribe_audio(file_path):
    """
    OpenAI Whisper API를 사용하여 오디오 파일을 텍스트로 변환합니다.
    
    Args:
        file_path (str): 변환할 오디오 파일의 경로
        
    Returns:
        dict: 변환 결과를 포함하는 딕셔너리
            - text: 변환된 텍스트
            - segments: 세그먼트별 변환 결과
            - language: 감지된 언어
    """
    try:
        # OpenAI API 키 확인
        api_key = current_app.config['OPENAI_API_KEY']
        logger.info(f"API 키 존재 여부: {'있음' if api_key else '없음'}")
        
        if not api_key:
            logger.error("OPENAI_API_KEY가 설정되지 않았습니다.")
            raise Exception("OPENAI_API_KEY가 설정되지 않았습니다.")

        # 파일 크기 확인 (25MB 제한)
        file_size = os.path.getsize(file_path)
        logger.info(f"파일 크기: {file_size / (1024*1024):.2f}MB")
        if file_size > 25 * 1024 * 1024:  # 25MB
            logger.error(f"파일 크기가 25MB를 초과합니다: {file_size / (1024*1024):.2f}MB")
            raise Exception("파일 크기가 25MB를 초과합니다.")

        # 파일 업로드
        headers = {
            "Authorization": f"Bearer {api_key}"
        }
        
        logger.info("OpenAI API 호출 시작...")
        with open(file_path, "rb") as audio_file:
            files = {
                "file": (os.path.basename(file_path), audio_file, "audio/mpeg"),
                "model": (None, "whisper-1"),
                "language": (None, "ko"),
                "response_format": (None, "verbose_json")
            }
            
            response = requests.post(
                "https://api.openai.com/v1/audio/transcriptions",
                headers=headers,
                files=files
            )
            
            logger.info(f"API 응답 상태 코드: {response.status_code}")
            if response.status_code != 200:
                logger.error(f"API 호출 실패: {response.text}")
                raise Exception(f"API 호출 실패: {response.text}")

            result = response.json()
            logger.info("변환 완료")
            
            return {
                'text': result['text'],
                'segments': result['segments'],
                'language': result['language']
            }
            
    except Exception as e:
        logger.error(f"음성 변환 중 오류 발생: {str(e)}")
        raise Exception(f"음성 변환 중 오류가 발생했습니다: {str(e)}") 