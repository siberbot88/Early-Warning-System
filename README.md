# Early Warning System - The Open University

**Analisis Big Data untuk Deteksi Dini Mahasiswa Berisiko Gagal atau Withdrawal pada Pembelajaran Daring: Studi Kasus The Open University, United Kingdom**

**Akses Dashboard:** [https://early-warning-system-bigdata.streamlit.app/](https://early-warning-system-bigdata.streamlit.app/)

Repositori ini memuat implementasi proyek *Early Warning System* berbasis data menggunakan dataset terbuka OULAD (*Open University Learning Analytics Dataset*). Sistem ini dirancang untuk mendeteksi secara dini mahasiswa yang berisiko gagal (*fail*) atau mengundurkan diri (*withdrawal*) dalam pembelajaran daring, sehingga intervensi akademik dapat dilakukan dengan lebih cepat dan tepat sasaran.

---

## Latar Belakang dan Tujuan
Institusi belum optimal dalam mendeteksi sejak awal mahasiswa yang berisiko *fail* atau *withdrawal* pada pembelajaran daring jarak jauh berbasis teknologi (VLE - *Virtual Learning Environment*). 

**Tujuan Strategis:**
1. Meningkatkan retensi mahasiswa (menurunkan *withdrawal rate*).
2. Meningkatkan keberhasilan akademik mahasiswa melalui pemantauan aktivitas belajar dan hasil asesmen.
3. Memperkuat pengambilan keputusan berbasis data agar dosen, tutor, dan tim *support* dapat memberi intervensi dini.

## Indikator Kinerja Utama (KPI)
Sistem ini berfokus pada pelacakan lima KPI utama:
- **Withdrawal Rate:** Persentase mahasiswa yang keluar dari modul sebelum selesai.
- **Fail Rate:** Persentase mahasiswa yang tidak lulus modul.
- **Student Engagement Rate:** Tingkat keterlibatan aktif mahasiswa dalam VLE.
- **Assessment Completion Rate:** Tingkat penyelesaian atau kepatuhan pengumpulan tugas.
- **Early Risk Detection Rate:** Persentase mahasiswa berisiko yang berhasil diidentifikasi lebih awal untuk proses intervensi.

## Model Analitik (Machine Learning)
Pendekatan analitik meliputi **Analisis Deskriptif** (memahami pola hasil akhir, tingkat aktivitas, asesmen) dan **Analisis Prediktif** untuk deteksi risiko.
* **Decision Tree (Model Utama):** Digunakan karena mampu mengklasifikasikan mahasiswa berisiko secara jelas, aturannya mudah diinterpretasi, serta dapat menunjukkan variabel yang paling berpengaruh secara langsung.
  * **Accuracy:** 93.04%
  * **Precision:** 96.80%
  * **Recall:** 89.77%
  * **F1-score:** 93.16%
* **Logistic Regression (Model Pembanding):** Digunakan untuk melihat performa prediksi berbasis probabilitas dengan akurasi klasifikasi sebesar 92.71%. Decision tree dipilih sebagai model utama karena pengklasifikasiannya sedikit lebih unggul.

## Data Lifecycle dan Arsitektur Sistem
Sistem memproses data mentah (CSV) dengan siklus hidup sebagai berikut:
1. **Data Acquisition:** Pengambilan set file OULAD dan pembacaan ke lingkungan pengolahan data.
2. **Data Storage:** Data mentah disimpan terpisah pada folder `raw/`. Data bersih dan hasil integrasi pada `processed/`, dan hasil model pada `output/`.
3. **Data Processing (Cleaning & Transformation):** Penanganan *missing values* (imputasi median pada skor) dan agregasi perilaku VLE level mahasiswa menjadi fitur komprehensif (`total_clicks`, `avg_score`, `assessment_completion_rate`).
4. **Data Integration:** Penyatuan berbagai sumber (`studentInfo`, `studentVle`, `studentAssessment`) untuk mendapatkan satu representasi berwujud `merged_processed_oulad.csv` dengan pelabelan target `risk_label`.
5. **Data Visualization:** Dashboard analitik peringatan dini dibangun menggunakan **Streamlit** dan di-deploy secara publik melalui [tautan dashboard ini](https://early-warning-system-bigdata.streamlit.app/).

## Tata Kelola Data (Data Governance & Quality)
* **Data Ownership:** *The Open University* bertindak sebagai pengendali data (*data controller*). 
* **Kebijakan Akses:** Diterapkan konsep *Role-Based Access Control* (Administrator/Data Analyst untuk agregasi makro; Tutor terbatas pada modul yang diampu) guna menjaga privasi peserta didik.
* **Evaluasi Kualitas Data:** Tingkat evaluasi *Completeness*, *Accuracy*, *Consistency*, dan *Timeliness* menunjukan integritas serta validitas kualitas data yang sangat layak dipergunakan untuk operasional sistem deteksi dini.

## Nilai Bisnis dan Dampak Sosial
* **Nilai Bisnis:** Pemanfaatan rekam jejak akademik sebagai landasan pendukung keputusan, memastikan efisiensi pengelolaan, menekan kerugian operasional akibat tingkat kelulusan yang rendah, serta penghematan dari beban ekstensi layanan.
* **Nilai Sosial:** Mahasiswa dengan gejala kesulitan mendapatkan peluang untuk diidentifikasi dan ditangani lebih awal. Hal ini mendorong pencapaian keadilan pendidikan jarak jauh yang holistik dan suportif.

---
**Diimplementasikan Oleh:** Mohammad Bayu Rizki
**Mata Kuliah:** Big Data dan IoT (Tugas ETS)
**Program Studi:** Sistem Informasi, Universitas Pembangunan Nasional "Veteran" Jawa Timur
