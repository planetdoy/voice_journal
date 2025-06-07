from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app, send_from_directory, jsonify
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from app.models.conversion import Conversion
from app.models.daily_usage import DailyUsage as DailyUsageModel
from app.utils.whisper import transcribe_audio
from app import db
import logging

logger = logging.getLogger(__name__)

bp = Blueprint('main', __name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'mp3', 'wav', 'm4a', 'ogg'}

@bp.route('/')
@login_required
def index():
    # 사용자의 변환 기록 가져오기
    conversions = Conversion.query.filter_by(user_id=current_user.id).order_by(Conversion.created_at.desc()).all()
    return render_template('main/index.html', conversions=conversions)

@bp.route('/upload', methods=['POST'])
@login_required
def upload_file():
    logger.info("파일 업로드 요청 받음")
    
    if 'file' not in request.files:
        logger.error("파일이 없음")
        return jsonify({
            'success': False,
            'message': '파일이 없습니다.'
        })
    
    file = request.files['file']
    if file.filename == '':
        logger.error("선택된 파일이 없음")
        return jsonify({
            'success': False,
            'message': '선택된 파일이 없습니다.'
        })
    
    if not allowed_file(file.filename):
        logger.error("허용되지 않은 파일 형식")
        return jsonify({
            'success': False,
            'message': '허용되지 않은 파일 형식입니다.'
        })
    
    try:
        # 오늘의 사용량 확인
        today = datetime.utcnow().date()
        daily_usage = DailyUsageModel.query.filter_by(
            user_id=current_user.id,
            date=today
        ).first()
        
        if not daily_usage:
            daily_usage = DailyUsageModel(user_id=current_user.id, date=today)
            db.session.add(daily_usage)
        
        if daily_usage.count is None:
            daily_usage.count = 0
        
        if daily_usage.count >= 5:  # 일일 5회 제한
            logger.error("일일 사용량 초과")
            return jsonify({
                'success': False,
                'message': '일일 변환 횟수를 초과했습니다.'
            })
        
        # 파일 저장
        filename = secure_filename(file.filename)
        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        saved_filename = f"{timestamp}_{filename}"
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], saved_filename)
        file.save(file_path)
        logger.info(f"파일 저장 완료: {file_path}")
        
        # 음성 변환
        logger.info("음성 변환 시작")
        result = transcribe_audio(file_path)
        logger.info("음성 변환 완료")
        
        # 변환 결과 저장
        conversion = Conversion(
            user_id=current_user.id,
            original_filename=saved_filename,
            text=result['text'],
            language=result['language']
        )
        db.session.add(conversion)
        
        # 사용량 증가
        daily_usage.count += 1
        
        db.session.commit()
        logger.info("변환 결과 저장 완료")
        
        return jsonify({
            'success': True,
            'message': '파일이 성공적으로 변환되었습니다.'
        })
        
    except Exception as e:
        logger.error(f"변환 중 오류 발생: {str(e)}")
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'변환 중 오류가 발생했습니다: {str(e)}'
        })

@bp.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)

@bp.route('/delete/<int:conversion_id>', methods=['POST'])
@login_required
def delete_conversion(conversion_id):
    conversion = Conversion.query.get_or_404(conversion_id)
    if conversion.user_id != current_user.id:
        flash('권한이 없습니다.', 'error')
        return redirect(url_for('main.index'))
    
    db.session.delete(conversion)
    db.session.commit()
    flash('변환 기록이 삭제되었습니다.', 'success')
    return redirect(url_for('main.index'))

@bp.route('/update_title', methods=['POST'])
@login_required
def update_title():
    conversion_id = request.form.get('conversion_id')
    title = request.form.get('title')
    
    conversion = Conversion.query.get_or_404(conversion_id)
    if conversion.user_id != current_user.id:
        return jsonify({'success': False, 'message': '권한이 없습니다.'})
    
    conversion.title = title
    db.session.commit()
    
    return jsonify({'success': True})

@bp.route('/update_text', methods=['POST'])
@login_required
def update_text():
    conversion_id = request.form.get('conversion_id')
    text = request.form.get('text')
    
    conversion = Conversion.query.get_or_404(conversion_id)
    if conversion.user_id != current_user.id:
        return jsonify({'success': False, 'message': '권한이 없습니다.'})
    
    conversion.text = text
    db.session.commit()
    
    return jsonify({'success': True})

@bp.route('/history')
@login_required
def history():
    # 사용자의 변환 기록 가져오기
    conversions = Conversion.query.filter_by(user_id=current_user.id).order_by(Conversion.created_at.desc()).all()
    return render_template('main/history.html', conversions=conversions) 