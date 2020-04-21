import os
import datetime
from flask import render_template, url_for, flash, redirect, request, abort, Markup, send_from_directory, jsonify, Blueprint
from portal import app, db, bcrypt, mail, csrf
from portal.models import User, Siswa, Mapel, Absen, Agama, Kehadiran, Kelas, JenisKelamin, Role, Guru, JadwalMapel
from portal.jadwal.forms import JadwalBelajarForm
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
import json
from sqlalchemy import func

jadwal = Blueprint('jadwal', __name__)

@jadwal.route("/jadwal-belajar", methods=['GET', 'POST'])
@login_required
def jadwal_belajar():
    kelas = Kelas.query.all()
    page_kelas = request.args.get('kelas')
    mapel = Kelas.query.filter_by(nama=page_kelas).first()
    return render_template('jadwal/home.html', kelas=kelas, mapel=mapel)

@jadwal.route("/tambah-jadwal-belajar", methods=['GET', 'POST'])
@login_required
def tambah_jadwal_belajar():
    form = JadwalBelajarForm()
    form.mapel.choices = [(str(mapel.id), mapel.nama)for mapel in Mapel.query.all()]
    form.mapel.choices.insert(0,('', '== Pilih Mata Pelajaran =='))
    form.kelas.choices = [(str(kelas.id), kelas.nama)for kelas in Kelas.query.all()]
    form.kelas.choices.insert(0,('', '== Pilih Kelas =='))
    form.guru.choices = [(str(u.id), u.nama)for u in Guru.query.all()]
    form.guru.choices.insert(0,('', '== Pilih Guru =='))
    form.hari.choices.insert(0,('', '== Pilih Hari =='))
    if form.validate_on_submit():
        cek_jadwal = JadwalMapel.query.filter_by(guru_id=form.guru.data, hari=form.hari.data).all()
        for cek in cek_jadwal:
            if cek.mulai <= form.mulai.data < cek.akhir:
                flash('Guru mengajar di kelas lain pada jam yang Anda pilih', 'is-danger')
                return render_template('jadwal/tambah_jadwal_belajar.html', form=form, title='Tambah Jadwal Belajar')
            else:
                jadwal = JadwalMapel(mapel_id=form.mapel.data, kelas_id=form.kelas.data, guru_id=form.guru.data, hari=form.hari.data, mulai=form.mulai.data, akhir=form.akhir.data)
                db.session.add(jadwal)
                db.session.commit()
                flash('Jadwal belajar berhasil ditambahkan', 'is-success')
                return redirect(url_for('jadwal.jadwal_belajar'))
    return render_template('jadwal/tambah_jadwal_belajar.html', form=form, title='Tambah Jadwal Belajar')