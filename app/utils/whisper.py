import whisper
import os
from datetime import datetime

def transcribe_audio(file_path):
    """
    오디오 파일을 텍스트로 변환합니다.
    
    Args:
        file_path (str): 변환할 오디오 파일의 경로
        
    Returns:
        dict: 변환 결과를 포함하는 딕셔너리
            - text: 변환된 텍스트
            - segments: 세그먼트별 변환 결과
            - language: 감지된 언어
    """
    try:
        # Whisper 모델 로드 (base 모델 사용)
        model = whisper.load_model("base")
        
        # 오디오 파일 변환
        result = model.transcribe(file_path)
        
        return {
            'text': result['text'],
            'segments': result['segments'],
            'language': result['language']
        }
    except Exception as e:
        raise Exception(f"음성 변환 중 오류가 발생했습니다: {str(e)}") 