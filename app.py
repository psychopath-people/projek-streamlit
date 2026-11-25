import streamlit as st
import pandas as pd

st.title("Dashboard Analisis Penjualan")

uploaded = st.file_uploader("Upload CSV", type="csv")

if uploaded:
    df = pd.read_csv(uploaded, low_memory=False, on_bad_lines="skip")
    df.columns = [c.rstrip(";") for c in df.columns]

    st.header("Sesi 1 — Info Data")
    st.write(f"Ukuran: **{df.shape[0]} baris, {df.shape[1]} kolom**")
    st.write("Daftar kolom:", list(df.columns))

    st.header("Sesi 2 — Kenali Isinya")
    if "Brandname" in df.columns:
        st.write("Merek:", df["Brandname"].unique().tolist())
    if "Kota" in df.columns:
        st.write(f"Jumlah kota unik: {df['Kota'].nunique()}")
    if "Salesman" in df.columns:
        st.write("Top 10 Salesman:")
        st.dataframe(df["Salesman"].value_counts().head(10))
    if "Business Type" in df.columns:
        st.write("Komposisi Tipe Pelanggan:")
        st.dataframe(df["Business Type"].value_counts())

    st.header("Sesi 3 — Filter Data")
    if "Kota" in df.columns and "Qty" in df.columns:
        col1, col2 = st.columns(2)
        with col1:
            kota_filter = st.selectbox("Pilih Kota", ["(Semua)"] + sorted(df["Kota"].dropna().unique().tolist()))
        with col2:
            brand_filter = st.selectbox("Pilih Brand", ["(Semua)"] + sorted(df["Brandname"].dropna().unique().tolist()) if "Brandname" in df.columns else ["(Semua)"])

        filtered = df.copy()
        if kota_filter != "(Semua)":
            filtered = filtered[filtered["Kota"] == kota_filter]
        if brand_filter != "(Semua)" and "Brandname" in df.columns:
            filtered = filtered[filtered["Brandname"] == brand_filter]

        st.write(f"Hasil filter: **{len(filtered)} baris**")
        preview_cols = [c for c in ["N. Customer", "Kota", "Brandname", "Qty", "Total"] if c in filtered.columns]
        st.dataframe(filtered[preview_cols].head(20))

    st.header("Sesi 4 — Konversi Tipe Data")
    kolom_angka = [k for k in ["Qty", "Harga", "Rupiah", "Total", "Tax"] if k in df.columns]
    for k in kolom_angka:
        df[k] = pd.to_numeric(df[k].astype(str).str.replace(",", ""), errors="coerce")

    if "Tanggal" in df.columns:
        df["Tanggal"] = pd.to_datetime(df["Tanggal"], format="mixed", dayfirst=True, errors="coerce")

    st.write("Null per kolom:")
    st.dataframe(df.isnull().sum().rename("Null Count"))

    st.header("Sesi 5 — Penjualan vs Retur")
    if "Qty" in df.columns:
        jual  = df[df["Qty"] > 0]
        retur = df[df["Qty"] < 0]
        st.metric("Baris Penjualan", len(jual))
        st.metric("Baris Retur", len(retur))
        if "Total" in df.columns:
            st.metric("Total Nilai Retur", f"Rp {retur['Total'].sum():,.0f}")

    csv_out = df.to_csv(index=False).encode("utf-8")
    st.download_button("Download Data Bersih", csv_out, "penjualan_bersih.csv", "text/csv")

else:
    st.info("Upload file CSV untuk mulai analisis.")
