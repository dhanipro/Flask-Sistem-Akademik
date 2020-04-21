import os
import datetime
from flask import render_template, url_for, flash, redirect, request, abort, Markup, send_from_directory, jsonify, Blueprint
from portal import app, db, bcrypt, mail, csrf, cors
from portal.models import User, Siswa, Mapel, Absen, Agama, Kehadiran, Kelas, JenisKelamin, Role, Guru
from portal.guru.forms import GuruForm
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
import json
from sqlalchemy import func

guru = Blueprint('guru', __name__)

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


@guru.route("/guru")
@login_required
def daftar_guru():
    guru = Guru.query.all()
    return render_template('guru/home.html', guru=guru)

@guru.route("/tambah_guru", methods=['GET', 'POST'])
@login_required
def tambah_guru():
    form = GuruForm()
    form.jenis_kelamin.choices = [(str(kelamin.id), kelamin.kelamin)for kelamin in JenisKelamin.query.all()]
    form.jenis_kelamin.choices.insert(0,('', '== Jenis Kelamin =='))
    form.agama.choices = [(str(agama.id), agama.agama.title())for agama in Agama.query.all()]
    form.agama.choices.insert(0,('', '== Agama =='))
    if form.validate_on_submit():
        guru = Guru(nama=form.nama.data, email=form.email.data, tgl_lahir=form.tanggal_lahir.data, jenis_kelamin_id=form.jenis_kelamin.data, agama_id=form.agama.data, alamat=form.alamat.data, slug=slugify(form.nama.data))
        db.session.add(guru)
        db.session.commit()
        flash('Data Guru berhasil ditambahkan', 'is-success')
        return redirect(url_for('guru.daftar_guru'))
    return render_template('guru/create_guru.html', form=form, title='Tambah Guru')

@guru.route("/mengajar", methods=['GET', 'POST'])
@login_required
def mengajar():
    today = datetime.date.today()
    mapel = Mapel.query.all()
    kelas = Kelas.query.all()
    page_mapel = request.args.get('mapel')
    get_id_mapel = Mapel.query.filter_by(nama=page_mapel).first()
    page_kelas = request.args.get('kelas')
    if page_mapel=='0' and page_kelas:
        flash('Pilih mata pelajaran dahulu', 'is-danger')
    elif page_kelas:
        siswa = Kelas.query.filter_by(nama=page_kelas).first_or_404()
        absen = Absen.query.all()
        return render_template('guru/mengajar.html', mapel=mapel, kelas=kelas, siswa=siswa, absen=absen, today=today, get_id_mapel=get_id_mapel)
    return render_template('guru/mengajar.html', mapel=mapel, kelas=kelas)

@guru.route("/kehadiran/<string:id>", methods=['POST'])
@login_required
def kehadiran(id):
    today = datetime.date.today()
    data = request.get_json(id)
    mapel = Mapel.query.filter_by(nama=data['mapel']).first_or_404()
    # siswa = Siswa.query.get(data['siswa_id'])
    # absensi_siswa = Absen.query.get(data['kehadiran'])
    kehadiran = Kehadiran.query.filter(Kehadiran.siswa_id==data['siswa_id'], Kehadiran.mapel_id==mapel.id, func.DATE(Kehadiran.waktu_absen)==today).first()
    # q = Kehadiran.query.with_for_update(nowait=True, of=Kehadiran).filter(Kehadiran.siswa==data['siswa_id'], func.DATE(Kehadiran.waktu_absen)==today).first()
    if kehadiran:
        # q = Kehadiran.query.with_for_update(nowait=True, of=Kehadiran).filter(Kehadiran.siswa==data['siswa_id'], func.DATE(Kehadiran.waktu_absen)==today).first()
        kehadiran.absen_id = data['kehadiran']
    else:
        absen = Kehadiran(siswa_id=data['siswa_id'], user_id=1, mapel_id=mapel.id, absen_id=data['kehadiran'])
        db.session.add(absen)   
    db.session.commit()
    return jsonify(data)