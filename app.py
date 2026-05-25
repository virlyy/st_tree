import streamlit as st

# ====================================================== #
# ============= KELAS NODE KATEGORI ==================== #
class KategoriNode:
    def __init__(self, nama_kategori):
        self.nama = nama_kategori
        self.sub_kategori = [] # INI ADALAH 'ANAK' ATAU CABANG DARI KATEGORI
    
    def tambah_sub(self, node_kategori):
        self.sub_kategori.append(node_kategori)
        return node_kategori # MENGEMBALIKAN NODE AGAR MUDAH DI SAMBUNG (CHAINING)
    
    # MENGUBAH FUNGSI STRING MENJADI RETURN STRING AGAR BISA DITAMPILKAN DI WEB 
    def dapatkan_tree_string(self, level=0):
        indentasi = "   " * level
        simbol = "-> " if level > 0 else " + "
        hasil = f"{indentasi}{simbol}{self.nama}\n"

        for sub in self.sub_kategori:
            hasil += sub.dapatkan_tree_string(level + 1)
        return hasil
    
    def cari_node(self, target_nama):
        # Mencari node spesifik untuk menambahkan anak di bawahnya
        if self.nama.lower() == target_nama.lower():
            return self
        
        for sub in self.sub_kategori:
            hasil = sub.cari_node(target_nama)
            if hasil:
                return hasil
            
        return None
    
    def cari_jalur(self, target, path=""):
        # Mencari jalur lengkap (breadcrumb) seperti studi kasus sebelumnya
        jalur_saat_ini = path + " > " + self.nama if path else self.nama

        if self.nama.lower() == target.lower():
            return jalur_saat_ini 
        
        for sub in self.sub_kategori:
            hasil = sub.cari_jalur(target, jalur_saat_ini)
            if hasil:
                return hasil
            
        return None
    
# ========================================================= #
# ============== PROGRAM UTAMA (INTERAKTIF) =============== #
# ========================================================= #
st.title("Pembuat Struktur Kategori")
st.write("Aplikasi interaktif untuk  mensimulasikan struktur data Tree")

# Inisialisasi session state untuk menyimpan struktur Tree agar tidak hilang saat halaman di refresh
if 'root' not in st.session_state:
    st.session_state.root = None
# Jika Root belum dibuat, tampilkan form pembuatan root
if st.session_state.root is None:
    st.info("Sistem belum dimiliki kategori utama. Silahkan buat terlebih dahulu")
    nama_root = st.text_input("Masukkan nama kategori utama (Root):", value="Toko Saya")

    if st.button("Buat Kategori Utama", type="Primary"):
        st.session_state.root = KategoriNode(nama_root)
        st.rerun() #refresh halaman
# Jika Root sudah ada, tampilkan menu utama menggunakan Tabs
else:
    root = st.session_state.root

    # Mengganti menu CLI dengan sistem Tab yang lebih modern
    tab1, tab2, tab3 = st.tabs(["Lihat Struktur", "+ Tambah Sub-Kategori", "Cari Jalur"])

    # Tab1: Lihat Struktur
    with tab1:
        st.subheader("Struktur Kategori saat ini")
        tree_teks = root.dapatkan_tree_string()
        #Menggunakan st.code agar format indentasi (spasi) tetap rapih
        st.code(tree_teks, language="text")
    
    # Tab2: Tambah Sub-Kategori
    with tab2:
        st.subheader("Tambah Cabang Baru")
        induk_nama = st.text_input("Nama Kategori induk tempat cabang ditambahkan:")
        anak_nama = st.text_input("Nama sub-kategori baru:")

        if st.button("Tambah Kategori"):
            if induk_nama and anak_nama:
                induk_node =  root.cari_node(induk_nama)
                if induk_node:
                    induk_node.tambah_sub(KategoriNode(anak_nama))
                    st.success(f"Berhasil menambahkan '{anak_nama}' dibawah '{induk_node.nama}'!")
                else:
                    st.error(f"Kategori '{induk_nama}' tidak ditemukan! Pastikan ejaanya benar")
            else:
                st.warning("Harap isi kedua kolom diatas")
    
    # Tab3: Cari Jalur
    with tab3:
        st.subheader("Pencarian Broadcrumb")
        target_cari = st.text_input("Nama Kategori yang ingin dicari jalurnya:")

        if st.button("Cari Jalur"):
            if target_cari:
                hasil = root.cari_jalur(target_cari)
                if hasil:
                    st.success("Ditemukan!")
                    st.info(f" Jalur: {hasil}")
                else:
                    st.error(f"Kategori '{target_cari}' tidak ditemukan dalam sistem")
            else:
                st.warning("Harap isi nama kategori yang dicari")

#Tombol Reset
st.divider()
if st.button("Reset Sistem / Mulai dari Awal"):
    st.session_state.root = None
    st.rerun()