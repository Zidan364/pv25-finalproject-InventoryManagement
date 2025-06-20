import sqlite3

DB_NAME = "inventory.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventory (
            id_barang INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_barang TEXT NOT NULL,
            kategori TEXT NOT NULL,
            tanggal_masuk TEXT NOT NULL,
            status_stok TEXT NOT NULL,
            catatan TEXT
        )
    """)
    conn.commit()
    conn.close()

def tambah_data(nama, kategori, tanggal, status, catatan):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO inventory (nama_barang, kategori, tanggal_masuk, status_stok, catatan)
        VALUES (?, ?, ?, ?, ?)
    """, (nama, kategori, tanggal, status, catatan))
    conn.commit()
    conn.close()

def ambil_semua_data():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM inventory")
    data = cursor.fetchall()
    conn.close()
    return data

def hapus_data(id_barang):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM inventory WHERE id_barang = ?", (id_barang,))
    conn.commit()
    conn.close()

def edit_data(id_barang, nama, kategori, tanggal, status, catatan):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE inventory
        SET nama_barang = ?, kategori = ?, tanggal_masuk = ?, status_stok = ?, catatan = ?
        WHERE id_barang = ?
    """, (nama, kategori, tanggal, status, catatan, id_barang))
    conn.commit()
    conn.close()
