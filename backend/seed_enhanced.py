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

async def seed_enhanced():
    print("🌱 Seeding enhanced data...")
    
    # Clear existing challenges
    await db.challenges.delete_many({})
    await db.feedbacks.delete_many({})
    
    challenges = [
        # Challenge 1: Multi-question Phishing Email
        {
            "id": str(uuid.uuid4()),
            "title": "Analisis Email Phishing Bank BCA",
            "category": "phishing",
            "difficulty": "beginner",
            "cialdini_principle": "authority",
            "challenge_type": "multi_choice",
            "description": "Analisis email phishing yang mengaku dari Bank BCA dengan beberapa red flags",
            "scenario": "Anda menerima email dengan subject 'URGENT: Verifikasi Akun BCA Dalam 24 Jam'. Email berisi logo BCA, mengancam pemblokiran akun, dan meminta klik link 'm-bca-verify.com/secure'. Sender: security@bcabank.co.id",
            "questions": [
                {
                    "question": "Apa red flag pertama dari domain email pengirim 'security@bcabank.co.id'?",
                    "options": [
                        "Tidak ada yang salah, domain terlihat resmi",
                        "Domain resmi BCA adalah 'bca.co.id' bukan 'bcabank.co.id' (typosquatting)",
                        "Email terlalu panjang",
                        "Menggunakan @ symbol"
                    ],
                    "correct_answer": 1,
                    "explanation": "Typosquatting adalah teknik menggunakan domain mirip. Domain resmi BCA adalah 'bca.co.id', bukan 'bcabank.co.id' atau variasi lainnya."
                },
                {
                    "question": "Link 'm-bca-verify.com' mencurigakan karena?",
                    "options": [
                        "Terlalu pendek",
                        "Bukan domain resmi BCA (klikbca.com) dan menggunakan taktik misleading dengan prefix 'm-'",
                        "Menggunakan https",
                        "Ada kata 'verify'"
                    ],
                    "correct_answer": 1,
                    "explanation": "Domain resmi BCA untuk mobile banking adalah 'm.klikbca.com', bukan 'm-bca-verify.com'. Pelaku menggunakan prefix 'm-' untuk menyesatkan."
                },
                {
                    "question": "Ancaman 'pemblokiran akun dalam 24 jam' menggunakan prinsip psikologi apa?",
                    "options": [
                        "Reciprocity - timbal balik",
                        "Scarcity - kelangkaan waktu untuk menciptakan panic",
                        "Liking - kesukaan",
                        "Commitment - komitmen"
                    ],
                    "correct_answer": 1,
                    "explanation": "Teknik Scarcity (kelangkaan waktu) digunakan untuk membuat korban panik dan bertindak cepat tanpa berpikir panjang. Ini adalah taktik social engineering klasik."
                }
            ],
            "points": 75,
            "tips": [
                "Bank tidak pernah meminta verifikasi via email dengan ancaman",
                "Cek domain dengan teliti - hover mouse di link sebelum klik",
                "Gunakan aplikasi resmi atau ketik URL langsung di browser",
                "Tekanan waktu adalah tanda phishing"
            ],
            "real_case_reference": "Modus phishing BCA dengan domain palsu sangat marak 2020-2024",
            "time_limit_seconds": 180,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        
        # Challenge 2: Chat Simulation with Scammer
        {
            "id": str(uuid.uuid4()),
            "title": "Simulasi Chat dengan Penipu WhatsApp",
            "category": "pretexting",
            "difficulty": "intermediate",
            "cialdini_principle": "authority",
            "challenge_type": "multi_choice",
            "description": "Chat WhatsApp dari nomor mengaku Customer Service e-commerce",
            "scenario": "Anda menerima WA: 'Halo, saya CS Tokopedia. Ada transaksi mencurigakan Rp 8.5 juta menggunakan akun Anda. Untuk cancel, mohon berikan kode OTP yang baru kami kirim via SMS. Fast response ya, transaksi akan diproses 15 menit lagi! 🙏'",
            "questions": [
                {
                    "question": "Red flag pertama dari pesan ini?",
                    "options": [
                        "Menggunakan emoji",
                        "CS resmi tidak pernah menghubungi via WA pribadi + meminta OTP",
                        "Menyebutkan nominal transaksi",
                        "Menggunakan bahasa Indonesia"
                    ],
                    "correct_answer": 1,
                    "explanation": "CS e-commerce resmi menghubungi via in-app chat atau telepon ke nomor resmi tercatat. TIDAK PERNAH meminta OTP."
                },
                {
                    "question": "Kenapa pelaku meminta 'fast response'?",
                    "options": [
                        "Untuk membantu Anda lebih cepat",
                        "Teknik pressure (scarcity) agar victim panik dan tidak berpikir",
                        "Karena sistem mereka lambat",
                        "Standard Operating Procedure"
                    ],
                    "correct_answer": 1,
                    "explanation": "Tekanan waktu adalah taktik social engineering untuk mencegah korban verifikasi kebenaran dan berpikir logis."
                },
                {
                    "question": "Apa yang HARUS Anda lakukan?",
                    "options": [
                        "Berikan OTP karena ingin cepat selesai",
                        "Balas dengan pertanyaan untuk menguji",
                        "Abaikan/block, cek app langsung, hubungi CS via channel resmi",
                        "Minta dia telepon saja"
                    ],
                    "correct_answer": 2,
                    "explanation": "Jangan pernah memberikan OTP. Abaikan pesan, buka aplikasi untuk cek transaksi, dan hubungi CS via channel resmi (in-app atau nomor official)."
                },
                {
                    "question": "Jika sudah terlanjur berikan OTP, langkah emergency?",
                    "options": [
                        "Tunggu saja",
                        "Immediately: Logout all device di app, ganti password, hubungi CS, lapor ke bank",
                        "Hapus chat",
                        "Block nomor saja"
                    ],
                    "correct_answer": 1,
                    "explanation": "Harus bertindak cepat: logout paksa semua device, ganti password, freeze akun e-wallet/banking, dan lapor ke CS + pihak berwenang."
                }
            ],
            "points": 100,
            "tips": [
                "OTP = password akun Anda. JANGAN PERNAH dibagikan",
                "CS resmi tidak menghubungi via WhatsApp pribadi",
                "Tekanan waktu adalah red flag besar",
                "Selalu verifikasi via channel resmi",
                "Simpan nomor CS resmi di kontak"
            ],
            "real_case_reference": "Modus penipuan OTP via WhatsApp paling marak di Indonesia, ribuan korban tiap bulan",
            "time_limit_seconds": 240,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        
        # Challenge 3: Spot the Difference - Fake vs Real Website
        {
            "id": str(uuid.uuid4()),
            "title": "Identifikasi Website Palsu vs Asli",
            "category": "phishing",
            "difficulty": "intermediate",
            "cialdini_principle": "authority",
            "challenge_type": "multi_choice",
            "description": "Analisis perbedaan antara website phishing dan website asli",
            "scenario": "Anda menerima email promosi 'Diskon 90% Shopee 12.12!' dengan link. Setelah diklik, muncul website yang sangat mirip Shopee meminta login. URL: shopee-promo.com",
            "questions": [
                {
                    "question": "Apa masalah utama dari URL 'shopee-promo.com'?",
                    "options": [
                        "Terlalu panjang",
                        "Bukan domain resmi Shopee (shopee.co.id), ini adalah domain phishing terpisah",
                        "Menggunakan dash (-)",
                        "Tidak ada masalah"
                    ],
                    "correct_answer": 1,
                    "explanation": "Domain resmi Shopee adalah 'shopee.co.id'. Domain 'shopee-promo.com' adalah domain terpisah yang dibeli penipu, bukan subdomain resmi."
                },
                {
                    "question": "Website meminta username dan password. Apa yang mencurigakan?",
                    "options": [
                        "Form login normal saja",
                        "Website promo seharusnya redirect ke shopee.co.id, tidak meminta login di domain berbeda",
                        "Ada captcha",
                        "Desain bagus"
                    ],
                    "correct_answer": 1,
                    "explanation": "Promo resmi akan redirect ke shopee.co.id untuk login. Website phishing meminta kredensial di domain palsu untuk mencuri akun."
                },
                {
                    "question": "Cek HTTPS (gembok hijau). Apakah itu jaminan aman?",
                    "options": [
                        "Ya, HTTPS = 100% aman",
                        "TIDAK! HTTPS hanya enkripsi koneksi, domain tetap bisa palsu. Phisher bisa beli SSL certificate murah",
                        "HTTPS lebih aman dari HTTP",
                        "Tidak ada bedanya"
                    ],
                    "correct_answer": 1,
                    "explanation": "HTTPS hanya mengenkripsi data transfer, BUKAN menjamin website legit. Phisher mudah mendapat SSL certificate gratis (Let's Encrypt). Yang penting adalah DOMAIN, bukan HTTPS."
                }
            ],
            "points": 90,
            "tips": [
                "Cek domain dengan sangat teliti sebelum input kredensial",
                "HTTPS bukan jaminan legit, lihat nama domainnya",
                "Promo resmi akan di domain/subdomain resmi",
                "Jangan login lewat link email, ketik manual di browser",
                "Gunakan password manager untuk deteksi domain palsu"
            ],
            "real_case_reference": "Website phishing e-commerce dengan SSL certificate sangat umum, tampilan 99% mirip asli",
            "time_limit_seconds": 200,
            "created_at": datetime.now(timezone.utc).isoformat()
        },

        # Challenge 4: Timeline Attack Analysis
        {
            "id": str(uuid.uuid4()),
            "title": "Kronologi Serangan Investasi Bodong",
            "category": "indonesian_case",
            "difficulty": "advanced",
            "cialdini_principle": "social_proof",
            "challenge_type": "multi_choice",
            "description": "Analisis tahapan serangan investasi bodong",
            "scenario": "Platform 'BinariBot Trading' menjanjikan profit 30%/bulan. Dipromosikan influencer, kantor mewah di Jakarta, member 100K+. Sistem referral wajib untuk withdraw. Tidak terdaftar OJK.",
            "questions": [
                {
                    "question": "Red flag PALING KRITIS yang mengindikasikan Ponzi scheme?",
                    "options": [
                        "Kantor mewah",
                        "Tidak terdaftar OJK + sistem referral wajib untuk withdraw = confirmed Ponzi",
                        "Profit 30% tinggi",
                        "Member banyak"
                    ],
                    "correct_answer": 1,
                    "explanation": "Investasi legal HARUS terdaftar OJK. Sistem referral wajib untuk withdraw adalah ciri Ponzi scheme - uang member baru bayar member lama."
                },
                {
                    "question": "Prinsip Cialdini apa yang digunakan dengan '100K+ member' dan influencer?",
                    "options": [
                        "Scarcity",
                        "Social Proof - 'banyak orang ikut pasti aman' (padahal bisa fake)",
                        "Reciprocity",
                        "Liking"
                    ],
                    "correct_answer": 1,
                    "explanation": "Social Proof dieksploitasi dengan menunjukkan 'banyak orang sudah ikut'. Jumlah member dan endorsement influencer menciptakan ilusi kredibilitas."
                },
                {
                    "question": "Kenapa 'kantor mewah di Jakarta' bukan jaminan aman?",
                    "options": [
                        "Lokasi tidak penting",
                        "Kantor fisik mudah disewa untuk kredibilitas palsu, yang penting izin OJK",
                        "Jakarta terlalu ramai",
                        "Kantor mewah pasti aman"
                    ],
                    "correct_answer": 1,
                    "explanation": "Kantor mewah hanya props untuk legitimasi. Sewa 1-2 tahun tidak mahal untuk scammer yang kumpulkan miliaran. Cek izin OJK adalah satu-satunya validasi."
                },
                {
                    "question": "Apa yang harus dilakukan sebelum invest?",
                    "options": [
                        "Lihat testimoni di website mereka",
                        "Cek di website OJK (cekreksa.ojk.go.id), research independent, konsultasi financial advisor",
                        "Ikut karena teman sudah profit",
                        "Coba invest kecil dulu"
                    ],
                    "correct_answer": 1,
                    "explanation": "WAJIB cek registrasi di website resmi OJK (cekreksa.ojk.go.id). Jangan percaya testimoni dari platform mereka atau 'profit' teman (bisa early member atau fake)."
                }
            ],
            "points": 120,
            "tips": [
                "Cek SELALU di cekreksa.ojk.go.id sebelum invest",
                "Return 30%/bulan = impossible di investasi legal",
                "Sistem referral wajib = pyramid scheme",
                "Influencer bisa dibayar atau jadi korban juga",
                "Kantor fisik bukan jaminan, izin OJK adalah jaminan"
            ],
            "real_case_reference": "Kasus Pandora, Robot Trading, Memiles di Indonesia rugikan investor miliaran rupiah",
            "time_limit_seconds": 300,
            "created_at": datetime.now(timezone.utc).isoformat()
        },

        # Challenge 5: File Baiting Analysis
        {
            "id": str(uuid.uuid4()),
            "title": "Analisis File Berbahaya: Gaji_Karyawan_2025.xlsx",
            "category": "baiting",
            "difficulty": "intermediate",
            "cialdini_principle": "reciprocity",
            "challenge_type": "multi_choice",
            "description": "Identifikasi bahaya file yang dibagikan di grup kantor",
            "scenario": "Di grup WA kantor, nomor tidak dikenal membagikan file 'Gaji_Karyawan_2025.xlsx' dengan pesan: 'Bocoran kenaikan gaji tahun depan nih, jangan sampai HRD tau ya 🤫'. File size: 25KB.",
            "questions": [
                {
                    "question": "Apa bahaya utama dari file Excel yang tidak jelas sumbernya?",
                    "options": [
                        "Tidak ada bahaya, hanya Excel",
                        "Bisa mengandung macro malicious yang install malware/ransomware saat dibuka",
                        "File terlalu kecil",
                        "Format .xlsx tidak berbahaya"
                    ],
                    "correct_answer": 1,
                    "explanation": "File Excel dapat berisi macro VBA yang execute code berbahaya. Malware dapat mencuri data, install ransomware, atau backdoor untuk akses remote."
                },
                {
                    "question": "File size 25KB untuk Excel 'daftar gaji' mencurigakan karena?",
                    "options": [
                        "Ukuran normal",
                        "Terlalu kecil untuk berisi data banyak, kemungkinan hanya macro/script",
                        "Terlalu besar",
                        "Tidak ada hubungannya"
                    ],
                    "correct_answer": 1,
                    "explanation": "Excel dengan data gaji karyawan biasanya >100KB. File 25KB kemungkinan mostly berisi macro malicious dengan data dummy sedikit sebagai kamuflase."
                },
                {
                    "question": "Prinsip social engineering apa yang dieksploitasi?",
                    "options": [
                        "Authority",
                        "Reciprocity - 'mendapat info bocoran' + curiosity membuat victim merasa 'beruntung' dan download",
                        "Commitment",
                        "Scarcity"
                    ],
                    "correct_answer": 1,
                    "explanation": "Reciprocity dimanfaatkan dengan 'memberikan' info eksklusif. Ditambah curiosity (penasaran gaji) dan thrill 'melanggar aturan' menurunkan kewaspadaan."
                },
                {
                    "question": "Langkah aman jika tetap ingin cek file?",
                    "options": [
                        "Langsung buka di komputer kantor",
                        "Upload ke VirusTotal.com, scan antivirus, buka di sandbox/VM, disable macro",
                        "Buka di HP",
                        "Forward ke IT dulu"
                    ],
                    "correct_answer": 1,
                    "explanation": "Best practice: scan dengan VirusTotal, buka di virtual machine terpisah dengan macro disabled. Jangan buka di komputer utama atau jaringan kantor."
                }
            ],
            "points": 100,
            "tips": [
                "Jangan download file dari sumber tidak jelas",
                "File size yang tidak wajar adalah red flag",
                "Excel dengan macro bisa sangat berbahaya",
                "Gunakan VirusTotal untuk scan file mencurigakan",
                "Curiosity dan 'info eksklusif' adalah jebakan"
            ],
            "real_case_reference": "Ransomware WannaCry dan banyak malware lain spread via malicious Office files",
            "time_limit_seconds": 220,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
    ]
    
    await db.challenges.insert_many(challenges)
    print(f"✅ {len(challenges)} enhanced challenges created")
    
    print("\n🎉 Enhanced seeding completed!")
    client.close()

if __name__ == "__main__":
    asyncio.run(seed_enhanced())