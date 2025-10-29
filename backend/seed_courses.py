import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
import uuid
from datetime import datetime, timezone

mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
client = AsyncIOMotorClient(mongo_url)
db = client['tegalsec_lab']

async def seed_courses():
    print("📚 Seeding courses...")
    
    await db.courses.delete_many({})
    
    courses = [
        {
            "id": str(uuid.uuid4()),
            "title": "Fundamental Social Engineering",
            "description": "Pelajari dasar-dasar social engineering dari teori hingga praktik dengan 6 prinsip Cialdini",
            "category": "fundamental",
            "difficulty": "beginner",
            "total_duration_minutes": 120,
            "prerequisites": [],
            "learning_outcomes": [
                "Memahami definisi dan konsep social engineering",
                "Menguasai 6 prinsip psikologi Cialdini",
                "Mengidentifikasi taktik social engineering umum",
                "Menerapkan defense strategies dalam kehidupan sehari-hari"
            ],
            "modules": [
                {
                    "module_number": 1,
                    "title": "Pengenalan Social Engineering",
                    "description": "Memahami apa itu social engineering dan mengapa penting",
                    "slides": [
                        {
                            "title": "Apa itu Social Engineering?",
                            "content": "**Social Engineering** adalah teknik manipulasi psikologis yang digunakan untuk menipu orang agar memberikan informasi rahasia atau melakukan tindakan yang menguntungkan attacker.\\n\\n**Key Points:**\\n- Bukan serangan teknis, tapi serangan psikologis\\n- Memanfaatkan sifat alami manusia: trust, helpful, respect authority\\n- Lebih mudah hack manusia daripada hack sistem\\n\\n**Fakta Mengejutkan:**\\n- 98% cyber attacks melibatkan social engineering (Verizon DBIR)\\n- Rata-rata perusahaan kehilangan $4.65 juta per data breach (IBM)\\n- 1 dari 3 orang pernah jadi victim social engineering"
                        },
                        {
                            "title": "Mengapa Social Engineering Efektif?",
                            "content": "Social engineering berhasil karena memanfaatkan **human vulnerabilities**, bukan system vulnerabilities.\\n\\n**Faktor Keberhasilan:**\\n\\n1. **Trust** - Manusia naturally percaya pada orang lain\\n2. **Fear** - Ancaman membuat panik dan tidak berpikir jernih\\n3. **Greed** - Iming-iming keuntungan menurunkan kewaspadaan\\n4. **Curiosity** - Penasaran adalah weakness yang diexploit\\n5. **Urgency** - Tekanan waktu prevent logical thinking\\n\\n**Contoh Real:**\\n- Target data breach 2013: akibat phishing email ke vendor\\n- Uber breach 2016: social engineering ke IT helpdesk\\n- Twitter Bitcoin scam 2020: manipulasi employee"
                        },
                        {
                            "title": "Jenis-jenis Social Engineering",
                            "content": "**1. Phishing**\\n- Email/SMS/call yang menyamar sebagai entitas terpercaya\\n- Tujuan: steal credentials, install malware\\n- Contoh: Email dari 'bank' minta verify account\\n\\n**2. Pretexting**\\n- Menciptakan skenario palsu untuk gain trust\\n- Attacker menggunakan false identity\\n- Contoh: Menyamar sebagai IT support\\n\\n**3. Baiting**\\n- Iming-iming sesuatu untuk lure victim\\n- File/device yang infected\\n- Contoh: USB 'gratis' di parking lot\\n\\n**4. Quid Pro Quo**\\n- Menawarkan sesuatu for exchange informasi\\n- 'Something for something'\\n- Contoh: Fake tech support offers help\\n\\n**5. Tailgating**\\n- Physical access dengan follow orang authorized\\n- Exploit courtesy (sopan santun)\\n- Contoh: 'Lupa badge' di entrance kantor"
                        }
                    ]
                },
                {
                    "module_number": 2,
                    "title": "6 Prinsip Cialdini",
                    "description": "Prinsip psikologi persuasi yang dieksploitasi dalam social engineering",
                    "slides": [
                        {
                            "title": "1. Reciprocity (Timbal Balik)",
                            "content": "**Definisi:** Kecenderungan manusia untuk membalas kebaikan yang diterima.\\n\\n**Cara Exploit:**\\n- Memberi hadiah/diskon 'gratis' lalu minta data\\n- 'Free trial' yang susah cancel\\n- Ebook/tools gratis yang mengandung malware\\n\\n**Defense:**\\n- 'Gratis' selalu ada hidden cost\\n- Baca terms & conditions\\n- Jangan merasa 'berhutang' untuk share data\\n\\n**Contoh Kasus:**\\n- App gratis yang jual data user (Facebook-Cambridge Analytica)\\n- 'Gift card' email phishing\\n- USB drive 'gratis' yang contain malware\\n\\n**Red Flags:**\\n- Too generous offer tanpa jelas business model\\n- Pressure untuk 'balas kebaikan'\\n- Gratis tapi minta banyak permissions"
                        },
                        {
                            "title": "2. Commitment & Consistency",
                            "content": "**Definisi:** Sekali commit, manusia cenderung konsisten dengan keputusan tersebut.\\n\\n**Cara Exploit:**\\n- Survey 'innocent' yang escalate ke data sensitif\\n- Small investment terus diminta invest lebih\\n- Foot-in-the-door technique\\n\\n**Defense:**\\n- Evaluate tiap request independently\\n- Sunk cost fallacy: uang sudah keluar bukan alasan continue\\n- OK untuk stop meski sudah mulai\\n\\n**Contoh Kasus:**\\n- Investment scam dengan minimal awal rendah\\n- MLM yang escalate dari member ke 'leader'\\n- Subscription service susah cancel\\n\\n**Red Flags:**\\n- Gradual escalation of requests\\n- 'You already started, why stop now?'\\n- Guilt trip untuk continue"
                        },
                        {
                            "title": "3. Social Proof (Bukti Sosial)",
                            "content": "**Definisi:** Mengikuti apa yang dilakukan orang banyak, especially saat ragu.\\n\\n**Cara Exploit:**\\n- Fake testimonials & reviews\\n- Bot followers/members\\n- 'Everyone is doing it' pressure\\n\\n**Defense:**\\n- Testimonial mudah dibuat\\n- Verify independently\\n- Cek review di multiple sources\\n\\n**Contoh Kasus:**\\n- Fake app dengan 4.5* rating dari bot\\n- Investment scheme dengan '100K members'\\n- Influencer paid endorsement untuk scam\\n\\n**Red Flags:**\\n- Generic testimonials tanpa detail\\n- Sudden spike in positive reviews\\n- Member count tidak match dengan actual engagement\\n- 'Limited slots, 1000 people joined today!'"
                        },
                        {
                            "title": "4. Authority (Otoritas)",
                            "content": "**Definisi:** Kecenderungan patuh pada figur authority/power.\\n\\n**Cara Exploit:**\\n- Fake email dari 'CEO' atau 'Police'\\n- Impersonate customer service\\n- Logo & branding official\\n\\n**Defense:**\\n- Verify melalui channel official\\n- Authority real tidak request data via email/phone\\n- Jangan panik saat di-intimidate\\n\\n**Contoh Kasus:**\\n- BEC (Business Email Compromise): fake CEO email\\n- Phishing dengan logo bank\\n- Fake police call minta transfer\\n\\n**Red Flags:**\\n- Unexpected contact from 'authority'\\n- Urgent request bypass normal process\\n- Threaten consequences jika tidak comply\\n- Request unusual information"
                        },
                        {
                            "title": "5. Liking (Kesukaan)",
                            "content": "**Definisi:** Lebih mudah terpengaruh oleh orang yang kita suka/mirip.\\n\\n**Cara Exploit:**\\n- Attacker sangat ramah & helpful\\n- Mencari kesamaan (alumni, hobi, daerah)\\n- Pujian berlebihan\\n\\n**Defense:**\\n- Separate security decision from feelings\\n- Tetap follow protocol meski orangnya 'baik'\\n- Keramahan bukan guarantee niat baik\\n\\n**Contoh Kasus:**\\n- Romance scam (build relationship \u2192 minta uang)\\n- Tailgating dengan 'friendly face'\\n- Fake recruiter yang 'sangat helpful'\\n\\n**Red Flags:**\\n- Too friendly too fast\\n- Mirror your interests suspiciously\\n- Excessive compliments\\n- Make you feel special/chosen"
                        },
                        {
                            "title": "6. Scarcity (Kelangkaan)",
                            "content": "**Definisi:** Menginginkan lebih kuat saat terlihat langka/terbatas.\\n\\n**Cara Exploit:**\\n- 'Limited time offer - today only!'\\n- 'Only 10 slots left!'\\n- 'Act now or account will be blocked!'\\n\\n**Defense:**\\n- Pressure waktu = RED FLAG\\n- Legitimate offer biasanya tidak hilang instant\\n- Take time untuk verify & think\\n\\n**Contoh Kasus:**\\n- Phishing dengan 'verify in 24h or blocked'\\n- Investment 'limited participant'\\n- Flash sale scam di e-commerce\\n\\n**Red Flags:**\\n- Countdown timer\\n- 'Last chance' messaging\\n- Threat of missing out (FOMO)\\n- Pressure immediate decision\\n- 'Stock terbatas' untuk digital product"
                        }
                    ]
                },
                {
                    "module_number": 3,
                    "title": "Defense Strategies",
                    "description": "Cara melindungi diri dari social engineering attacks",
                    "slides": [
                        {
                            "title": "Defense Framework: STOP",
                            "content": "Framework sederhana untuk defend terhadap social engineering:\\n\\n**S - Slow Down**\\n- Jangan panic atau rush\\n- Attacker rely on quick decisions\\n- Take time untuk think & verify\\n\\n**T - Think Critically**\\n- Apakah request ini masuk akal?\\n- Mengapa mereka contact saya?\\n- Apa motivation mereka?\\n\\n**O - Observe Red Flags**\\n- Urgency, threats, too good to be true\\n- Unsolicited contact\\n- Unusual requests\\n\\n**P - Protect & Verify**\\n- Verify through official channels\\n- Protect your credentials\\n- Report suspicious activity"
                        },
                        {
                            "title": "Security Hygiene Checklist",
                            "content": "**Email Security:**\\n✓ Hover over links before clicking\\n✓ Check sender domain carefully\\n✓ Be suspicious of urgent requests\\n✓ Never open unexpected attachments\\n✓ Use email security tools\\n\\n**Password Security:**\\n✓ Unique password per account\\n✓ Use password manager\\n✓ Enable 2FA (preferably app-based, not SMS)\\n✓ Never share OTP/password\\n✓ Change password if suspicious activity\\n\\n**Social Media:**\\n✓ Limit personal info publicly\\n✓ Be careful what you share\\n✓ Verify friend requests\\n✓ Adjust privacy settings\\n✓ Think before posting"
                        },
                        {
                            "title": "Incident Response",
                            "content": "**Jika Anda Sudah Jadi Victim:**\\n\\n**Immediate Actions:**\\n1. **Change passwords** - All compromised accounts\\n2. **Enable 2FA** - If not already enabled\\n3. **Check account activity** - Unauthorized access?\\n4. **Contact financial institutions** - If financial info exposed\\n5. **Scan for malware** - If you clicked link/downloaded file\\n\\n**Reporting:**\\n- Report ke platform terkait (bank, e-commerce, etc)\\n- Lapor ke polisi cyber (patrolisiber.id)\\n- Report phishing ke Google/Microsoft\\n- Warn contacts jika email/social media compromised\\n\\n**Learn & Improve:**\\n- Analyze what went wrong\\n- Update security measures\\n- Share experience untuk awareness"
                        }
                    ]
                }
            ],
            "created_by": "admin",
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Advanced Phishing Techniques",
            "description": "Deep dive into modern phishing techniques dan cara mendeteksinya",
            "category": "phishing",
            "difficulty": "advanced",
            "total_duration_minutes": 90,
            "prerequisites": ["Fundamental Social Engineering"],
            "learning_outcomes": [
                "Mengidentifikasi berbagai jenis phishing attacks",
                "Menganalisis anatomy of phishing emails",
                "Mendeteksi domain typosquatting & spoofing",
                "Melakukan phishing investigation"
            ],
            "modules": [
                {
                    "module_number": 1,
                    "title": "Modern Phishing Landscape",
                    "description": "Phishing techniques yang digunakan 2024-2025",
                    "slides": [
                        {
                            "title": "Evolution of Phishing",
                            "content": "**Phishing Era Timeline:**\\n\\n**2000s - Basic Email Phishing**\\n- Nigerian Prince scams\\n- Obvious grammar mistakes\\n- Generic greetings\\n\\n**2010s - Spear Phishing**\\n- Targeted attacks\\n- Personalized content\\n- Better social engineering\\n\\n**2020s - AI-Powered Phishing**\\n- ChatGPT-generated emails (perfect grammar)\\n- Deepfake voice/video calls\\n- Dynamic phishing pages\\n- Real-time phishing kits\\n\\n**Current Trends:**\\n- MFA bypass techniques\\n- Adversary-in-the-Middle (AitM)\\n- QR code phishing\\n- Cloud service impersonation\\n- Cryptocurrency phishing"
                        },
                        {
                            "title": "Anatomy of Phishing Email",
                            "content": "**Components of Phishing Email:**\\n\\n**1. Sender Address**\\n- Spoofed 'From' name\\n- Similar domain (typosquatting)\\n- Compromised legitimate account\\n\\n**2. Subject Line**\\n- Urgency: 'URGENT ACTION REQUIRED'\\n- Fear: 'Your account will be suspended'\\n- Curiosity: 'You have a package'\\n\\n**3. Body Content**\\n- Official logo (copy-paste)\\n- Professional language (AI-generated)\\n- Call-to-action button\\n- Social engineering trigger\\n\\n**4. Malicious Element**\\n- Phishing link\\n- Malicious attachment\\n- Fake login form\\n- QR code to phishing site"
                        }
                    ]
                }
            ],
            "created_by": "admin",
            "created_at": datetime.now(timezone.utc).isoformat()
        }
    ]
    
    await db.courses.insert_many(courses)
    print(f"✅ {len(courses)} courses created!")
    
    print("\\n🎉 Course seeding completed!")
    client.close()

if __name__ == "__main__":
    asyncio.run(seed_courses())
