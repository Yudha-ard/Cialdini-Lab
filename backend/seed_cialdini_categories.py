import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
import uuid
from datetime import datetime, timezone

mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
client = AsyncIOMotorClient(mongo_url)
db = client['tegalsec_lab']

async def seed_cialdini_challenges():
    print("🎯 Seeding Cialdini-categorized challenges...")
    
    # Clear existing
    await db.challenges.delete_many({})
    
    challenges = [
        # RECIPROCITY (5 challenges)
        {
            "id": str(uuid.uuid4()),
            "title": "Free Trial Credit Card Trap",
            "category": "quid_pro_quo",
            "difficulty": "beginner",
            "cialdini_principle": "reciprocity",
            "challenge_type": "multi_choice",
            "description": "Analisis taktik reciprocity pada free trial yang sulit di-cancel",
            "scenario": "Streaming service 'FlixPrime' offers 'Free 1-month trial - no credit card needed!' Setelah daftar dengan email, tiba-tiba: 'Upgrade to Premium - just Rp 1 for first month!' Butuh credit card. Setelah input kartu, auto-charge Rp 199K/month dimulai tanpa notif jelas. Cancel subscription buried 5 menu deep.",
            "questions": [
                {
                    "question": "Bagaimana reciprocity dieksploitasi di sini?",
                    "options": [
                        "Free trial 1 bulan adalah hadiah genuine",
                        "Setelah 'menerima' free service, user merasa obligated continue/pay - plus dark pattern cancel process",
                        "Rp 1 offer sangat murah",
                        "Tidak ada reciprocity"
                    ],
                    "correct_answer": 1,
                    "explanation": "Free trial creates sense of obligation. Setelah enjoy service, user feels 'berhutang' untuk continue. Dark pattern: cancel process disembunyikan agar user malas cancel = otomatis bayar."
                },
                {
                    "question": "Red flag dari 'no credit card' yang berubah jadi 'need credit card'?",
                    "options": [
                        "Normal business practice",
                        "Bait-and-switch tactic: promise 'no card' untuk hook, lalu require card for 'upgrade' - lock-in strategy",
                        "Mereka lupa mention",
                        "Perlu verifikasi umur"
                    ],
                    "correct_answer": 1,
                    "explanation": "Classic bait-and-switch: advertise 'no credit card' untuk attract, lalu pressure 'upgrade' yang require card. Once card stored, charging becomes automatic."
                },
                {
                    "question": "Cara aman handle free trials?",
                    "options": [
                        "Pakai credit card utama",
                        "Use virtual card/burner card with limit, set calendar reminder BEFORE trial ends, screenshot cancel terms",
                        "Percaya auto-cancel",
                        "Ignore sampai tagihan datang"
                    ],
                    "correct_answer": 1,
                    "explanation": "Best practice: virtual card (limit Rp 10K), calendar alert 2 days before end, screenshot ToS for dispute, test cancel process immediately after signup."
                }
            ],
            "points": 60,
            "tips": [
                "Virtual cards untuk trial (Privacy.com di US, Jenius di Indo)",
                "Set calendar alert SEBELUM trial end",
                "Test cancel process immediately",
                "Screenshot terms untuk dispute",
                "Read cancellation policy BEFORE signup"
            ],
            "time_limit_seconds": 180,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Survey Reward Scam",
            "category": "phishing",
            "difficulty": "beginner",
            "cialdini_principle": "reciprocity",
            "description": "Survey yang 'memberi' hadiah tapi sebenarnya steal data",
            "scenario": "Pop-up: 'Congratulations! You've been selected for exclusive survey. Complete 3-minute survey, get FREE iPhone 15 Pro Max!' Klik \u2192 survey mudah (fav color, age) \u2192 'Claim prize: enter name, phone, email, address, bank for shipping verification'",
            "questions": [
                {
                    "question": "Reciprocity exploitation disini?",
                    "options": [
                        "Survey legit",
                        "Setelah 'invest' 3 menit waktu untuk survey, victim feels entitled to 'reward' \u2192 lower guard for data entry",
                        "Hadiah pasti real",
                        "Tidak ada manipulation"
                    ],
                    "correct_answer": 1,
                    "explanation": "Time investment creates reciprocity: 'I gave them 3 minutes, they owe me iPhone'. This lowers skepticism saat diminta data sensitif. No legitimate survey 'gives' iPhone."
                },
                {
                    "question": "Red flags dari survey ini?",
                    "options": [
                        "Survey online umum",
                        "Unsolicited pop-up + unrealistic prize + asking bank details for 'shipping' = SCAM",
                        "iPhone 15 mahal tapi possible",
                        "Survey pendek oke"
                    ],
                    "correct_answer": 1,
                    "explanation": "Red flags combo: 1) Unsolicited, 2) Prize too good, 3) Bank info for 'shipping' (impossible reason), 4) Pressure 'limited time'. Legit survey pays $1-5, bukan iPhone."
                }
            ],
            "points": 55,
            "tips": [
                "Legit survey: Swagbucks, Toluna - paid $1-10, NOT iPhone",
                "Never give bank info to 'claim prize'",
                "Unsolicited 'you won' = 99% scam",
                "Time investment shouldn't lower critical thinking"
            ],
            "time_limit_seconds": 150,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        
        # COMMITMENT (5 challenges)
        {
            "id": str(uuid.uuid4()),
            "title": "Pyramid Scheme Progressive Commitment",
            "category": "money_app",
            "difficulty": "advanced",
            "cialdini_principle": "commitment",
            "description": "MLM yang escalate commitment secara bertahap",
            "scenario": "Step 1: Join 'business opportunity' webinar gratis. Step 2: Beli 'starter kit' Rp 500K. Step 3: 'For serious member, invest Rp 5 juta jadi distributor'. Step 4: 'Top performer invest Rp 20 juta jadi leader, dapat mobil'. Setiap step, dibuat merasa sudah invest banyak, sayang stop.",
            "questions": [
                {
                    "question": "Bagaimana commitment principle dieksploitasi?",
                    "options": [
                        "Investasi bertahap reasonable",
                        "Foot-in-the-door technique: small commit \u2192 bigger commit. Sunk cost fallacy: 'sudah invest 5 juta, sayang stop'",
                        "Sistem legit",
                        "Tidak ada manipulation"
                    ],
                    "correct_answer": 1,
                    "explanation": "Classic escalation: start free/cheap \u2192 gradually increase. Each investment makes victim feel 'too invested to quit'. Sunk cost fallacy: uang sudah keluar bukan alasan untuk continue losing."
                },
                {
                    "question": "Cara break dari commitment trap ini?",
                    "options": [
                        "Continue karena sudah invest banyak",
                        "Evaluate CURRENT decision independently dari past investment. Cut loss lebih baik dari deeper loss",
                        "Invest lebih untuk 'balik modal'",
                        "Recruit lebih banyak downline"
                    ],
                    "correct_answer": 1,
                    "explanation": "Key mindset: 'Sunk cost is sunk'. Past investment tidak relevant untuk future decision. Question: 'If I haven't invested anything, would I invest NOW?' If no \u2192 quit."
                },
                {
                    "question": "Diferensiasi MLM legit vs pyramid scheme?",
                    "options": [
                        "Semua MLM sama saja",
                        "MLM legit: income dari SALES ke customer. Pyramid: income dari RECRUITMENT downline + pressure upgrade member",
                        "Ada produk = legit",
                        "Registered = aman"
                    ],
                    "correct_answer": 1,
                    "explanation": "Key difference: income source. Legit MLM (Tupperware): commission dari retail sales. Pyramid (Tianshi): focus pada recruitment + member upgrade (products adalah facade)."
                }
            ],
            "points": 120,
            "tips": [
                "Sunk cost adalah sunk - don't let it dictate future decisions",
                "Evaluate each 'upgrade' independently",
                "MLM legit = retail sales focused, bukan recruitment",
                "Cek di Google: '[company name] pyramid scheme lawsuit'",
                "FTC website untuk verify MLM complaints"
            ],
            "time_limit_seconds": 280,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        
        # SOCIAL PROOF (5 challenges)  
        {
            "id": str(uuid.uuid4()),
            "title": "Fake Review Ecosystem",
            "category": "money_app",
            "difficulty": "intermediate",
            "cialdini_principle": "social_proof",
            "description": "Produk dengan review palsu untuk manipulasi social proof",
            "scenario": "Amazon/Shopee: 'Miracle Weight Loss Tea - 10K reviews, 4.8 stars'. Reviews: 'Lost 15kg in 2 weeks!', 'Amazing product!'. Tapi: 1) Review generic, 2) Burst of 500 reviews in 1 day, 3) Reviewer profiles new/low activity, 4) Photos uploaded same day, 5) Critical review (1-2 star) quickly buried",
            "questions": [
                {
                    "question": "Bagaimana social proof dimanipulasi?",
                    "options": [
                        "10K reviews pasti genuine",
                        "Fake reviews (paid/bot) create false social proof: 'If 10K people bought, must be good' - exploit herd mentality",
                        "Rating tinggi = quality",
                        "Tidak ada manipulation"
                    ],
                    "correct_answer": 1,
                    "explanation": "Fake review industry: $1000 = 1000 reviews + 4.5 star average. Creates social proof illusion untuk manipulate buyer psychology: 'everyone bought this, so it's safe'."
                },
                {
                    "question": "Red flags dari review pattern ini?",
                    "options": [
                        "Review bagus = produk bagus",
                        "Burst reviews, generic text, new reviewer accounts, suspicious photo timing = coordinated fake reviews",
                        "4.8 star legitimate",
                        "Banyak yang beli"
                    ],
                    "correct_answer": 1,
                    "explanation": "Fake review red flags: 1) Unnatural burst (500 in 1 day), 2) Generic language, 3) New accounts, 4) Photos uploaded together, 5) No negative reviews (real products have critics)."
                },
                {
                    "question": "Cara verify genuine reviews?",
                    "options": [
                        "Trust platform rating",
                        "Check Fakespot.com/ReviewMeta, search YouTube independent reviews, check Reddit threads, suspicious if ONLY positive",
                        "5 star = legit",
                        "Total review count matters"
                    ],
                    "correct_answer": 1,
                    "explanation": "Tools: Fakespot (grade A-F), ReviewMeta (adjusted rating), search '[product] reddit review' for honest opinions. Real products: mix of 5-star and critical reviews."
                }
            ],
            "points": 85,
            "tips": [
                "Use Fakespot.com or ReviewMeta.com untuk analyze reviews",
                "Check critical (1-2 star) reviews untuk real problems",
                "Search Reddit/YouTube untuk unbiased opinions",
                "100% positive reviews adalah red flag",
                "Check reviewer profiles - real people have history"
            ],
            "time_limit_seconds": 200,
            "created_at": datetime.now(timezone.utc).isoformat()
        },

        # AUTHORITY (5 challenges)
        {
            "id": str(uuid.uuid4()),
            "title": "Fake Government Official Call",
            "category": "pretexting",
            "difficulty": "advanced",
            "cialdini_principle": "authority",
            "description": "Penipuan mengatasnamakan pejabat pemerintah",
            "scenario": "Telepon dari caller ID 'KEMENKUMHAM RI': 'Anda terlibat kasus pencucian uang. Rekening akan diblokir. Transfer dana ke rekening aman negara untuk investigasi atau akan ditangkap dalam 24 jam'. Intimidasi, data pribadi Anda disebutkan (nama, NIK, alamat).",
            "questions": [
                {
                    "question": "Bagaimana authority principle dieksploitasi?",
                    "options": [
                        "Pemerintah memang bisa telepon",
                        "Impersonate authority (government) untuk trigger fear + compliance. Data pribadi (leaked) membuat tampak legit",
                        "Caller ID 'KEMENKUMHAM' = real",
                        "Procedure normal"
                    ],
                    "correct_answer": 1,
                    "explanation": "Authority exploitation: 1) Government agency name (intimidating), 2) Threat arrest (fear), 3) Personal data (from breach) untuk 'legitimacy'. Real gov agency: official letter, NEVER phone transfer."
                },
                {
                    "question": "Data pribadi disebutkan kenapa tetap red flag?",
                    "options": [
                        "Berarti mereka real government",
                        "Data pribadi MUDAH diperoleh dari data breach (Tokopedia, BPJS, dll) - bukan bukti legitimacy",
                        "Hanya government yang punya data",
                        "Mereka verified"
                    ],
                    "correct_answer": 1,
                    "explanation": "Indonesia mengalami massive data breaches: Tokopedia (91M), BPJS (279M), eHAC (1.3M). Data nama-NIK-alamat dijual dark web $50-100. Scammer buy data untuk 'legitimacy'."
                },
                {
                    "question": "Action jika terima telepon seperti ini?",
                    "options": [
                        "Transfer ke 'rekening negara'",
                        "Tutup telpon, cek langsung ke website resmi instansi (kemenkumham.go.id), lapor ke polisi cyber, NEVER transfer",
                        "Nego jumlah transfer",
                        "Tanya detail kasus"
                    ],
                    "correct_answer": 1,
                    "explanation": "Response protocol: 1) TUTUP telepon immediately, 2) Visit official website/call public number (NOT number from caller), 3) Report ke polisi (patrolisiber.id), 4) NEVER transfer money."
                }
            ],
            "points": 130,
            "tips": [
                "Government agency NEVER ask transfer via phone",
                "Caller ID can be spoofed easily",
                "Data pribadi Anda likely leaked (check: haveibeenpwned.com)",
                "Real legal process: official letter + in-person",
                "Report ke patrolisiber.id dan nomor scammer ke provider"
            ],
            "time_limit_seconds": 260,
            "created_at": datetime.now(timezone.utc).isoformat()
        },

        # LIKING (4 challenges)
        {
            "id": str(uuid.uuid4()),
            "title": "Fake Influencer Endorsement",
            "category": "money_app",
            "difficulty": "intermediate",
            "cialdini_principle": "liking",
            "description": "Influencer di-pay untuk promote produk scam",
            "scenario": "Influencer 500K followers promote 'BinancePro Trading Bot - I earned $50K in 1 month!' dengan screenshot profit. Followers ikut invest karena 'trust' influencer. Ternyata: 1) Screenshot fake, 2) Influencer paid $5K promote, 3) Bot adalah ponzi scheme, 4) Influencer tidak actually use product.",
            "questions": [
                {
                    "question": "Bagaimana 'liking' principle dieksploitasi?",
                    "options": [
                        "Influencer always honest",
                        "Followers 'like' influencer \u2192 lower skepticism. Trust transfered dari person ke product tanpa verify",
                        "500K followers = credibility",
                        "Screenshot = proof"
                    ],
                    "correct_answer": 1,
                    "explanation": "Liking exploitation: follower relationship dengan influencer creates trust. Trust transfered ke produk tanpa critical evaluation. Parasocial relationship lowers guard."
                },
                {
                    "question": "Red flags dari endorsement ini?",
                    "options": [
                        "Influencer pasti test produk",
                        "$50K/month claim unrealistic + no disclosure 'paid partnership' + profit screenshot easy to fake = sponsored scam",
                        "Screenshot proof legitimate",
                        "Trading bot bisa profit segitu"
                    ],
                    "correct_answer": 1,
                    "explanation": "Red flags: 1) Unrealistic returns, 2) No #ad disclosure (FTC/EU requires), 3) Generic testimonial, 4) Inspect element makes fake screenshot in 30 seconds. Many influencers promote scam for quick $.

"
                },
                {
                    "question": "Verify legit vs paid scam endorsement?",
                    "options": [
                        "Trust influencer you follow",
                        "Check: #ad disclosure, independent reviews, influencer actually uses product long-term, verify claims independently",
                        "Follower count = trustworthy",
                        "Celebrity wouldn't lie"
                    ],
                    "correct_answer": 1,
                    "explanation": "Verification: 1) #ad or 'partnership' disclosed?, 2) Google '[product] scam', 3) Influencer posting long-term or one-time?, 4) DYOR independent dari endorsement. Celebrities promote scams too (Kardashians-Bitconnect)."
                }
            ],
            "points": 95,
            "tips": [
                "Influencer endorsement ≠ product quality",
                "Required by law: #ad or #sponsored disclosure",
                "Many influencers promote without using product",
                "Research independently, don't rely on parasocial trust",
                "Check if influencer has scam promotion history"
            ],
            "time_limit_seconds": 220,
            "created_at": datetime.now(timezone.utc).isoformat()
        },

        # SCARCITY (5 challenges)
        {
            "id": str(uuid.uuid4()),
            "title": "Flash Sale Countdown Manipulation",
            "category": "phishing",
            "difficulty": "beginner",
            "cialdini_principle": "scarcity",
            "description": "E-commerce dengan fake countdown timer untuk create urgency",
            "scenario": "Tokopedia: 'FLASH SALE ENDS IN 00:15:00! iPhone 15 Pro Max 90% OFF - Rp 1.5 juta (normal Rp 15 juta)!' Timer mencapai 00:00:00 \u2192 reset ke 01:00:00. 'Only 3 left in stock!' Refresh page: still '3 left'. Beli \u2192 uang hilang, barang fake/tidak datang.",
            "questions": [
                {
                    "question": "Bagaimana scarcity principle dieksploitasi?",
                    "options": [
                        "Countdown dan 'limited stock' real",
                        "Fake timer + fake stock untuk create artificial scarcity \u2192 panic buying tanpa verify legitimacy",
                        "Flash sale umum di e-commerce",
                        "90% discount possible"
                    ],
                    "correct_answer": 1,
                    "explanation": "Scarcity manipulation: 1) Countdown resets (fake urgency), 2) Stock number static (fake scarcity), 3) Unrealistic discount. Purpose: prevent rational thinking, force impulse buy."
                },
                {
                    "question": "Red flags dari deal ini?",
                    "options": [
                        "Great deal, buy cepat",
                        "90% off flagship product unrealistic + timer reset + static stock + too good to be true = SCAM seller",
                        "Tokopedia protect buyer",
                        "Limited time legit"
                    ],
                    "correct_answer": 1,
                    "explanation": "Legitimate flash sale: 10-30% off, NOT 90% on new iPhone. Timer resets adalah JS trick. Even on legit platform (Tokopedia), check seller rating/verification carefully."
                },
                {
                    "question": "Verify legit flash sale?",
                    "options": [
                        "Jika ada timer, buy cepat",
                        "Check seller rating/reviews, compare price to official store, screenshot for dispute, if too good = probably scam",
                        "Platform besar = safe",
                        "Countdown = real urgency"
                    ],
                    "correct_answer": 1,
                    "explanation": "Verification: 1) Seller badge (official/power merchant?), 2) Seller rating + review text, 3) Compare to brand official store, 4) Too good to be true = scam. Scam sellers exist on all platforms."
                }
            ],
            "points": 70,
            "tips": [
                "Countdown timer can be infinite JavaScript loop",
                "'Only X left' often fake (F12 inspect element)",
                "90% off new product = impossible/scam",
                "Take time to verify despite 'urgency'",
                "Compare price across multiple sellers"
            ],
            "time_limit_seconds": 180,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
    ]
    
    await db.challenges.insert_many(challenges)
    print(f"✅ Added {len(challenges)} Cialdini-categorized challenges")
    
    # Count by principle
    principles = {}
    for c in challenges:
        p = c['cialdini_principle']
        principles[p] = principles.get(p, 0) + 1
    
    print("\n📊 Challenges by Cialdini Principle:")
    for principle, count in principles.items():
        print(f"  - {principle.title()}: {count} challenges")
    
    print("\n🎉 Seeding completed!")
    client.close()

if __name__ == "__main__":
    asyncio.run(seed_cialdini_challenges())
