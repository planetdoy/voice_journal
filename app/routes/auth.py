from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from app import db
from app.models.user import User
from app.forms import RegistrationForm, LoginForm, ResetPasswordRequestForm, ResetPasswordForm
from app.utils.email import send_verification_email, send_password_reset_email
import secrets

bp = Blueprint('auth', __name__)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        # 이메일 중복 확인
        if User.query.filter_by(email=form.email.data).first():
            flash('이미 등록된 이메일 주소입니다.', 'error')
            return redirect(url_for('auth.register'))
        
        # 토큰 생성
        token = secrets.token_urlsafe(32)
        
        # 사용자 생성
        user = User(
            email=form.email.data,
            verification_token=token
        )
        user.set_password(form.password.data)
        
        db.session.add(user)
        db.session.commit()
        
        # 이메일 발송
        send_verification_email(user.email, token)
        
        flash('회원가입이 완료되었습니다. 이메일을 확인하여 계정을 인증해주세요.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', form=form)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('이메일 또는 비밀번호가 올바르지 않습니다.', 'error')
            return redirect(url_for('auth.login'))
        
        if not user.is_verified:
            flash('이메일 인증이 필요합니다. 이메일을 확인해주세요.', 'warning')
            return redirect(url_for('auth.login'))
        
        login_user(user)
        next_page = request.args.get('next')
        return redirect(next_page or url_for('main.index'))
    
    return render_template('auth/login.html', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/verify/<token>')
def verify_email(token):
    user = User.query.filter_by(verification_token=token).first()
    if user is None:
        flash('유효하지 않은 인증 링크입니다.', 'error')
        return redirect(url_for('auth.login'))
    
    user.is_verified = True
    user.verification_token = None
    db.session.commit()
    
    flash('이메일 인증이 완료되었습니다. 로그인해주세요.', 'success')
    return redirect(url_for('auth.login'))

@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('비밀번호 재설정 이메일이 발송되었습니다.', 'info')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/reset_password_request.html', form=form)

@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    # 토큰 검증 로직 구현 필요
    form = ResetPasswordForm()
    if form.validate_on_submit():
        # 비밀번호 재설정 로직 구현 필요
        flash('비밀번호가 재설정되었습니다.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/reset_password.html', form=form) 