import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
import uuid
from datetime import datetime, timezone

mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
client = AsyncIOMotorClient(mongo_url)
db = client['tegalsec_lab']

async def seed_ultimate():
    print("🚀 Seeding 10 ULTIMATE challenges...")
    
    challenges = [
        # 1. NFT Rugpull
        {
            "id": str(uuid.uuid4()),
            "title": "NFT Rugpull: Bored Monkey Club Indonesia",
            "category": "indonesian_case",
            "difficulty": "advanced",
            "cialdini_principle": "scarcity",
            "challenge_type": "multi_choice",
            "description": "Analisis proyek NFT Indonesia yang ternyata rugpull",
            "scenario": "'Bored Monkey Club Indonesia' - proyek NFT dengan 10K supply, roadmap ambisius (metaverse game, token $BMC, whitelist influencer). Pre-mint 0.5 ETH, public mint 0.8 ETH. Website slick, Discord 50K member, Twitter verified. Founder anonim tapi 'doxxed ke core team'. Sold out 2 jam, floor price pump 3 ETH. Hari ke-5: website down, Discord hilang, Twitter suspended, founder menghilang dengan 4000 ETH.",
            "questions": [
                {
                    "question": "Red flag TERBESAR dari proyek ini yang seharusnya terdeteksi SEBELUM mint?",
                    "options": [
                        "Harga mint 0.8 ETH terlalu mahal",
                        "Founder ANONIM + roadmap terlalu ambisius tanpa proof of work = classic rugpull pattern",
                        "Supply 10K terlalu banyak",
                        "Website terlalu bagus"
                    ],
                    "correct_answer": 1,
                    "explanation": "Founder anonim dengan roadmap besar tanpa proof-of-work/prototype adalah RED FLAG UTAMA. 'Doxxed ke core team' meaningless jika core team juga anonim. Proyek legit punya founder public dengan track record."
                },
                {
                    "question": "Discord 50K member dan Twitter verified apakah jaminan aman?",
                    "options": [
                        "Ya, verified badge = legit",
                        "TIDAK! Member bisa dibeli/bot, verified bisa dicuri/dipalsukan. Cek engagement quality",
                        "50K member pasti real",
                        "Twitter verified = aman"
                    ],
                    "correct_answer": 1,
                    "explanation": "Member Discord mudah inflate dengan bot ($100 = 10K bot). Twitter verified bisa dibeli/dicuri/dipalsukan. Yang penting: quality engagement, founder identity, smart contract audit."
                },
                {
                    "question": "Sebelum mint NFT, apa yang WAJIB dicek?",
                    "options": [
                        "Hanya roadmap dan artwork",
                        "Smart contract audit, founder doxxed (KYC), tokenomics, liquidity lock, team token vesting",
                        "Hype di Twitter saja",
                        "Influencer endorsement"
                    ],
                    "correct_answer": 1,
                    "explanation": "WAJIB: 1) Smart contract audit (CertiK/Hacken), 2) Founder fully doxxed dengan KYC, 3) Team allocation dengan vesting, 4) Clear utility, 5) Prototype/MVP. Tanpa ini = JANGAN MINT."
                },
                {
                    "question": "Cara recovery setelah jadi victim rugpull?",
                    "options": [
                        "Tidak bisa apa-apa",
                        "Report ke Binance/OpenSea, lapor polisi cyber, join class action lawsuit, block scammer wallet",
                        "Terima saja sebagai pembelajaran",
                        "Coba kontak founder"
                    ],
                    "correct_answer": 1,
                    "explanation": "Action: 1) Report ke platform (OpenSea/Binance), 2) Lapor ke Bareskrim cyber, 3) Join victim group untuk class action, 4) Report wallet address ke blockchain explorer. Chance recovery kecil tapi wajib action."
                }
            ],
            "points": 150,
            "tips": [
                "DYOR (Do Your Own Research) - jangan FOMO",
                "Founder anonim = RED FLAG (unless established project like Satoshi)",
                "Smart contract audit dari firma reputable wajib",
                "Never invest lebih dari yang sanggup loss",
                "Too good to be true = probably scam"
            ],
            "real_case_reference": "Inspired by Bored Bunny, Evolved Apes, Frosties - rugpull projects yang rugikan ribuan investor miliaran dollar",
            "time_limit_seconds": 300,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        
        # 2. Fake Crypto Wallet
        {
            "id": str(uuid.uuid4()),
            "title": "Fake Crypto Wallet App: MyWallet Pro",
            "category": "money_app",
            "difficulty": "intermediate",
            "cialdini_principle": "social_proof",
            "challenge_type": "multi_choice",
            "description": "Wallet crypto palsu di Play Store yang mencuri private key",
            "scenario": "'MyWallet Pro' - wallet crypto di Play Store dengan 4.8 rating, 100K+ downloads, 'Support BTC, ETH, USDT'. Review positif banyak. Anda download, input seed phrase lama untuk recover wallet. Besoknya: semua crypto hilang, wallet tidak bisa dibuka.",
            "questions": [
                {
                    "question": "Kenapa crypto Anda bisa dicuri?",
                    "options": [
                        "Jaringan WiFi tidak aman",
                        "App palsu mencuri seed phrase yang Anda input dan kirim ke server attacker",
                        "HP terkena virus",
                        "Exchange di-hack"
                    ],
                    "correct_answer": 1,
                    "explanation": "Fake wallet app designed untuk steal seed phrase. Saat Anda input seed untuk 'recover', app kirim ke server scammer. Dengan seed phrase, scammer bisa akses wallet dari mana saja."
                },
                {
                    "question": "100K downloads dan 4.8 rating di Play Store = aman?",
                    "options": [
                        "Ya, pasti aman",
                        "TIDAK! Downloads dan rating bisa dimanipulasi. Cek developer identity dan official website",
                        "Play Store verify semua app",
                        "Rating tinggi = legit"
                    ],
                    "correct_answer": 1,
                    "explanation": "Downloads dan rating mudah dimanipulasi ($500 = 50K downloads + 4.5 rating dari bot). Google Play tidak fully verify app. WAJIB cek: developer official website, community social media, audit report."
                },
                {
                    "question": "Cara aman download crypto wallet?",
                    "options": [
                        "Download dari Play Store langsung",
                        "Download HANYA dari official website project → verify URL domain → crosscheck dengan community",
                        "Lihat rating tertinggi di store",
                        "Download yang paling populer"
                    ],
                    "correct_answer": 1,
                    "explanation": "Best practice: 1) Go to official website (e.g., metamask.io), 2) Download link dari website official, 3) Verify checksum/hash file, 4) Crosscheck dengan official Twitter/Discord. JANGAN search di store langsung."
                }
            ],
            "points": 100,
            "tips": [
                "NEVER input seed phrase di app yang tidak 100% verified",
                "Download wallet HANYA dari official website",
                "Store rating bisa fake - cek community official",
                "Hardware wallet (Ledger/Trezor) untuk large amount",
                "Double check app developer name dengan official"
            ],
            "real_case_reference": "Banyak fake wallet di Play Store seperti fake Electrum, fake Metamask yang steal private keys - kerugian jutaan dollar",
            "time_limit_seconds": 200,
            "created_at": datetime.now(timezone.utc).isoformat()
        },

        # 3. MLM Recruitment
        {
            "id": str(uuid.uuid4()),
            "title": "MLM Recruitment: Health Product Miracle",
            "category": "indonesian_case",
            "difficulty": "intermediate",
            "cialdini_principle": "commitment",
            "challenge_type": "multi_choice",
            "description": "Multi Level Marketing yang focus recruitment bukan penjualan",
            "scenario": "Teman SMA tiba-tiba contact setelah 5 tahun. Ajak coffee, cerita success story: 6 bulan join 'HealthMax Indonesia', income 50 juta/bulan dari 'bisnis kesehatan'. Produk: suplemen 'miracle' 1 paket Rp 5 juta. Sistem: beli paket starter Rp 10 juta, recruit 5 orang dapat bonus Rp 15 juta, setiap downline recruit dapat passive income. Presentasi di hotel mewah, banyak testimony 'sukses'. Pressure: 'Slot terbatas, join sekarang atau rugi'.",
            "questions": [
                {
                    "question": "Apa indikator ini MLM scheme, bukan bisnis legit?",
                    "options": [
                        "Produk kesehatan",
                        "Income UTAMA dari recruitment (bukan penjualan produk) + pressure recruit = pyramid scheme",
                        "Pertemuan di hotel",
                        "Ada produk fisik"
                    ],
                    "correct_answer": 1,
                    "explanation": "MLM legit: income dari PENJUALAN produk ke konsumen. Pyramid scheme: income dari RECRUITMENT downline. Jika 'recruit 5 orang' lebih ditekankan dari 'jual produk', itu pyramid scheme (illegal)."
                },
                {
                    "question": "Kenapa teman lama tiba-tiba contact adalah red flag?",
                    "options": [
                        "Tidak ada yang salah",
                        "Taktik MLM: target warm market (teman/keluarga) karena trust tinggi - relationship dijadikan sales tool",
                        "Dia benar-benar kangen",
                        "Mau berbagi kesempatan"
                    ],
                    "correct_answer": 1,
                    "explanation": "MLM training mengajarkan target 'warm market' dulu (teman/keluarga) karena trust. Ini exploitation relationship untuk profit. Red flag jika tiba-tiba contact setelah lama hilang dan langsung offer bisnis."
                },
                {
                    "question": "'Slot terbatas, join sekarang' adalah taktik apa?",
                    "options": [
                        "Informasi genuine",
                        "Scarcity manipulation - create false urgency agar tidak ada waktu berpikir/research",
                        "Opportunity memang terbatas",
                        "Marketing biasa"
                    ],
                    "correct_answer": 1,
                    "explanation": "Taktik scarcity untuk pressure decision cepat. Bisnis legit tidak butuh pressure 'join sekarang or never'. Ini prevent Anda dari research dan berpikir jernih."
                }
            ],
            "points": 90,
            "tips": [
                "MLM legit: income dari SALES, bukan recruitment",
                "Research company di Google: '[nama] scam/review/lawsuit'",
                "Waspada jika teman lama suddenly contact dengan 'opportunity'",
                "Pressure 'join now' adalah RED FLAG",
                "Income claim tanpa proof = meaningless"
            ],
            "real_case_reference": "Pattern mirip MLM di Indonesia seperti kasus beberapa MLM yang ditutup OJK karena model pyramid scheme",
            "time_limit_seconds": 220,
            "created_at": datetime.now(timezone.utc).isoformat()
        },

        # 4. Romance Scam
        {
            "id": str(uuid.uuid4()),
            "title": "Romance Scam: Foreign Boyfriend Investment",
            "category": "pretexting",
            "difficulty": "intermediate",
            "cialdini_principle": "liking",
            "challenge_type": "multi_choice",
            "description": "Penipuan online dating dengan modus investasi",
            "scenario": "Match di dating app dengan 'David', claims engineer USA. Chat 3 bulan, video call (tapi always busy, quick call). Romantic, perhatian. Suddenly: 'I have investment opportunity in crypto, we can invest together, I'll guide you'. Minta transfer ke wallet address untuk 'joint investment' - promise 10x return dalam 2 bulan. Setelah transfer 100 juta: ghosted, blocked, wallet address tidak bisa di-trace.",
            "questions": [
                {
                    "question": "Red flag terbesar dari 'relationship' ini?",
                    "options": [
                        "Long distance relationship",
                        "Never meet in person + mixing romance with money request = classic romance scam",
                        "Video call pendek",
                        "Chatting 3 bulan"
                    ],
                    "correct_answer": 1,
                    "explanation": "Romance scam pattern: build emotional connection → minta uang/investasi. NEVER campur romance dengan money request. Video call bisa fake (deepfake/pre-recorded). Red flag: tidak pernah ketemu + minta uang."
                },
                {
                    "question": "Kenapa video call pendek tetap mencurigakan?",
                    "options": [
                        "Tidak mencurigakan",
                        "Scammer bisa pakai deepfake, pre-recorded video, atau hire actor. Inconsistent availability adalah red flag",
                        "Dia memang sibuk",
                        "Timezone berbeda"
                    ],
                    "correct_answer": 1,
                    "explanation": "Modern scammer bisa pakai deepfake technology atau hire actor untuk video call. Pattern 'always busy, quick call' adalah tactics untuk avoid detection. Real person tidak konsisten avoid call."
                },
                {
                    "question": "Tindakan pencegahan untuk online dating?",
                    "options": [
                        "Trust semua orang",
                        "Never send money to online contact, verify identity via multiple channels, meet in person before trust, reverse image search photo",
                        "Video call cukup",
                        "Chat lama = aman"
                    ],
                    "correct_answer": 1,
                    "explanation": "Rules: 1) NEVER send money to online-only contact, 2) Reverse image search profile pic, 3) Verify identity via multiple platforms, 4) Meet in person (public place), 5) Red flag jika gabung romance + money."
                }
            ],
            "points": 100,
            "tips": [
                "NEVER send money to someone you've never met in person",
                "Romance + money request = SCAM",
                "Reverse image search profile pictures",
                "Scammer very patient - bisa chat berbulan-bulan",
                "Too perfect/romantic terlalu cepat = red flag"
            ],
            "real_case_reference": "Romance scam FBI report: $304 million loss in 2020, highest loss category. Banyak kasus di Indonesia via dating apps",
            "time_limit_seconds": 200,
            "created_at": datetime.now(timezone.utc).isoformat()
        },

        # 5. Job Scam - Remote Work
        {
            "id": str(uuid.uuid4()),
            "title": "Job Scam: High Paying Remote Admin Job",
            "category": "quid_pro_quo",
            "difficulty": "beginner",
            "cialdini_principle": "reciprocity",
            "challenge_type": "multi_choice",
            "description": "Penipuan lowongan kerja remote dengan gaji fantastis",
            "scenario": "LinkedIn: 'Admin Assistant - Remote - $5000/month - No experience needed'. Company: 'GlobalTech Solutions Inc' (website professional). Email offer: 'Congrats! You're selected. Send $500 for laptop, software license, training kit - akan direimburse di gaji pertama. Start ASAP!'. Website company bagus, LinkedIn profile verified.",
            "questions": [
                {
                    "question": "Apa red flag utama dari job offer ini?",
                    "options": [
                        "Remote work",
                        "Company LEGITIMATE tidak pernah minta uang dari calon employee untuk equipment - itu SCAM",
                        "Salary terlalu tinggi",
                        "No experience needed"
                    ],
                    "correct_answer": 1,
                    "explanation": "Company legit provide equipment atau reimburse SETELAH purchase dengan PO (purchase order). Minta uang upfront untuk 'equipment/training' = SCAM. Tidak ada 'reimburse di gaji pertama' yang real."
                },
                {
                    "question": "Website professional dan LinkedIn verified = legit?",
                    "options": [
                        "Ya, pasti legit",
                        "TIDAK! Website mudah dibuat, LinkedIn bisa fake/bought. Cek company via Glassdoor, LinkedIn employee count, office address Google Maps",
                        "LinkedIn verified = aman",
                        "Website bagus = real company"
                    ],
                    "correct_answer": 1,
                    "explanation": "Website professional = $50 dan 1 hari. LinkedIn profile bisa dibeli/fake. Verification: 1) Glassdoor reviews, 2) LinkedIn REAL employee profiles (multiple), 3) Physical office (Google Maps Street View), 4) Company registration check."
                },
                {
                    "question": "Cara verify legitimate job offer?",
                    "options": [
                        "Percaya email saja",
                        "Call company via official number (NOT from email), check domain email, verify recruiter LinkedIn, research Glassdoor",
                        "Reply email langsung",
                        "Website bagus = legit"
                    ],
                    "correct_answer": 1,
                    "explanation": "Verify: 1) Call company via number dari website official (BUKAN dari email), 2) Email domain match official (@company.com bukan @gmail), 3) Recruiter LinkedIn legit dengan connection, 4) Glassdoor company reviews."
                }
            ],
            "points": 80,
            "tips": [
                "Legitimate company NEVER minta uang untuk equipment/training",
                "Too good to be true salary for basic job = red flag",
                "Verify company via Glassdoor dan LinkedIn real employees",
                "Call company via official number untuk confirm job offer",
                "Pressure 'start ASAP' adalah taktik scammer"
            ],
            "real_case_reference": "Job scam sangat marak terutama remote work post-pandemic. FBI IC3 report: employment scams meningkat 200% tahun 2020-2021",
            "time_limit_seconds": 180,
            "created_at": datetime.now(timezone.utc).isoformat()
        },

        # 6. Pump and Dump Crypto
        {
            "id": str(uuid.uuid4()),
            "title": "Pump and Dump: Telegram Crypto Signal Group",
            "category": "money_app",
            "difficulty": "advanced",
            "cialdini_principle": "social_proof",
            "challenge_type": "multi_choice",
            "description": "Grup sinyal crypto yang manipulasi harga (pump and dump)",
            "scenario": "Telegram: 'VIP Crypto Signals 🚀 - 200K members - 95% win rate'. Gratis join, banyak testimony profit. Hari Senin: 'BUY $SHIB NOW! PUMP INCOMING 1000%! 🚀🚀🚀'. Anda beli $10K SHIB. Harga naik 20% dalam 5 menit - euphoria. Tiba-tiba: massive sell wall, harga dump 60% dalam 2 menit. Anda panik sell: loss $6K. Admin grup: 'Market manipulation by whales, next signal better!' Kemudian Anda tahu: admin dan inner circle sudah beli sebelum announce, dump saat member retail buy.",
            "questions": [
                {
                    "question": "Apa yang sebenarnya terjadi?",
                    "options": [
                        "Whale manipulation",
                        "Pump & Dump scheme: admin pre-pump, announce ke member retail, dump ke member = profit untuk inner circle",
                        "Market volatility normal",
                        "Bad timing"
                    ],
                    "correct_answer": 1,
                    "explanation": "Classic Pump & Dump: 1) Inner circle beli dulu (accumulation), 2) Announce 'signal' ke member retail, 3) Retail FOMO buy → harga pump, 4) Inner circle dump ke retail → profit. Retail jadi exit liquidity. Ini ILLEGAL manipulation."
                },
                {
                    "question": "'95% win rate' dan '200K members' mencurigakan karena?",
                    "options": [
                        "Angka real",
                        "Fake metrics untuk credibility. Real win rate impossible 95%. Member count inflate dengan bot. Testimony bisa fake/paid",
                        "Grup memang pro",
                        "Tidak mencurigakan"
                    ],
                    "correct_answer": 1,
                    "explanation": "95% win rate impossible di crypto volatile. Member 200K mudah fake (bot = $200). Testimony bisa fabricated/paid/early members yang untung. These metrics designed untuk lure victim."
                },
                {
                    "question": "Kenapa grup 'gratis' tetap menguntungkan untuk scammer?",
                    "options": [
                        "Mereka baik hati",
                        "Profit dari pump & dump ke member (member = exit liquidity), referral fees dari exchanges, VIP subscription upsell",
                        "Tidak ada profit",
                        "Donasi member"
                    ],
                    "correct_answer": 1,
                    "explanation": "Revenue model: 1) Dump token ke member retail (main profit), 2) Exchange referral kickback, 3) Upsell 'VIP faster signals', 4) Sell member data. Free member = product (exit liquidity), bukan customer."
                },
                {
                    "question": "Cara trading crypto yang lebih aman?",
                    "options": [
                        "Join banyak signal group",
                        "DYOR, invest long-term in established coins, DCA strategy, never FOMO, ignore pump signals",
                        "Follow semua signals cepat",
                        "All-in saat ada signal"
                    ],
                    "correct_answer": 1,
                    "explanation": "Safe approach: 1) DYOR (research fundamental), 2) Invest established project (BTC/ETH), 3) DCA (dollar-cost average), 4) Long-term hold, 5) Ignore pump groups, 6) Never invest lebih dari loss tolerance."
                }
            ],
            "points": 130,
            "tips": [
                "Pump & dump groups = ILLEGAL market manipulation",
                "'Free signal group' = Anda adalah produk (exit liquidity)",
                "95%+ win rate claim = mathematically impossible, RED FLAG",
                "FOMO adalah enemy terbesar dalam trading",
                "Do Your Own Research (DYOR), never follow blind signals"
            ],
            "real_case_reference": "McAfee pump & dump case: charged by SEC. Banyak Telegram pump groups aktif manipulasi altcoin low cap",
            "time_limit_seconds": 280,
            "created_at": datetime.now(timezone.utc).isoformat()
        },

        # 7. Online Loan Shark
        {
            "id": str(uuid.uuid4()),
            "title": "Pinjaman Online Ilegal: KreditKilat App",
            "category": "indonesian_case",
            "difficulty": "intermediate",
            "cialdini_principle": "scarcity",
            "challenge_type": "multi_choice",
            "description": "Pinjol ilegal dengan bunga mencekik dan terror debt collector",
            "scenario": "Butuh dana urgent Rp 5 juta. Google: 'pinjaman cepat tanpa jaminan'. Install app 'KreditKilat' di Play Store - 4.2 rating, 50K downloads. Approve instant Rp 5 juta, tenor 30 hari, 'bunga 0.5% per hari'. Sign digital tanpa baca detail. Hari ke-31: tagihan Rp 7.5 juta (bunga 50%). Tidak bisa bayar. Mulai: SMS terror ke kontak HP, blast WA ke keluarga dengan fitnah, edit foto jadi pornografi, ancam tangkap polisi.",
            "questions": [
                {
                    "question": "Kenapa ini pinjol ILEGAL?",
                    "options": [
                        "Online lending memang ilegal",
                        "Tidak terdaftar OJK + bunga 0.5%/hari (182.5%/tahun) > maksimum legal + akses kontak + terror = ILEGAL",
                        "Semua pinjol begini",
                        "Bunga wajar"
                    ],
                    "correct_answer": 1,
                    "explanation": "Red flags ilegal: 1) Tidak registered di OJK, 2) Bunga >0.8%/hari (OJK max), 3) Akses seluruh kontak HP, 4) Terror/ancaman debt collector, 5) Edit foto victim. Cek registered pinjol: ojk.go.id/fintech"
                },
                {
                    "question": "Play Store rating 4.2 dan 50K downloads kenapa tidak menjamin?",
                    "options": [
                        "Itu jaminan aman",
                        "Rating/downloads bisa manipulated. Google tidak fully verify app legality/OJK registration",
                        "Play Store verify semua",
                        "50K pengguna pasti aman"
                    ],
                    "correct_answer": 1,
                    "explanation": "Google Play tidak verify OJK registration atau business model legality. Rating/downloads bisa dibeli. WAJIB cross-check di ojk.go.id/fintech sebelum install pinjol app."
                },
                {
                    "question": "Cara handle jika sudah jadi korban pinjol ilegal?",
                    "options": [
                        "Bayar berapapun untuk stop terror",
                        "Lapor ke OJK, AFPI, SJK OJK, polisi cyber - JANGAN bayar full illegal interest. Screenshot semua terror sebagai bukti",
                        "Ganti nomor HP",
                        "Diam saja"
                    ],
                    "correct_answer": 1,
                    "explanation": "Action: 1) Lapor OJK (kontak.ojk.go.id), 2) Lapor SJK OJK (082-157-157-157), 3) Lapor polisi cyber, 4) Screenshot semua terror, 5) Bayar HANYA pokok + bunga legal rate. Debt collector terror adalah PIDANA."
                }
            ],
            "points": 110,
            "tips": [
                "Cek pinjol di ojk.go.id/fintech - HANYA gunakan yang registered",
                "Bunga legal maksimum 0.8% per hari (OJK)",
                "Pinjol legal TIDAK akses kontak atau galeri HP",
                "Debt collector legal TIDAK terror/ancam/fitnah",
                "Lapor pinjol ilegal ke OJK dan polisi - ada perlindungan hukum"
            ],
            "real_case_reference": "Satgas Waspada Investasi OJK tutup ratusan pinjol ilegal. Ribuan laporan terror debt collector ke polisi tiap bulan",
            "time_limit_seconds": 200,
            "created_at": datetime.now(timezone.utc).isoformat()
        },

        # 8. Fake Airdrop Crypto
        {
            "id": str(uuid.uuid4()),
            "title": "Fake Airdrop: Ethereum 2.0 Giveaway",
            "category": "phishing",
            "difficulty": "beginner",
            "cialdini_principle": "reciprocity",
            "challenge_type": "multi_choice",
            "description": "Phishing via fake airdrop yang minta connect wallet",
            "scenario": "Twitter post: '@VitalikButerin VERIFIED ✓ celebrating ETH 2.0! Airdrop 10 ETH! Visit: ethfoundation-airdrop.com - Connect wallet - Claim now! Limited 1000 participants!' Link terlihat legit, website mirip Ethereum Foundation. Anda connect MetaMask, approve transaction 'Claim Airdrop'. Tiba-tiba: semua ETH dan token di wallet drained. Transaction history: 'Approve unlimited spend' untuk scam contract.",
            "questions": [
                {
                    "question": "Apa yang salah?",
                    "options": [
                        "Metamask bermasalah",
                        "Website fake + 'approve transaction' adalah approval untuk scam contract drain entire wallet",
                        "ETH 2.0 scam",
                        "WiFi tidak aman"
                    ],
                    "correct_answer": 1,
                    "explanation": "Saat 'claim airdrop', Anda approve smart contract yang punya unlimited access ke wallet. Contract ini transfer semua asset ke scammer. Always check contract address dan NEVER approve unlimited spend."
                },
                {
                    "question": "Twitter verified dan domain mirip = aman?",
                    "options": [
                        "Ya, verified = legit",
                        "TIDAK! Verified bisa fake/hacked account. Domain typosquatting: ethfoundation-airdrop.com bukan ethereum.org",
                        "Verified pasti real",
                        "Domain .com = official"
                    ],
                    "correct_answer": 1,
                    "explanation": "Twitter verified bisa: 1) Hacked account, 2) Paid verified (Twitter Blue), 3) Impersonation. Domain: ethereum.org vs ethfoundation-airdrop.com = different. Real Ethereum NEVER airdrop via connect wallet."
                },
                {
                    "question": "Red flag dari 'airdrop' ini?",
                    "options": [
                        "Airdrop amount besar",
                        "Legitimate airdrop NEVER minta connect wallet atau approve transaction - airdrop langsung ke address",
                        "Limited participants",
                        "Twitter post"
                    ],
                    "correct_answer": 1,
                    "explanation": "Airdrop real: project DROP token langsung ke eligible addresses (snapshot based). Tidak perlu connect wallet, approve, atau 'claim transaction'. Minta connect wallet = 99% SCAM."
                }
            ],
            "points": 85,
            "tips": [
                "Real airdrop NEVER minta connect wallet atau approve",
                "Check contract address before approve ANY transaction",
                "Never approve 'unlimited spend' untuk unknown contract",
                "Twitter verified tidak guarantee legitimacy (bisa hacked)",
                "Use burner wallet untuk interact dengan unknown dApps"
            ],
            "real_case_reference": "Fake airdrop adalah salah satu phishing tersering di crypto - BadgerDAO hack $120M via fake airdrop",
            "time_limit_seconds": 180,
            "created_at": datetime.now(timezone.utc).isoformat()
        },

        # 9. Dropshipping Scam
        {
            "id": str(uuid.uuid4()),
            "title": "Dropshipping Course Scam: Passive Income Guarantee",
            "category": "money_app",
            "difficulty": "intermediate",
            "cialdini_principle": "commitment",
            "challenge_type": "multi_choice",
            "description": "Kursus dropshipping dengan janji passive income",
            "scenario": "Instagram ads: 'Hasilkan 100 juta/bulan dari rumah! Dropshipping secret revealed! Join Bootcamp hanya Rp 15 juta - mentoring 6 bulan - guarantee profit or money back!' Testimonial banyak, mentor show off Lambo. Setelah bayar: dapat video tutorial generic (bisa gratis di YouTube), 'mentoring' = grup Telegram 5000 orang, tidak ada personal guidance. Coba jalankan: Shopify monthly cost, FB ads burn tanpa sale, supplier China slow/scam. 6 bulan: rugi 40 juta total, minta refund: 'Anda tidak execute dengan benar, no refund'.",
            "questions": [
                {
                    "question": "Kenapa ini scam course?",
                    "options": [
                        "Dropshipping memang sulit",
                        "Promise 'passive income guarantee' + overprice generic content + fake mentoring + no refund = scam course model",
                        "Anda tidak execute",
                        "Bisnis memang ada risk"
                    ],
                    "correct_answer": 1,
                    "explanation": "Scam course signs: 1) Guarantee income (impossible), 2) Overprice (15 juta untuk info gratis di YouTube), 3) Fake 'mentoring' (grup 5000 orang), 4) Refund dengan 'excuse', 5) Focus jual course bukan execute bisnis sendiri."
                },
                {
                    "question": "Testimonial dan Lambo mentor = bukti success?",
                    "options": [
                        "Ya, pasti sukses",
                        "TIDAK! Testimonial bisa paid/fake, Lambo bisa rental/bukan dari dropshipping (income dari jual course). Check actual business proof",
                        "Testimonial pasti real",
                        "Lambo = dropship profit"
                    ],
                    "correct_answer": 1,
                    "explanation": "Testimonial mudah fabricate ($50/testimonial di Fiverr). Lambo bisa rental atau income dari JUAL COURSE (bukan dropshipping). Real mentor show: actual store revenue, traffic proof, not lifestyle flex."
                },
                {
                    "question": "Cara evaluate course/mentor sebelum beli?",
                    "options": [
                        "Lihat Instagram lifestyle saja",
                        "Research: review independent (Reddit/YouTube), ask proof of revenue, free value first, avoid 'guarantee' claims, check refund policy REAL enforcement",
                        "Testimonial course cukup",
                        "Harga mahal = quality"
                    ],
                    "correct_answer": 1,
                    "explanation": "Due diligence: 1) Independent review (Reddit/Trustpilot), 2) Free content quality test, 3) Actual business proof (tidak hanya lifestyle), 4) No income guarantee promise, 5) Clear refund terms, 6) Check scam reports."
                }
            ],
            "points": 95,
            "tips": [
                "Income 'guarantee' course = SCAM (no one can guarantee)",
                "Banyak info dropshipping gratis di YouTube/blog",
                "Mentor real show business proof, not lifestyle flex",
                "Testimonial mudah fake - check independent reviews",
                "Start small, belajar gratis dulu before invest course mahal"
            ],
            "real_case_reference": "Banyak 'guru' dropshipping di Indonesia yang income utama dari jual course, bukan actual dropshipping. FTC crackdown multiple 'get rich' course scams",
            "time_limit_seconds": 210,
            "created_at": datetime.now(timezone.utc).isoformat()
        },

        # 10. SIM Swap Attack
        {
            "id": str(uuid.uuid4()),
            "title": "SIM Swap Attack: Stolen Phone Number",
            "category": "indonesian_case",
            "difficulty": "advanced",
            "cialdini_principle": "authority",
            "challenge_type": "multi_choice",
            "description": "Serangan dengan mengambil alih nomor telepon korban",
            "scenario": "Tiba-tiba HP Anda no signal. Pikir masalah jaringan. 1 jam kemudian: email notif 'Password changed' dari banking, e-commerce, crypto. WhatsApp logout. Cek: semua akun diakses dari device lain, OTP SMS masuk ke scammer, rekening bank kosong, crypto wallet drained. Ternyata: scammer convince telco CS (social engineering) untuk switch SIM Anda ke kartu mereka (SIM swap), dapat kontrol nomor = kontrol semua OTP.",
            "questions": [
                {
                    "question": "Bagaimana scammer bisa SIM swap?",
                    "options": [
                        "Hack jaringan operator",
                        "Social engineering telco CS: 'Lost phone, need SIM replacement' dengan data pribadi stolen (dari data breach/social media)",
                        "Virus di HP",
                        "Hack SIM card langsung"
                    ],
                    "correct_answer": 1,
                    "explanation": "Scammer call telco CS, pretend jadi Anda: 'Handphone hilang, butuh SIM replacement urgent'. Mereka punya data pribadi Anda (dari data breach/OSINT) untuk verify. CS yang tidak strict bisa approve SIM swap ke kartu mereka."
                },
                {
                    "question": "Kenapa SIM swap sangat berbahaya?",
                    "options": [
                        "Hanya akses WhatsApp",
                        "Kontrol nomor = kontrol SMS OTP = akses semua akun (bank, crypto, email) yang pakai SMS 2FA",
                        "Hanya telpon tidak bisa",
                        "Bisa diganti lagi"
                    ],
                    "correct_answer": 1,
                    "explanation": "SIM swap = scammer kontrol nomor telepon Anda. Semua OTP SMS masuk ke mereka. Bisa reset password akun apapun (email, bank, crypto, socmed) yang pakai SMS 2FA. Literally kontrol digital life Anda."
                },
                {
                    "question": "Cara protect dari SIM swap?",
                    "options": [
                        "Tidak ada cara",
                        "Use authenticator app (Google Auth/Authy) instead SMS OTP, set SIM PIN/PUK, register 'port protection' di telco, enable account-based 2FA not SMS",
                        "Ganti nomor sering",
                        "Pakai HP mahal"
                    ],
                    "correct_answer": 1,
                    "explanation": "Protection: 1) Use TOTP app (Authy/Google Authenticator) not SMS, 2) Set SIM card PIN/PUK, 3) Register telco 'porting protection', 4) Minimize phone number di public, 5) Use hardware key (Yubikey) untuk critical accounts."
                },
                {
                    "question": "Data pribadi apa yang memudahkan SIM swap?",
                    "options": [
                        "Hanya nomor HP",
                        "Nama lengkap, tanggal lahir, alamat, NIK, nama ibu kandung - semua bisa dari data breach atau social media oversharing",
                        "Email saja",
                        "Password"
                    ],
                    "correct_answer": 1,
                    "explanation": "Telco CS verify dengan: nama, tanggal lahir, alamat, NIK, nama ibu kandung. Data ini often leaked di data breach (Tokopedia, BPJS, dll) atau overshare di social media. Protect personal info publicly."
                }
            ],
            "points": 140,
            "tips": [
                "Switch dari SMS OTP ke authenticator app (Google Auth/Authy)",
                "Set SIM card PIN code di HP settings",
                "Register 'port protection' di provider (Telkomsel/Indosat/XL)",
                "Jangan overshare data pribadi di social media",
                "Monitor account activity - setup alert untuk login dari device baru"
            ],
            "real_case_reference": "Jack Dorsey (CEO Twitter) victim SIM swap 2019. Banyak kasus di Indonesia - crypto investor kehilangan miliaran via SIM swap",
            "time_limit_seconds": 300,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
    ]
    
    await db.challenges.insert_many(challenges)
    print(f"✅ {len(challenges)} ULTIMATE challenges created!")
    
    print("\n🎉 Ultimate seeding completed!")
    client.close()

if __name__ == "__main__":
    asyncio.run(seed_ultimate())