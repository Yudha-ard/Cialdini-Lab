import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
import uuid
from datetime import datetime, timezone

mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ.get('DB_NAME', 'tegalsec_lab')]

async def seed_final_10_challenges():
    print("🎯 Seeding 10 additional comprehensive challenges...")
    
    challenges = [
        # Challenge 1: Phishing sophistiqué
        {
            "id": str(uuid.uuid4()),
            "title": "Spear Phishing Attack: CEO Fraud Anatomy",
            "category": "phishing",
            "difficulty": "advanced",
            "cialdini_principle": "authority",
            "challenge_type": "multi_choice",
            "description": "Analisis mendalam spear phishing attack targeting CFO",
            "scenario": "Email dari 'CEO' ke CFO: 'Urgent wire transfer needed for acquisition. Send $500K to: [account]. Confidential - don't discuss with team.' Email perfect: logo, signature, sender ceo@company.co (domain typosquatting: .co not .com).",
            "questions": [
                {"question": "Primary vulnerability exploited?", "options": ["Technical (malware)", "Authority + Urgency + Secrecy combo to bypass normal verification", "Network weakness", "Software bug"], "correct_answer": 1, "explanation": "Spear phishing exploits human psychology: authority (CEO), urgency (immediate action), secrecy (don't verify with team). Technical defenses useless against social engineering."},
                {"question": "Best mitigation?", "options": ["Better antivirus", "Dual-channel verification: any large transfer request via email must confirm via phone/in-person", "Email filter", "Employee training only"], "correct_answer": 1, "explanation": "Dual-channel verification: separate communication method (phone) to confirm email requests. Prevents email-only attacks. Authority exploitation defeated by process."},
                {"question": "Domain typosquatting detection?", "options": ["Visual inspection sufficient", "DMARC/SPF/DKIM + hover links + check exact domain (company.co vs company.com) + use of email authentication indicators", "Antivirus catches it", "Training enough"], "correct_answer": 1, "explanation": "Technical + human defense: DMARC (email authentication), hover links (reveal real domain), exact domain check. Typosquatting (similar domain) bypasses visual inspection."}
            ],
            "points": 200,
            "tips": ["Dual-channel verification mandatory for financial transactions", "Check exact domain, not just display name", "DMARC/SPF/DKIM implementation"],
            "time_limit_seconds": 360,
            "created_at": datetime.now(timezone.utc)
        },
        
        # Challenge 2: Insider threat
        {
            "id": str(uuid.uuid4()),
            "title": "Insider Threat: Disgruntled Employee Data Exfiltration",
            "category": "pretexting",
            "difficulty": "advanced",
            "cialdini_principle": "commitment",
            "challenge_type": "multi_choice",
            "description": "Detect dan prevent insider threat scenario",
            "scenario": "Employee akan resign. 2 minggu notice period: unusual behavior - access sensitive files outside job scope, large USB usage, upload to personal cloud, after-hours database queries. Exit interview: acts normal.",
            "questions": [
                {"question": "Behavioral red flags?", "options": ["Normal pre-resignation activity", "All listed: out-of-scope file access, USB usage spike, personal cloud upload, unusual hours = data exfiltration pattern", "Coincidental timing", "Not security concern"], "correct_answer": 1, "explanation": "Insider threat indicators: access unusual data, physical media (USB), external upload (cloud), timing (before exit). Pattern suggests planned data theft."},
                {"question": "Technical controls?", "options": ["None, trust employees", "DLP (Data Loss Prevention): monitor/block unusual file access, USB disable, cloud upload detection, database audit logs", "Antivirus sufficient", "Only after-incident investigation"], "correct_answer": 1, "explanation": "DLP: monitors data movement, blocks unauthorized transfers, alerts on policy violations. Essential for insider threats. Audit logs track access patterns."},
                {"question": "Legal/HR coordination?", "options": ["Fire immediately", "Document evidence (logs, files), coordinate with HR/Legal for proper investigation, secure interview before exit to gather info, potential legal action", "Ignore - resigned anyway", "Just revoke access"], "correct_answer": 1, "explanation": "Insider threat = potential crime. Document evidence, proper legal process. Secure interview (may reveal info), coordinate HR/Legal. Premature firing = destroy evidence chain."}
            ],
            "points": 200,
            "tips": ["DLP implementation critical", "Monitor pre-resignation activity", "Coordinate Security-HR-Legal"],
            "time_limit_seconds": 360,
            "created_at": datetime.now(timezone.utc)
        },
        
        # Challenge 3-10: Add more diverse challenges
        {
            "id": str(uuid.uuid4()),
            "title": "Deepfake Voice Phishing: AI-Generated CEO Voice",
            "category": "indonesian_case",
            "difficulty": "advanced",
            "cialdini_principle": "authority",
            "challenge_type": "multi_choice",
            "description": "Detect AI-generated deepfake voice in vishing attack",
            "scenario": "Finance manager receives call: sounds EXACTLY like CEO (voice deepfake from YouTube videos). 'Emergency, wire $200K now, I'm in meeting can't video call.' Voice perfect, knows internal projects. Manager suspicious.",
            "questions": [
                {"question": "Deepfake voice indicators?", "options": ["Perfect voice = genuine CEO", "Subtle: unnatural pauses, background noise inconsistent, no video (deepfake voice easier than video), urgency to prevent verification", "Voice match proves identity", "Can't detect without tools"], "correct_answer": 1, "explanation": "Deepfake detection: audio artifacts (unnatural pauses, breathing), no video option (harder to fake), unusual urgency. Technology improving - rely on process, not audio alone."},
                {"question": "Anti-deepfake protocol?", "options": ["Trust voice recognition", "Shared secret phrase/code word (not in public videos) + video call mandatory for approvals + callback to known number + dual authorization", "Hang up and ignore", "Audio analysis software"], "correct_answer": 1, "explanation": "Anti-deepfake: shared secrets (not public), video call (harder to fake real-time), callback (verify number), dual auth (two people required). Multi-factor verification."},
                {"question": "Prevention at source?", "options": ["Nothing - technology inevitable", "Limit public exposure of executive voices (videos, podcasts), train team on deepfake threat, establish verbal/written protocols not in public domain", "Ban phone calls", "AI detection only"], "correct_answer": 1, "explanation": "Prevention: reduce training data (limit public voice samples), awareness (deepfake threat real), secret protocols (not publicly known). Can't prevent fully but reduce attack surface."}
            ],
            "points": 250,
            "tips": ["Deepfakes real and sophisticated", "Shared secrets not in public", "Multi-factor verification always"],
            "time_limit_seconds": 360,
            "created_at": datetime.now(timezone.utc)
        },
        
        {
            "id": str(uuid.uuid4()),
            "title": "Supply Chain Attack: Compromised Vendor Access",
            "category": "pretexting",
            "difficulty": "advanced",
            "cialdini_principle": "social_proof",
            "challenge_type": "multi_choice",
            "description": "Identify supply chain social engineering",
            "scenario": "Trusted IT vendor (3 years relationship) emails: 'We're upgrading your systems. Install this remote access tool: [link].' Email from vendor domain, contact is known person. Link downloads RAT (Remote Access Trojan).",
            "questions": [
                {"question": "Attack vector?", "options": ["Malware only", "Supply chain: attacker compromised vendor email, uses trusted relationship (social proof) to deploy malware via 'legitimate' channel", "Vendor intentionally malicious", "Network vulnerability"], "correct_answer": 1, "explanation": "Supply chain attack: compromise trusted third party, leverage relationship for access. Victim trusts vendor = lower guard. Known contact + legitimate domain = high success rate."},
                {"question": "Verification process?", "options": ["Trust vendor email", "Call vendor via independent number (not from email), verify via ticket system, request details of 'upgrade' from account manager, scan file before install", "Install if from known contact", "Antivirus check sufficient"], "correct_answer": 1, "explanation": "Verify via independent channel: phone (known number, not email), ticketing system, account manager. Even trusted sources verify via separate method. Scan file with multiple AV."},
                {"question": "Vendor security requirements?", "options": ["Not your responsibility", "Require vendors: MFA, security audits, incident notification, limited access scope, regular security reviews, contractual security standards", "Trust their security", "Basic NDA enough"], "correct_answer": 1, "explanation": "Vendor security = your security. Contractual requirements: MFA, audits, incident notification, access scope limits. Compromise of vendor = compromise of you. Regular reviews essential."}
            ],
            "points": 200,
            "tips": ["Verify vendor requests independently", "Vendor security is your security", "Least privilege for vendor access"],
            "time_limit_seconds": 360,
            "created_at": datetime.now(timezone.utc)
        },
        
        {
            "id": str(uuid.uuid4()),
            "title": "Social Media OSINT: Information Disclosure Risk",
            "category": "indonesian_case",
            "difficulty": "intermediate",
            "cialdini_principle": "liking",
            "challenge_type": "multi_choice",
            "description": "Understand OSINT gathering from social media for targeted attacks",
            "scenario": "Employee posts LinkedIn: 'Excited about Q4 product launch!' Instagram: office photo with whiteboard visible (project codenames). Facebook: 'Bad week, lots of IT issues at work.' Attacker aggregates info for spear phishing.",
            "questions": [
                {"question": "OSINT attack preparation?", "options": ["Social media posts harmless", "Attacker uses: product launch timing (context), project names (insider knowledge), IT issues (vulnerability window) to craft convincing spear phishing with insider info", "Posts don't reveal sensitive data", "Privacy settings prevent this"], "correct_answer": 1, "explanation": "OSINT: aggregate public info for attack context. Product launch (timing), project names (legitimacy), IT issues (vulnerability). Each post minor, combined = attack intel."},
                {"question": "Information disclosure policy?", "options": ["Ban social media", "Educate: no project names/schedules publicly, sanitize photos (no whiteboards/screens), don't discuss company issues, separate personal/professional posts", "Privacy settings sufficient", "Only HR concern"], "correct_answer": 1, "explanation": "Balance awareness with freedom: educate on OSINT risk, guidelines (no internal names/schedules), photo awareness (backgrounds). Privacy settings help but not sufficient - public posts aggregate."},
                {"question": "Company social media monitoring?", "options": ["Invasion of privacy", "Monitor public posts (not private) for sensitive disclosures, educate when found, establish reporting mechanism for concerning posts, competitive intel gathering", "Not necessary", "Let employees post freely"], "correct_answer": 1, "explanation": "Public post monitoring legitimate (already public). Not surveillance - protection. Competitive intel: what attackers can learn? Educate on findings, establish safe posting culture."}
            ],
            "points": 150,
            "tips": ["OSINT from aggregated public info", "Educate on safe posting", "Monitor public posts for risk"],
            "time_limit_seconds": 300,
            "created_at": datetime.now(timezone.utc)
        },
        
        {
            "id": str(uuid.uuid4()),
            "title": "Physical Security: Tailgating & Shoulder Surfing",
            "category": "tailgating",
            "difficulty": "beginner",
            "cialdini_principle": "liking",
            "challenge_type": "multi_choice",
            "description": "Physical security breach via social engineering",
            "scenario": "Friendly person carrying boxes follows employee into secure building (tailgating). Inside, stands behind employee at ATM/terminal, observes password entry (shoulder surfing). Uses credentials later.",
            "questions": [
                {"question": "Tailgating success factors?", "options": ["Badge malfunction", "Social engineering: politeness (hold door), hands full (boxes), friendly appearance = employee compliance despite security policy", "Broken access control", "Guard negligence only"], "correct_answer": 1, "explanation": "Tailgating exploits politeness/social norms. Hard to deny entry to friendly person with hands full. Security policy: everyone badges individually - enforcing feels rude. Training: polite enforcement."},
                {"question": "Anti-tailgating measures?", "options": ["More guards", "Mantraps (one-person entry), turnstiles, security culture (challenge unknown people), visitor badges, CCTV with alerts, no-tailgating training", "Trust badge system", "Locked doors sufficient"], "correct_answer": 1, "explanation": "Multi-layer: physical (mantraps prevent multiple entry), culture (challenge unknowns - not rude, security), technology (CCTV alerts), process (visitor management). Train: security over politeness."},
                {"question": "Shoulder surfing prevention?", "options": ["Memorize passwords", "Privacy screens, password masking (dots), awareness (check surroundings), MFA (reduces password value), position screens away from view, security awareness", "Longer passwords", "Faster typing"], "correct_answer": 1, "explanation": "Multi-defense: physical (privacy screens, screen positioning), awareness (environment check), technology (masking, MFA reduces password alone value). Assume observation possible - reduce impact."}
            ],
            "points": 100,
            "tips": ["Everyone badges individually - no tailgating", "Challenge unknown people politely", "MFA reduces password compromise impact"],
            "time_limit_seconds": 240,
            "created_at": datetime.now(timezone.utc)
        },
        
        {
            "id": str(uuid.uuid4()),
            "title": "Ransomware Social Engineering: Emotet to Ryuk Chain",
            "category": "baiting",
            "difficulty": "advanced",
            "cialdini_principle": "scarcity",
            "challenge_type": "multi_choice",
            "description": "Understand multi-stage ransomware attack via social engineering entry",
            "scenario": "Phishing email: 'Invoice overdue! Pay within 24h or legal action.' Excel attachment with macros. Employee opens, enables macros (Emotet malware). Days later: Ryuk ransomware deploys, encrypts network, demands $1M Bitcoin.",
            "questions": [
                {"question": "Social engineering + technical combo?", "options": ["Pure malware attack", "Entry: social engineering (urgency, fear of legal action) bypasses technical (employee enables macros). Then: technical exploitation (lateral movement, privilege escalation, encryption)", "Only technical vulnerability", "Accidental infection"], "correct_answer": 1, "explanation": "Modern ransomware: social engineering for initial access (macros require user action), then automated technical exploitation. Human = weakest link for entry, then machines take over."},
                {"question": "Macro enable = why dangerous?", "options": ["Macros always malware", "Macros = code execution capability. Emotet uses macros to: download payload, establish persistence, steal credentials, spread laterally. Enabling = give attacker code execution", "Macros safe if from known sender", "Antivirus blocks macro malware"], "correct_answer": 1, "explanation": "Macros = code. Disabling macros by default security measure. Enabling = intentionally run attacker code. Emotet specifically abuses macros for initial foothold. Known sender irrelevant if compromised."},
                {"question": "Ransomware defense layers?", "options": ["Backups only", "Prevention: email filtering, macro disable, training. Detection: EDR, network monitoring. Response: backups (offline, tested), incident response plan, NO MACRO ENABLE POLICY", "Antivirus sufficient", "Pay ransom if hit"], "correct_answer": 1, "explanation": "Defense in depth: prevent (email filter, macros disabled, awareness), detect (EDR catches post-infection), respond (backups = recovery without payment). No single defense perfect - layers essential."}
            ],
            "points": 250,
            "tips": ["NEVER enable macros from email attachments", "Offline backups tested regularly", "EDR + email filtering essential"],
            "time_limit_seconds": 360,
            "created_at": datetime.now(timezone.utc)
        },
        
        {
            "id": str(uuid.uuid4()),
            "title": "Watering Hole Attack: Compromised Industry Website",
            "category": "baiting",
            "difficulty": "advanced",
            "cialdini_principle": "social_proof",
            "challenge_type": "multi_choice",
            "description": "Detect watering hole attack targeting specific industry",
            "scenario": "Industry association website (high trust, frequented by professionals) compromised. Injects malware via drive-by download. Targets: company employees visiting legitimate site. No phishing - direct infection via trusted site.",
            "questions": [
                {"question": "Watering hole = how different from phishing?", "options": ["Same attack", "Watering hole: compromise site VICTIMS visit (no direct contact needed). Phishing: direct contact. Watering hole leverages trusted site + routine visits", "More sophisticated phishing", "Random website malware"], "correct_answer": 1, "explanation": "Watering hole targets congregate: compromise site they naturally visit (industry sites, news). No phishing needed - victims come to attacker. More targeted, harder to detect (trusted site)."},
                {"question": "Detection & prevention?", "options": ["Antivirus only", "Network: IDS/IPS detect exploit attempts, web filtering (reputation), endpoint: AV/EDR detect post-infection. Process: frequent patching (reduce exploitability), segmentation (limit spread)", "Don't visit external sites", "Trust reputable sites only"], "correct_answer": 1, "explanation": "Multi-layer: network (IDS/IPS, web filtering), endpoint (AV, EDR), hygiene (patching, segmentation). Trusted sites can be compromised - defenses assume compromise possible."},
                {"question": "Post-compromise indicators?", "options": ["Antivirus alert only", "Indicators: unusual outbound traffic from multiple hosts, new processes/services, credential dumps, lateral movement attempts, beacon traffic patterns. Compromise detection via behavior, not signature", "Single host infection", "Obvious immediate symptoms"], "correct_answer": 1, "explanation": "Watering hole = targeted campaign. Multiple infections likely. Indicators: network-wide anomalies (multiple beacons), coordinated lateral movement. Focus: behavioral detection, not just malware signatures."}
            ],
            "points": 200,
            "tips": ["Trusted sites can be compromised", "Network behavior monitoring critical", "Assume breach mindset"],
            "time_limit_seconds": 360,
            "created_at": datetime.now(timezone.utc)
        },
        
        {
            "id": str(uuid.uuid4()),
            "title": "Pretexting: Fake IT Support Call",
            "category": "pretexting",
            "difficulty": "intermediate",
            "cialdini_principle": "authority",
            "challenge_type": "multi_choice",
            "description": "Recognize pretexting via fake IT support",
            "scenario": "Call from 'IT Support': 'Your computer flagged for security issue. Need to remote in to fix. What's your employee ID and password for authentication?' Caller has internal knowledge (manager name, recent IT maintenance window).",
            "questions": [
                {"question": "Pretexting = what makes it work?", "options": ["Technical hacking", "Pretexting = fake scenario (IT issue) + authority (IT support) + urgency (fix now) + insider knowledge (legitimacy) = extract credentials. Psychological manipulation.", "Lucky guess", "Password weakness"], "correct_answer": 1, "explanation": "Pretexting: fabricated scenario with plausible details. Authority (IT support), urgency (security issue), insider info (manager name, maintenance) create legitimacy. Goal: credentials extraction."},
                {"question": "Insider knowledge - where from?", "options": ["Insider accomplice", "OSINT (social media, company site, previous low-level compromise, dumpster diving, LinkedIn employee list). Insider knowledge doesn't require insider - just research.", "Magic/hacking", "Random guess"], "correct_answer": 1, "explanation": "Attackers research targets: company website (org chart), LinkedIn (employee names/roles), social media (events/maintenance), previous breaches. Insider knowledge = research, not necessarily insider access."},
                {"question": "Proper response protocol?", "options": ["Give password - IT needs it", "NEVER give password by phone. IT NEVER asks passwords. Proper: hang up, call IT via known internal number, verify if issue/ticket exists, create ticket if concerned. IT has admin access - no password needed", "Ask for employee ID first", "Only share employee ID"], "correct_answer": 1, "explanation": "Golden rule: IT never asks passwords. Admins have elevated access - don't need user passwords. Verify via independent channel (call IT desk directly). Phone caller ID spoofable - don't trust."}
            ],
            "points": 150,
            "tips": ["IT NEVER asks for passwords", "Verify via independent channel", "Insider knowledge ≠ insider access"],
            "time_limit_seconds": 300,
            "created_at": datetime.now(timezone.utc)
        },
        
        {
            "id": str(uuid.uuid4()),
            "title": "Quid Pro Quo: Free Security Audit Scam",
            "category": "quid_pro_quo",
            "difficulty": "intermediate",
            "cialdini_principle": "reciprocity",
            "challenge_type": "multi_choice",
            "description": "Identify quid pro quo attack disguised as free service",
            "scenario": "Cold call: 'Free security audit for your company! Just install our assessment tool.' Tool = actually backdoor. Report provided after = real vulnerabilities + malware planted for later exploitation.",
            "questions": [
                {"question": "Quid pro quo manipulation?", "options": ["Legitimate free service", "Exchange: 'free audit' (perceived value) for tool install (malware). Reciprocity: feel obligated to reciprocate free service by trusting. Tool = Trojan.", "Competitive offer", "Normal marketing"], "correct_answer": 1, "explanation": "Quid pro quo: something for something. 'Free' audit (value) for tool install (access). Exploits reciprocity (free = trust) and desire for security. Actual goal: backdoor installation."},
                {"question": "Free service red flags?", "options": ["Free = always scam", "Red flags: unsolicited (cold call), immediate install request (no verification), 'free' with no clear business model, pressure to install, unknown company. Legit security: established company, no immediate install", "Free audits common", "All marketing similar"], "correct_answer": 1, "explanation": "Unsolicited + free + install request = extreme caution. Legitimate security companies: established reputation, no pressure, assessment via agreement not cold call. If too good + unsolicited = scam likely."},
                {"question": "Safe assessment approach?", "options": ["Install any audit tool", "Proper: engage known reputable firms, scope agreed in writing, use of own/verified tools (not theirs), references checked, no installs from unknown sources, sandboxed testing", "Accept free offers", "Trust caller ID"], "correct_answer": 1, "explanation": "Security assessment: vet firm (reputation, references), define scope, control tooling (not unknown installs), formal agreement. Free unsolicited = automatically reject. Security = too critical for opportunistic offers."}
            ],
            "points": 150,
            "tips": ["Free + unsolicited + install = scam", "Vet security firms extensively", "Control assessment tooling"],
            "time_limit_seconds": 300,
            "created_at": datetime.now(timezone.utc)
        }
    ]
    
    print(f"Created {len(challenges)} new challenges")
    
    # Insert
    if challenges:
        await db.challenges.insert_many(challenges)
        print(f"✅ Seeded {len(challenges)} challenges")
    
    # Total count
    total = await db.challenges.count_documents({})
    print(f"\n📊 TOTAL CHALLENGES: {total}")

if __name__ == "__main__":
    asyncio.run(seed_final_10_challenges())
