from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from portal import db, login_manager, app
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    register_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    activate_on = db.Column(db.DateTime)
    roles_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False, default=1)
    guru = db.relationship('Kehadiran', lazy='dynamic', backref='guru')

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return "User('{self.username}', '{self.email}', '{self.image_file}')"

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    roles = db.Column(db.String(20), nullable=False)
    users = db.relationship('User', backref='level', lazy=True)

class Kehadiran(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    siswa_id = db.Column(db.Integer, db.ForeignKey('siswa.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    mapel_id = db.Column(db.Integer, db.ForeignKey('mapel.id'))
    absen_id = db.Column(db.Integer, db.ForeignKey('absen.id'))
    waktu_absen = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    siswas = db.relationship('Siswa', backref='kehadiran_siswa', lazy=True)
    # user = db.relationship('User', backref='pengabsen', lazy=True)
    mapel = db.relationship('Mapel', backref='mata_pelajaran', lazy=True)
    absen = db.relationship('Absen', backref='data_absen', lazy=True)

class Guru(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    tgl_lahir = db.Column(db.DateTime, nullable=False)
    agama_id = db.Column(db.Integer, db.ForeignKey('agama.id'), nullable=False)
    jenis_kelamin_id = db.Column(db.Integer, db.ForeignKey('jenis_kelamin.id'), nullable=False)
    alamat = db.Column(db.Text, nullable=False)
    image_thumb = db.Column(db.String(255), nullable=False, default='default.jpg')
    slug = db.Column(db.String(255), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    jadwal_mapel = db.relationship('JadwalMapel', backref='jadwal_guru', lazy=True)


class Siswa(db.Model):
    # query_class = PostQuery
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(255), nullable=False)
    jenis_kelamin_id = db.Column(db.Integer, db.ForeignKey('jenis_kelamin.id'), nullable=False)
    agama_id = db.Column(db.Integer, db.ForeignKey('agama.id'), nullable=False)
    tgl_lahir = db.Column(db.DateTime, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    alamat = db.Column(db.Text, nullable=False)
    image_thumb = db.Column(db.String(255), nullable=False, default='default.jpg')
    slug = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean(), nullable=False, server_default='1')
    kelas_id = db.Column(db.Integer, db.ForeignKey('kelas.id'))
    # absensi = db.relationship('Kehadiran', lazy='dynamic', backref='pelajar')
    spp_siswa = db.relationship('PembayaranSpp', backref='spp_siswa', lazy=True)
    absensi = db.relationship('Absen', secondary='kehadiran')
    nilai_ujian = db.relationship('NilaiUjian', backref='nilai_ujian')

    def __repr__(self):
        return "Siswa('{self.nama}', '{self.date_posted}')"

class JenisKelamin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kelamin = db.Column(db.String(255), nullable=False)
    siswas = db.relationship('Siswa', backref='kelamin', lazy=True)
    guru = db.relationship('Guru', backref='kelamin_guru', lazy=True)

    def __repr__(self):
        return "Post('{self.kelamin}')"

class Agama(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    agama = db.Column(db.String(255), nullable=False)
    siswas = db.relationship('Siswa', backref='agama_siswa', lazy=True)
    guru = db.relationship('Guru', backref='agama_guru', lazy=True)

    def __repr__(self):
        return "Post('{self.agama}')"

class Mapel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(255), nullable=False)
    absen_mapel = db.relationship('Absen', secondary='kehadiran')
    jadwal_mapel = db.relationship('JadwalMapel', backref='jadwal_mapel', lazy=True)

class Kelas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(255), nullable=False)
    siswas = db.relationship('Siswa', backref='kelas_siswa', lazy=True)
    jadwal_kelas = db.relationship('JadwalMapel', backref='jadwal_kelas', lazy=True)

class Absen(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(255), nullable=False)
    siswa = db.relationship('Kehadiran', backref='absen_siswa', lazy=True)

class JadwalMapel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mapel_id = db.Column(db.Integer, db.ForeignKey('mapel.id'), nullable=False)
    kelas_id = db.Column(db.Integer, db.ForeignKey('kelas.id'), nullable=False)
    guru_id = db.Column(db.Integer, db.ForeignKey('guru.id'), nullable=False)
    hari = db.Column(db.String(8), nullable=False)
    mulai = db.Column(db.Time, nullable=False)
    akhir = db.Column(db.Time, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class JadwalUjian(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mapel_id = db.Column(db.Integer, db.ForeignKey('mapel.id'), nullable=False)
    kelas_id = db.Column(db.Integer, db.ForeignKey('kelas.id'), nullable=False)
    waktu_ujian = db.Column(db.DateTime, nullable=False)
    akhir_ujian = db.Column(db.DateTime, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    nilai = db.relationship('NilaiUjian', backref='jadwal_ujian', lazy=True)

class NilaiUjian(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    siswa_id = db.Column(db.Integer, db.ForeignKey('siswa.id'), nullable=False)
    jadwal_ujian_id = db.Column(db.Integer, db.ForeignKey('jadwal_ujian.id'), nullable=False)
    nilai = db.Column(db.Float)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class UangSpp(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nilai = db.Column(db.Numeric(precision=8, asdecimal=False, decimal_return_scale=None))
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    edit_posted = db.Column(db.DateTime)
    pembayaran_spp = db.relationship('PembayaranSpp', backref='pembayaran_spp', lazy=True)

class PembayaranSpp(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    siswa_id = db.Column(db.Integer, db.ForeignKey('siswa.id'), nullable=False)
    dibayarkan = db.Column(db.Boolean, default=False)
    beasiswa = db.Column(db.Boolean, default=False)
    uangspp_id = db.Column(db.Integer, db.ForeignKey('uang_spp.id'), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)