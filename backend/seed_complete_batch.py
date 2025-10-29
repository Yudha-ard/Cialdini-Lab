import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
import uuid
from datetime import datetime, timezone

mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ.get('DB_NAME', 'tegalsec_lab')]

async def seed_complete_challenges():
    print("🚀 Seeding COMPLETE challenge set untuk 30+ total challenges...")
    
    challenges = []
    
    # SOCIAL PROOF - 10 soal
    challenges.append({
        "id": str(uuid.uuid4()),
        "title": "Social Proof Attack: From Fake Reviews to Viral Scams",
        "category": "indonesian_case",
        "difficulty": "intermediate",
        "cialdini_principle": "social_proof",
        "challenge_type": "multi_choice",
        "description": "10 kasus social proof manipulation di Indonesia - fake reviews, testimonials, followers",
        "scenario": "Social proof adalah kecenderungan manusia mengikuti tindakan orang lain. Di digital era, ini dimanipulasi lewat fake reviews, bot followers, staged testimonials.",
        "questions": [
            {
                "question": "Toko online 1000+ review 5-star dalam 1 minggu. Profile reviewer: no photo, generic names (Budi123, User456), review copy-paste format sama. Red flag?",
                "options": [
                    "Toko memang bagus, banyak satisfied customer",
                    "FAKE REVIEWS: 1000 review/week impossible organically. Bot accounts (no photo, generic names), identical format = paid review farm",
                    "Review banyak berarti trusted",
                    "Platform sudah verify seller"
                ],
                "correct_answer": 1,
                "explanation": "Red flags fake reviews: (1) Volume impossible (1000/week), (2) Bot accounts (generic names, no history), (3) Copy-paste format (automation). Legitimate reviews: varied, detailed, spread over time."
            },
            {
                "question": "Instagram influencer 100K followers, tapi post like average 50-100. Engagement rate <0.1%. Comment generic ('Nice post!', 'Love this!'). Analisis?",
                "options": [
                    "Low engagement normal untuk influencer besar",
                    "FAKE FOLLOWERS: 100K followers dengan 50-100 likes = 0.05-0.1% engagement (normal: 3-5%). Bought bot followers, not real audience",
                    "Followers tidak aktif di platform",
                    "Content quality issue"
                ],
                "correct_answer": 1,
                "explanation": "Fake follower detection: engagement rate. Legitimate influencer 10K+ followers: 2-5% engagement (200-500 likes). <0.5% = bot followers. Generic comments = engagement pod/bots."
            },
            {
                "question": "Webinar zoom 2000 participants ditampilkan. Tapi chat sepi, Q&A tidak ada pertanyaan, poll tidak ada respons. Possible manipulation?",
                "options": [
                    "Audience pasif, hanya mendengarkan",
                    "FAKE PARTICIPANTS: Host bisa add bot accounts sebagai 'participants'. Inflated number for social proof, but zero real engagement",
                    "Webinar content membosankan",
                    "2000 orang terlalu banyak untuk interact"
                ],
                "correct_answer": 1,
                "explanation": "Zoom/Google Meet manipulation: host add fake accounts (bots) to inflate numbers. Social proof: '2000 orang join = must be valuable'. Reality: 50 real, 1950 fake. Check: engagement, not just numbers."
            },
            {
                "question": "Testimoni video di website: 10 orang, semua shot di background sama (ruangan/studio sama), professional lighting, scripted speech. Testimonial genuine?",
                "options": [
                    "Professional video production = testimonial legitimate",
                    "STAGED TESTIMONIALS: Identical background, lighting, scripted = paid actors di studio, bukan real customer. Real testimonial: varied locations, natural speech",
                    "Customer diminta rekaman di kantor brand",
                    "High quality production menunjukkan brand profesional"
                ],
                "correct_answer": 1,
                "explanation": "Fake testimonial markers: (1) Identical background = shot di studio sama, (2) Professional production for 'customer' video (inconsistent), (3) Scripted = not genuine experience. Real: varied, natural, unpolished."
            },
            {
                "question": "YouTube channel 1 juta subscribers, tapi setiap video cuma 1K-5K views dalam minggu pertama. Subscriber/view ratio sangat tinggi. Red flag?",
                "options": [
                    "Subscribers lama, inactive di YouTube",
                    "BOUGHT SUBSCRIBERS: 1 juta subscribers → video should get min 10K-50K views (1-5%). Only 0.1-0.5% = bot subscribers. Real audience tiny",
                    "Content tidak menarik untuk existing subscribers",
                    "Algorithm YouTube tidak promote"
                ],
                "correct_answer": 1,
                "explanation": "YouTube bot subscribers: subscriber count high, view count disproportionately low. Bought subscribers (bot farms) inflate number for social proof, but don't watch videos. Check: view/subscriber ratio."
            },
            {
                "question": "Crowdfunding campaign 5000 backers, tapi forum discussion sepi, social media mention minimal, no one talking about it anywhere. Contradiction?",
                "options": [
                    "Backers quiet, not active in community",
                    "FAKE BACKERS: Bot accounts/fake pledges inflate backer count. Real campaigns: organic buzz, forums active, social media mentions. Silence despite '5000 backers' = fabricated",
                    "Product niche, limited interest",
                    "Backers waiting for product delivery"
                ],
                "correct_answer": 1,
                "explanation": "Crowdfunding social proof test: real 5000 backers generate organic discussion, social media activity, forum posts. If number high but engagement zero = fake backers (possibly from creator accounts)."
            },
            {
                "question": "Aplikasi '1 juta+ downloads' di app store. Reviews 50K, rating 4.8. Tapi Google search 'nama app review' cuma dapat 10 blog posts, minimal discussion online. Analisis?",
                "options": [
                    "App popular tapi tidak dibahas blogger",
                    "DOWNLOAD/REVIEW MANIPULATION: 1 juta downloads + 50K reviews should generate substantial online discussion. Minimal presence = inflated numbers, possibly bot downloads/reviews",
                    "App baru, belum banyak coverage",
                    "Private company, tidak fokus marketing"
                ],
                "correct_answer": 1,
                "explanation": "Download manipulation detection: cross-reference app store numbers dengan online footprint. Real 1M downloads: substantial blog posts, YouTube reviews, forum discussions. Minimal footprint = fake numbers."
            },
            {
                "question": "E-commerce promo: 'Sold 100K units in 24 hours!' Tapi stock indicator selalu available, never out of stock. Reviews tidak ada spike corresponding dengan 100K sale. Scam indicator?",
                "options": [
                    "Stock besar, 100K tidak habiskan",
                    "FALSE SCARCITY + FAKE SALES: Impossible to sell 100K and maintain unlimited stock. Reviews should spike (100K = massive review increase). No spike = fake sales claim",
                    "Supplier resupply super cepat",
                    "100K across multiple sellers"
                ],
                "correct_answer": 1,
                "explanation": "Fake sales claim detection: (1) Physical impossibility (100K units stock always available?), (2) Review patterns (100K sales should generate 5K-10K reviews spike). No correlation = fake numbers."
            },
            {
                "question": "LinkedIn 'Thought Leader' 500K followers, tapi posts get 20-50 likes/reactions. Article shares minimal. Speaking engagement claims, but no verifiable events. Fake authority?",
                "options": [
                    "Followers tidak engage dengan content",
                    "BOUGHT LINKEDIN FOLLOWERS: 500K followers → posts should get 5K-25K engagements (1-5%). <50 = bot followers. Check: event verification, company validation, actual audience",
                    "Content quality decreased over time",
                    "Professional network less interactive"
                ],
                "correct_answer": 1,
                "explanation": "LinkedIn fake authority: bought followers (bot accounts) inflate credibility. Real 500K: significant engagement, verifiable speaking gigs, company endorsements. Low engagement + unverifiable claims = fake."
            },
            {
                "question": "Investment telegram group 50K members. 'Member testimonials': daily posts '100% profit!', screenshots identical format, same grammar errors across 'different' people. Group authentic?",
                "options": [
                    "Many successful members posting results",
                    "FAKE TESTIMONIALS: Identical formatting, same grammar patterns = one person/team creating fake accounts. Real 50K: varied testimonials, different formats, writing styles. Uniform = fabricated",
                    "Members copy each other's format",
                    "Success strategy consistent across members"
                ],
                "correct_answer": 1,
                "explanation": "Telegram scam group pattern: fake testimonials by admins using multiple accounts. Same format, grammar errors, screenshot style = automation. Real diverse group: varied communication styles."
            }
        ],
        "points": 200,
        "tips": ["Cross-reference numbers dengan actual engagement", "Bot followers: high count, low engagement", "Fake reviews: patterns, timing, generic content"],
        "real_case_reference": "E-commerce, influencer, crowdfunding scams Indonesia 2020-2024",
        "time_limit_seconds": 420,
        "created_at": datetime.now(timezone.utc)
    })
    
    # AUTHORITY - 12 soal
    challenges.append({
        "id": str(uuid.uuid4()),
        "title": "Authority Manipulation: Impersonation & False Credentials",
        "category": "indonesian_case",
        "difficulty": "advanced",
        "cialdini_principle": "authority",
        "challenge_type": "multi_choice",
        "description": "12 kasus impersonation authority figures - dari dokter palsu sampai fake police",
        "scenario": "Authority principle: orang cenderung comply dengan figur otoritas. Scammers exploit dengan impersonation, fake credentials, false affiliations.",
        "questions": [
            {
                "question": "WhatsApp dari 'Dokter Spesialis': profil foto lab coat, nama 'Dr. Budi, Sp.PD'. Recommend suplemen Rp 3 juta/bulan. No clinic mentioned, consult via WA only. Red flags?",
                "options": [
                    "Telemedicine modern, wajar via WhatsApp",
                    "RED FLAGS: (1) No clinic/hospital affiliation (unverifiable), (2) Expensive suplemen recommendation immediately (sales focus), (3) WhatsApp-only (no official platform). Real doctor: verifiable practice, hospital affiliation",
                    "Dokter independen, suplemen premium",
                    "Telemedicine legal di Indonesia"
                ],
                "correct_answer": 1,
                "explanation": "Fake doctor detection: real medical professionals have verifiable affiliations (hospital, clinic, IDI registration). WhatsApp-only + immediate expensive recommendation + no practice location = scam. Verify: cek IDI online registry."
            },
            {
                "question": "Email 'CEO perusahaan' minta transfer urgent Rp 500 juta. Sender: ceo@company-name.com (bukan company.com). Email tone demanding, threatens firing if delayed. Authority attack?",
                "options": [
                    "CEO memang butuh transfer urgent",
                    "CEO FRAUD (BEC Attack): Domain typo (company-name.com vs company.com), urgency + threat tactic. Real CEO: proper domain, tidak threaten firing via email, ada prosedur for large transfers",
                    "Startup CEO informal communication style",
                    "Email legitimate karena ada signature"
                ],
                "correct_answer": 1,
                "explanation": "Business Email Compromise (BEC): impersonate authority (CEO) untuk coerce action. Red flags: (1) Domain typo, (2) Threats (not professional), (3) Bypass normal procedures. Always verify large requests via secondary channel (phone)."
            },
            {
                "question": "Notifikasi 'POLRI Cyber Crime': 'Akun Anda terlibat kasus kriminal. Transfer Rp 10 juta denda dalam 24 jam atau ditangkap.' Link bayar via e-wallet. Legitimate?",
                "options": [
                    "Cyber crime division might use online notice",
                    "FAKE POLICE SCAM: Real police: (1) Never request payment via e-wallet, (2) Summons delivered formally (surat), (3) Payment via bank with receipt. Urgency + threat + e-wallet = scam",
                    "Digital era, polisi modern",
                    "Link aman kalau via e-wallet"
                ],
                "correct_answer": 1,
                "explanation": "Police impersonation scam: exploit authority fear. Real legal process: formal letters, court summons, bank payments with receipts. E-wallet payment + 24-hour threat = scam. Verify: visit police station directly."
            },
            {
                "question": "LinkedIn profile 'Harvard MBA, Ex-McKinsey, Angel Investor'. Profile photo professional, well-written bio. Offers 'mentorship' for Rp 50 juta program. How verify legitimacy?",
                "options": [
                    "LinkedIn profile adalah proof cukup",
                    "VERIFY CREDENTIALS: (1) Harvard MBA: check alumni directory public search, (2) McKinsey: email format @mckinsey.com, LinkedIn colleague network, (3) Portfolio: verifiable investments. Profile easy to fake",
                    "Mentorship fee indicates seriousness",
                    "Professional photo = credible"
                ],
                "correct_answer": 1,
                "explanation": "Credential verification: LinkedIn self-reported, easy to fake. Verify: (1) University alumni search (many public), (2) Company email/network connections (ex-McKinsey know each other), (3) Track record (verifiable past). High fee ≠ legitimacy."
            },
            {
                "question": "Website klinik 'Partner Kemenkes RI', logo Kemenkes di footer, testimonial 'Disetujui Kementerian Kesehatan'. Selling herbal medicine Rp 2 juta. How verify partnership?",
                "options": [
                    "Logo dan text claim adalah bukti",
                    "VERIFY OFFICIAL PARTNERSHIP: (1) Check Kemenkes official website partner list, (2) Logo usage: may be unauthorized (easy to copy), (3) 'Disetujui' ≠ 'Partner'. Call Kemenkes hotline to verify. Most are fake claims",
                    "Herbal medicine tidak perlu persetujuan",
                    "Website profesional = legitimate"
                ],
                "correct_answer": 1,
                "explanation": "Government affiliation verification: (1) Official list (most ministries publish partners), (2) Logo ≠ affiliation (easy to copy), (3) Direct contact verification. Herbal medicine claims 'approved by Kemenkes' often false."
            },
            {
                "question": "Telegram investment 'Tim Ex-Banker BCA, Mandiri, UBS'. Daily signals '90% win rate'. Signal service Rp 5 juta/month. Profile pictures professional suits. Verify banker claims how?",
                "options": [
                    "Ex-banker common in investment consulting",
                    "VERIFY EMPLOYMENT: Real banker: (1) LinkedIn dengan extensive network in banking, (2) Colleagues can confirm, (3) Track record verifiable. Telegram-only + anonymous = likely fake. Request LinkedIn, verify connections",
                    "Banking experience valuable, worth Rp 5 juta",
                    "90% win rate proof of expertise"
                ],
                "correct_answer": 1,
                "explanation": "Ex-banker claim verification: (1) LinkedIn (real bankers: extensive network, recommendations), (2) Banking network (bankers know each other, can verify), (3) Track record. Anonymous Telegram + unverifiable = red flag. 90% win rate impossible consistently."
            },
            {
                "question": "YouTube channel 'Lawyer Explains Law' 500K subscribers, discusses legal issues confidently. Selling legal consultation Rp 10 juta. Never mentions which law firm, no bar association number shown. Verify lawyer status?",
                "options": [
                    "Content quality proves legal knowledge",
                    "VERIFY BAR MEMBERSHIP: Real lawyer: (1) Must be Peradi member (Indonesia bar), (2) Peradi number public, searchable, (3) Law firm affiliation (or solo practice address). No bar number = not licensed lawyer, illegal practice",
                    "YouTube tidak require license disclosure",
                    "Consultation offer indicates professional"
                ],
                "correct_answer": 1,
                "explanation": "Lawyer verification Indonesia: (1) Peradi (Indonesia bar association) membership mandatory, (2) Bar number searchable online, (3) Practice location. 'Legal advice' without license = illegal. Content knowledge ≠ licensed to practice."
            },
            {
                "question": "Instagram 'Certified Financial Planner' selling investment plan Rp 20 juta. Certificate image on profile (looks official). How verify CFP certification real?",
                "options": [
                    "Certificate photo adalah proof sufficient",
                    "VERIFY CFP: (1) Indonesia: CFP® hanya issued by FPSB Indonesia, (2) Check FPSB Indonesia registry online (public), (3) Certificate template verifiable. Fake certificates common (Photoshop), always verify registry",
                    "Instagram verified badge enough",
                    "Certificate looks professional"
                ],
                "correct_answer": 1,
                "explanation": "Professional certification verification: (1) Issuing body registry (FPSB Indonesia for CFP), (2) Online searchable, (3) Certificate format standardized. Fake certificates rampant (Photoshop, print). Never trust certificate image alone, verify registry."
            },
            {
                "question": "Email 'Microsoft Security Team': 'Your Office 365 compromised, reset password immediately: [link]'. Sender: security@micros0ft.com (zero, not O). Email format professional, Microsoft logo correct. Phishing?",
                "options": [
                    "Microsoft security might email about compromise",
                    "PHISHING VIA TYPOSQUATTING: Domain micros0ft.com (zero) vs microsoft.com (letter O) = typosquatting. Real Microsoft: (1) @microsoft.com (no variations), (2) Reset via account.microsoft.com direct, never email link. Logo easy to copy",
                    "Security issues require immediate action",
                    "Email looks official with logo"
                ],
                "correct_answer": 1,
                "explanation": "Authority phishing: impersonate tech giant using typosquatting domain (character substitution: 0 vs O, rn vs m). Real tech companies: (1) Exact domain, (2) Direct you to official site (no links), (3) Never ask password via email."
            },
            {
                "question": "WhatsApp 'Bank Account Verification Team' dari nomor +62-877-xxxx (bukan shortcode 4 digit bank). Ask nomor kartu, CVV, OTP 'untuk verifikasi'. Bank procedure?",
                "options": [
                    "Verification team mungkin dari outsource center",
                    "BANK IMPERSONATION: Real bank: (1) Call from official shortcode (4 digit, e.g., 1500), (2) NEVER ask CVV/OTP (bank already knows CVV unnecessary, OTP purpose), (3) Verify via app/website, not WhatsApp. This is fraud",
                    "WhatsApp verification modern",
                    "Bank update security procedures"
                ],
                "correct_answer": 1,
                "explanation": "Bank verification scam: (1) Banks use official shortcodes (government-registered 4-digit), not random numbers, (2) NEVER ask CVV (bank doesn't need) or OTP (defeats OTP purpose = one-time for your use). Asking these = 100% scam."
            },
            {
                "question": "Zoom meeting invite 'Minister of Trade - UMKM Partnership Program'. Zoom ID public, no password, generic link. In meeting: request business data, NIB, NPWP, then 'registration fee Rp 5 juta for program'. Government meeting protocol?",
                "options": [
                    "Government modernizing with Zoom meetings",
                    "FAKE GOVERNMENT MEETING: Real government: (1) Official email domain (@kemendag.go.id), (2) Formal invitation via official letter, (3) No registration fees for government programs, (4) Secure meeting (password-protected). Generic Zoom = fake",
                    "UMKM program require contribution",
                    "Zoom ID sufficient proof"
                ],
                "correct_answer": 1,
                "explanation": "Government impersonation: fake officials via Zoom easy (anyone can name 'Minister'). Real government: (1) Official email domain, (2) Formal letters (surat resmi), (3) Zero fees (government programs free), (4) Secure official meetings. Public Zoom + fees = scam."
            },
            {
                "question": "Website 'Indonesia COVID-19 Task Force' selling PCR test kit Rp 500K, logo Satgas COVID identical. Domain: satgas-covid.org (bukan covid19.go.id). How verify official?",
                "options": [
                    "Logo dan domain hampir sama, legitimate",
                    "TYPOSQUATTING + LOGO THEFT: Real government: (1) Always .go.id domain (government official), (2) .org/.com = not government. Logo easy to copy. Verify: covid19.go.id official only. Fake site selling products",
                    "Alternative official domain",
                    "PCR kit distribution authorized"
                ],
                "correct_answer": 1,
                "explanation": "Government website verification Indonesia: (1) .go.id ONLY for government (guaranteed by Kominfo), (2) .com/.org/.id = not official, (3) Logo copy easy. Always check .go.id, ignore similar domains. Fake sites: product sales, data theft."
            }
        ],
        "points": 240,
        "tips": ["Verify credentials via official registries", "Real authority: verifiable affiliations, proper domains", "Logo ≠ legitimacy (easy to copy)"],
        "real_case_reference": "Authority impersonation cases: BEC, fake police, credential fraud Indonesia 2020-2024",
        "time_limit_seconds": 480,
        "created_at": datetime.now(timezone.utc)
    })
    
    # LIKING - 10 soal
    challenges.append({
        "id": str(uuid.uuid4()),
        "title": "Liking Principle: Friendship as Weapon",
        "category": "indonesian_case",
        "difficulty": "intermediate",
        "cialdini_principle": "liking",
        "challenge_type": "multi_choice",
        "description": "10 kasus manipulation via false friendship, similarity, dan likability exploitation",
        "scenario": "Liking principle: kita lebih compliant dengan orang yang kita suka. Scammers manufacture likability via false friendship, similarity, dan attractiveness.",
        "questions": [
            {
                "question": "Teman SMA inactive 10 tahun tiba-tiba chat: 'Long time! Gimana kabarnya?' Talk 1 jam via video call, genuinely nice. Next day: 'Btw, I'm in insurance business, can I offer you policy?' Liking tactic?",
                "options": [
                    "Teman genuine reconnect, business separate",
                    "MANUFACTURED FRIENDSHIP: Reconnect ONLY to sell (not genuine). Initial hour: build rapport/likability (liking principle), then leverage relationship for sale. If reject = ruin 'friendship'. Liking weaponized",
                    "Business and friendship dapat coexist",
                    "Insurance is valuable financial product"
                ],
                "correct_answer": 1,
                "explanation": "Manufactured friendship detection: timing (inactive 10 years, suddenly chat), pattern (reconnect → nice talk → sales pitch 24-48 hours). Genuine reconnect: no sales pitch. Business contact: upfront, not disguised as friendship."
            },
            {
                "question": "Dating app match: incredibly attractive, similar interests (hobbies, music, books match 90%!), texts daily for weeks, love-bomb. Never video call. Then: 'Emergency, need Rp 10 juta loan, will repay.' Scam type?",
                "options": [
                    "Genuine connection, emergency happens",
                    "ROMANCE SCAM: Profile curated for YOUR interests (data mining your profile for 'similarity'), attractiveness (stolen photos), love-bombing (rapid intimacy). Avoid video = not real person. Loan request = goal from start",
                    "Long-distance relationship challenges",
                    "Attraction can happen quickly"
                ],
                "correct_answer": 1,
                "explanation": "Romance scam pattern: (1) Profile matches YOUR interests perfectly (too coincidental), (2) Rapid intimacy (love-bombing), (3) Avoid video (fake identity), (4) Money request (always the goal). Similarity manufactured for likability."
            },
            {
                "question": "Salesperson rumah: 'Sama nih, saya juga dari Jogja! Alumni UGM juga? Wah kampus sama!' Bonding over shared background 30 minutes. Then hard sell rumah Rp 2 miliar. Technique used?",
                "options": [
                    "Genuine connection over shared background",
                    "SIMILARITY LIKING: Salesperson trained find commonalities (hometown, alma mater) to create artificial bond. Likability → trust → sales leverage. May be true or false, but strategically used to manipulate",
                    "Small talk normal in sales",
                    "UGM alumni network genuine"
                ],
                "correct_answer": 1,
                "explanation": "Manufactured similarity: sales training technique - find ANY commonality (hometown, school, hobby) to create 'connection'. Even if true, strategic use = manipulation. Genuine connection: spontaneous, not sales-focused. Here: similarity as sales tool."
            },
            {
                "question": "MLM recruiter: beautiful, charming, compliments constantly ('You're so smart!', 'Natural leader!'). Coffee meeting feels good, ego boosted. Recruit pitch: 'Someone like YOU will definitely succeed in this business!' Manipulation?",
                "options": [
                    "Genuine assessment of capability",
                    "LIKABILITY via FLATTERY: Constant compliments create liking + ego boost → lower critical thinking. 'You're special' pitch = feel good about joining. Attractiveness + flattery + 'you're different' = liking principle exploitation",
                    "Compliments sincere observation",
                    "Confidence boost helps business success"
                ],
                "correct_answer": 1,
                "explanation": "Flattery-based liking: (1) Constant compliments (ego boost → like person), (2) 'You're special' (feel valued), (3) Attractiveness (physical liking). Result: lower defenses, comply with recruit. Genuine business: merit-based, not flattery-based."
            },
            {
                "question": "Crypto investment Telegram: admin super friendly, helpful, answers questions patiently. Free signals actually profitable (small amounts). Feels like community, admin 'cares'. Then: 'VIP group Rp 20 juta for big signals.' Liking build-up?",
                "options": [
                    "Admin genuine helpful, VIP offer value",
                    "LIKABILITY BUILD-UP: (1) Friendly/helpful = create liking, (2) Free profitable signals = trust-building (reciprocity), (3) Community feeling = belonging. After likability established → big ask. Liking + trust = compliance with Rp 20 juta",
                    "Free signals proof of expertise",
                    "VIP exclusive knowledge worth cost"
                ],
                "correct_answer": 1,
                "explanation": "Long-game liking: gradual trust building via helpfulness, small wins (free signals work = trust), community (belonging). Once likability/trust peak → large financial ask. Investment based on liking admin, not actual analysis."
            },
            {
                "question": "Webinar host: charismatic, funny, relatable stories ('I was broke too!'), audience laughing/engaged entire session. End: 'I want to help YOU succeed, special price Rp 15 juta course, TODAY ONLY.' Liking leverage?",
                "options": [
                    "Host genuine entertaining and helpful",
                    "CHARISMA-BASED LIKING: (1) Humor/relatability = audience likes host, (2) Shared struggle story = similarity/connection, (3) Entertainment = positive emotions. High likability + 'I want to help YOU' + urgency = sales pressure via liking",
                    "Course legitimate business offer",
                    "Charisma indicates expertise"
                ],
                "correct_answer": 1,
                "explanation": "Charismatic sales: create liking (humor, relatability) → audience defenses down → pitch. 'I want to help YOU' = leverages established likability. Decision based on liking person (not course value). Urgency prevents critical evaluation."
            },
            {
                "question": "Freelance client: super nice, compliments work constantly, easy-going, fun to work with. Project 1: paid fair. Project 2: 'You're SO good, can you do discount? You're my favorite!' Like client, give discount. Project 3: bigger discount requested. Pattern?",
                "options": [
                    "Client appreciates work, loyalty discount fair",
                    "LIKING for EXPLOITATION: Nice behavior strategic to create likability → leverage for discounts. Pattern: establish liking (compliments, fun) → small ask → escalate asks. Likability weaponized for financial gain (discounts add up)",
                    "Long-term client deserves discount",
                    "Being favorite is compliment"
                ],
                "correct_answer": 1,
                "explanation": "Likability exploitation pattern: (1) Be extremely nice/fun (create liking), (2) Compliment (ego boost), (3) Leverage likability for progressive asks (discount escalation). Genuine client: respect rates. This client: liking as discount tool."
            },
            {
                "question": "LinkedIn request: shared 15 mutual connections, same industry, engaging profile. Accept, person messages: friendly industry chat, shares valuable article. Weeks later: 'Can I get intro to [your CEO]? Need 15 minutes.' Networking or manipulation?",
                "options": [
                    "Legitimate networking, intro request normal",
                    "STRATEGIC FRIENDING: (1) Mutual connections = trust proxy, (2) Valuable content = reciprocity + likability, (3) Friendly chat = relationship building. Goal from start: access to CEO via YOUR likability bridge. Networking OR manipulation depends on transparency",
                    "Industry networking natural",
                    "Intro request professional courtesy"
                ],
                "correct_answer": 1,
                "explanation": "Strategic vs genuine networking: (1) Strategic: goal-oriented from start (access person), use likability as tool, (2) Genuine: organic relationship, mutual benefit. Red flag: timeline (friendly → immediate ask for high-value intro). Transparency vs manipulation."
            },
            {
                "question": "Gym trainer: attractive, attentive, remembers personal details (birthday, family), checks in via WhatsApp 'How's your day?'. Feel special. Then: push expensive supplement Rp 5 juta/month, personal training package Rp 30 juta. Liking tactics?",
                "options": [
                    "Good customer service, genuine care",
                    "ARTIFICIAL INTIMACY: (1) Attractiveness (physical liking), (2) Personal attention (feel special), (3) Relationship-like behavior (texts, remember details) = create emotional connection. Leverage connection for expensive sales. Professional ≠ friend",
                    "Trainer invested in client success",
                    "Supplement and PT legitimate recommendations"
                ],
                "correct_answer": 1,
                "explanation": "Liking via artificial intimacy: blur professional/personal boundaries (texts, birthday) to create friendship illusion. Feel 'cared for' → likability → compliance with expensive purchases. Genuine trainer: professional boundaries, unbiased recommendations."
            },
            {
                "question": "Teman kantor: daily lunch together 6 months, close friendship. Tiba-tiba: 'I'm joining this investment, let's invest together! More fun with friend!' Invest Rp 50 juta together. Investment scam. Friend knew? Liking exploitation?",
                "options": [
                    "Friend also victim, genuine invitation",
                    "AMBIGUOUS: Possibly (1) Friend victim, shares 'opportunity' with good intention, OR (2) Recruited by MLM/scheme, targets friends for commission. Both cases: friendship exploited (likability → trust → investment without due diligence)",
                    "Friends invest together commonly",
                    "Investment risk shared better"
                ],
                "correct_answer": 1,
                "explanation": "Friendship-based investment risk: (1) If friend recruited by MLM/pyramid: trained target friends (liking = sales tool), (2) If friend genuine: still likability bias (trust friend → skip due diligence). Both cases: friendship clouds judgment, enables scam."
            }
        ],
        "points": 200,
        "tips": ["Genuine relationship: no agenda. Manufactured: strategic friendliness toward goal", "Liking bias: harder to say no to people we like", "Separate person from proposition - evaluate objectively"],
        "real_case_reference": "MLM friendship exploitation, romance scams, sales manipulation Indonesia 2020-2024",
        "time_limit_seconds": 420,
        "created_at": datetime.now(timezone.utc)
    })
    
    # SCARCITY - 10 soal
    challenges.append({
        "id": str(uuid.uuid4()),
        "title": "Scarcity Tactics: Fake Urgency & Limited Availability",
        "category": "indonesian_case",
        "difficulty": "intermediate",
        "cialdini_principle": "scarcity",
        "challenge_type": "multi_choice",
        "description": "10 kasus scarcity manipulation - dari fake stock limits sampai time pressure tactics",
        "scenario": "Scarcity principle: orang menghargai yang langka/terbatas. Scammers create false scarcity via fake countdowns, limited slots, manufactured urgency.",
        "questions": [
            {
                "question": "E-commerce: 'Flash Sale! Harga Rp 100K → Rp 50K! Stok: 3 tersisa! Timer: 04:58!' Refresh page: Timer reset 04:58, stok still 3. Next hour: same. Scarcity real?",
                "options": [
                    "Flash sale repeating, stock continuously replenished",
                    "FAKE SCARCITY: Timer reset (loop), stok always '3' (static) = fake urgency. Real scarcity: timer counts down to zero, stock depletes. Purpose: trigger panic buying without actual limitation",
                    "Technical glitch displaying timer",
                    "Warehouse system slow update stock"
                ],
                "correct_answer": 1,
                "explanation": "Fake scarcity detection: (1) Timer reset (refresh = restart), (2) Stock static (always '3 remaining'), (3) Repeats indefinitely. Real scarcity: timer end → sale end, stock → 0. Fake = psychological manipulation, no actual limit."
            },
            {
                "question": "Webinar registration: 'Only 50 slots! 200 people trying to register!' Join link: instant acceptance, no waitlist. Check 1 hour later: still '50 slots, 200 trying to register'. Slot limit real?",
                "options": [
                    "Slots limit technical, some failed payments",
                    "FAKE SLOT LIMIT: Instant acceptance (no real limit), message unchanged hours later (static '50 slots') = manufactured urgency. Real limitation: would hit capacity, show waitlist, or close registration",
                    "Registration system high capacity",
                    "Virtual webinar unlimited seats"
                ],
                "correct_answer": 1,
                "explanation": "False scarcity: (1) Claim 'only 50 slots', (2) Instant acceptance (no queue), (3) Message never changes = not tracking real numbers. Purpose: urgency for registration. Virtual webinar: essentially unlimited capacity, '50 slots' is lie."
            },
            {
                "question": "Course: 'Early Bird Rp 1 juta (normal Rp 5 juta)! Ends tonight!' Check course history (Wayback Machine): 'Early Bird' price for 2 years straight, never changed to Rp 5 juta. Scarcity tactic?",
                "options": [
                    "Course perpetually in early bird phase",
                    "PERMANENT 'LIMITED-TIME' OFFER: 'Early bird' implies temporary discount. Reality: Rp 1 juta is regular price, Rp 5 juta is fake 'original price' never charged. False urgency (ends tonight) + false discount = scarcity manipulation",
                    "Course continuously recruiting new cohorts",
                    "Early adopters get better price"
                ],
                "correct_answer": 1,
                "explanation": "Fake deadline scarcity: 'ends tonight' repeated indefinitely (check history: always 'ending soon'). Real price Rp 1 juta, fake 'original' Rp 5 juta (never actual). Tactic: urgency + fear of missing out (FOMO), but no real expiration."
            },
            {
                "question": "Investment opportunity: 'Only 10 investors accepted! Already 7 committed, 3 slots left! Decide within 24 hours or lose opportunity!' No verifiable info on other 7 investors. Scarcity authentic?",
                "options": [
                    "Limited partners common in private investment",
                    "MANUFACTURED SCARCITY: (1) Unverifiable claim ('7 committed' = no proof), (2) Arbitrary number ('only 10'), (3) 24-hour pressure = prevent due diligence. Real scarce investment: verifiable investor list, legitimate reason for limit",
                    "Private investment requires confidentiality",
                    "24 hours sufficient for decision"
                ],
                "correct_answer": 1,
                "explanation": "Investment scarcity red flags: (1) Unverifiable claims ('7 investors' no proof), (2) Arbitrary limits (why 10?), (3) Extreme urgency (24h prevent research). Legitimate limited investment: verifiable, rational capacity limit, reasonable timeline."
            },
            {
                "question": "Property: 'Grand Opening! First 20 buyers dapat discount 30%! Sudah 18 sold today, tinggal 2 unit!' Sales office empty, no other buyers visible. Verify scarcity claim how?",
                "options": [
                    "Other buyers might visit different times",
                    "VERIFY: (1) Request proof (sales data, notary records), (2) Check developer reputation & past projects, (3) Visit multiple times (if always '2 units left' = fake). Empty office despite 'sold 18 today' = suspicious",
                    "Buyers might finish transaction already",
                    "Developer offer legitimate"
                ],
                "correct_answer": 1,
                "explanation": "Property false scarcity: (1) '18 sold today' but empty office (inconsistency), (2) Always '2 units left' (visit multiple days = static), (3) Can't verify buyers. Real scarcity: visible buyer activity, verifiable sales data, notary records."
            },
            {
                "question": "Online course: 'Bonus: free 1-on-1 mentoring (worth Rp 10 juta) if buy today! Tomorrow bonusmenghilang!' Check course website 1 week later: same bonus, same 'today only' message. Tactic?",
                "options": [
                    "Bonus available for all new enrollments",
                    "PERPETUAL 'TODAY ONLY': Message 'today only' but repeats daily (check: still there weeks later) = false deadline. Bonus likely included always (or minimal cost to provider). Purpose: artificial urgency for impulsive purchase",
                    "Course continuously enrolling, bonus ongoing",
                    "Mentoring bonus valuable regardless"
                ],
                "correct_answer": 1,
                "explanation": "False deadline: 'today only' / 'tomorrow gone' but repeats indefinitely (verify: check multiple days, same message). Real limited bonus: actually expires, removed after deadline. Perpetual urgency = manipulation tactic."
            },
            {
                "question": "Membership gym: 'New Year promo: Rp 500K/year (normal Rp 2 juta)! Promo ends January 31!' Check February, March, April: same 'promo' price Rp 500K, same 'normal Rp 2 juta' claim. Annual pricing?",
                "options": [
                    "Gym extends promo due to low enrollment",
                    "FAKE ORIGINAL PRICE: Rp 500K is regular price (always charged), Rp 2 juta is fake 'original' (never actual). 'Promo' creates discount illusion + urgency. Real price Rp 500K year-round, scarcity fabricated",
                    "Fitness industry competitive pricing",
                    "January promo extended for members"
                ],
                "correct_answer": 1,
                "explanation": "Fake original price scarcity: (1) 'Promo' never ends (same price year-round), (2) 'Normal' price never charged (Rp 2 juta fake), (3) Create urgency (ends Jan 31) but extends indefinitely. Real price: Rp 500K always."
            },
            {
                "question": "Suplemen: 'Stok terbatas! Bahan import hanya datang setahun sekali!' Check shipping: continuous in-stock, orders fulfilled daily for months. Import scarcity consistent with availability?",
                "options": [
                    "Large initial import order lasts months",
                    "INCONSISTENT SCARCITY CLAIM: 'Import once/year' but always in stock, ship daily for months = not scarce. Real scarcity: stock-outs, delays, pre-orders. Claim 'limited' while constantly available = manufactured urgency for sales",
                    "Efficient inventory management",
                    "High quality import justifies claim"
                ],
                "correct_answer": 1,
                "explanation": "Scarcity claim verification: observe availability over time. Claim 'limited' but consistently in stock = false scarcity. Real supply constraint: periodic stock-outs, pre-orders, wait times. Continuous availability contradicts 'scarce' claim."
            },
            {
                "question": "Event ticket: 'Last 100 tickets! Selling fast!' Purchase link: no queue, instant checkout. 1 week later: 'Last 100 tickets!' still. Event capacity online: 5000. Ticket scarcity?",
                "options": [
                    "Batch release, last 100 of current batch",
                    "FALSE 'LAST' TICKETS: (1) 'Last 100' unchanged for week (static), (2) Event capacity 5000 (100 is tiny fraction), (3) Instant purchase (no demand pressure). Not last, just sales urgency tactic",
                    "Organizer releases tickets in waves",
                    "Last 100 before price increase"
                ],
                "correct_answer": 1,
                "explanation": "Fake 'last tickets' tactic: (1) 'Last X' unchanged extended period, (2) Large capacity venue (5000 >> 100), (3) No actual purchase difficulty. Real scarcity: sold out sections, price increases, queue to buy. Constant 'last' = fake urgency."
            },
            {
                "question": "Cryptocurrency: 'ICO ending in 48 hours! Limited supply 1 million tokens!' Check smart contract (blockchain): supply adjustable, no hard cap coded. Scarcity claim verifiable?",
                "options": [
                    "ICO end date creates legitimate deadline",
                    "FAKE TOKEN SCARCITY: Claim '1 million limit' but smart contract allows supply increase (no hard cap) = not scarce. Real scarcity: hard-coded supply limit in contract. Blockchain transparency allows verification - always check contract, not just marketing",
                    "Token supply managed by team post-ICO",
                    "Deadline for ICO participation real"
                ],
                "correct_answer": 1,
                "explanation": "Crypto scarcity verification: (1) Read smart contract (public on blockchain), (2) Check for hard supply cap (coded limit), (3) If no cap or adjustable = not scarce despite marketing claims. ICO deadline real, but token supply scarcity often fabricated."
            }
        ],
        "points": 200,
        "tips": ["Verify scarcity claims: check over time (does 'limited' ever run out?)", "Fake scarcity: static counters, perpetual 'last chance', always available", "Real scarcity: depletes, causes wait times, verifiable constraints"],
        "real_case_reference": "E-commerce, course, property, event false scarcity tactics Indonesia 2020-2024",
        "time_limit_seconds": 420,
        "created_at": datetime.now(timezone.utc)
    })
    
    # Additional challenges untuk reach 30+ total
    # More Indonesian-specific cases
    challenges.append({
        "id": str(uuid.uuid4()),
        "title": "Pinjol Predatory Practices Deep Dive",
        "category": "indonesian_case",
        "difficulty": "advanced",
        "cialdini_principle": "reciprocity",
        "challenge_type": "multi_choice",
        "description": "10 red flags dan manipulation tactics dalam pinjaman online Indonesia",
        "scenario": "Pinjol (pinjaman online) di Indonesia banyak yang ilegal dan predatory. Kenali taktik manipulation untuk menghindari debt trap.",
        "questions": [
            {
                "question": "Pinjol app permissions: akses kontak, SMS, foto, lokasi, camera, microphone. Alasan: 'verifikasi identitas'. Permission level reasonable?",
                "options": [
                    "Digital lending butuh data comprehensive",
                    "EXCESSIVE PERMISSIONS: Legitimate verification need: KTP photo (camera OK), location basic. NOT need: all contacts (for harassment), SMS (read private data), microphone. Illegal pinjol harvest data for threats",
                    "Fintech standard practice",
                    "Anti-fraud measure"
                ],
                "correct_answer": 1,
                "explanation": "Pinjol permission red flags: (1) All contacts = harvest untuk harass (SMS terror ke family/friends), (2) SMS read = blackmail material (private conversations), (3) Photos = steal for fake accounts. Legitimate: KTP scan only, basic location."
            },
            {
                "question": "Pinjol: 'Bunga 0%, biaya admin 20% (satu kali)'. Loan Rp 1 juta, terima Rp 800K (potong Rp 200K admin). Tenor 1 bulan. Effective APR berapa?",
                "options": [
                    "0% karena tidak ada bunga",
                    "240% APR: Bayar Rp 1 juta untuk terima Rp 800K = Rp 200K fee / Rp 800K principal = 25% dalam 1 bulan = 25% × 12 = 300% YEARLY, bukan 0%",
                    "20% admin fee transparently disclosed",
                    "Satu kali charge, not recurring"
                ],
                "correct_answer": 1,
                "explanation": "Pinjol math trick: claim '0% bunga' but massive upfront fee. Reality: borrow Rp 800K (received), repay Rp 1 juta = 25% cost in 1 month. Annualized (APR): 25% × 12 = 300% APR. Legal limit Indonesia: 0.8%/day = ~292% APR max (often violated)."
            },
            {
                "question": "Pinjol late payment: day 1 overdue, get 50 SMS to all contacts: 'YourName hutang, kontak segera!' WhatsApp family: 'YourName penipuan!'. Legal debt collection?",
                "options": [
                    "Urgent debt collection measure",
                    "ILLEGAL HARASSMENT: AFPI (debt collector association) code: (1) No contact third parties (family, friends, colleagues), (2) Max 1 contact/day to borrower, (3) Cannot accuse 'penipuan' publicly. This violates all rules - report to OJK",
                    "Debt collection standard practice",
                    "Borrower at fault for late payment"
                ],
                "correct_answer": 1,
                "explanation": "Legal debt collection Indonesia (AFPI code): (1) Contact borrower only (not third parties), (2) Max frequency 1/day, no harassment, (3) Cannot defame (call 'penipuan'). Illegal pinjol: mass SMS, harass family, public shaming. Report: OJK hotline 157."
            },
            {
                "question": "Pinjol registration: tidak ada proses interview, tidak cek slip gaji, tidak cek pekerjaan. Instant approval Rp 10 juta limit dalam 5 minutes. Red flag?",
                "options": [
                    "AI-powered instant approval modern fintech",
                    "RED FLAG: No creditworthiness check = likely illegal/predatory. Legal lender: verify income (slip gaji, tax, bank statement), employment, credit score. Instant large limit without verification = debt trap, expect predatory terms",
                    "Data-driven approval algorithm",
                    "Competitive lending market"
                ],
                "correct_answer": 1,
                "explanation": "Legitimate lending: verify repayment ability (income, employment, debt-to-income ratio). Instant approval high limit without checks = red flag for predatory lending. Goal: get people in debt regardless of ability to repay, then harass for payment."
            },
            {
                "question": "Pinjol app not in Play Store/App Store, download via APK link dari website/WhatsApp. Company address: ruko alamat tidak jelas. Risk level?",
                "options": [
                    "Alternative distribution channel",
                    "HIGH RISK ILLEGAL: (1) Not in official app store = not vetted, likely malware/data theft, (2) APK install = bypass security, can access all phone data, (3) Unclear address = unregistered, illegal operation. Only use OJK-registered pinjol",
                    "Lower overhead, cheaper interest",
                    "Direct download faster"
                ],
                "correct_answer": 1,
                "explanation": "Illegal pinjol markers: (1) Not in app store (Play Store/App Store vet apps), (2) APK install (full phone access, malware risk), (3) No clear address (unregistered). Legal pinjol: (a) OJK registered (check list), (b) In official app stores."
            },
            {
                "question": "Cicilan Rp 1 juta loan jadi Rp 1.5 juta (tenor 1 bulan). Telat 1 hari: denda Rp 500K. Total bayar Rp 2 juta untuk pinjam Rp 1 juta (30 days late). Denda legal?",
                "options": [
                    "Denda late payment standar practice",
                    "EXCESSIVE PENALTY: Rp 500K denda untuk 1 hari = Rp 500K/30 hari = Rp 16.6K per hari = 1.66% daily. OJK maksimal denda: 0.8% daily. Ini DOUBLE legal limit. Predatory, report OJK",
                    "Penalty discourages late payment",
                    "Borrower agreed to terms"
                ],
                "correct_answer": 1,
                "explanation": "OJK regulation: max interest + fee = 0.8% per day. Example: Rp 500K penalty/30 days = 1.66% daily (exceeds limit). Legal max for Rp 1M loan/30 days: Rp 1M × 0.8% × 30 = Rp 240K total. Anything above = illegal, report."
            },
            {
                "question": "Pinjol offer perpanjang tenor: 'Can't pay Rp 1.5 juta? Pay Rp 500K now, extend 1 month (new total Rp 2 juta).' Month 2: 'Extend again? Pay Rp 500K, new total Rp 2.5 juta.' Debt trajectory?",
                "options": [
                    "Flexible repayment help borrower",
                    "DEBT SPIRAL: Each extension add interest + fee. Original Rp 1M → Rp 1.5M → Rp 2M → Rp 2.5M in 3 months. Paying small amounts just covers fees, principal untouched. TRAP: debt grows, never reduce. Better: negotiate settlement",
                    "Installment plan reasonable",
                    "Avoid default pada credit score"
                ],
                "correct_answer": 1,
                "explanation": "Debt trap mechanism: extension payments cover interest/fees, principal unchanged. Each extension adds cost. Example: Rp 1M loan → Rp 2.5M after 3 months (150% increase). Designed to never pay off. Escape: (1) OJK mediation, (2) Full settlement negotiation."
            },
            {
                "question": "Pinjol term: 'Settle full Rp 3 juta (principal Rp 1M + interest Rp 2M) or legal action'. Check: app not OJK registered, collector not certified. Can they sue?",
                "options": [
                    "Legal threat enforces contract",
                    "EMPTY THREAT: Illegal pinjol (not OJK registered) cannot sue - court would expose illegal operation. Uncertified collector = illegal (AFPI registration required). Threat is intimidation only. Action: report to OJK, police (illegal lending)",
                    "Contract still binding",
                    "Court enforces debt regardless"
                ],
                "correct_answer": 1,
                "explanation": "Illegal pinjol lawsuit impossibility: (1) Court requires legitimate business (OJK registration) - illegal pinjol cannot prove standing, (2) Excessive interest (> OJK limit) unenforceable, (3) Harassment evidence used AGAINST pinjol. Threat = bluff."
            },
            {
                "question": "Pinjol marketing: celebrity endorsement (influencer popular), testimonial 'Helped me in emergency!', app rating 4.5 stars (10K reviews). Trust indicators?",
                "options": [
                    "Celebrity endorsement and reviews show trustworthiness",
                    "FAKE TRUST SIGNALS: (1) Celeb endorsers paid, not verify legitimacy, (2) Testimonials can be fake/paid, (3) App ratings bought (review farms). ONLY trust indicator: OJK registration (check official list). Ignore social proof for financial products",
                    "4.5 stars rating high quality",
                    "Testimonials from real users"
                ],
                "correct_answer": 1,
                "explanation": "Pinjol trust verification: IGNORE social proof (celebs, reviews, testimonials) - all can be fabricated. ONLY check: (1) OJK registered fintech list (official website), (2) Company legal entity (Kemenkumham database), (3) Clear address/contact. Reviews/endorsements = marketing, not legitimacy."
            },
            {
                "question": "Sudah pinjam 5 pinjol berbeda (total Rp 5 juta), dapat offer pinjol baru: 'Consolidate debt! Pinjam Rp 5 juta, bayar all 5 pinjol, only owe us!' Interest higher than average of 5 pinjol. Good deal?",
                "options": [
                    "Debt consolidation simplifies repayment",
                    "FALSE CONSOLIDATION: Trading 5 debts for 1 bigger debt with HIGHER interest = worse situation. Real consolidation: LOWER interest (e.g. bank personal loan). This: debt remains, higher cost, still owe same/more. Trap: simplicity illusion, worse terms",
                    "Single payment easier to manage",
                    "Avoid multiple collection calls"
                ],
                "correct_answer": 1,
                "explanation": "Fake consolidation trap: (1) New loan higher interest than average = worse, not better, (2) Total debt unchanged or increased, (3) 'Simplicity' marketed, but economics worse. Real consolidation: lower rate (bank), reduce total cost, mathematical benefit."
            }
        ],
        "points": 250,
        "tips": ["Check OJK registered fintech list (official only)", "Legal max: 0.8% per day", "Excessive permissions = data theft/harassment tool", "Report illegal: OJK 157 hotline"],
        "real_case_reference": "Pinjol illegal practices reported to OJK, police cases 2020-2024 Indonesia",
        "time_limit_seconds": 480,
        "created_at": datetime.now(timezone.utc)
    })
    
    print(f"Created {len(challenges)} new challenges")
    
    # Insert all
    if challenges:
        await db.challenges.insert_many(challenges)
        print(f"✅ Seeded {len(challenges)} challenges successfully")
    
    # Summary
    total = await db.challenges.count_documents({})
    print(f"\n📊 TOTAL CHALLENGES IN DATABASE: {total}")
    
    for principle in ["reciprocity", "commitment", "social_proof", "authority", "liking", "scarcity"]:
        count = await db.challenges.count_documents({"cialdini_principle": principle})
        print(f"  - {principle.title()}: {count} challenges")

if __name__ == "__main__":
    asyncio.run(seed_complete_challenges())
