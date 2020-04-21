from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms.fields.html5 import DateField
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

class GuruForm(FlaskForm):
    nama = StringField('Nama Lengkap', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(message='Email dibutuhkan')])
    tanggal_lahir = DateField('Tanggal lahir', validators=[DataRequired()], format='%Y-%m-%d')
    alamat = TextAreaField('Alamat', validators=[DataRequired()])
    jenis_kelamin = SelectField('Jenis Kelamin', validators=[DataRequired()], choices = [])
    agama = SelectField('Agama', validators=[DataRequired()], choices = [])
    thumbnail = FileField('Upload Foto', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    submit = SubmitField('Submit')