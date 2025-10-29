import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
import uuid
from datetime import datetime, timezone

mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ.get('DB_NAME', 'tegalsec_lab')]

async def seed_indonesia_challenges():
    print("🇮🇩 Seeding Indonesian case challenges with Cialdini categories...")
    
    # Don't delete existing, just add more
    challenges = [
        # RECIPROCITY - Indonesian Cases (5 challenges)
        {
            "id": str(uuid.uuid4()),
            "title": "Jebakan Pinjol: Pinjaman Rp 500 ribu Jadi Rp 5 juta",
            "category": "indonesian_case",
            "difficulty": "intermediate",
            "cialdini_principle": "reciprocity",
            "challenge_type": "multi_choice",
            "description": "Kasus nyata pinjaman online predatory yang memanfaatkan prinsip reciprocity",
            "scenario": "Bu Siti butuh dana darurat Rp 500 ribu. Dapat iklan 'Pinjol Cepat Cair 5 Menit - Bunga 0%!'. Setelah approve, ternyata dana cair Rp 450 ribu (potongan admin Rp 50 ribu tidak dijelaskan). Notifikasi muncul: 'Terima kasih sudah percaya kami! Sebagai ucapan terima kasih, limit Anda naik jadi Rp 5 juta!'. 2 minggu kemudian, tagihan muncul: Rp 750 ribu (bunga 50% per 2 minggu). SMS teror dimulai, ancam sebar data ke kontak.",
            "questions": [
                {
                    "question": "Bagaimana reciprocity dimanipulasi dalam kasus ini?",
                    "options": [
                        "Pinjol memberikan pinjaman dengan baik hati",
                        "'Terima kasih sudah percaya' dan 'limit naik' menciptakan rasa berhutang budi, tekanan psikologis untuk 'membalas kebaikan' dengan bayar tanpa protes",
                        "Bunga 0% adalah penawaran jujur",
                        "SMS teror adalah prosedur normal"
                    ],
                    "correct_answer": 1,
                    "explanation": "Pinjol menciptakan ilusi 'kebaikan' dan 'kepercayaan' agar korban merasa berhutang budi secara emosional, tidak hanya finansial. 'Limit naik' dibingkai sebagai reward, bukan jebakan utang lebih besar."
                },
                {
                    "question": "Red flag utama dari 'Bunga 0%' di iklan?",
                    "options": [
                        "Tidak ada red flag, bunga memang 0%",
                        "Hidden fee ekstrem (admin 10%, bunga 50% per 2 minggu) tidak disclosed upfront - classic bait advertising",
                        "Wajar untuk bisnis",
                        "Legal karena ada di T&C"
                    ],
                    "correct_answer": 1,
                    "explanation": "Bunga 0% di iklan adalah clickbait. Fee sebenarnya hidden di T&C halaman 20. Total APR bisa >300%. Di Indonesia, banyak pinjol ilegal tidak terdaftar OJK."
                }
            ],
            "points": 150,
            "tips": ["Cek registrasi OJK", "Hitung total biaya sebelum pinjam", "Jangan mudah tergiur 'bunga 0%'"],
            "real_case_reference": "Kasus serupa pinjol ilegal yang viral 2023-2024 dengan ratusan korban",
            "time_limit_seconds": 240,
            "created_at": datetime.now(timezone.utc)
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Voucher Gratis Marketplace: Trap Belanja Minimal",
            "category": "indonesian_case",
            "difficulty": "beginner",
            "cialdini_principle": "reciprocity",
            "challenge_type": "multi_choice",
            "description": "Analisis taktik reciprocity pada voucher gratis e-commerce Indonesia",
            "scenario": "Dapat notifikasi dari Tokobeli: 'Selamat! Anda dapat voucher GRATIS Rp 100 ribu!'. Klik langsung, excited. Di halaman voucher: 'Voucher Rp 100K - Min. belanja Rp 500K - Berlaku hari ini saja!'. Produk yang mau dibeli Rp 200K, jadi beli produk lain sampai Rp 500K untuk 'manfaatkan voucher'. Total bayar Rp 400K (500K - 100K). Tanpa voucher, cuma butuh Rp 200K.",
            "questions": [
                {
                    "question": "Bagaimana reciprocity dieksploitasi?",
                    "options": [
                        "Voucher gratis adalah genuine gift",
                        "'Voucher gratis' creates obligation to use it. Minimal belanja Rp 500K forces spending Rp 400K lebih untuk 'save' Rp 100K - net loss Rp 200K",
                        "User untung Rp 100K",
                        "Strategi marketing biasa"
                    ],
                    "correct_answer": 1,
                    "explanation": "Psychological trap: 'Gratis Rp 100K' feels like obligation to use (reciprocity). User rationalizes 'rugi kalau tidak pakai', padahal forced spending Rp 300K extra barang tidak butuh."
                },
                {
                    "question": "Taktik urgensi 'Berlaku hari ini saja' bertujuan untuk?",
                    "options": [
                        "Membantu user segera hemat",
                        "Kombinasi scarcity + reciprocity: user panic tidak mau 'buang' voucher gratis, impulsive buying tanpa pikir panjang",
                        "Sistem otomatis marketplace",
                        "Regulasi pemerintah"
                    ],
                    "correct_answer": 1,
                    "explanation": "Time pressure (scarcity) + voucher 'gratis' (reciprocity) = powerful combo untuk impulsive buying. User tidak sempat calculate apakah benar-benar hemat."
                }
            ],
            "points": 100,
            "tips": ["Calculate total spending vs voucher", "Jangan beli barang tidak perlu demi voucher", "Cek apakah benar hemat"],
            "real_case_reference": "Taktik umum marketplace Indonesia: Tokopedia, Shopee, Lazada",
            "time_limit_seconds": 180,
            "created_at": datetime.now(timezone.utc)
        },
        
        # COMMITMENT & CONSISTENCY - Indonesian Cases (4 challenges)
        {
            "id": str(uuid.uuid4()),
            "title": "MLM Skincare: Sudah Beli Starter Pack, Rugi Kalau Berhenti",
            "category": "indonesian_case",
            "difficulty": "intermediate",
            "cialdini_principle": "commitment",
            "challenge_type": "multi_choice",
            "description": "Analisis commitment trap dalam MLM Indonesia",
            "scenario": "Teman kulama ajak 'peluang bisnis'. Presentasi MLM skincare 'BeautéPro': 'Omset 50 juta/bulan!'. Starter pack Rp 5 juta (produk + 'member reseller'). Setelah beli, produk susah laku. Upline bilang: 'Kamu sudah invest 5 juta, sayang kalau berhenti sekarang! Beli paket Rp 10 juta, bisa jadi leader, passive income!'. 3 bulan jalan, sudah invest Rp 20 juta, omset Rp 500 ribu. Tapi merasa 'sudah terlanjur basah', terus invest.",
            "questions": [
                {
                    "question": "Bagaimana commitment & consistency dieksploitasi?",
                    "options": [
                        "MLM adalah bisnis legitimate",
                        "Initial investment Rp 5 juta creates commitment. Sunk cost fallacy: 'Sudah invest banyak, rugi kalau stop' - padahal stop now = cut loss",
                        "Passive income 50 juta adalah realistic",
                        "Upline membantu dengan genuine advice"
                    ],
                    "correct_answer": 1,
                    "explanation": "Setiap investment creates stronger commitment. Upline exploit sunk cost fallacy: 'sudah invest X, jangan sia-siakan!' Truth: past investment tidak bisa kembali, stop now = prevent further loss."
                },
                {
                    "question": "Red flag dari 'Omset 50 juta/bulan'?",
                    "options": [
                        "Income disclosure yang realistic",
                        "Survivorship bias: hanya top 1% berhasil (rekrut downline banyak), 99% rugi. Average member MLM di Indonesia rugi bersih",
                        "Semua bisa capai dengan kerja keras",
                        "Legal dan terdaftar"
                    ],
                    "correct_answer": 1,
                    "explanation": "MLM income primarily dari rekrut downline, bukan jual produk. 'Success story' adalah top pyramid. Study: 99% MLM participants lose money atau break-even."
                }
            ],
            "points": 150,
            "tips": ["Waspada sunk cost fallacy", "MLM income from recruitment, not product", "Calculate actual ROI"],
            "real_case_reference": "Banyak MLM skincare, suplemen, investasi di Indonesia dengan pola serupa",
            "time_limit_seconds": 240,
            "created_at": datetime.now(timezone.utc)
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Arisan Online: Sudah 10x Transfer, Tinggal 2x Lagi",
            "category": "indonesian_case",
            "difficulty": "advanced",
            "cialdini_principle": "commitment",
            "challenge_type": "multi_choice",
            "description": "Money game dengan commitment manipulation",
            "scenario": "Arisan online 'Blessing Limpah': sistem 1 orang dapat 'blessing' Rp 10 juta, butuh 12 peserta @ Rp 1 juta. Diajak teman, 'Aku sudah dapat blessing Rp 10 juta, sekarang giliranmu!'. Join dengan transfer Rp 1 juta. Setelah 10x 'support' (transfer Rp 1 juta ke member baru), tracking: 'Kamu tinggal 2x support lagi untuk dapat Rp 10 juta!'. Tiba-tiba group sepi, admin off. Sudah transfer total Rp 10 juta, belum dapat Rp 10 juta back.",
            "questions": [
                {
                    "question": "Bagaimana commitment digunakan untuk jebakan?",
                    "options": [
                        "Arisan online adalah sistem fair",
                        "Setiap transfer Rp 1 juta deepens commitment. At 10x transfer (Rp 10 juta), stopping feels impossible - 'tinggal 2x lagi!' padahal Ponzi scheme akan collapse",
                        "Admin temporary busy",
                        "Blessing system adalah rejeki"
                    ],
                    "correct_answer": 1,
                    "explanation": "Classic Ponzi commitment trap: setiap 'support' increases sunk cost. Progress bar '10/12' creates false hope. Scheme need continuous new members; when slows = collapse, last members lose all."
                },
                {
                    "question": "Mengapa sistem ini unsustainable secara matematis?",
                    "options": [
                        "Bisa sustainable kalau semua jujur",
                        "Ponzi scheme: butuh eksponential growth members. 12 → 144 → 1,728 → 20,736 members in 4 cycles. Akan collapse when recruitment slows",
                        "Rezeki tidak bisa dihitung",
                        "Sistem arisan tradisional proven"
                    ],
                    "correct_answer": 1,
                    "explanation": "Mathematical impossibility: each cycle need 12x more members. After beberapa cycle, exceed population. Early members profit from later members' loss. Indonesia: many cases (MMM, arisan berantai, dinar dirham)."
                }
            ],
            "points": 200,
            "tips": ["Ponzi scheme selalu collapse", "Hitung exponential growth requirement", "If sounds too good to be true, it is"],
            "real_case_reference": "Kasus arisan online berantai yang viral di WhatsApp Group Indonesia 2020-2024",
            "time_limit_seconds": 300,
            "created_at": datetime.now(timezone.utc)
        },
        
        # SOCIAL PROOF - Indonesian Cases (4 challenges)
        {
            "id": str(uuid.uuid4()),
            "title": "Investasi Crypto Ponzi: 2000 Member Grup Telegram",
            "category": "indonesian_case",
            "difficulty": "advanced",
            "cialdini_principle": "social_proof",
            "challenge_type": "multi_choice",
            "description": "Ponzi scheme menggunakan social proof palsu",
            "scenario": "Dapat invite Telegram group 'Crypto Profits Indonesia' - 2,000 members. Tiap hari ratusan 'testimony': 'Terima kasih admin! Profit Rp 50 juta dalam 3 bulan!', with screenshot transfer. Admin post: 'Trading bot AI 95% win rate, guaranteed 30% monthly return. Minimal deposit Rp 5 juta'. Lihat begitu banyak orang success, FOMO. Deposit Rp 10 juta. 2 bulan dapat 'profit' Rp 5 juta (bisa withdraw). Excited, deposit Rp 50 juta. 1 bulan kemudian, group tiba-tiba disbanded, website offline, uang Rp 50 juta hilang.",
            "questions": [
                {
                    "question": "Bagaimana social proof dimanipulasi?",
                    "options": [
                        "2000 members dan ratusan testimony adalah genuine proof",
                        "Fake members (bots), fake testimonies (admin accounts), initial withdraw (bait) - semua engineered untuk create social proof palsu",
                        "Trading bot AI memang profitable",
                        "Kebetulan website down"
                    ],
                    "correct_answer": 1,
                    "explanation": "Scammer use bots untuk inflate member count, paid actors untuk fake testimony, allow small initial withdrawals (dari deposit member baru) as 'proof'. Create illusion of social proof untuk attract bigger victims."
                },
                {
                    "question": "Mengapa '30% monthly return guaranteed' adalah red flag besar?",
                    "options": [
                        "Possible dengan AI trading bot",
                        "Mathematically impossible to guarantee: 30%/month = 2,300% annually. Warren Buffett rata-rata 20%/year. 'Guaranteed' high return = definitely scam",
                        "Crypto sangat volatile, bisa saja",
                        "Indonesia market berbeda"
                    ],
                    "correct_answer": 1,
                    "explanation": "Financial rule: returns correlate with risk. 'Guaranteed' + 'high return' tidak bisa coexist. 30% monthly = Ponzi scheme red flag. No legitimate investment can guarantee ini."
                }
            ],
            "points": 200,
            "tips": ["Verify testimonies (reverse image search)", "No investment guarantees high return", "Check legal registration"],
            "real_case_reference": "Banyak kasus crypto Ponzi di Indonesia: Indodax scam impersonators, Binance fake groups, 2021-2024",
            "time_limit_seconds": 300,
            "created_at": datetime.now(timezone.utc)
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Toko Online Fake: 10,000 Followers Instagram",
            "category": "indonesian_case",
            "difficulty": "beginner",
            "cialdini_principle": "social_proof",
            "challenge_type": "multi_choice",
            "description": "E-commerce scam menggunakan social proof palsu",
            "scenario": "Cari iPhone 15 Pro murah di Instagram. Dapat akun @gadgetmurahofficial - 10,000 followers, 500+ post, ratusan comments positif setiap post. Harga iPhone 15 Pro: Rp 8 juta (normal Rp 20 juta). Story: 'Sisa 3 unit! 50 orang sudah order hari ini!' Transfer Rp 8 juta via rekening pribadi (bukan merchant). Setelah transfer, diblock. Report Instagram, akun terhapus.",
            "questions": [
                {
                    "question": "Bagaimana scammer create fake social proof?",
                    "options": [
                        "Semua followers dan comments adalah genuine",
                        "Buy followers dari bot/fake accounts (Rp 100K for 10K followers), hire paid commenters, steal product photos - create illusion legitimacy",
                        "Toko memang trusted",
                        "Instagram verify akun tersebut"
                    ],
                    "correct_answer": 1,
                    "explanation": "Easy to fake social proof: buy followers, bot comments, stolen product images from real stores. Check: follower engagement ratio (10K followers but only 50 real likes = bot followers), no verification badge."
                },
                {
                    "question": "Red flag dari harga dan payment method?",
                    "options": [
                        "Harga murah adalah promo genuine",
                        "Harga 60% under market + transfer rekening pribadi (bukan merchant/escrow) = classic scam pattern. Legitimate stores use marketplace escrow",
                        "Toko sedang sale besar-besaran",
                        "Normal untuk toko Instagram"
                    ],
                    "correct_answer": 1,
                    "explanation": "Too good to be true price + personal account transfer = scam. Legitimate online stores: use marketplace (Tokopedia, Shopee) with buyer protection, atau payment gateway, never personal rekening."
                }
            ],
            "points": 100,
            "tips": ["Check follower/engagement ratio", "Reverse image search product photos", "Use marketplace escrow, never transfer to personal account"],
            "real_case_reference": "Ribuan kasus online shop scam di Instagram/Facebook Indonesia, korban jutaan rupiah",
            "time_limit_seconds": 180,
            "created_at": datetime.now(timezone.utc)
        },
        
        # AUTHORITY - Indonesian Cases (4 challenges)
        {
            "id": str(uuid.uuid4()),
            "title": "Penipuan Telepon: 'Ini dari Bank BCA, Kartu Anda Diblokir'",
            "category": "indonesian_case",
            "difficulty": "intermediate",
            "cialdini_principle": "authority",
            "challenge_type": "multi_choice",
            "description": "Vishing attack mengeksploitasi trust terhadap authority",
            "scenario": "Dapat telpon dari nomor mirip BCA Customer Service (021-xxxx). Suara professional: 'Selamat siang Pak Budi, ini Customer Service BCA. Kartu ATM Anda terindikasi transaksi mencurigakan di Surabaya Rp 50 juta. Untuk keamanan, kartu kami blokir. Tolong konfirmasi: nomor kartu, CVV, dan OTP yang akan kami kirim untuk verifikasi dan unblock.' Panic, tapi ragu. Scammer tambah: 'Pak, ini urgent. Kalau tidak verifikasi dalam 10 menit, rekening akan suspend permanently. Ini prosedur keamanan bank.'",
            "questions": [
                {
                    "question": "Bagaimana scammer mengeksploitasi authority?",
                    "options": [
                        "Caller memang dari BCA genuine",
                        "Impersonate bank authority (formal language, caller ID spoofing), create urgency, demand sensitive info. People comply karena respect authority + panic",
                        "Prosedur bank memang begitu",
                        "OTP perlu dibagikan untuk verifikasi"
                    ],
                    "correct_answer": 1,
                    "explanation": "Scammer impersonate authority (bank) + create panic (rekening suspend) untuk bypass critical thinking. Exploit: respect for bank authority makes people comply tanpa verify."
                },
                {
                    "question": "Red flag dan proper action?",
                    "options": [
                        "Harus cepat share CVV dan OTP sebelum rekening suspend",
                        "NEVER share CVV/OTP via phone. Real banks NEVER ask ini. Proper action: tutup telepon, call official BCA number (021-2358-8000) untuk verify",
                        "Tunggu 10 menit baru decide",
                        "Share OTP tapi tidak CVV"
                    ],
                    "correct_answer": 1,
                    "explanation": "Golden rule: bank NEVER ask CVV, PIN, atau OTP by phone. Caller ID can be spoofed. Always call back using official number from bank website/kartu, not from caller."
                }
            ],
            "points": 150,
            "tips": ["Bank never ask CVV/OTP by phone", "Caller ID can be spoofed", "Always call official number to verify"],
            "real_case_reference": "Modus vishing sangat umum di Indonesia target nasabah BCA, Mandiri, BRI 2020-2024",
            "time_limit_seconds": 240,
            "created_at": datetime.now(timezone.utc)
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Email Phishing: Dari 'Tim IT Perusahaan'",
            "category": "indonesian_case",
            "difficulty": "beginner",
            "cialdini_principle": "authority",
            "challenge_type": "multi_choice",
            "description": "Phishing email menggunakan internal authority",
            "scenario": "Senin pagi, dapat email: From: it.support@perusahaan-anda.com, Subject: '[URGENT] Verifikasi Akun - Akses Email Akan Ditutup'. Body: 'Dear Team, Sistem email perusahaan sedang upgrade. Untuk menjaga akses email Anda, silakan verifikasi akun melalui link ini dalam 24 jam: [Link]. Jika tidak verifikasi, email akan suspend. Regards, Tim IT'. Link membawa ke halaman login yang mirip portal perusahaan.",
            "questions": [
                {
                    "question": "Bagaimana authority dieksploitasi di sini?",
                    "options": [
                        "Email dari IT genuine",
                        "Attacker impersonate internal authority (IT dept), people comply karena respect corporate hierarchy + fear (email suspend). Exploit power dynamic",
                        "Upgrade sistem memang terjadi",
                        "Link aman karena dari IT"
                    ],
                    "correct_answer": 1,
                    "explanation": "Phishing exploit authority: impersonate IT support (power position in company) + urgency (suspend email) = bypass skepticism. Employees comply untuk avoid trouble with 'atasan'."
                },
                {
                    "question": "Cara identify email phishing ini?",
                    "options": [
                        "Tidak ada red flag",
                        "Check sender email carefully (fake domain: perusahaan-anda.com vs perusahaananda.co.id), hover link (lihat actual URL berbeda), IT never ask password via email link",
                        "Urgency adalah tanda genuine issue",
                        "Format email terlihat professional"
                    ],
                    "correct_answer": 1,
                    "explanation": "Red flags: slight domain typo (hyphen, .com vs .co.id), suspicious link (hover to check real URL), urgency tactic. Real IT: announce via internal portal/in-person, never ask password via email."
                }
            ],
            "points": 100,
            "tips": ["Verify sender email domain carefully", "Hover links before clicking", "Contact IT directly when doubt"],
            "real_case_reference": "Internal phishing attacks common di perusahaan Indonesia, credential theft",
            "time_limit_seconds": 180,
            "created_at": datetime.now(timezone.utc)
        },
        
        # LIKING - Indonesian Cases (3 challenges)
        {
            "id": str(uuid.uuid4()),
            "title": "Romance Scam: Cinta Online, Pinjam Uang Rp 100 Juta",
            "category": "indonesian_case",
            "difficulty": "advanced",
            "cialdini_principle": "liking",
            "challenge_type": "multi_choice",
            "description": "Romance scam menggunakan prinsip liking",
            "scenario": "Match dengan 'David Anderson' di dating app. Profile: tampan, expat engineer di Singapore, salary $10K/month. Chat sweet setiap hari 3 bulan: 'You're special', 'I love you', 'Want to meet you soon'. Tiba-tiba: 'Darling, emergency. Mother sick in UK, need surgery $30K. My money locked in investment. Can you help? I'll pay back double next month when investment mature.' Karena sudah sayang, pinjamkan Rp 100 juta. Setelah transfer, David menghilang, ternyata foto stolen dari model Instagram.",
            "questions": [
                {
                    "question": "Bagaimana liking principle dieksploitasi?",
                    "options": [
                        "David genuine mencintai korban",
                        "Scammer build emotional connection (liking) over time, exploit feelings untuk extract money. Victim more willing give karena 'cinta' dan trust",
                        "Emergency is real",
                        "David akan pay back"
                    ],
                    "correct_answer": 1,
                    "explanation": "Romance scammer invest waktu (weeks/months) build deep emotional bond. Once victim 'jatuh cinta', exploit feeling with sob story. Victim rationalize: 'dia cinta aku, pasti pay back' - blinded by emotion."
                },
                {
                    "question": "Red flags dari profile dan request?",
                    "options": [
                        "Tidak ada red flag, genuine relationship",
                        "Too perfect profile (model looks, high salary), never meet in person, sudden emergency money request, money 'locked' story - classic romance scam pattern",
                        "Emergency bisa terjadi pada siapa saja",
                        "Investment money locked adalah common"
                    ],
                    "correct_answer": 1,
                    "explanation": "Red flags: overly attractive profile (stolen photos - reverse image search), never video call/meet, sudden crisis needing money, elaborate story why his money unavailable. Romance scammer target lonely people, build trust, then strike."
                }
            ],
            "points": 200,
            "tips": ["Reverse image search profile photos", "Never send money to online partner you haven't met", "Video call to verify identity"],
            "real_case_reference": "Romance scam sangat umum di Indonesia, korban kehilangan puluhan hingga ratusan juta",
            "time_limit_seconds": 300,
            "created_at": datetime.now(timezone.utc)
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Sales Asuransi: Teman SMA Tiba-tiba Peduli",
            "category": "indonesian_case",
            "difficulty": "beginner",
            "cialdini_principle": "liking",
            "challenge_type": "multi_choice",
            "description": "Exploitasi friendship untuk sales pressure",
            "scenario": "Teman SMA yang 10 tahun tidak kontak tiba-tiba chat: 'Hai! Lama tidak ketemu, gimana kabarnya? Kangen banget sama kamu!'. Video call, ngobrol nostalgia 30 menit, sangat friendly. Akhir call: 'Oh iya, sekarang aku kerja di asuransi. Kebetulan ada produk investment bagus, guaranteed return 20%/year, cocok buat kamu yang mau nabung. Karena kita teman, aku kasih special discount. Gimana, mau join? Minimal Rp 50 juta.'",
            "questions": [
                {
                    "question": "Bagaimana liking principle digunakan untuk sales?",
                    "options": [
                        "Teman genuine peduli dan rekomendasikan produk bagus",
                        "Reconnect tiba-tiba bukan karena friendship, tapi target sales. Build rapport (liking) sebelum pitch. People sulit reject teman lama - social obligation",
                        "Produk investment memang cocok",
                        "Special discount adalah keuntungan"
                    ],
                    "correct_answer": 1,
                    "explanation": "Manipulative sales tactic: use old friendship untuk lower guard, build liking, then exploit dengan sales pitch. Victim feels obligated tidak refuse karena 'teman' dan tidak mau ruin friendship."
                },
                {
                    "question": "Red flag dari investment offer?",
                    "options": [
                        "Guaranteed 20% return adalah realistic",
                        "'Guaranteed return 20%/year' is huge red flag - unrealistic. Pressure from friend (liking) override financial logic. Research product independently",
                        "Teman tidak akan scam teman",
                        "Asuransi selalu safe investment"
                    ],
                    "correct_answer": 1,
                    "explanation": "20% guaranteed annual return extremely suspicious (bank deposit ~5%, stock market average ~10% tidak guaranteed). Friend might be naive atau pressured by company quota. Always research independently, don't invest karena takut reject teman."
                }
            ],
            "points": 100,
            "tips": ["Friendship tidak = financial advice", "Research investment independently", "OK to say no to friends"],
            "real_case_reference": "Umum di Indonesia: teman lama suddenly contact untuk asuransi/MLM sales",
            "time_limit_seconds": 180,
            "created_at": datetime.now(timezone.utc)
        },
        
        # SCARCITY - Indonesian Cases (4 challenges)
        {
            "id": str(uuid.uuid4()),
            "title": "Flash Sale Palsu: Stok Tinggal 2, Timer 5 Menit!",
            "category": "indonesian_case",
            "difficulty": "beginner",
            "cialdini_principle": "scarcity",
            "challenge_type": "multi_choice",
            "description": "Fake scarcity dalam e-commerce flash sale",
            "scenario": "Browsing Shoppe, muncul pop-up: 'FLASH SALE! iPhone 14 Pro: Rp 10 juta → Rp 7 juta! Stok: 2 unit tersisa! Timer: 04:58'. Countdown timer bergerak cepat, stock indicator merah. Panic buy, checkout cepat. Esok hari, check lagi product page: 'FLASH SALE! iPhone 14 Pro Rp 7 juta! Stok: 2 unit tersisa! Timer: 04:58' - SAMA PERSIS. Realize: fake scarcity, sale selalu available.",
            "questions": [
                {
                    "question": "Bagaimana scarcity dimanipulasi?",
                    "options": [
                        "Stock memang limited dan timer genuine",
                        "Fake countdown (reset setiap refresh) + fake low stock indicator (always '2 unit') create false scarcity untuk trigger panic buying",
                        "Flash sale memang recurring",
                        "Sistem otomatis marketplace"
                    ],
                    "correct_answer": 1,
                    "explanation": "Dark pattern: countdown timer reset every refresh, stock always show 'tinggal 2' untuk create urgency. Not real scarcity - psychological manipulation untuk impulsive purchase tanpa compare price."
                },
                {
                    "question": "Impact psychological dari fake scarcity?",
                    "options": [
                        "Tidak ada impact, user tetap rational",
                        "Amygdala hijack: scarcity + time pressure trigger fight-or-flight, shutdown rational thinking. Decision jadi emotional, skip price comparison/need evaluation",
                        "User senang dapat discount",
                        "Ini strategi marketing normal"
                    ],
                    "correct_answer": 1,
                    "explanation": "Scarcity + urgency trigger primitive brain (amygdala), override prefrontal cortex (rational thinking). Result: impulsive buying without proper evaluation. Marketplace exploit ini untuk boost conversion."
                }
            ],
            "points": 100,
            "tips": ["Screenshot dan refresh page to verify scarcity", "Compare price di multiple stores", "Wait 24 hours before buying"],
            "real_case_reference": "Taktik umum Shopee, Tokopedia, Lazada flash sale Indonesia",
            "time_limit_seconds": 180,
            "created_at": datetime.now(timezone.utc)
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Investasi Tanah: 'Lokasi Premium, Tinggal 3 Kavling!'",
            "category": "indonesian_case",
            "difficulty": "intermediate",
            "cialdini_principle": "scarcity",
            "challenge_type": "multi_choice",
            "description": "Real estate scam dengan artificial scarcity",
            "scenario": "Dapat broadcast WA dari 'Property Investment Consultant': 'LOKASI PREMIUM BOGOR - Dekat Tol + CBD Baru! Kavling 100m² harga Rp 300 juta (harga market Rp 500 juta!). TERSISA 3 KAVLING DARI 50 UNIT! Besok naik jadi Rp 400 juta! Survey location Minggu ini, 20 orang interested!'. Visit location: tanah kosong di pinggir jalan desa, tidak ada CBD/toll terdekat. Agent pressure: '2 kavling sudah booked, tinggal 1! Decide sekarang!'",
            "questions": [
                {
                    "question": "Bagaimana scarcity diciptakan untuk pressure?",
                    "options": [
                        "Kavling memang limited dan high demand",
                        "Artificial scarcity: '3 tersisa' (padahal masih banyak/tidak sold), 'besok naik' (false deadline), '20 orang interested' (fake social proof) - semua create panic buying",
                        "Location premium adalah fakta",
                        "Harga memang akan naik"
                    ],
                    "correct_answer": 1,
                    "explanation": "Classic real estate scam: artificial scarcity ('tinggal 3') + false urgency ('besok naik') + fake demand ('20 interested'). Reality: banyak stock, harga overprice (market value jauh lebih rendah), location not as promised."
                },
                {
                    "question": "Red flags dan due diligence proper?",
                    "options": [
                        "Harus decide cepat sebelum kehabisan",
                        "Red flags: too good to be true price, extreme urgency, pressure on-site decide. Due diligence: check legal (sertifikat di BPN), survey sendiri tanpa agent, compare price 5+ listings nearby",
                        "Agent tidak akan scam karena reputation",
                        "Property investment selalu profitable"
                    ],
                    "correct_answer": 1,
                    "explanation": "NEVER decide on-site under pressure. Proper due diligence: verify sertifikat di BPN (bukan fotokopi), check area development plan di Pemda, hire independent surveyor, compare prices. Scarcity tactic = red flag."
                }
            ],
            "points": 150,
            "tips": ["Never decide under pressure", "Verify legal docs at BPN", "Independent price comparison"],
            "real_case_reference": "Banyak kasus investasi tanah fiktif atau sertifikat ganda di Indonesia",
            "time_limit_seconds": 240,
            "created_at": datetime.now(timezone.utc)
        },
    ]
    
    # Insert challenges
    if challenges:
        await db.challenges.insert_many(challenges)
        print(f"✅ Seeded {len(challenges)} Indonesian case challenges")
    
    # Print summary by Cialdini principle
    print("\n📊 Summary by Cialdini Principle:")
    for principle in ["reciprocity", "commitment", "social_proof", "authority", "liking", "scarcity"]:
        count = await db.challenges.count_documents({"cialdini_principle": principle})
        print(f"  - {principle.title()}: {count} challenges")

if __name__ == "__main__":
    asyncio.run(seed_indonesia_challenges())
