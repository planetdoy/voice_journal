from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError

class RegistrationForm(FlaskForm):
    email = StringField('이메일', validators=[
        DataRequired(),
        Email(message='유효한 이메일 주소를 입력해주세요.')
    ])
    password = PasswordField('비밀번호', validators=[
        DataRequired(),
        Length(min=6, message='비밀번호는 최소 6자 이상이어야 합니다.')
    ])
    password2 = PasswordField('비밀번호 확인', validators=[
        DataRequired(),
        EqualTo('password', message='비밀번호가 일치하지 않습니다.')
    ])
    submit = SubmitField('회원가입')

class LoginForm(FlaskForm):
    email = StringField('이메일', validators=[
        DataRequired(),
        Email(message='유효한 이메일 주소를 입력해주세요.')
    ])
    password = PasswordField('비밀번호', validators=[DataRequired()])
    submit = SubmitField('로그인')

class ResetPasswordRequestForm(FlaskForm):
    email = StringField('이메일', validators=[
        DataRequired(),
        Email(message='유효한 이메일 주소를 입력해주세요.')
    ])
    submit = SubmitField('비밀번호 재설정 요청')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('새 비밀번호', validators=[
        DataRequired(),
        Length(min=6, message='비밀번호는 최소 6자 이상이어야 합니다.')
    ])
    password2 = PasswordField('비밀번호 확인', validators=[
        DataRequired(),
        EqualTo('password', message='비밀번호가 일치하지 않습니다.')
    ])
    submit = SubmitField('비밀번호 재설정')

class UploadForm(FlaskForm):
    audio_file = FileField('음성 파일', validators=[
        DataRequired(message='파일을 선택해주세요.')
    ])
    submit = SubmitField('변환하기')

    def validate_audio_file(self, field):
        if field.data:
            # 파일 확장자 검사
            allowed_extensions = {'mp3', 'wav', 'm4a', 'ogg'}
            filename = field.data.filename
            if '.' not in filename or \
               filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
                raise ValidationError('지원하지 않는 파일 형식입니다. (지원 형식: mp3, wav, m4a, ogg)') 