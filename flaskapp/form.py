from flask.app import Flask
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, validators
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskapp.models import signup

class SignUp(FlaskForm):
    username = StringField('Istifadeci Adi',
                           validators=[DataRequired(), Length(min=2, max=20)],render_kw={"placeholder": "Istifadeci adi"})
    email = StringField('Email', validators=[validators.Email(message="Xahiş edirik doğru bir email daxil edin!")], render_kw={"placeholder": "you@example.com"})
    password = PasswordField('Parol', validators=[DataRequired()], render_kw={"placeholder": "Parol"})
    confirm_password = PasswordField('Tekrar Parol',
                                     validators=[DataRequired(), EqualTo('password')], render_kw={"placeholder": "Təkrar parol"})

    submit = SubmitField('Hesab Yarat')

    def validate_username(self, username):
        user = signup.query.filter_by(username=username.data).first()

        if user:
            raise ValidationError('Bu istifadeci adi mövcuddur xahis edirik başqa istifadeci adi daxil edin!', "danger")

    def validate_email(self,email):
        email_data = signup.query.filter_by(email = email.data).first()
        if email_data:
            raise ValidationError("Bu email mövcuddur!",'danger')







class Login(FlaskForm):
    username = StringField('İstifadeəçi adı',
                           validators=[DataRequired(), Length(min=2, max=20)],render_kw={"placeholder": "İstifadəçi adı"})

    password = PasswordField('Parol', validators=[DataRequired()], render_kw={"placeholder": "Parol"})

    submit = SubmitField('Login')

class UpdateInfo(FlaskForm):
    username = StringField('Istifadeci Adi',
                           validators=[DataRequired(), Length(min=2, max=20)],render_kw={"placeholder": "Istifadeci adi"})
    email = StringField('Email',
                        validators=[DataRequired(), Email()], render_kw={"placeholder": "you@example.com"})

    submit = SubmitField('Yenile')
class CreateArticle(FlaskForm):
    title = StringField('Məqalə başlığı',
                           validators=[DataRequired(), Length(min=2, max=20)])
    content = TextAreaField('Mövzu',
                        validators=[DataRequired()])




    submit = SubmitField('Təsdiqlə')

class ForgotPassword(FlaskForm):
    username = StringField('Istifadeci Adi',
                           validators=[DataRequired(), Length(min=2, max=20)],render_kw={"placeholder": "Istifadeci adi"})

    password = PasswordField('Parol', validators=[DataRequired()], render_kw={"placeholder": "Parol"})

    confirm_password = PasswordField('Tekrar Parol',
                                     validators=[DataRequired(), EqualTo('password')])


class ApprovePass(FlaskForm):
    approve = StringField('Dogrulama Kodu',
                           validators=[DataRequired(), Length(min=2, max=20)],render_kw={"placeholder": "Dogrulama kodu"})

    submit = SubmitField('Tesdiq')




