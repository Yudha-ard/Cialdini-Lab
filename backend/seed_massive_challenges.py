import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
import uuid
from datetime import datetime, timezone

mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ.get('DB_NAME', 'tegalsec_lab')]

async def seed_massive_challenges():
    print("🚀 Seeding massive challenges dengan 10-20 soal per challenge...")
    
    # Don't delete, just add more
    challenges = [
        # RECIPROCITY - Deep Dive Challenge
        {
            "id": str(uuid.uuid4()),
            "title": "Master Class: Reciprocity Attack Patterns",
            "category": "indonesian_case",
            "difficulty": "advanced",
            "cialdini_principle": "reciprocity",
            "challenge_type": "multi_choice",
            "description": "Master-level challenge covering 15 reciprocity attack scenarios dari basic sampai advanced",
            "scenario": "Anda adalah Security Analyst di perusahaan fintech Indonesia. Dalam 30 hari terakhir, 15 karyawan melaporkan berbagai serangan social engineering. Task Anda: identifikasi reciprocity manipulation di setiap case.",
            "questions": [
                {
                    "question": "Case 1: Free VPN Trial - User install 'SecureVPN Pro' dengan free trial 7 hari. Hari ke-8, charged Rp 500K tanpa notif jelas. Cancel button di-hide 5 layer deep di menu. Reciprocity manipulation:",
                    "options": [
                        "Tidak ada, user dapat free trial legitimate",
                        "Free trial create obligation, auto-charge tanpa consent + hidden cancel = exploit reciprocity + dark pattern",
                        "User lupa cancel, kesalahan sendiri",
                        "Harga Rp 500K wajar untuk VPN"
                    ],
                    "correct_answer": 1,
                    "explanation": "Free trial psychological effect: user merasa 'dapat gratis', jadi feel obligated continue atau minimal tidak protes. Dikombinasi auto-charge tanpa clear consent + hidden cancel = exploit reciprocity principle for revenue."
                },
                {
                    "question": "Case 2: Webinar 'Gratis' - Marketing webinar 'Free Social Media Marketing Masterclass'. Di akhir: 'Terima kasih sudah hadir! Special offer course Rp 5 juta (discount 80%) hanya untuk attendees. Tersisa 3 slot!' Pattern reciprocity:",
                    "options": [
                        "Genuine offer, tidak ada manipulation",
                        "Free webinar create obligation untuk 'return favor' dengan beli course. Urgency (3 slot) + discount as 'gift' reinforce reciprocity",
                        "Webinar memang valuable, course worth it",
                        "Attendees free pilih beli atau tidak"
                    ],
                    "correct_answer": 1,
                    "explanation": "Classic reciprocity sales funnel: free valuable content → feel indebted → pressure to buy. 'Special offer for attendees' framed as exclusive gift (reciprocity amplifier). Urgency prevent critical thinking."
                },
                {
                    "question": "Case 3: Beta Tester 'Rewards' - Startup app: 'Jadi beta tester, dapat Rp 100K e-wallet!' After testing 2 bulan, bugs galore, reward belum dibayar. Follow up: 'Reward delayed, tapi kamu sudah invest waktu, sayang kalau stop sekarang.' Reciprocity trap:",
                    "options": [
                        "Startup genuine, reward akan dibayar eventually",
                        "Bait with reward (anticipated reciprocity) → sunk cost fallacy + reciprocity = continue testing despite no payment",
                        "2 bulan testing tidak lama",
                        "Beta testing adalah volunteer work"
                    ],
                    "correct_answer": 1,
                    "explanation": "Anticipated reciprocity: promise of reward create obligation. When reward tidak materialize, sunkcost + 'you already invested' guilt trip  = continue unpaid labor. Exploitation of reciprocity + commitment."
                },
                {
                    "question": "Case 4: Influencer 'Gifting' - Brand kirim free product (worth Rp 2 juta) ke influencer micro (5K followers). Email: 'No obligation to post, but if you like it, we'd love a review!' Influencer post positive review. Reciprocity dynamic:",
                    "options": [
                        "Influencer genuinely likes product, review adalah honest",
                        "Free expensive gift create powerful reciprocity obligation. 'No obligation' is false - psychological pressure to reciprocate with positive review",
                        "Micro-influencer lucky dapat free product",
                        "Brand marketing strategy yang fair"
                    ],
                    "correct_answer": 1,
                    "explanation": "High-value gift (Rp 2 juta) to low-follower influencer = disproportionate reciprocity pressure. 'No obligation' legally safe but psychologically manipulative - influencer feel must reciprocate. Review likely biased by gift, not genuine."
                },
                {
                    "question": "Case 5: Free Sample 'Tester' - Mall promo: 'Free sample perfume!' Setelah spray di tangan, promoter: 'Wanginya cocok! Kebetulan lagi promo, dari Rp 800K jadi Rp 400K. Mau beli?' Reciprocity pressure point:",
                    "options": [
                        "Sample memang gratis, tidak ada pressure",
                        "Free sample create immediate obligation. Physical touch (spray di tangan) + personal compliment + on-spot pressure = reciprocity amplified",
                        "Discount 50% adalah benefit genuine",
                        "Customer bebas walk away"
                    ],
                    "correct_answer": 1,
                    "explanation": "Face-to-face + free sample = reciprocity obligation. Spray langsung di tangan (vs test strip) = personal investment (sample 'consumed'). Immediate ask prevent escape. Social pressure (reject = rude) amplify compliance."
                },
                {
                    "question": "Case 6: Charity 'Emotional Investment' - Door-to-door fundraiser: 'Saya volunteers untuk anak yatim. Bisa donate Rp 50K?' After reject: 'Rp 20K saja?' Then: 'Rp 10K untuk satu anak makan?' Reciprocity technique:",
                    "options": [
                        "Fundraiser persistent tapi legitimate cause",
                        "Door-to-door reciprocity (time invested) + rejection-then-retreat technique (Rp 50K → 10K) = feel obligated agree to smaller ask",
                        "Charity cause justify any persuasion method",
                        "Rp 10K adalah amount kecil"
                    ],
                    "correct_answer": 1,
                    "explanation": "Rejection-then-retreat: start high (Rp 50K), retreat to low (Rp 10K) = concession. Reciprocity dictate: they 'gave up' their ask, you should 'give up' your resistance. Door-to-door = time investment = obligation."
                },
                {
                    "question": "Case 7: SaaS Free Trial Auto-Upgrade - Business tool free trial: 'Unlimited users, all features 14 days!' Day 10: 'Your team loves it! Upgrade now for 20% lifetime discount!' Day 14: Auto-charge Rp 10 juta annual plan. Reciprocity exploitation level:",
                    "options": [
                        "Standard SaaS practice, transparent pricing",
                        "Team invested time (setup, training) + free full features = strong reciprocity + sunk cost. Auto-charge + urgency discount = coerced commitment",
                        "Business decision, ROI calculation possible",
                        "Rp 10 juta reasonable untuk enterprise tool"
                    ],
                    "correct_answer": 1,
                    "explanation": "Unlimited trial = maximum feature exposure = maximum investment. Team training + data migration = sunk cost. Auto-charge exploit: user busy, forget to cancel. Reciprocity + sunk cost + urgency = low resistance purchase."
                },
                {
                    "question": "Case 8: Scholarship 'String Attached' - Bootcamp offer: 'Full scholarship Rp 30 juta! Only condition: work at our partner company 2 years with salary Rp 5 juta/month (market rate: Rp 12 juta).' Reciprocity trap analysis:",
                    "options": [
                        "Fair exchange, scholarship worth commitment",
                        "Disguised debt bondage via reciprocity. 'Scholarship' = Rp 30 juta, but salary underpay Rp 7 juta/month × 24 months = Rp 168 juta total loss",
                        "Work experience valuable, not just salary",
                        "Legal contract, student choice"
                    ],
                    "correct_answer": 1,
                    "explanation": "Reciprocity as exploitation: 'free' scholarship create massive obligation. Salary Rp 5 juta vs market Rp 12 juta = Rp 7 juta/month underpay × 24 = Rp 168 juta loss for Rp 30 juta 'scholarship'. Math: student pays 5.6× scholarship value."
                },
                {
                    "question": "Case 9: Credit Card 'Welcome Bonus' - Bank: 'Apply card, dapat welcome bonus Rp 500K!' Hidden: annual fee Rp 500K/year, interest 2.95%/month on balance. Bonus require Rp 5 juta spending in 3 months. Reciprocity bait mechanics:",
                    "options": [
                        "Bonus Rp 500K is genuine reward",
                        "Bonus = reciprocity bait. Force Rp 5 juta spending (likely debt) + hidden fees > bonus value. Reciprocity create loyalty despite negative economics",
                        "Credit card benefits legitimate",
                        "Consumers can spend responsibly"
                    ],
                    "correct_answer": 1,
                    "explanation": "Bonus hook: Rp 500K seems free, but force spending Rp 5 juta (may cause debt). Annual fee Rp 500K = bonus neutral. Interest 2.95%/month (42.4% APR) on induced debt = massive profit for bank. Reciprocity create brand loyalty."
                },
                {
                    "question": "Case 10: MLM 'Mentor' Investment - MLM upline: 'I'll personally mentor you, share my secrets, help you succeed! Just invest Rp 10 juta starter pack.' After join: mentor unavailable, generic training only, no personal help. Reciprocity manipulation pattern:",
                    "options": [
                        "Mentor genuine offer, business requires investment",
                        "False reciprocity promise: 'personal mentorship' create obligation. Reality: transactional (upline profit from downline buy). Mentorship tidak delivered post-purchase",
                        "MLM model requires patience",
                        "Starter pack has actual product value"
                    ],
                    "correct_answer": 1,
                    "explanation": "Personal relationship false promise: 'I'll personally help you' = reciprocity obligation (you owe me for my time). Reality: transactional - upline only profit from sales. Post-purchase: mentorship ghost. Investment Rp 10 juta >> value received."
                },
                {
                    "question": "Case 11: Insurance Agent 'Free Financial Planning' - Agent: 'Free financial health check, no obligation!' After 2-hour meeting with detailed analysis: 'You need insurance Rp 500K/month for 20 years to secure family.' Reciprocity psychology:",
                    "options": [
                        "Free consultation valuable, insurance recommendation genuine",
                        "2 hours 'free' time create reciprocity debt. Agent invested significant effort, rude to not buy. Recommendation may be biased by commission incentive",
                        "Financial planning legitimately shows insurance need",
                        "Customer can still walk away"
                    ],
                    "correct_answer": 1,
                    "explanation": "Time investment reciprocity: 2 hours detailed analysis = significant 'gift'. Psychologically awkward to reject after agent invested time. Recommendation bias: commission on insurance > genuine need. Social pressure (face-to-face) amplify."
                },
                {
                    "question": "Case 12: Gym Membership 'Trial + Personal Training' - Gym: 'Free 1-day pass + free personal training session!' After workout, trainer: 'Great session! I see your potential. Special offer: 1-year membership + 10 PT sessions = Rp 8 juta.' Reciprocity stacking:",
                    "options": [
                        "Gym trial normal marketing, trainer genuine",
                        "Double reciprocity: free pass + free 1-on-1 PT (high value service) = strong obligation. On-spot pressure post-workout (endorphins + tired = low resistance)",
                        "Rp 8 juta reasonable for services offered",
                        "Customer evaluated gym, informed decision"
                    ],
                    "correct_answer": 1,
                    "explanation": "Stacked reciprocity: free facility + free personal training (normally expensive) = compound obligation. Post-workout state: endorphins (feel good) + tired (low cognitive resistance). On-spot pressure + social (1-on-1) = high conversion."
                },
                {
                    "question": "Case 13: Freelancer 'Spec Work Trap' - Client: 'Show me sample design first, if I like it, I'll hire you for full project Rp 20 juta.' Freelancer creates custom design. Client: 'Nice, but need revisions. Do this, then we'll talk contract.' After 3 revisions: 'Budget cut, can only pay Rp 5 juta.' Reciprocity exploitation:",
                    "options": [
                        "Client testing skill legitimate, revision normal",
                        "Spec work = free labor disguised as 'opportunity'. Sunk cost (time invested) + reciprocity (client 'considering' you) = accept lowball Rp 5 juta vs walk away with nothing",
                        "Freelancer should have contract upfront",
                        "Rp 5 juta still payment"
                    ],
                    "correct_answer": 1,
                    "explanation": "Spec work trap: 'opportunity' = false reciprocity (client doing favor by considering you). Freelancer invest time/skill for free. Multiple revisions = sunk cost. Final lowball (Rp 5 juta vs Rp 20 juta) accepted due to loss aversion."
                },
                {
                    "question": "Case 14: Marketplace 'Cashback Game' - App: 'Play game, collect points, cashback Rp 50K!' Game requires visit app daily 30 days, watch 20 ads/day. At day 29: 'Cashback pending, verify account (input email friends).' Day 30: 'Cashback Rp 50K issued as voucher min. purchase Rp 500K.' Reciprocity deception:",
                    "options": [
                        "Game adalah fun, cashback bonus",
                        "Time investment 30 days + 600 ads watched = reciprocity obligation to platform. Cashback 'bait' become voucher (must spend Rp 500K) = not real benefit",
                        "Voucher still has value",
                        "User voluntarily participate"
                    ],
                    "correct_answer": 1,
                    "explanation": "Gamification reciprocity: 30 days × 20 ads = 600 ads watched (revenue for platform). Time investment (sunk cost) + anticipation (almost there!) = complete task. Bait-and-switch: Rp 50K cash → voucher min. Rp 500K = forced spending."
                },
                {
                    "question": "Case 15: Course 'Money Back Guarantee' - Online course Rp 3 juta: '30-day money back guarantee, risk-free!' After 2 weeks learning: 'Complete all modules (50 videos, 100 exercises) within 30 days for full refund.' User spend 20+ hours, can't complete in time. Reciprocity + sunk cost combination:",
                    "options": [
                        "Guarantee is legitimate, user didn't meet terms",
                        "False 'risk-free': require impossible time commitment (50 videos + 100 exercises in 30 days). Time invested (20 hours) = sunk cost + reciprocity to platform. User unlikely request refund",
                        "Course content valuable despite terms",
                        "User should have checked requirements"
                    ],
                    "correct_answer": 1,
                    "explanation": "False guarantee: 'risk-free' implies easy refund. Reality: unrealistic completion requirement (impossible for working adults). Time invested (20 hours watching) = reciprocity + sunk cost. User rationalizes: 'I learned something' to justify not refunding."
                }
            ],
            "points": 300,
            "tips": ["Reciprocity dapat stacked dengan principle lain", "Sunk cost amplifies reciprocity", "Time investment = powerful reciprocity trigger"],
            "real_case_reference": "Compilation of real Indonesian e-commerce, SaaS, MLM, dan digital service manipulations 2020-2024",
            "time_limit_seconds": 600,
            "created_at": datetime.now(timezone.utc)
        },
        
        # COMMITMENT - Deep Dive
        {
            "id": str(uuid.uuid4()),
            "title": "Master Class: Commitment & Consistency Traps",
            "category": "indonesian_case",
            "difficulty": "advanced",
            "cialdini_principle": "commitment",
            "challenge_type": "multi_choice",
            "description": "12-soal deep dive tentang bagaimana commitment awal dieksploitasi untuk manipulasi berkelanjutan",
            "scenario": "Analisa 12 kasus commitment escalation dari small ask ke massive commitment, plus sunk cost fallacy exploitation.",
            "questions": [
                {
                    "question": "Case 1: Investment App Foot-in-Door - App: 'Daftar gratis, invest Rp 10K untuk coba!' After signup: 'Invest Rp 100K dapat bonus 10%!' Then: 'Top investor invest min Rp 10 juta, join mereka!' User already invested Rp 110K. Commitment escalation pattern:",
                    "options": [
                        "Progressive investment normal, user choose each step",
                        "Foot-in-door technique: small commitment (Rp 10K) → medium (Rp 100K + bonus bait) → large ask (Rp 10 juta). Each step use previous commitment to justify next",
                        "Bonus 10% is genuine incentive",
                        "Top investor status aspirational"
                    ],
                    "correct_answer": 1,
                    "explanation": "Classic foot-in-door: start small (Rp 10K barrier minimal), escalate with incentive (bonus), final ask massive (Rp 10 juta). Each step: committed already, 'just one more step' to goal. Bonus: short-term gain mask long-term commitment trap."
                },
                {
                    "question": "Case 2: Subscription Trap - Service: 'Bulan pertama Rp 9.900!' Auto-renew Rp 99K/month. After 3 months (paid Rp 207.900), want cancel. Service: 'Sayang sudah invest 3 bulan, tinggal 3 bulan lagi dapat loyalty reward Rp 300K!' Commitment exploitation:",
                    "options": [
                        "Loyalty reward is valuable retention strategy",
                        "Sunk cost fallacy: spent Rp 207.900, feel obligated continue. 'Loyalty reward' require additional Rp 297K (3 months × Rp 99K) for Rp 300K voucher (net: Rp 3K benefit, but 6 months lock-in)",
                        "Cancel can happen anytime",
                        "3 months not long commitment"
                    ],
                    "correct_answer": 1,
                    "explanation": "Sunk cost exploitation: Rp 207.900 already spent = 'wasted' if cancel. Reward math: spend additional Rp 297K for Rp 300K voucher (likely restricted) = barely break even, but 6 months total lock-in. Commitment + loss aversion manipulated."
                },
                {
                    "question": "Case 3: Goal Setting Trap - Fitness challenge: 'Commit to 100-day transformation! Post daily update!' Day 50: exhausted, want quit. Community: 'You're halfway! Don't waste 50 days progress!' Psychological commitment mechanism:",
                    "options": [
                        "Community support motivates to continue",
                        "Public commitment + progress paradox: 50 days invested + public accountability = strong pressure continue despite diminishing returns. Progress itself trap (halfway = 'too far to quit')",
                        "100 days is reasonable fitness goal",
                        "Quitting is personal choice"
                    ],
                    "correct_answer": 1,
                    "explanation": "Commitment mechanisms: (1) Public declaration (posted daily) = social accountability, (2) Progress paradox: 50% complete = psychologically 'too invested to quit', (3) Community reinforcement = external pressure. Internal motivation replaced by external obligation."
                },
                {
                    "question": "Case 4: Multi-Step Form Dark Pattern - Website checkout: Step 1 (cart) → 2 (shipping) → 3 (payment) → 4 (review) → 5 (insurance add-on Rp 50K) → 6 (warranty Rp 100K) → 7 (final confirm). Each pre-checked. User spent 10 minutes filling. Commitment dark pattern:",
                    "options": [
                        "Steps necessary for transaction security",
                        "Excessive steps = time investment commitment. Add-ons late in process + pre-checked + time sunk = user likely just complete vs restart. Commitment (time) weaponized for revenue",
                        "User can uncheck add-ons",
                        "Insurance and warranty optional"
                    ],
                    "correct_answer": 1,
                    "explanation": "Dark pattern combo: (1) Excessive steps = time commitment, (2) Pre-checked expensive add-ons placed late = cognitive fatigue, (3) Sunk time (10 minutes) = pressure to complete. Likely outcome: user just finish vs critically evaluate Rp 150K add-ons."
                },
                {
                    "question": "Case 5: Pledge Escalation - Crowdfunding: 'Pledge Rp 50K tier!' After campaign ends: 'Thanks! Btw, production delayed, need additional Rp 50K/backer to continue. Your Rp 50K forfeit if we cancel.' Commitment escalation trap:",
                    "options": [
                        "Production delays common, additional fund reasonable",
                        "Initial pledge create commitment. Threat of loss (Rp 50K forfeit) + responsibility guilt (project success depends on you) = pressure pay additional Rp 50K. Total: Rp 100K vs initial Rp 50K",
                        "Crowdfunding is risk understood",
                        "Backers choice to continue"
                    ],
                    "correct_answer": 1,
                    "explanation": "Escalating commitment + loss aversion: Rp 50K pledged = committed. Additional ask with threat (forfeit if not pay) = coerced escalation. Responsibility guilt: 'project fails because of you' (false - creator's issue). Total cost doubles, commitment weaponized."
                },
                {
                    "question": "Case 6: Low-Ball Technique - Car dealer: 'Price Rp 200 juta!' After test drive, paperwork, 2 hours spent: 'Sorry, calculation error, actual price Rp 220 juta plus Rp 15 juta fees.' Time invested + excitement (already imaging ownership). Commitment technique:",
                    "options": [
                        "Honest calculation error, price adjustment transparent",
                        "Low-ball technique: attract with low price, create commitment (test drive, paperwork, 2 hours), then reveal true price. Time + emotional investment = pressure to accept despite 17.5% higher cost",
                        "Rp 15 juta fees legitimate",
                        "Buyer can walk away"
                    ],
                    "correct_answer": 1,
                    "explanation": "Low-ball classic: (1) Initial attractive offer (Rp 200 juta), (2) Create commitment (time + paperwork + emotional attachment - test drive), (3) Reveal true cost (+Rp 35 juta = 17.5% more). Sunk time + emotional attachment = weak resistance."
                },
                {
                    "question": "Case 7: Survey Trap - App: 'Answer 5-minute survey, dapat Rp 20K!' Survey actually 30 minutes, 50 questions. Question 45: 'For reward, must download partner app and subscribe Rp 50K/month.' Already spent 25 minutes. Commitment exploitation:",
                    "options": [
                        "Survey longer than expected, but reward still offered",
                        "Time trap: advertise 5-minute, actually 30-minute = sunk time commitment. Reward requirement (subscribe Rp 50K) hidden at end, after massive time investment = pressure comply to not 'waste' 25 minutes",
                        "Rp 20K reward covers subscription first month",
                        "User can stop survey anytime"
                    ],
                    "correct_answer": 1,
                    "explanation": "Time investment trap: 5-min promise → 30-min reality = sunk 25 minutes at question 45. Hidden requirement (Rp 50K subscription) near end = commitment exploited. Likely decision: subscribe to not waste time. Net: lose Rp 30K for Rp 20K reward."
                },
                {
                    "question": "Case 8: Contest Multiple Entry Fee - Contest: 'Win Rp 100 juta! Entry Rp 50K.' After losing round 1: 'Special offer! Re-enter Rp 40K, higher chance!' Then: 'Final round, Rp 60K entry, guaranteed top 100!' User invested Rp 150K. Commitment escalation:",
                    "options": [
                        "Multiple entries increase winning chance",
                        "Escalating commitment gambling: initial Rp 50K create invested stake. Each subsequent offer exploit sunk cost ('already spent X, might as well continue'). Total Rp 150K for low probability win",
                        "Contest transparent about odds",
                        "Gambling is personal choice"
                    ],
                    "correct_answer": 1,
                    "explanation": "Escalation of commitment + gambling fallacy: each loss → offer re-entry (exploit sunk cost). User rationalizes: 'already spent Rp 150K, next one might win' (gamblers fallacy). Low probability (likely <1%) vs Rp 150K invested = poor math, pure commitment trap."
                },
                {
                    "question": "Case 9: Training Program Installment - Course: 'Pay Rp 1 juta/month for 12 months (total Rp 12 juta).' Month 6 (paid Rp 6 juta): 'Training inadequate, want refund.' Policy: 'No refund after 3 months. Plus you're halfway, sayang waste progress!' Commitment lock-in:",
                    "options": [
                        "No-refund policy standard, user agreed terms",
                        "Installment = gradual commitment, each payment deepens sunk cost. Halfway point = psychological peak ('too invested to quit'). No refund policy + progress guilt = forced completion despite poor quality",
                        "6 months training has some value",
                        "Completion may still benefit"
                    ],
                    "correct_answer": 1,
                    "explanation": "Installment trap: gradual payment feel smaller (Rp 1 juta vs Rp 12 juta), but create incremental commitment. At month 6: sunk Rp 6 juta + halfway = powerful obligation to continue. No-refund policy enforce completion despite quality issues."
                },
                {
                    "question": "Case 10: Identity-Based Commitment - Community: 'Are you a high achiever? Join our elite group!' After join (pay Rp 5 juta membership): 'High achievers invest in themselves. Upgrade Rp 20 juta for mentorship.' Self-image commitment:",
                    "options": [
                        "Mentorship valuable for high achievers",
                        "Identity commitment: label as 'high achiever' create self-image pressure to act consistently. Upgrade ask challenge identity ('if you don't upgrade, you're not really high achiever'). Rp 5 juta sunk + identity pressure = comply",
                        "Elite membership has exclusive benefits",
                        "Rp 20 juta investment self-determined"
                    ],
                    "correct_answer": 1,
                    "explanation": "Identity-based commitment strongest form: 'high achiever' label → internal pressure to act consistently with identity. Upgrade framed as identity-congruent ('high achievers invest'). Reject = threaten self-image. Rp 5 juta sunk + identity = powerful compliance tool."
                },
                {
                    "question": "Case 11: Relationship Commitment Exploitation - Dating app premium: 'Find soulmate! Premium Rp 100K/month.' After 6 months (Rp 600K), match minimal. 'Upgrade Rp 300K/month for AI matching!' User invested 6 months time + Rp 600K. Commitment compound:",
                    "options": [
                        "AI matching may improve results",
                        "Time + money sunk (6 months + Rp 600K) = double commitment. Hope for soulmate (emotional investment) + sunk cost → pressure upgrade despite poor results. Emotional + financial commitment compound",
                        "Dating requires patience",
                        "Rp 300K/month for potential love reasonable"
                    ],
                    "correct_answer": 1,
                    "explanation": "Compound commitment: (1) Time invested (6 months searching), (2) Money (Rp 600K), (3) Emotional (hope for relationship). Triple commitment  = strong obligation continue. Upgrade exploit this: 'already invested so much, upgrade might work'."
                },
                {
                    "question": "Case 12: Written Commitment Weaponized - Multi-level business: 'Sign this: I commit to achieve Rp 50 juta income in 1 year!' After sign, performance poor. Upline: 'You signed commitment! Are you giving up on your word? Invest Rp 5 juta more for success!' Written commitment psychology:",
                    "options": [
                        "Written goal increases accountability and motivation",
                        "Written commitment weaponized: signature = public/permanent commitment. Underperformance questioned as character flaw ('giving up on word'). Pressure invest more money to preserve self-image of 'person who keeps commitments'",
                        "Goal setting is effective strategy",
                        "Rp 5 juta investment may turn business around"
                    ],
                    "correct_answer": 1,
                    "explanation": "Written commitment = most powerful form (permanent, public). When fail, upline weaponize: frame as character issue ('Are you quitter?') not business model issue. Signature psychological weight = pressure invest more despite evidence of failing model."
                }
            ],
            "points": 240,
            "tips": ["Commitment strongest when: public, written, active (not passive)", "Sunk cost fallacy amplifier", "Identity-based commitment = most powerful"],
            "real_case_reference": "MLM, Ponzi schemes, subscription traps, dan contest scams Indonesia 2020-2024",
            "time_limit_seconds": 480,
            "created_at": datetime.now(timezone.utc)
        }
    ]
    
    # Insert challenges
    if challenges:
        await db.challenges.insert_many(challenges)
        print(f"✅ Seeded {len(challenges)} massive challenges dengan soal banyak")
    
    # Print summary
    total_challenges = await db.challenges.count_documents({})
    print(f"\n📊 Total challenges in database: {total_challenges}")

if __name__ == "__main__":
    asyncio.run(seed_massive_challenges())
