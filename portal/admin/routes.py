import os
import secrets
import datetime
from dateutil import relativedelta
import calendar
from flask import render_template, url_for, flash, redirect, request, abort, Markup, send_from_directory, jsonify, Blueprint
from PIL import Image
from portal import app, db, bcrypt, mail
from portal.models import User, Kehadiran, Siswa, Mapel, Absen, Agama, Kelas, JenisKelamin, Role, UangSpp, PembayaranSpp
from portal.admin.forms import RegistrationForm, LoginForm, UpdateAccountForm, SiswaForm, RequestResetForm, ResetPasswordForm, CommentForm, KategoriForm, TopikForm, KelasMapelAgamaForm, SppForm
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
from sqlalchemy import func

admin = Blueprint('admin', __name__)

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/upload/img_thumbnail', picture_fn)

    output_size = (400, 400)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@admin.route("/admin2451")
@login_required
def panel():
    today = datetime.datetime.today()

    mulai_bulan_ini = today - datetime.timedelta(days=today.day - 1)
    akhir_tgl_bulan_ini = calendar.monthrange(today.year, today.month)[1]
    tgl_bln_akhir_ini = datetime.date(today.year, today.month, akhir_tgl_bulan_ini)

    bulan_lalu = datetime.date.today() - relativedelta.relativedelta(months=1)
    mulai_bulan_lalu = bulan_lalu - datetime.timedelta(days=datetime.date.today().day - 1)
    tgl_terakhir_lalu = calendar.monthrange(bulan_lalu.year, bulan_lalu.month)[1]
    format_tgl_terakhir_lalu = datetime.date(bulan_lalu.year, bulan_lalu.month, tgl_terakhir_lalu)

    siswas = Siswa.query.all()
    total_agama = Agama.query.all()
    gender = JenisKelamin.query.all()
    uang_spp = UangSpp.query.order_by(UangSpp.date_posted.desc()).first()

    total_spp_bulan_lalu = PembayaranSpp.query.filter(PembayaranSpp.date_posted.between(mulai_bulan_lalu, format_tgl_terakhir_lalu), PembayaranSpp.dibayarkan==True).all()
    sum_bulan_lalu = 0
    for s in total_spp_bulan_lalu:
        sum_bulan_lalu += s.pembayaran_spp.nilai


    total_spp_bulan_ini = PembayaranSpp.query.filter(PembayaranSpp.date_posted.between(mulai_bulan_ini.date(), tgl_bln_akhir_ini), PembayaranSpp.dibayarkan==True).all()
    sum_bulan_ini = 0
    for s in total_spp_bulan_ini:
        sum_bulan_ini += s.pembayaran_spp.nilai
    return render_template('admin/home.html', siswas=siswas, total_agama=total_agama, gender=gender, uang_spp=uang_spp, sum_bulan_ini=sum_bulan_ini, sum_bulan_lalu=sum_bulan_lalu)

@admin.route("/daftar-siswa")
@login_required
def daftar_siswa():
    siswas = Siswa.query.all()
    total_agama = Agama.query.all()
    gender = JenisKelamin.query.all()
    return render_template('admin/daftar_siswa.html', siswas=siswas)

@admin.route("/tambah_siswa", methods=['GET', 'POST'])
@login_required
def tambah_siswa():
    form = SiswaForm()
    form.jenis_kelamin.choices = [(str(kelamin.id), kelamin.kelamin)for kelamin in JenisKelamin.query.all()]
    form.jenis_kelamin.choices.insert(0,('', '== Jenis Kelamin =='))
    form.agama.choices = [(str(agama.id), agama.agama.title())for agama in Agama.query.all()]
    form.agama.choices.insert(0,('', '== Agama =='))
    form.kelas.choices = [(str(kelas.id), kelas.nama.title())for kelas in Kelas.query.all()]
    form.kelas.choices.insert(0,('', '== Kelas =='))
    if form.validate_on_submit():
        siswa = Siswa(nama=form.nama.data, jenis_kelamin_id=form.jenis_kelamin.data, agama_id=form.agama.data, tgl_lahir=form.tanggal_lahir.data, alamat=form.alamat.data, slug=slugify(form.nama.data), kelas_id=form.kelas.data)
        db.session.add(siswa)
        db.session.commit()
        flash('Data siswa berhasil ditambahkan', 'is-success')
        return redirect(url_for('admin.panel'))
    return render_template('admin/create_siswa.html', form=form, title='Tambah Siswa')

@admin.route("/edit_siswa/<int:id>/edit", methods=['GET', 'POST'])
@login_required
def edit_siswa(id):
    siswa = Siswa.query.get_or_404(id)
    form = SiswaForm(jenis_kelamin=siswa.jenis_kelamin_id, agama=siswa.agama_id)
    form.jenis_kelamin.choices = [(str(kelamin.id), kelamin.kelamin)for kelamin in JenisKelamin.query.all()]
    form.agama.choices = [(str(agama.id), agama.agama.title())for agama in Agama.query.all()]
    form.kelas.choices = [(str(kelas.id), kelas.nama)for kelas in Kelas.query.all()]
    if form.validate_on_submit():
        siswa.nama = form.nama.data
        siswa.tgl_lahir = form.tanggal_lahir.data
        siswa.alamat = form.alamat.data
        siswa.jenis_kelamin_id = form.jenis_kelamin.data
        siswa.agama_id = form.agama.data
        siswa.kelas_id = form.kelas.data
        db.session.commit()
        flash('Data Siswa berhasil diupdate', 'is-success')
        return redirect(url_for('admin.panel'))
    elif request.method == 'GET':
        form.nama.data = siswa.nama
        form.tanggal_lahir.data = siswa.tgl_lahir
        form.alamat.data = siswa.alamat
    return render_template('admin/create_siswa.html', form=form, title='Edit Siswa')

@admin.route("/siswa/delete/<int:id>", methods=['POST'])
@login_required
def delete_siswa(id):
    siswa = Siswa.query.get(id)
    db.session.delete(siswa)
    db.session.commit()
    flash('Data Siswa berhasil dihapus', 'is-success')
    return redirect(url_for('admin.panel'))

@admin.route("/siswa/detail/<int:id>", methods=['GET', 'POST'])
@login_required
def siswa_detail(id):
    data = {}
    siswa = Siswa.query.get_or_404(id)
    data['id'] = siswa.id
    data['kelamin'] = siswa.kelamin.kelamin
    data['lahir'] = siswa.tgl_lahir.strftime('%d %B %Y')
    data['agama'] = siswa.agama_siswa.agama
    data['alamat'] = siswa.alamat
    data['image'] = url_for('static', filename='img/'+siswa.image_thumb)
    data['kelas'] = siswa.kelas_siswa.nama
    return jsonify(data)

@admin.route("/siswa/data-absen/<int:id>", methods=['GET', 'POST'])
@login_required
def siswa_absen(id):
    siswa = Siswa.query.get_or_404(id)
    absen = Absen.query.all()
    return render_template('admin/siswa_detail.html', siswa=siswa, absen=absen)


@admin.route("/daftar_kelas", methods=['GET', 'POST'])
@login_required
def daftar_kelas():
    kelas = Kelas.query.all()
    return render_template('admin/daftar_kelas.html', kelas=kelas)

@admin.route("/tambah_kelas", methods=['GET', 'POST'])
@login_required
def tambah_kelas():
    form = KelasMapelAgamaForm()
    if form.validate_on_submit():
        kelas = Kelas(nama=form.nama.data)
        db.session.add(kelas)
        db.session.commit()
        flash('Kelas berhasil ditambahkan', 'is-success')
        return redirect(url_for('admin.daftar_kelas'))
    return render_template('admin/kelas_mapel.html', form=form)

@admin.route("/tambah_agama", methods=['GET', 'POST'])
@login_required
def tambah_agama():
    form = KelasMapelAgamaForm()
    if form.validate_on_submit():
        agama = Agama(nama=form.nama.data)
        db.session.add(agama)
        db.session.commit()
    return render_template('admin/kelas_mapel.html', form=form)

@admin.route("/daftar_mapel")
@login_required
def daftar_mapel():
    mapel = Mapel.query.all()
    return render_template('admin/daftar_mapel.html', mapel=mapel)

@admin.route("/tambah_mapel", methods=['GET', 'POST'])
@login_required
def tambah_mapel():
    form = KelasMapelAgamaForm()
    if form.validate_on_submit():
        mapel = Mapel(nama=form.nama.data)
        db.session.add(mapel)
        db.session.commit()
        flash('Mata pelajaran berhasil ditambahkan', 'is-success')
        return redirect(url_for('admin.daftar_mapel'))
    return render_template('admin/kelas_mapel.html', form=form)

@admin.route("/role")
@login_required
def role():
    role = Role.query.all()
    return render_template('admin/role.html', role=role)

@admin.route("/tambah-role", methods=['GET', 'POST'])
@login_required
def tambah_role():
    form = KelasMapelAgamaForm()
    if form.validate_on_submit():
        role = Role(roles=form.nama.data)
        db.session.add(role)
        db.session.commit()
        flash('Role berhasil ditambahkan', 'is-success')
        return redirect(url_for('admin.role'))
    return render_template('admin/kelas_mapel.html', form=form)

@admin.route("/tambah-spp", methods=['GET', 'POST'])
@login_required
def tambah_spp():
    form = SppForm()
    if form.validate_on_submit():
        spp = UangSpp(nilai=form.nama.data)
        db.session.add(spp)
        db.session.commit()
        flash('Data Uang SPP berhasil ditambahkan', 'is-success')
        return redirect(url_for('admin.daftar_siswa'))
    return render_template('admin/kelas_mapel.html', form=form)

@admin.route("/bayar-spp")
@login_required
def bayar_spp():
    today = datetime.datetime.today()
    mulai_bulan_ini = today - datetime.timedelta(days=today.day - 1)
    akhir_tgl = calendar.monthrange(today.year, today.month)[1]
    tgl_bln_akhir = datetime.date(today.year, today.month, akhir_tgl)

    siswas = Siswa.query.all()
    uang_spp = UangSpp.query.order_by(UangSpp.date_posted.desc()).first()
    for siswa in siswas:
        cek_spp = PembayaranSpp.query.filter(PembayaranSpp.date_posted.between(mulai_bulan_ini.date(), tgl_bln_akhir), PembayaranSpp.siswa_id==siswa.id).first()
        if not cek_spp:
            input_spp = PembayaranSpp(siswa_id=siswa.id, uangspp_id=uang_spp.id)
            db.session.add(input_spp)
    db.session.commit()

    siswas = PembayaranSpp.query.filter(PembayaranSpp.date_posted.between(mulai_bulan_ini.date(), tgl_bln_akhir)).order_by(PembayaranSpp.dibayarkan==True).all()
    total_agama = Agama.query.all()
    gender = JenisKelamin.query.all()
    spp_terakhir = UangSpp.query.order_by(UangSpp.date_posted.desc()).first()
    return render_template('admin/bayar_spp.html', siswas=siswas, today=today, spp_terakhir=spp_terakhir)

@admin.route("/update-spp/<int:id>", methods=['GET', 'POST'])
@login_required
def update_spp(id):
    uang_spp = UangSpp.query.order_by(UangSpp.date_posted.desc()).first()
    cek_spp = PembayaranSpp.query.get_or_404(id)
    if cek_spp.dibayarkan == True:
        cek_spp.dibayarkan = False
    else:
        cek_spp.dibayarkan = True
    db.session.commit()
    flash('Data siswa berhasil diupdate', 'is-success')
    return redirect(url_for('admin.bayar_spp'))

@admin.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'is-success')
        return redirect(url_for('admin.login'))
    return render_template('admin/register.html', title='Register', form=form)


@admin.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.panel'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('admin.panel'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'is-danger')
    return render_template('admin/login.html', title='Login', form=form)

@admin.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('admin.login'))