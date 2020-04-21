from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms.fields.html5 import DateField
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, IntegerField
from wtforms_components import TimeField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

class JadwalBelajarForm(FlaskForm):
    mapel = SelectField('Mata Pelajaran', validators=[DataRequired()], choices = [])
    kelas = SelectField('Kelas', validators=[DataRequired()], choices = [])
    guru = SelectField('Guru', validators=[DataRequired()], choices = [])
    hari = SelectField('Hari', validators=[DataRequired()], choices = [('Senin','Senin'),('Selasa','Selasa'),('Rabu','Rabu'),('Kamis','Kamis'),('Jumat','Jumat'),('Sabtu','Sabtu'),('Minggu','Minggu')])
    mulai = TimeField('Mulai', validators=[DataRequired(message='Isi jam mulai belajar')])
    akhir = TimeField('Akhir', validators=[DataRequired(message='Isi jam akhir belajar')])
    submit = SubmitField('Submit')