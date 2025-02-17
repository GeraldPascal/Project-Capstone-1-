from tabulate import tabulate
from datetime import datetime

# Data pengguna untuk login dengan username, password, dan role (admin/user)
users = {
    "admin": {"password": "admin123", "role": "admin"},
    "user": {"password": "user123", "role": "user"}
}

# Variabel global untuk menyimpan informasi pengguna yang sedang login
current_user = None

# Daftar barang yang tersedia di toko
barangList = [
    {"nama": "Laptop", "harga": 7000000, "stok": 5},
    {"nama": "Mouse", "harga": 150000, "stok": 30},
    {"nama": "Keyboard", "harga": 300000, "stok": 20},
    {"nama": "Monitor", "harga": 2000000, "stok": 10},
    {"nama": "Headset", "harga": 500000, "stok": 15}
]

# Recycle bin untuk menyimpan barang yang dihapus
recycleBin = []

def login():
    """Fungsi untuk login pengguna."""
    global current_user
    while True:
        username = input("Masukkan username: ")
        password = input("Masukkan password: ")

         # Mengecek apakah username dan password sesuai dengan database pengguna
        if username in users and users[username]["password"] == password:
            current_user = users[username] # Menyimpan data pengguna yang login
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S") # Catat waktu login
            print(f"\n[{timestamp}] Login berhasil! Selamat datang, {username.capitalize()} (Role: {current_user['role']})\n")
            break
        else:
            print("Login gagal! Username atau password salah. Silakan coba lagi.\n")

def logout():
    """Fungsi untuk logout pengguna."""
    global current_user
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S") # Catat waktu logout
    print(f"\n[{timestamp}] Logout berhasil! Sampai jumpa kembali.\n")
    current_user = None # Menghapus status login pengguna
    main()

def tampilkanDaftarBarang():
    """Menampilkan daftar barang di toko."""
    if not barangList:
        print("Tidak ada barang dalam daftar.")
        return
    print("\nDaftar Barang Toko:")
    data_barang = [[i, b["nama"], b["harga"], b["stok"]] for i, b in enumerate(barangList)]
    print(tabulate(data_barang, headers=["Index", "Nama", "Harga", "Stok"], tablefmt="grid"))

def tambahBarang():
    """Menambahkan barang baru ke dalam daftar barang."""
    if current_user["role"] != "admin":
        print("Hanya admin yang bisa menambah barang!\n")
        return
    
    nama = input("Masukkan nama barang baru: ")
    
    while True:
        try:
            harga = int(input("Masukkan harga barang: "))
            break
        except ValueError:
            print("Hanya menerima angka! Silakan masukkan harga yang valid.")
    
    while True:
        try:
            stok = int(input("Masukkan jumlah stok: "))
            break
        except ValueError:
            print("Hanya menerima angka! Silakan masukkan jumlah stok yang valid.")
    
    barangList.append({"nama": nama, "harga": harga, "stok": stok})
    print(f"Barang {nama} berhasil ditambahkan.")

def hapusBarang():
    """Menghapus barang berdasarkan index."""
    if current_user["role"] != "admin":
        print("Hanya admin yang bisa menghapus barang!\n")
        return
    tampilkanDaftarBarang()
    try:
        indexHapus = int(input("Masukkan index barang yang ingin dihapus: "))
        if 0 <= indexHapus < len(barangList):
            barangTerhapus = barangList.pop(indexHapus) # Hapus barang dari daftar
            recycleBin.append(barangTerhapus) # Simpan barang ke recycle bin
            print(f"Barang {barangTerhapus['nama']} berhasil dihapus.")
        else:
            print("Nomor tidak valid!")
    except ValueError:
        print("Masukkan angka yang valid!")

def tampilkanRecycleBin():
    """Menampilkan daftar barang di recycle bin."""
    if current_user["role"] != "admin":
        print("Hanya admin yang bisa melihat recycle bin!\n")
        return
    
    if not recycleBin:
        print("Recycle bin kosong.")
        return
    print("\nRecycle Bin:")
    data_barang = [[i, b["nama"], b["harga"], b["stok"]] for i, b in enumerate(recycleBin)]
    print(tabulate(data_barang, headers=["Index", "Nama", "Harga", "Stok"], tablefmt="grid"))

def restoreBarang():
    """Mengembalikan barang dari recycle bin."""
    if current_user["role"] != "admin":
        print("Hanya admin yang bisa merestore barang!\n")
        return
    
    tampilkanRecycleBin()
    try:
        indexRestore = int(input("Masukkan index barang yang ingin dipulihkan: "))
        if 0 <= indexRestore < len(recycleBin):
            barangDipulihkan = recycleBin.pop(indexRestore)
            barangList.append(barangDipulihkan)
            print(f"Barang {barangDipulihkan['nama']} berhasil dipulihkan.")
        else:
            print("Nomor tidak valid!")
    except ValueError:
        print("Masukkan angka yang valid!")

def beliBarang():
    """Membeli barang dari daftar."""
    daftarBelanja = []
    totalHarga = 0
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    while True:
        tampilkanDaftarBarang()
        while True:
            try:
                indexBeli = int(input("Masukkan index barang yang ingin dibeli: "))
                if 0 <= indexBeli < len(barangList):
                    break
                else:
                    print("Nomor tidak valid! Silakan masukkan index yang benar.")
            except ValueError:
                print("Masukkan angka yang valid!")
        
        while True:
            try:
                jumlah = int(input(f"Berapa banyak {barangList[indexBeli]['nama']} yang ingin dibeli? "))
                if 0 < jumlah <= barangList[indexBeli]['stok']:
                    break
                else:
                    print(f"Stok tidak cukup atau jumlah tidak valid! Sisa stok: {barangList[indexBeli]['stok']}")
            except ValueError:
                print("Masukkan angka yang valid!")
        
        barangList[indexBeli]['stok'] -= jumlah
        harga = barangList[indexBeli]['harga'] * jumlah
        totalHarga += harga
        daftarBelanja.append([barangList[indexBeli]['nama'], jumlah, harga, timestamp])
        
        lanjut = input("Ingin membeli barang lain? (ya/tidak): ").lower()
        if lanjut != "ya":
            break
    
    print(f"\nNota Pembelian ({timestamp}):")
    print(tabulate(daftarBelanja, headers=["Nama", "Jumlah", "Harga", "Waktu Pembelian"], tablefmt="grid"))
    print(f"Total Harga: Rp{totalHarga}")

def editBarang():
    """Mengedit informasi barang di dalam daftar."""
    if current_user["role"] != "admin":
        print("Hanya admin yang bisa mengedit barang!\n")
        return
    
    tampilkanDaftarBarang()
    
    try:
        indexEdit = int(input("Masukkan index barang yang ingin diedit: "))
        if 0 <= indexEdit < len(barangList):
            barang = barangList[indexEdit]
            print(f"\nMengedit barang: {barang['nama']}")

            # Edit nama barang
            namaBaru = input(f"Masukkan nama baru ({barang['nama']} untuk tetap sama): ")
            if namaBaru.strip():
                barang["nama"] = namaBaru
            
            # Edit harga barang
            while True:
                hargaBaru = input(f"Masukkan harga baru ({barang['harga']} untuk tetap sama): ")
                if hargaBaru.strip():
                    try:
                        barang["harga"] = int(hargaBaru)
                        break
                    except ValueError:
                        print("Harga harus berupa angka!")
                else:
                    break
            
            # Edit stok barang
            while True:
                stokBaru = input(f"Masukkan stok baru ({barang['stok']} untuk tetap sama): ")
                if stokBaru.strip():
                    try:
                        barang["stok"] = int(stokBaru)
                        break
                    except ValueError:
                        print("Stok harus berupa angka!")
                else:
                    break

            print(f"\nBarang berhasil diperbarui: {barang['nama']} | Harga: {barang['harga']} | Stok: {barang['stok']}")
        else:
            print("Nomor tidak valid!")
    except ValueError:
        print("Masukkan angka yang valid!")   

def main():
    login()
    while True:
        print("\n====== TOKO BAHAGIA ======")
        print("1. Tampilkan daftar barang")
        print("2. Beli barang")
        print("3. Tambah barang")
        print("4. Hapus barang")
        print("5. Tampilkan recycle bin")
        print("6. Restore barang dari recycle bin")
        print("7. Edit barang")  # Dipindahkan ke opsi 7
        print("8. Logout")  # Logout pindah ke opsi 8
        
        pilihan = input("Pilih menu (1-8): ")
        if pilihan == "1":
            tampilkanDaftarBarang()
        elif pilihan == "2":
            beliBarang()
        elif pilihan == "3":
            tambahBarang()
        elif pilihan == "4":
            hapusBarang()
        elif pilihan == "5":
            tampilkanRecycleBin()
        elif pilihan == "6":
            restoreBarang()
        elif pilihan == "7":
            editBarang()  # Panggil fungsi editBarang()
        elif pilihan == "8":
            logout()
            break
        else:
            print("Pilihan tidak valid! Silakan pilih menu 1-8.")

main()