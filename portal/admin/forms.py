from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms.fields.html5 import DateField, IntegerField
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from portal.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(message='Tidak boleh kosong'), Length(min=3, max=20, message='Nama harus berada 3-20 karakter')])
    email = StringField('Email',
                        validators=[DataRequired(), Email()], render_kw={"placeholder": "Email"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Password"})
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')], render_kw={"placeholder": "Confirm Password"})
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email sudah terdaftar, silahkan gunakan email yang lain.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()], render_kw={"placeholder": "Email"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Password"})
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email sudah didaftarkan, coba yang lain')

class SiswaForm(FlaskForm):
    nama = StringField('Nama Lengkap', validators=[DataRequired()])
    tanggal_lahir = DateField('Tanggal lahir', validators=[DataRequired()], format='%Y-%m-%d')
    jenis_kelamin = SelectField('Jenis Kelamin', validators=[DataRequired()], choices = [])
    agama = SelectField('Agama', validators=[DataRequired()], choices = [])
    kelas = SelectField('Kelas', validators=[DataRequired()], choices = [])
    alamat = TextAreaField('Alamat', validators=[DataRequired()])
    thumbnail = FileField('Upload Foto', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    is_aktif = BooleanField('Aktif', default=True)
    # multiple_company = AjaxSelectMultipleField(
    #     loader=tag_loader,
    #     label='Masukkan Tags',
    #     allow_blank=False
    # )
    submit = SubmitField('Submit')

class KelasMapelAgamaForm(FlaskForm):
    nama = StringField('Nama', validators=[DataRequired()])
    submit = SubmitField('Submit')

class KategoriForm(FlaskForm):
    nama = StringField('Nama kategori', validators=[DataRequired()])
    is_gutters = BooleanField('Jadikan Gutters', default=False)
    submit = SubmitField('Submit')

    def validate_nama(form, field):
        if len(field.data) < 3:
            raise ValidationError('Nama harus lebih dari 3 huruf')

class TopikForm(FlaskForm):
    nama = StringField('Nama Topik', validators=[DataRequired()])
    submit = SubmitField('Submit')

class CommentForm(FlaskForm):
    comment = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField('Comments')

class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')

class SppForm(FlaskForm):
    nama = IntegerField('Uang SPP', validators=[DataRequired(message='Masukkan nilai yang harus dibayarkan siswa, cth: 250000 ')])
    submit = SubmitField('Submit')