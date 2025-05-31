from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from app.models.user import User

class LoginForm(FlaskForm):
    username = StringField('Tên đăng nhập', validators=[DataRequired()])
    password = PasswordField('Mật khẩu', validators=[DataRequired()])
    remember_me = BooleanField('Ghi nhớ đăng nhập')
    submit = SubmitField('Đăng nhập')

class RegistrationForm(FlaskForm):
    username = StringField('Tên đăng nhập', validators=[
        DataRequired(),
        Length(min=4, max=64)
    ])
    email = StringField('Email', validators=[
        DataRequired(),
        Email(),
        Length(max=120)
    ])
    full_name = StringField('Họ và tên', validators=[
        DataRequired(),
        Length(max=120)
    ])
    password = PasswordField('Mật khẩu', validators=[
        DataRequired(),
        Length(min=8, message='Mật khẩu phải có ít nhất 8 ký tự')
    ])
    password2 = PasswordField('Xác nhận mật khẩu', validators=[
        DataRequired(),
        EqualTo('password', message='Mật khẩu không khớp')
    ])
    submit = SubmitField('Đăng ký')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Tên đăng nhập đã được sử dụng.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Email đã được sử dụng.')

class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Yêu cầu đặt lại mật khẩu')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Mật khẩu mới', validators=[
        DataRequired(),
        Length(min=8, message='Mật khẩu phải có ít nhất 8 ký tự')
    ])
    password2 = PasswordField('Xác nhận mật khẩu mới', validators=[
        DataRequired(),
        EqualTo('password', message='Mật khẩu không khớp')
    ])
    submit = SubmitField('Đặt lại mật khẩu') 