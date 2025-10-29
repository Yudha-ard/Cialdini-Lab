import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from passlib.context import CryptContext
import uuid
from datetime import datetime, timezone

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
client = AsyncIOMotorClient(mongo_url)
db = client['tegalsec_lab']

async def seed_data():
    print("🌱 Seeding database...")
    
    # Clear existing data
    await db.users.delete_many({})
    await db.challenges.delete_many({})
    await db.education.delete_many({})
    
    # Create admin user
    admin_id = str(uuid.uuid4())
    admin = {
        "id": admin_id,
        "username": "admin",
        "email": "admin@tegalsec.org",
        "password": pwd_context.hash("admin123"),
        "full_name": "Admin Tegalsec",
        "role": "admin",
        "points": 0,
        "level": "Beginner",
        "completed_challenges": [],
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    await db.users.insert_one(admin)
    print("✅ Admin user created (username: admin, password: admin123)")
    
    # Create demo user
    user_id = str(uuid.uuid4())
    user = {
        "id": user_id,
        "username": "demouser",
        "email": "demo@example.com",
        "password": pwd_context.hash("demo123"),
        "full_name": "Demo User",
        "role": "user",
        "points": 0,
        "level": "Beginner",
        "completed_challenges": [],
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    await db.users.insert_one(user)
    print("✅ Demo user created (username: demouser, password: demo123)")
    
    # Seed challenges
    challenges = [
        {
            "id": str(uuid.uuid4()),
            "title": "Email Phishing Bank BCA",
            "category": "phishing",
            "difficulty": "beginner",
            "cialdini_principle": "authority",
            "description": "Anda menerima email yang mengaku dari Bank BCA",
            "scenario": "Anda menerima email dengan subject 'PENTING: Verifikasi Akun BCA Anda'. Email tersebut menyatakan bahwa akun Anda akan diblokir dalam 24 jam jika tidak melakukan verifikasi. Email memiliki logo BCA dan link yang terlihat seperti 'm-bca.co.id/verify'.",
            "question": "Apa tanda-tanda bahwa ini adalah email phishing?",
            "options": [
                "Email memiliki logo resmi bank",
                "Menggunakan domain yang mirip tapi bukan resmi (m-bca.co.id bukan klikbca.com)",
                "Email dikirim pada hari kerja",
                "Email berbahasa Indonesia"
            ],
            "correct_answer": 1,
            "explanation": "Domain yang mirip (typosquatting) adalah tanda utama phishing. Domain resmi BCA adalah klikbca.com, bukan m-bca.co.id. Pelaku menggunakan prinsip Authority (otoritas) Cialdini dengan menyamar sebagai institusi terpercaya.",
            "points": 50,
            "tips": [
                "Selalu periksa domain pengirim dengan teliti",
                "Bank tidak akan meminta verifikasi via email dengan ancaman pemblokiran",
                "Hover mouse di atas link untuk melihat URL sebenarnya sebelum klik",
                "Gunakan aplikasi resmi atau ketik URL langsung di browser"
            ],
            "real_case_reference": "Kasus phishing BCA marak terjadi di Indonesia sejak 2020",
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Aplikasi Penghasil Uang Snack Video",
            "category": "money_app",
            "difficulty": "beginner",
            "cialdini_principle": "scarcity",
            "description": "Aplikasi yang menjanjikan uang dari menonton video",
            "scenario": "Anda melihat iklan aplikasi 'Cash Snack Video' di media sosial yang menjanjikan Rp 500.000 hanya dengan menonton video 1 jam sehari. Aplikasi meminta izin akses ke kontak, SMS, dan lokasi. Untuk withdraw, Anda harus mengajak 10 teman daftar terlebih dahulu.",
            "question": "Apa yang paling mencurigakan dari aplikasi ini?",
            "options": [
                "Janji uang terlalu besar untuk aktivitas sederhana",
                "Meminta banyak izin yang tidak relevan + sistem referral wajib",
                "Tersedia di Google Play Store",
                "Memiliki rating 4.5 bintang"
            ],
            "correct_answer": 1,
            "explanation": "Kombinasi izin yang berlebihan (kontak, SMS) dengan sistem referral wajib adalah red flag. Aplikasi semacam ini sering mengumpulkan data pribadi untuk dijual atau digunakan untuk penipuan. Prinsip Scarcity (kelangkaan) digunakan dengan iming-iming uang besar yang 'mudah didapat'.",
            "points": 50,
            "tips": [
                "Waspadai aplikasi yang meminta izin tidak relevan dengan fungsinya",
                "Tidak ada uang gratis, jika terlalu bagus untuk jadi kenyataan, mungkin memang bukan kenyataan",
                "Cek review mendalam, bukan hanya rating (bisa dimanipulasi)",
                "Sistem referral wajib untuk withdraw adalah tanda pyramid scheme"
            ],
            "real_case_reference": "Banyak aplikasi serupa di Indonesia yang ternyata mengumpulkan data dan sulit melakukan penarikan uang",
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Penipuan Customer Service Tokopedia",
            "category": "pretexting",
            "difficulty": "intermediate",
            "cialdini_principle": "authority",
            "description": "Seseorang menelepon mengaku dari CS Tokopedia",
            "scenario": "Anda menerima telepon dari nomor yang mengaku sebagai CS Tokopedia. Mereka mengatakan ada transaksi mencurigakan senilai Rp 5 juta atas nama Anda dan meminta Anda memberikan kode OTP yang baru saja dikirim untuk 'membatalkan transaksi palsu' tersebut. Mereka terdengar profesional dan mengetahui nama lengkap Anda.",
            "question": "Apa yang HARUS Anda lakukan?",
            "options": [
                "Berikan kode OTP karena mereka ingin membantu",
                "Tolak memberikan OTP, tutup telpon, cek aplikasi/hubungi CS resmi",
                "Minta mereka menelepon lagi nanti",
                "Berikan setengah kode OTP untuk verifikasi"
            ],
            "correct_answer": 1,
            "explanation": "TIDAK PERNAH memberikan kode OTP kepada siapapun, termasuk yang mengaku CS. CS resmi tidak akan pernah meminta OTP. Ini adalah social engineering dengan pretexting (menciptakan skenario palsu) dan memanfaatkan authority. Data nama Anda bisa didapat dari berbagai sumber bocoran data.",
            "points": 75,
            "tips": [
                "OTP adalah kunci akun Anda, JANGAN PERNAH dibagikan ke siapapun",
                "CS resmi tidak akan menelepon meminta OTP atau password",
                "Selalu verifikasi lewat channel resmi (aplikasi/website resmi)",
                "Jangan panik saat ditelepon, pelaku sengaja membuat Anda panik"
            ],
            "real_case_reference": "Modus ini sangat marak di Indonesia, banyak korban kehilangan uang karena memberikan OTP",
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "title": "File Gaji 2025.xlsx",
            "category": "baiting",
            "difficulty": "intermediate",
            "cialdini_principle": "reciprocity",
            "description": "Rekan kerja mengirim file Excel di grup WhatsApp",
            "scenario": "Di grup WhatsApp kantor, seseorang dengan nomor tidak dikenal (tapi menggunakan foto profil logo perusahaan) membagikan file 'Daftar Gaji Karyawan 2025.xlsx'. Pesan tersebut mengatakan 'Info bocoran gaji tahun depan nih, jangan sampe ketahuan HRD ya'. Beberapa rekan Anda sudah mengunduh dan penasaran.",
            "question": "Apa risiko terbesar dari mengunduh file tersebut?",
            "options": [
                "File mungkin berisi malware/virus yang bisa mencuri data",
                "Melanggar aturan perusahaan",
                "Ukuran file terlalu besar",
                "Format .xlsx tidak kompatibel"
            ],
            "correct_answer": 0,
            "explanation": "File Excel dapat mengandung macro berbahaya yang bisa menginfeksi komputer dan mencuri data. Ini adalah teknik baiting (umpan) dengan memanfaatkan rasa penasaran (reciprocity - Anda merasa 'diuntungkan' dengan info bocoran). Pelaku menggunakan konteks kantor untuk menurunkan kewaspadaan.",
            "points": 75,
            "tips": [
                "Jangan download file dari sumber tidak jelas, meski di grup 'terpercaya'",
                "Verifikasi identitas pengirim sebelum download file",
                "Gunakan antivirus dan scan file sebelum membuka",
                "Waspadai file dengan ekstensi ganda (.xlsx.exe) atau macro",
                "Jika terlalu menarik atau kontroversial, kemungkinan besar jebakan"
            ],
            "real_case_reference": "Modus penyebaran malware via file palsu sangat umum di Indonesia, terutama di lingkungan perkantoran",
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Hadiah Shopee 12.12",
            "category": "quid_pro_quo",
            "difficulty": "beginner",
            "cialdini_principle": "scarcity",
            "description": "SMS hadiah dari Shopee",
            "scenario": "Anda menerima SMS: 'Selamat! Anda memenangkan hadiah Shopee 12.12 senilai Rp 10 juta + iPhone 15 Pro Max. Klaim sekarang di: shopee-hadiah.com/claim?id=XXX. Buruan! Hanya berlaku 2 jam!'. Link terlihat meyakinkan dan ada batas waktu.",
            "question": "Kenapa ini adalah penipuan?",
            "options": [
                "Shopee tidak pernah memberi hadiah via SMS",
                "Domain bukan shopee.co.id (resmi) + tidak pernah daftar undian + tekanan waktu",
                "Hadiah terlalu besar",
                "SMS dikirim tengah malam"
            ],
            "correct_answer": 1,
            "explanation": "Kombinasi domain palsu, tidak pernah ikut undian, dan tekanan waktu ('hanya 2 jam') adalah ciri khas penipuan. Ini adalah Quid Pro Quo (sesuatu untuk sesuatu) - Anda diberi 'hadiah' tapi nanti akan diminta data pribadi, transfer 'biaya admin', atau install aplikasi berbahaya. Prinsip Scarcity (kelangkaan waktu) digunakan agar Anda tidak berpikir panjang.",
            "points": 50,
            "tips": [
                "Perusahaan resmi mengumumkan pemenang via channel resmi (aplikasi/email terverifikasi)",
                "Tidak ada 'hadiah mendadak' tanpa Anda pernah mengikuti undian",
                "Waspadai tekanan waktu yang membuat Anda panik",
                "Cek domain dengan teliti, typosquatting sangat umum",
                "Hadiah asli tidak pernah minta transfer biaya admin"
            ],
            "real_case_reference": "Modus hadiah palsu e-commerce sangat marak menjelang hari belanja besar di Indonesia",
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Investasi Bodong dengan Influencer",
            "category": "indonesian_case",
            "difficulty": "advanced",
            "cialdini_principle": "social_proof",
            "description": "Program investasi yang dipromosikan selebriti",
            "scenario": "Seorang influencer terkenal dengan 2 juta followers mempromosikan platform investasi 'CryptoGold Indonesia' yang menjanjikan return 30% per bulan. Ada testimoni banyak orang yang sudah withdraw jutaan rupiah. Website terlihat profesional, ada kantor fisik di Jakarta, dan sistem membernya sudah 50.000+ orang. Minimal investasi Rp 1 juta.",
            "question": "Apa red flag terbesar yang menunjukkan ini investasi bodong?",
            "options": [
                "Influencer pasti dibayar untuk promosi, bukan bukti aman",
                "Return 30%/bulan tidak realistis + tidak terdaftar OJK = ponzi scheme",
                "Minimal investasi Rp 1 juta terlalu rendah",
                "Website terlalu bagus"
            ],
            "correct_answer": 1,
            "explanation": "Return 30% per bulan tidak masuk akal dalam investasi legal apapun. Investasi resmi harus terdaftar di OJK (Otoritas Jasa Keuangan). Ini adalah Ponzi scheme yang menggunakan Social Proof (bukti sosial) dengan influencer, testimoni, dan jumlah member untuk menciptakan ilusi kredibilitas. Kantor fisik dan website profesional mudah dibuat.",
            "points": 100,
            "tips": [
                "Cek SELALU apakah investasi terdaftar resmi di OJK (cekreksa.ojk.go.id)",
                "Return tinggi = risiko tinggi, 30%/bulan adalah impossible di investasi legal",
                "Influencer endorsement bukan jaminan, mereka bisa dibayar atau tertipu juga",
                "Testimoni dan member banyak bisa dimanipulasi/dibuat-buat",
                "Jika diminta merekrut member lain untuk untung, itu adalah skema piramida"
            ],
            "real_case_reference": "Banyak kasus investasi bodong di Indonesia seperti Memiles, Pandora, Robot Trading yang merugikan ribuan orang miliaran rupiah",
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Teknik Tailgating di Kantor",
            "category": "tailgating",
            "difficulty": "intermediate",
            "cialdini_principle": "liking",
            "description": "Seseorang mengikuti Anda masuk ke area terbatas kantor",
            "scenario": "Anda baru keluar dari lift di lantai kantor yang memerlukan akses kartu. Seseorang berpakaian rapi, membawa laptop dan terlihat terburu-buru, mengatakan 'Aduh maaf, kartu saya ketinggalan di meja. Boleh nebeng masuk? Lagi urgent meeting nih'. Orang tersebut ramah dan terlihat seperti karyawan.",
            "question": "Apa yang sebaiknya Anda lakukan?",
            "options": [
                "Biarkan masuk karena terlihat seperti karyawan",
                "Minta dia menunggu, hubungi resepsionis/security untuk verifikasi",
                "Tanya nama dan department-nya saja",
                "Biarkan tapi awasi gerak-geriknya"
            ],
            "correct_answer": 1,
            "explanation": "Ini adalah tailgating, teknik masuk ke area terlarang dengan mengikuti orang yang memiliki akses sah. Pelaku menggunakan Liking principle (orang ramah lebih dipercaya) dan membuat skenario urgent. Protokol keamanan harus ditegakkan tanpa pandang bulu. Verifikasi melalui pihak berwenang adalah satu-satunya cara tepat.",
            "points": 75,
            "tips": [
                "Jangan merasa tidak enak, keamanan perusahaan lebih penting",
                "Setiap orang harus menggunakan akses sendiri, tidak ada 'nebeng'",
                "Pelaku social engineering ahli dalam membuat skenario darurat",
                "Laporkan segera ke security jika ada yang mencoba tailgating",
                "Penampilan profesional bukan jaminan identitas"
            ],
            "real_case_reference": "Tailgating adalah teknik umum yang digunakan untuk akses fisik ke data center atau kantor yang menyimpan informasi sensitif",
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Panggilan Palsu dari 'Polisi Cyber'",
            "category": "pretexting",
            "difficulty": "advanced",
            "cialdini_principle": "authority",
            "description": "Telepon dari seseorang yang mengaku polisi cyber",
            "scenario": "Anda menerima telepon dari nomor dengan caller ID 'POLRI CYBER'. Mereka mengatakan nomor Anda terlibat dalam kasus pencucian uang dan terorisme. Mereka meminta Anda transfer seluruh saldo ke 'rekening aman negara' untuk pemeriksaan, atau akan ditangkap. Mereka bisa menyebutkan data pribadi Anda dan berbicara dengan nada mengintimidasi.",
            "question": "Bagaimana cara terbaik menangani situasi ini?",
            "options": [
                "Transfer karena takut ditangkap",
                "Minta nomor resmi, tutup telepon, lapor ke polisi.go.id, dan ke bank",
                "Tanya detail kasusnya",
                "Rekam pembicaraan saja"
            ],
            "correct_answer": 1,
            "explanation": "Ini adalah penipuan sophisticate menggunakan authority principle. Polisi ASLI tidak akan pernah: 1) Meminta transfer uang, 2) Menginterogasi via telepon, 3) Meminta data sensitif. Caller ID bisa dipalsukan. Data pribadi Anda bisa dari kebocoran data. Pelaku menggunakan intimidasi untuk membuat Anda panik dan tidak berpikir jernih.",
            "points": 100,
            "tips": [
                "Polisi tidak akan meminta transfer uang untuk 'penyelidikan'",
                "Caller ID dapat dipalsukan dengan mudah (caller ID spoofing)",
                "Jika benar ada kasus, akan ada surat resmi atau panggilan langsung ke kantor polisi",
                "Jangan panik, tetap tenang dan verifikasi lewat channel resmi",
                "Segera lapor ke bank untuk blokir rekening jika sudah terlanjur transfer"
            ],
            "real_case_reference": "Modus penipuan mengatasnamakan polisi atau jaksa sangat marak di Indonesia, banyak korban kehilangan ratusan juta rupiah",
            "created_at": datetime.now(timezone.utc).isoformat()
        }
    ]
    
    await db.challenges.insert_many(challenges)
    print(f"✅ {len(challenges)} challenges created")
    
    # Seed education content
    education = [
        {
            "id": str(uuid.uuid4()),
            "title": "Prinsip Reciprocity (Timbal Balik)",
            "content_type": "cialdini_principle",
            "principle": "reciprocity",
            "content": "**Reciprocity** adalah kecenderungan manusia untuk membalas kebaikan. Dalam social engineering, pelaku memberikan sesuatu (hadiah, informasi, bantuan) agar korban merasa 'berhutang budi' dan lebih mudah dimanipulasi.\n\n**Contoh Serangan:**\n- Aplikasi 'gratis' yang sebenarnya mencuri data\n- Hadiah atau diskon palsu yang meminta data pribadi\n- File atau tools 'gratis' yang mengandung malware\n\n**Cara Melindungi Diri:**\n- Tidak ada yang benar-benar gratis, selalu ada trade-off\n- Tanyakan: 'Kenapa mereka memberi saya ini secara gratis?'\n- Baca terms & conditions, terutama perihal data pribadi\n- Jangan merasa 'harus' membalas dengan memberikan informasi sensitif"
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Prinsip Commitment (Komitmen)",
            "content_type": "cialdini_principle",
            "principle": "commitment",
            "content": "**Commitment** adalah kecenderungan untuk tetap konsisten dengan keputusan yang sudah dibuat. Pelaku membuat korban melakukan komitmen kecil, lalu secara bertahap meminta lebih banyak.\n\n**Contoh Serangan:**\n- Survey 'tidak berbahaya' yang bertanya data pribadi secara bertahap\n- Investasi kecil awal, lalu diminta invest lebih besar\n- 'Coba dulu gratis' yang berujung langganan berbayar sulit dibatalkan\n\n**Cara Melindungi Diri:**\n- Evaluasi setiap permintaan secara terpisah, tidak berdasar komitmen sebelumnya\n- Jangan takut untuk berhenti meski sudah 'terlanjur' mulai\n- Waspadai teknik 'foot-in-the-door' (minta kecil dulu, lalu besar)\n- Sunk cost fallacy: uang/waktu yang sudah keluar bukan alasan untuk terus"
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Prinsip Social Proof (Bukti Sosial)",
            "content_type": "cialdini_principle",
            "principle": "social_proof",
            "content": "**Social Proof** adalah kecenderungan mengikuti perilaku orang lain, terutama saat tidak yakin. Pelaku membuat ilusi bahwa 'banyak orang sudah melakukannya' untuk menurunkan kewaspadaan.\n\n**Contoh Serangan:**\n- Testimoni palsu dari 'ribuan pengguna'\n- 'Teman Anda sudah download file ini'\n- Influencer endorsement untuk produk/investasi scam\n- Notifikasi palsu 'X orang baru saja membeli'\n\n**Cara Melindungi Diri:**\n- Testimoni bisa dibuat-buat atau dibeli\n- Jumlah followers/members bisa dimanipulasi\n- Verifikasi independen, jangan hanya percaya 'kata orang'\n- Influencer bisa dibayar atau bahkan tertipu juga\n- Cek review di berbagai platform, bukan hanya di website mereka"
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Prinsip Authority (Otoritas)",
            "content_type": "cialdini_principle",
            "principle": "authority",
            "content": "**Authority** adalah kecenderungan patuh pada figur otoritas. Pelaku menyamar sebagai orang/institusi berkuasa untuk membuat korban lebih mudah percaya dan taat.\n\n**Contoh Serangan:**\n- Email palsu dari 'bank', 'polisi', atau 'pemerintah'\n- Telepon dari 'customer service' atau 'security team'\n- Website dengan logo resmi yang sebenarnya palsu\n- Seseorang berpakaian formal/seragam untuk akses fisik\n\n**Cara Melindungi Diri:**\n- Verifikasi SELALU melalui channel resmi (website/nomor resmi)\n- Otoritas asli tidak akan meminta data sensitif via telepon/email\n- Logo, seragam, dan caller ID dapat dipalsukan\n- Jangan panik saat diintimidasi, tetap berpikir logis\n- Jika ragu, tutup komunikasi dan hubungi instansi terkait langsung"
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Prinsip Liking (Kesukaan)",
            "content_type": "cialdini_principle",
            "principle": "liking",
            "content": "**Liking** adalah kecenderungan lebih mudah terpengaruh oleh orang yang kita sukai atau mirip dengan kita. Pelaku membangun rapport dan kesamaan untuk menurunkan kewaspadaan.\n\n**Contoh Serangan:**\n- Pelaku bersikap sangat ramah dan helpful\n- Mencari kesamaan (alumni, hobi, asal daerah)\n- Pujian berlebihan untuk menurunkan guard\n- 'Teman dari teman' untuk membangun trust\n\n**Cara Melindungi Diri:**\n- Pisahkan keputusan keamanan dari perasaan pribadi\n- Keramahan bukan jaminan niat baik\n- Tetap ikuti protokol keamanan meski orangnya 'baik'\n- Kesamaan bisa dicari tahu dari media sosial (stalking)\n- Jangan merasa 'tidak enak' untuk menolak atau memverifikasi"
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Prinsip Scarcity (Kelangkaan)",
            "content_type": "cialdini_principle",
            "principle": "scarcity",
            "content": "**Scarcity** adalah kecenderungan menginginkan sesuatu lebih kuat saat terlihat langka atau terbatas. Pelaku menciptakan urgency agar korban bertindak cepat tanpa berpikir panjang.\n\n**Contoh Serangan:**\n- 'Penawaran terbatas, hanya hari ini!'\n- 'Hanya 2 jam lagi atau akun diblokir'\n- 'Stok terbatas, buruan!'\n- 'Kesempatan terakhir untuk klaim hadiah'\n\n**Cara Melindungi Diri:**\n- Tekanan waktu adalah red flag, bukan motivasi\n- Penawaran bagus biasanya tidak hilang dalam hitungan jam\n- Ambil waktu untuk berpikir dan verifikasi, tidak perlu buru-buru\n- Jika memang legit, opportunity akan datang lagi\n- Scarcity artifisial: dibuat-buat untuk manipulasi"
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Tips Umum Pencegahan Social Engineering",
            "content_type": "prevention_tips",
            "content": "**10 Golden Rules Melindungi Diri dari Social Engineering:**\n\n1. **Verifikasi, Verifikasi, Verifikasi** - Selalu konfirmasi identitas melalui channel resmi\n2. **Jangan Panik** - Pelaku sengaja membuat Anda panik agar tidak berpikir jernih\n3. **Slow Down** - Tekanan waktu adalah taktik manipulasi, ambil waktu untuk berpikir\n4. **JANGAN PERNAH Bagi OTP/Password** - Tidak ada alasan valid untuk membagikannya\n5. **Cek Domain & URL** - Typosquatting sangat umum (toped.com vs tokopedia.com)\n6. **Too Good to Be True** - Jika terlalu bagus, kemungkinan besar memang bukan real\n7. **Protect Your Data** - Jangan sembarangan isi survey atau beri informasi pribadi\n8. **Update Knowledge** - Modus selalu berkembang, stay informed\n9. **Trust Your Gut** - Jika ada yang terasa aneh, kemungkinan memang aneh\n10. **Report Suspicious Activity** - Bantu orang lain dengan melaporkan penipuan\n\n**Khusus Indonesia:**\n- Cek investasi di OJK (cekreksa.ojk.go.id)\n- Lapor penipuan ke patrolisiber.id\n- Gunakan QRIS resmi, hindari transfer ke rekening pribadi\n- Aktifkan notifikasi transaksi perbankan\n- Jangan install APK dari luar Play Store/App Store"
        }
    ]
    
    await db.education.insert_many(education)
    print(f"✅ {len(education)} education contents created")
    
    print("\n🎉 Database seeding completed successfully!")
    client.close()

if __name__ == "__main__":
    asyncio.run(seed_data())