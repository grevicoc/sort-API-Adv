## Deskripsi
No basa basi background story or whatever maap ga kreatip gw<br>
Untuk tugas seleksi ini, silahkan kalian menggunakan **python** untuk mengimplementasikan sorting menggunakan selection sort terhadap sebuah tabel data berbentuk csv, lalu program tersebut kalian pasang ke sebuah API yang memiliki Database, dikarenakan code program python, maka **disarankan** untuk menggunakan **Flask** untuk implementasi API, namun **penggunaan Framework lain dipersilahkan** untuk implementasi APInya, selama source code sorting tetap menggunakan python. **Database diwajibkan menggunakan MySQl**.

## Keypoint yang akan dihadapi dalam tugas ini
1. Belajar API
2. Implementasi Sorting
3. Database MySQL
4. Autentikasi dalam API (Bonus)
5. Data preprocessing (Bonus)

## Spesifikasi Wajib ( 1500 point )

### Database
1. Tabel 'sorts'
- Tabel sorts menyimpan hasil sorting tiap request yang dilakukan dan memiliki kolom kolom sebagai berikut :
- id untuk primary key (int, auto increment, primary key)
- tanggal dan waktu sorting dilakukan(DATE)
- algoritma yang dipakai (VARCHAR)
- hasil sorting yang di convert ke str menjadi format csv (blob/VARCHAR)
- execution time (float/double ato kalo mau dibuletin ke INT boleh)

### Route route yang harus ada di API kalian antara lain :

#### rute 1 : /sort/selection
- Methods : POST
- Request type : Form
- Isi request param : file csv berisi tabel, nomor kolom yang jadi acuan sort, orientasi sort (ASC/DESC)
- Proses yang terjadi : Sorting, lalu hasil sorting dimasukkan ke sebuah table sorts sesuai format table
- Yang direturn rute 1 : tabel hasil sorting dibentuk jadi HTML Table lalu direturn, tambahkan execution time sorting dan id di database
  
#### rute 2 : /sort/result
- Methods : GET
- Request params : Bisa gada, bisa dispecify dengan ?id=
- Yang direturn : Jika tidak dispecify param id, maka hasil sorting terbaru di table sorting, jika ada maka sesuai dengan idnya <br>

## Bonus ( 1000 point max )

### SEGALA PERUBAHAN BAGIAN SPEK WAJIB YANG DIPERLUKAN DEMI MEMBUAT SPEK BONUS DIPERSILAHKAN, ASAL DIJELASKAN APA DAN MENGAPA PERLU SAAT DEMO NANTI

### More sort ( 300 point )
Tambahkan algoritma sorting lain dengan menambahkan rute baru dengan method POST dengan url /sort/namaalgoritma, format request dan return sama dengan selection sort.

### Data Preprocess ( 200 point )
Data file csv merupakan tabel, dan tabel memiliki beberapa kolom, namun bisa jadi beberapa kolom tidak konsisten, bisa jadi kolom 2 seharusnya string, tapi terkadang ada baris yang malah memiliki INT di kolom 2, hapuslah data data yang invalid ini dari tabel sebelum sorting dilakukan.

### Autentikasi ( 500 point )
Tambahkan autentikasi dalam implementasi API, autentikasi menggunakan JWT atau json web token. Tambahkan rute POST yang jika dikirimkan user dan password valid, akan mengembalikan access token, dan buat sehingga semua rute membutuhkan access token.


## Pengerjaaan dan Pengumpulan dan Demo
Fork dari repo ini lalu kerjakan di repo hasil fork kalian <br>
Buatlah pull requests jika sudah ingin submit, hubungi line : aids.dragon untuk janjian demo. <br>
Kalopun udh pull requests dan mau ngubah ngubah sebelum demo sok aja gapapa

## Contact Person
Jika ada pertanyaan, buatlah issue github di repo ini lalu pc gw di line : aids.dragon