import whisper
import os
import numpy as np
from datetime import datetime
import torch

def transcribe_audio(file_path):
    """
    오디오 파일을 텍스트로 변환합니다.
    청크 단위로 처리하여 메모리 사용량을 최적화합니다.
    
    Args:
        file_path (str): 변환할 오디오 파일의 경로
        
    Returns:
        dict: 변환 결과를 포함하는 딕셔너리
            - text: 변환된 텍스트
            - segments: 세그먼트별 변환 결과
            - language: 감지된 언어
    """
    try:
        # Whisper tiny 모델 로드 (메모리 사용량 최소화)
        model = whisper.load_model("tiny")
        
        # 오디오 파일을 청크로 나누어 처리
        audio = whisper.load_audio(file_path)
        
        # 30초 단위로 청크 분할
        chunk_length = 30 * 16000  # 30초 * 16000Hz
        chunks = [audio[i:i + chunk_length] for i in range(0, len(audio), chunk_length)]
        
        # 각 청크 처리
        all_text = []
        all_segments = []
        
        for i, chunk in enumerate(chunks):
            # 청크 패딩
            chunk = whisper.pad_or_trim(chunk)
            
            # 변환 실행
            result = model.transcribe(chunk)
            
            # 결과 저장
            all_text.append(result['text'])
            
            # 세그먼트 시간 조정
            for segment in result['segments']:
                segment['start'] += i * 30
                segment['end'] += i * 30
                all_segments.append(segment)
            
            # 메모리 해제
            del chunk
            torch.cuda.empty_cache() if torch.cuda.is_available() else None
        
        return {
            'text': ' '.join(all_text),
            'segments': all_segments,
            'language': result['language']
        }
    except Exception as e:
        raise Exception(f"음성 변환 중 오류가 발생했습니다: {str(e)}")
    finally:
        # 메모리 정리
        if 'model' in locals():
            del model
        torch.cuda.empty_cache() if torch.cuda.is_available() else None 