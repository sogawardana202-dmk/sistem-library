from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory
from werkzeug.utils import secure_filename
from datetime import datetime
import os

from models import db, User, Buku, Peminjaman, Surat
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()
    # Buat default admin jika belum ada
    if not User.query.filter_by(username='admin').first():
        from werkzeug.security import generate_password_hash
        admin = User(username='admin', password=generate_password_hash('admin1', method='sha256'))
        db.session.add(admin)
        db.session.commit()

# ====================== USER ROUTES ======================
@app.route('/')
def index():
    search = request.args.get('search')
    if search:
        buku_list = Buku.query.filter(Buku.judul.like(f'%{search}%')).all()
    else:
        buku_list = Buku.query.all()
    return render_template('index.html', buku_list=buku_list)

@app.route('/books')
def books():
    buku_list = Buku.query.all()
    return render_template('books.html', buku_list=buku_list)

@app.route('/book/<int:buku_id>')
def book_detail(buku_id):
    buku = Buku.query.get_or_404(buku_id)
    return render_template('book_detail.html', buku=buku)

@app.route('/borrow/<int:buku_id>', methods=['GET','POST'])
def borrow(buku_id):
    buku = Buku.query.get_or_404(buku_id)
    if request.method == 'POST':
        user_name = request.form['user_name']
        tanggal_pinjam = datetime.strptime(request.form['tanggal_pinjam'], '%Y-%m-%d')
        jam_pinjam = datetime.strptime(request.form['jam_pinjam'], '%H:%M').time()
        tanggal_kembali = datetime.strptime(request.form['tanggal_kembali'], '%Y-%m-%d')
        peminjaman = Peminjaman(
            buku_id=buku.id,
            user_name=user_name,
            tanggal_pinjam=tanggal_pinjam,
            jam_pinjam=jam_pinjam,
            tanggal_kembali=tanggal_kembali
        )
        db.session.add(peminjaman)
        db.session.commit()
        flash('Peminjaman berhasil!')
        return redirect(url_for('books'))
    return render_template('borrow.html', buku=buku)

@app.route('/letters')
def letters():
    surat_list = Surat.query.all()
    return render_template('letters.html', surat_list=surat_list)

# ====================== ADMIN ROUTES ======================
@app.route('/admin/login', methods=['GET','POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        from werkzeug.security import check_password_hash
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['admin'] = user.username
            return redirect(url_for('admin_dashboard'))
        flash('Username atau password salah!')
    return render_template('admin_login.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    return redirect(url_for('admin_login'))

def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'admin' not in session:
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    buku_count = Buku.query.count()
    peminjaman_count = Peminjaman.query.count()
    surat_count = Surat.query.count()
    return render_template('admin_dashboard.html', buku_count=buku_count,
                           peminjaman_count=peminjaman_count, surat_count=surat_count)

@app.route('/admin/books', methods=['GET','POST'])
@admin_required
def admin_books():
    if request.method == 'POST':
        judul = request.form['judul']
        penulis = request.form['penulis']
        tahun = request.form['tahun']
        foto_file = request.files['foto']
        if foto_file:
            filename = secure_filename(foto_file.filename)
            foto_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            filename = None
        buku = Buku(judul=judul, penulis=penulis, tahun=tahun, foto=filename)
        db.session.add(buku)
        db.session.commit()
        flash('Buku berhasil ditambahkan!')
        return redirect(url_for('admin_books'))
    buku_list = Buku.query.all()
    return render_template('admin_books.html', buku_list=buku_list)

@app.route('/admin/borrowings')
@admin_required
def admin_borrowings():
    borrowings = Peminjaman.query.all()
    return render_template('admin_borrowings.html', borrowings=borrowings)

@app.route('/admin/letters', methods=['GET','POST'])
@admin_required
def admin_letters():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            surat = Surat(
                judul=request.form['judul'],
                pengirim=request.form['pengirim'],
                penerima=request.form['penerima'],
                file=filename
            )
            db.session.add(surat)
            db.session.commit()
            flash('Surat berhasil diunggah!')
        return redirect(url_for('admin_letters'))
    surat_list = Surat.query.all()
    return render_template('admin_letters.html', surat_list=surat_list)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Edit Buku
@app.route('/admin/books/edit/<int:buku_id>', methods=['GET','POST'])
@admin_required
def admin_edit_book(buku_id):
    buku = Buku.query.get_or_404(buku_id)
    if request.method == 'POST':
        buku.judul = request.form['judul']
        buku.penulis = request.form['penulis']
        buku.tahun = request.form['tahun']
        foto_file = request.files['foto']
        if foto_file:
            filename = secure_filename(foto_file.filename)
            foto_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            buku.foto = filename
        db.session.commit()
        flash('Buku berhasil diupdate!')
        return redirect(url_for('admin_books'))
    return render_template('admin_edit_book.html', buku=buku)

# Delete Buku
@app.route('/admin/books/delete/<int:buku_id>')
@admin_required
def admin_delete_book(buku_id):
    buku = Buku.query.get_or_404(buku_id)
    db.session.delete(buku)
    db.session.commit()
    flash('Buku berhasil dihapus!')
    return redirect(url_for('admin_books'))

@app.route('/admin/borrowings/delete/<int:borrow_id>')
@admin_required
def admin_delete_borrowing(borrow_id):
    p = Peminjaman.query.get_or_404(borrow_id)
    db.session.delete(p)
    db.session.commit()
    flash('Peminjaman berhasil dihapus!')
    return redirect(url_for('admin_borrowings'))

# Edit Surat
@app.route('/admin/letters/edit/<int:letter_id>', methods=['GET','POST'])
@admin_required
def admin_edit_letter(letter_id):
    s = Surat.query.get_or_404(letter_id)
    if request.method == 'POST':
        s.judul = request.form['judul']
        s.pengirim = request.form['pengirim']
        s.penerima = request.form['penerima']
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            s.file = filename
        db.session.commit()
        flash('Surat berhasil diupdate!')
        return redirect(url_for('admin_letters'))
    return render_template('admin_edit_letter.html', surat=s)

# Delete Surat
@app.route('/admin/letters/delete/<int:letter_id>')
@admin_required
def admin_delete_letter(letter_id):
    s = Surat.query.get_or_404(letter_id)
    db.session.delete(s)
    db.session.commit()
    flash('Surat berhasil dihapus!')
    return redirect(url_for('admin_letters'))


# ====================== RUN APP ======================
if __name__ == "__main__":
    app.secret_key = app.config['SECRET_KEY']
    app.run(debug=True)

