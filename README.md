# Early Warning System - The Open University

**Analisis Big Data untuk Deteksi Dini Mahasiswa Berisiko Gagal atau Withdrawal pada Pembelajaran Daring: Studi Kasus The Open University, United Kingdom**

Repositori ini memuat implementasi proyek *Early Warning System* berbasis data menggunakan dataset terbuka OULAD (*Open University Learning Analytics Dataset*). Sistem ini dirancang untuk mendeteksi secara dini mahasiswa yang berisiko gagal (*fail*) atau mengundurkan diri (*withdrawal*) dalam pembelajaran daring, sehingga intervensi akademik dapat dilakukan dengan lebih cepat dan tepat sasaran.

---

## 🎯 Latar Belakang & Tujuan
Institusi/kampus belum optimal dalam mendeteksi sejak awal mahasiswa yang berisiko *fail* atau *withdrawal* pada pembelajaran daring jarak jauh berbasis teknologi (VLE - *Virtual Learning Environment*). 

**Tujuan Strategis:**
1. Meningkatkan retensi mahasiswa (menurunkan *withdrawal rate*).
2. Meningkatkan keberhasilan akademik mahasiswa melalui pemantauan aktivitas belajar dan hasil asesmen.
3. Memperkuat pengambilan keputusan berbasis data agar dosen, tutor, dan tim *support* dapat memberi intervensi dini.

## 📊 Indikator Kinerja Utama (KPI)
Sistem ini berfokus pada pelacakan lima (5) KPI utama:
- **Withdrawal Rate:** Persentase mahasiswa yang keluar dari modul sebelum selesai.
- **Fail Rate:** Persentase mahasiswa yang tidak lulus modul.
- **Student Engagement Rate:** Tingkat keterlibatan aktif mahasiswa dalam VLE.
- **Assessment Completion Rate:** Tingkat penyelesaian atau kepatuhan pengumpulan tugas.
- **Early Risk Detection Rate:** Persentase mahasiswa berisiko yang berhasil diidentifikasi lebih awal untuk proses intervensi.

## 🛠 Model Analitik (Machine Learning)
Pendekatan analitik meliputi **Analisis Deskriptif** (memahami pola hasil akhir, tingkat aktivitas, asesmen, dll) dan **Analisis Prediktif** untuk deteksi risiko.
* **Decision Tree (Model Utama):** Digunakan karena mampu mengklasifikasikan mahasiswa berisiko secara jelas, *rules*-nya mudah diinterpretasi, serta dapat menunjukkan variabel yang paling berpengaruh secara langsung.
  * **Accuracy:** 93.04%
  * **Precision:** 96.80%
  * **Recall:** 89.77%
  * **F1-score:** 93.16%
* **Logistic Regression (Model Pembanding):** Digunakan untuk melihat performa prediksi berbasis probabilitas dengan akurasi klasifikasi sebesar 92.71%. Decision tree dipilih sebagai model utama karena sedikit lebih unggul.

## 🔄 Data Lifecycle & Arsitektur Sistem
Sistem memproses data mentah (CSV) dengan siklus hidup sebagai berikut:
1. **Data Acquisition:** Pengambilan set file OULAD dan pembacaan ke lingkungan pengolahan data.
2. **Data Storage:** Data mentah disimpan terpisah pada folder `raw/`. Data bersih dan hasil integrasi pada `processed/`, dan hasil model pada `output/`.
3. **Data Processing (Cleaning & Transformation):** Penanganan *missing values* (seperti median imputation pada skor) dan agregasi perilaku VLE level mahasiswa menjadi fitur komprehensif (`total_clicks`, `avg_score`, `assessment_completion_rate`, dll).
4. **Data Integration:** Penyatuan berbagai sumber (`studentInfo`, `studentVle`, `studentAssessment`, dll) untuk mendapatkan 1 representasi berwujud `merged_processed_oulad.csv` dengan pelabelan target `risk_label`.
5. **Data Visualization:** Dashboard analitik peringatan dini dibangun menggunakan **Streamlit**.

## 🛡️ Tata Kelola Data (Data Governance & Quality)
* **Data Ownership:** *The Open University* bertindak sebagai pengendali data (*data controller*). 
* **Kebijakan Akses:** Diterapkan konsep *Role-Based Access Control* (Administrator/Data Analyst untuk agregasi makro; Tutor terbatas pada modul yang mereka pegang) guna menjaga aspek kerahasiaan (*confidentiality*).
* **Evaluasi Kualitas Data:** Tingkat evaluasi *Completeness*, *Accuracy*, *Consistency*, dan *Timeliness* menunjukan integritas dan validitas kualitas data tingkat tinggi, membuatnya sangat layak digunakan untuk sistem deteksi dini.

## 💼 Nilai Bisnis dan Sosial (Impact)
* **Nilai Bisnis:** Pemanfaatan rekam jejak akademik operasional sebagai landasan pendukung keputusan, memastikan efisiensi pengelolaan, potensi terhindar dari kerugian sistem persentase kelulusan rendah, serta penghematan dari beban layanan.
* **Nilai Sosial:** Mahasiswa dengan gejala kesulitan/risiko mendapat peluang nyata untuk segera ditolong & dimonitor secara inklusif. Hal ini mendorong pencapaian keadilan pendidikan jarak jauh yang holistik.

---
**Diimplementasikan Oleh:** Mohammad Bayu Rizki
**Mata Kuliah:** Big Data dan IoT (Tugas ETS)
**Program Studi:** Sistem Informasi, Universitas Pembangunan Nasional "Veteran" Jawa Timur
