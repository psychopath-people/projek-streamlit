import pandas as pd

# ─────────────────────────────────────────────
# SESI 1 — Buka dan Intip
# ─────────────────────────────────────────────
print("=" * 55)
print("SESI 1 — Buka dan Intip")
print("=" * 55)

df = pd.read_csv("Test.csv", low_memory=False, on_bad_lines="skip")
df.columns = [c.rstrip(";") for c in df.columns]  # bersihkan sisa karakter rusak di nama kolom
print(f"\nUkuran data: {df.shape[0]} baris, {df.shape[1]} kolom\n")
df.info()
print("\nDaftar kolom:")
print(list(df.columns))

# ─────────────────────────────────────────────
# SESI 2 — Kenali Isinya
# ─────────────────────────────────────────────
print("\n" + "=" * 55)
print("SESI 2 — Kenali Isinya")
print("=" * 55)

print("\nMerek yang ada:")
print(df["Brandname"].unique())

print(f"\nJumlah kota unik: {df['Kota'].nunique()}")

print("\nTop 10 Salesman:")
print(df["Salesman"].value_counts().head(10))

print("\nKomposisi Tipe Pelanggan:")
print(df["Business Type"].value_counts())

# ─────────────────────────────────────────────
# SESI 3 — Saring Baris
# ─────────────────────────────────────────────
print("\n" + "=" * 55)
print("SESI 3 — Saring Baris")
print("=" * 55)

surabaya = df[df["Kota"] == "SURABAYA"]
print(f"\nTransaksi di Surabaya: {len(surabaya)} baris")

foxled = df[df["Brandname"] == "FOXLED"]
print(f"Transaksi FOXLED: {len(foxled)} baris")

# Qty terbaca sebagai teks — konversi dulu sebelum pakai operator >
qty = pd.to_numeric(df["Qty"], errors="coerce")
bali_jual = df[(df["Kota"] == "BALI") & (qty > 0)]
print(f"Penjualan di Bali (Qty > 0): {len(bali_jual)} baris")

print("\nSampel 10 baris (kolom pilihan):")
print(df[["N. Customer", "Kota", "Brandname", "Qty", "Total"]].head(10))

# ─────────────────────────────────────────────
# SESI 4 — Perbaiki Tipe Data (Angka)
# ─────────────────────────────────────────────
print("\n" + "=" * 55)
print("SESI 4 — Perbaiki Tipe Data (Angka & Tanggal)")
print("=" * 55)

kolom_angka = ["Qty", "Harga", "Rupiah", "Total", "Tax"]

for k in kolom_angka:
    df[k] = pd.to_numeric(
        df[k].astype(str).str.replace(",", ""),
        errors="coerce"
    )

# Data punya 2 format tanggal: '05/01/2026' dan '31 Aug 2026'
# format='mixed' + dayfirst=True menangani keduanya sekaligus
df["Tanggal"] = pd.to_datetime(
    df["Tanggal"], format="mixed", dayfirst=True, errors="coerce"
)

print("\nInfo setelah konversi:")
df.info()

print("\nJumlah nilai kosong per kolom:")
print(df.isnull().sum())

# ─────────────────────────────────────────────
# SESI 4b — Tanggal Berantakan (Mixed Date Format)
# ─────────────────────────────────────────────
print("\n" + "=" * 55)
print("SESI 4b — Tanggal Berantakan")
print("=" * 55)

# Simulasi data tanggal campur format
contoh_tanggal = pd.Series([
    "05/01/2026",       # dd/mm/yyyy
    "2026-01-06",       # yyyy-mm-dd (ISO)
    "January 7, 2026",  # format teks
    "08-Jan-26",        # format pendek
    "99/99/9999",       # tidak valid
    "",                 # kosong
    None,               # NaN
    "12/01/2026",       # normal
])

print("\nData mentah:")
print(contoh_tanggal)

# Cara salah — strict format
print("\n--- Cara SALAH (strict format) ---")
try:
    pd.to_datetime(contoh_tanggal, format="%d/%m/%Y")
except Exception as e:
    print(f"ERROR: {e}")

# Cara BERBAHAYA — tidak crash tapi tanggal Indonesia terbalik diam-diam!
print("\n--- Cara BERBAHAYA (tanpa dayfirst) ---")
hasil_salah = pd.to_datetime(contoh_tanggal, errors="coerce")
print(hasil_salah)
print(f"\n05/01/2026 terbaca: {hasil_salah[0]} ← harusnya 5 Januari, bukan 1 Mei!")

# Cara AMAN — format='mixed' + dayfirst=True + errors='coerce'
print("\n--- Cara AMAN (format='mixed', dayfirst=True) ---")
hasil_aman = pd.to_datetime(contoh_tanggal, format="mixed", dayfirst=True, errors="coerce")
print(hasil_aman)

# Deteksi baris yang masih gagal
gagal = contoh_tanggal[hasil_aman.isna()]
print(f"\nBaris tidak bisa dikonversi: {gagal.count()}")
print(gagal)

# Terapkan ke data asli
print(f"\nBaris kosong di kolom Tanggal (data asli): {df['Tanggal'].isna().sum()}")
df["Tanggal"] = pd.to_datetime(df["Tanggal"], format="mixed", dayfirst=True, errors="coerce")
rusak = df[df["Tanggal"].isna()]
print(f"Baris tanggal bermasalah setelah konversi: {len(rusak)}")

# ─────────────────────────────────────────────
# SESI 5 — Pisahkan, Buang, Simpan
# ─────────────────────────────────────────────
print("\n" + "=" * 55)
print("SESI 5 — Pisahkan, Buang, Simpan")
print("=" * 55)

jual  = df[df["Qty"] > 0]
retur = df[df["Qty"] < 0]

print(f"\nJumlah baris penjualan : {len(jual)}")
print(f"Jumlah baris retur     : {len(retur)}")
print(f"Total nilai retur      : Rp {retur['Total'].sum():,.0f}")

kolom_buang = ["Sales", "Nama Barang", "unique_Kota"]
df = df.drop(columns=kolom_buang)

print(f"\nKolom tersisa ({len(df.columns)}):")
print(list(df.columns))

df.to_csv("penjualan_bersih.csv", index=False)
print("\nFile 'penjualan_bersih.csv' berhasil disimpan.")
