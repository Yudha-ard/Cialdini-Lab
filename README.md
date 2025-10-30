# Tegalsec Social Engineering Lab

🎯 **Platform pembelajaran cybersecurity pertama di Indonesia** yang fokus pada social engineering dengan kasus nyata Indonesia.

![Version](https://img.shields.io/badge/version-4.0-emerald) ![By Tegalsec](https://img.shields.io/badge/by-Tegalsec%20Community-cyan) ![Challenges](https://img.shields.io/badge/challenges-36%2B-yellow)

## 🌟 Tentang Project

Tegalsec Social Engineering Lab adalah platform edukasi hands-on untuk memahami, mendeteksi, dan mencegah serangan social engineering. Terinspirasi dari DVWA (Damn Vulnerable Web Application) namun fokus pada aspek psikologi dan manipulasi manusia.

---

## 🚀 Quick Start dengan Docker

### Prerequisites
- Docker & Docker Compose installed
- 4GB RAM minimum
- Port 3000, 8001, 27017 available

### Installation (Recommended)

```bash
# Clone atau download project
git clone <repository-url>
cd tegalsec-lab

# Run auto-install script
chmod +x install.sh
./install.sh

# Atau manual:
docker-compose up --build -d

# Check logs
docker-compose logs -f
```

**Access:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8001
- API Docs: http://localhost:8001/docs

**Default Accounts:**
- Admin: `username=admin, password=admin123`
- User: `username=user, password=user123`

---

## 💻 Manual Installation (Development)

### Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Setup MongoDB (local or Docker)
docker run -d -p 27017:27017 --name mongodb mongo:7.0

# Create .env file
cat > .env << EOF
MONGO_URL=mongodb://localhost:27017
DB_NAME=tegalsec_lab
JWT_SECRET_KEY=your-super-secret-key-change-in-production
ALGORITHM=HS256
EOF

# Seed database
python seed_data.py
python seed_indonesia_challenges.py
python seed_massive_challenges.py
python seed_complete_batch.py
python seed_final_10.py
python seed_courses.py

# Run backend
uvicorn server:app --reload --host 0.0.0.0 --port 8001
```

### Frontend Setup
```bash
cd frontend

# Install dependencies
yarn install

# Create .env file
cat > .env << EOF
REACT_APP_BACKEND_URL=http://localhost:8001
WDS_SOCKET_PORT=0
EOF

# Run frontend
yarn start
```

Access: http://localhost:3000

---

## ✨ Fitur Utama

### 🎯 Challenge System
- **36+ challenges** komprehensif dengan kasus nyata Indonesia
- **200+ pertanyaan** mendalam (10-15 per challenge)
- Grouped by **Cialdini's 6 Principles**:
  * Reciprocity (Timbal Balik) - 6 challenges
  * Commitment & Consistency - 5 challenges
  * Social Proof (Bukti Sosial) - 5 challenges
  * Authority (Otoritas) - 5 challenges
  * Liking (Kesukaan) - 5 challenges
  * Scarcity (Kelangkaan) - 5 challenges
  * Mixed (Advanced Topics) - 5 challenges

**Indonesian-specific cases:**
- Pinjol predatory practices (10 soal)
- E-commerce scams
- Crypto ponzi schemes
- MLM traps
- Romance scams
- Spear phishing
- Deepfake attacks
- Supply chain attacks
- Insider threats

### 📚 Course System (Enhanced)
- Interactive slide-based learning
- Module-by-module progression
- Progress tracking per user
- **Admin CRUD**: Create/Edit courses dengan module & slide management
- Prerequisites & Learning outcomes
- Quiz integration
- Auto-generated certificates

### ⚡ Quiz Mode (Rapid Fire)
- 10 random questions
- 60 seconds time limit
- 1.5x speed bonus
- Confetti for high score
- Global leaderboard

### 🎮 Mini Game: "Spot the Phishing"
- Quick interactive phishing detection game
- Real-world email examples
- 60 seconds, 3 lives
- Streak bonus system
- Educational red flags

### 🏆 Achievement System
- **8 unlockable achievements**
- 4 rarity levels: Common, Rare, Epic, Legendary
- Unlock animations dengan confetti
- Achievement points tracking
- Progress heatmap (GitHub-style)

### 📱 Social Sharing
- Share certificates to social media
- Twitter, Facebook, LinkedIn integration
- Copy-to-clipboard

### 👨‍💼 Admin Panel (Full CRUD)
- **Challenges**: Create, Edit, Delete dengan multi-question support
- **Courses**: Module & slide management
- **Education**: Content management by Cialdini principle
- **Users**: Edit (name, email, password), Delete
- Platform analytics dashboard
- Recent activity monitoring

### 🔥 Gamification
- Daily Challenge (2x points bonus)
- Streak system dengan animation
- Badge & Achievement system
- Certificate auto-generation
- Real-time leaderboard
- Activity heatmap calendar
- Today's stats dashboard

### 🔐 Security Features
- **RBAC** (Role-Based Access Control)
- **Rate Limiting**: Login (5/5min), Register (3/hour)
- JWT authentication
- Password hashing (bcrypt)
- **Admin-only endpoints** with `require_admin` dependency
- **No Privilege Escalation**: Users cannot become admin
- Input validation
- Forgot password flow

---

## 🛡️ Security Architecture

### Authentication & Authorization
```python
# RBAC Implementation
@api_router.post("/admin/courses")
async def create_course(course: Course, admin_user: dict = Depends(require_admin)):
    # Only admin can access - automatic 403 for users
    ...

# Rate Limiting
check_rate_limit(f"login_{username}", limit=5, window=300)  # 5 attempts per 5 minutes
```

### Protected Routes
All `/admin/*` routes require admin role. User role cannot access:
- Course CRUD
- User management
- Education content management
- System statistics

### Data Security
- Passwords: bcrypt hashed
- JWTs: signed with secret key
- MongoDB: No ObjectId exposure (UUIDs only)
- User data: Password excluded from responses

---

## 📊 Database Schema

### Collections
- `users`: User accounts (role, points, streak, completed_challenges)
- `challenges`: Challenge data with questions & Cialdini principle
- `education`: Educational content
- `courses`: Course structure with modules & slides
- `progress`: User progress tracking
- `feedback`: User feedback
- `certificates`: Auto-generated certificates

### Indexes
- `users`: username (unique), email (unique)
- `challenges`: cialdini_principle, difficulty
- `courses`: category, difficulty

---

## 🎯 Challenge Statistics

| Category | Count | Questions | Difficulty Mix |
|----------|-------|-----------|----------------|
| Reciprocity | 6 | 60+ | 2 Beginner, 2 Intermediate, 2 Advanced |
| Commitment | 5 | 50+ | 1 Beginner, 2 Intermediate, 2 Advanced |
| Social Proof | 5 | 50+ | 1 Beginner, 2 Intermediate, 2 Advanced |
| Authority | 5 | 50+ | 1 Beginner, 2 Intermediate, 2 Advanced |
| Liking | 5 | 40+ | 2 Beginner, 2 Intermediate, 1 Advanced |
| Scarcity | 5 | 40+ | 2 Beginner, 2 Intermediate, 1 Advanced |
| Advanced Topics | 5 | 30+ | All Advanced |
| **TOTAL** | **36** | **320+** | 10 Beginner, 14 Intermediate, 12 Advanced |

---

## 🧪 Testing

### Run Security Tests
```bash
# Test rate limiting
for i in {1..10}; do curl -X POST http://localhost:8001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"test"}'; done

# Test RBAC (should return 403 for user role)
curl http://localhost:8001/api/admin/users \
  -H "Authorization: Bearer <user_token>"

# Test achievement system (new user should have 0 achievements)
# Login as new user → Dashboard → Check achievements
```

### Frontend Tests
```bash
cd frontend
yarn test
```

---

## 📝 API Documentation

Access interactive API docs: http://localhost:8001/docs

### Key Endpoints

**Authentication:**
- `POST /api/auth/register` - Register new user (Rate limited: 3/hour)
- `POST /api/auth/login` - Login (Rate limited: 5/5min)

**Challenges:**
- `GET /api/challenges` - List all challenges
- `GET /api/challenges/{id}` - Get challenge detail
- `POST /api/challenges/{id}/attempt` - Submit challenge attempt

**Admin (Requires admin role):**
- `GET /api/admin/stats` - Platform statistics
- `POST /api/admin/courses` - Create course
- `PUT /api/admin/users/{id}` - Update user
- `DELETE /api/admin/users/{id}` - Delete user

**Quiz:**
- `GET /api/quiz/random` - Get random quiz (10 questions)

---

## 🔧 Troubleshooting

### Challenges tidak muncul
```bash
# Re-seed database
cd backend
python seed_data.py
python seed_indonesia_challenges.py
python seed_massive_challenges.py
python seed_complete_batch.py
python seed_final_10.py

# Verify
python -c "from motor.motor_asyncio import AsyncIOMotorClient; import asyncio; async def check(): client = AsyncIOMotorClient('mongodb://localhost:27017'); db = client['tegalsec_lab']; count = await db.challenges.count_documents({}); print(f'Total challenges: {count}'); asyncio.run(check())"
```

### Frontend compile error
```bash
cd frontend
rm -rf node_modules yarn.lock
yarn install
yarn start
```

### Backend not starting
```bash
# Check MongoDB
docker ps | grep mongo

# Check logs
tail -f /var/log/supervisor/backend.err.log

# Restart
sudo supervisorctl restart backend
```

### "User is not defined" error
Already fixed - ensure all lucide-react imports include `User` icon.

---

## 🤝 Contributing

Contributions welcome! Areas untuk improvement:
- More Indonesian case studies
- Additional Cialdini principle challenges
- Course content expansion
- UI/UX enhancements
- Security hardening

---

## 📜 License

Educational use only. © Tegalsec Community 2024-2025

---

## 👥 Credits

**Developed by:** Tegalsec Community (tegalsec.org)
**Framework:** React + FastAPI + MongoDB
**Inspiration:** DVWA, Cialdini's "Influence: The Psychology of Persuasion"

---

## 📞 Support

- Website: https://tegalsec.org
- Issues: [GitHub Issues](link)
- Community: Telegram/Discord (link)

---

**Version 4.0** - Complete rebuild dengan Docker support, 36 challenges, RBAC, rate limiting, dan comprehensive security fixes.

## 🌟 Tentang Project

Tegalsec Social Engineering Lab adalah platform edukasi hands-on untuk memahami, mendeteksi, dan mencegah serangan social engineering. Terinspirasi dari DVWA (Damn Vulnerable Web Application) namun fokus pada aspek psikologi dan manipulasi manusia.

### ✨ Fitur Utama

**🎯 Challenge System (NEW: Cialdini Categories)**
- 30+ challenges interaktif dengan kasus nyata Indonesia
- **Grouped by Cialdini's 6 Principles**: Reciprocity, Commitment, Social Proof, Authority, Liking, Scarcity
- Multi-question per challenge (3-4 pertanyaan mendalam)
- Indonesian-specific cases: Pinjol predatory, E-commerce scams, Crypto Ponzi, MLM traps
- Time-based scoring dengan speed multipliers
- Partial credit system
- Tab navigation per kategori Cialdini

**📚 Course System (Enhanced)**
- Interactive slide-based learning
- Module-by-module progression with nested structure
- Progress tracking per user
- **Admin CRUD**: Create/Edit courses dengan module & slide management
- Prerequisites & Learning outcomes tracking

**⚡ Quiz Mode (Rapid Fire)**
- 10 random questions
- 60 seconds time limit
- 1.5x speed bonus
- Confetti animation untuk high score

**🎮 Mini Game: "Spot the Phishing" (NEW!)**
- Quick interactive game untuk latihan deteksi phishing
- Real-world email examples (legitimate vs phishing)
- 60 seconds time limit dengan 3 lives
- Streak bonus system (+2pts per streak)
- Red flags education setelah game over
- Score leaderboard

**🏆 Achievement System (NEW!)**
- 8 unlockable achievements dengan rarity tiers
- Unlock animations dengan confetti
- Achievement points tracking
- Locked achievements dengan mystery reveal
- Rarity levels: Common, Rare, Epic, Legendary
- Toast notifications untuk new unlocks

**📱 Social Sharing (NEW!)**
- Share certificates ke social media
- Twitter, Facebook, LinkedIn integration
- Copy-to-clipboard functionality
- Custom share text dengan achievement highlights

**🔥 Gamification**
- Daily Challenge (2x points bonus)
- Streak system (consecutive days with animation)
- Badge & Achievement system dengan unlock animations
- Certificate auto-generation
- Leaderboard real-time

**👨‍💼 Admin Panel (Enhanced)**
- Full CRUD: Challenges, Courses, **Education (NEW)**
- Course module & slide management
- Education content management by Cialdini principle
- User management & statistics
- Recent activity monitoring
- Platform analytics dashboard

**📚 Education CRUD (NEW)**
- Admin can create/edit/delete education content
- Content types: Cialdini Principle, Prevention Tips, Case Study
- Filterable by principle
- Rich text support

**🔐 Security Features**
- JWT authentication (multi-role: Admin/User)
- Forgot password flow
- Anti-cheat mechanisms
- Time-based validation

---

## 📊 Content Overview

### Challenges by Cialdini Principle

**1. Reciprocity (Timbal Balik)**
- Free Trial Credit Card Trap
- Survey Reward Scam  
- Aplikasi Penghasil Uang
- File "Gratis" Berbahaya

**2. Commitment & Consistency**
- Pyramid Scheme Progressive
- Investment Scam Escalation
- Subscription Dark Pattern
- MLM Recruitment Funnel

**3. Social Proof (Bukti Sosial)**
- Fake Review Ecosystem
- Influencer Crypto Scam
- Investment "100K Members"
- Testimonial Manipulation

**4. Authority (Otoritas)**
- Fake Government Official
- Phishing Bank BCA
- Customer Service Palsu
- Police Cyber Scam

**5. Liking (Kesukaan)**
- Romance Scam Investment
- Fake Influencer Endorsement
- Tailgating di Kantor
- Fake Recruiter

**6. Scarcity (Kelangkaan)**
- Flash Sale Countdown Fake
- Limited Slot Investment
- Shopee Hadiah Palsu
- Urgent Account Verification

### Special Categories

**💰 Crypto & NFT Scams**
- NFT Rugpull (Bored Monkey Club)
- Fake Crypto Wallet
- Pump & Dump Telegram
- Fake Airdrop Phishing

**📱 Indonesian Cases**
- Pinjol Ilegal + Terror Collector
- SIM Swap Attack
- Investasi Bodong (Pandora-style)
- MLM Kesehatan

**💼 Job & Money Scams**
- Remote Job Scam
- Dropshipping Course Scam
- Trading Bot Ponzi
- Money Game Applications

---

## 🛠️ Tech Stack

- **Frontend**: React 19 + Tailwind CSS + Shadcn/UI
- **Backend**: FastAPI (Python 3.11)
- **Database**: MongoDB
- **Authentication**: JWT
- **Deployment**: Docker + Kubernetes

---

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- Python 3.11+
- MongoDB 5.0+
- Yarn

### Installation

```bash
# Clone repository
git clone <repo-url>
cd tegalsec-lab

# Backend setup
cd backend
pip install -r requirements.txt
python seed_data.py
python seed_courses.py
uvicorn server:app --reload --host 0.0.0.0 --port 8001

# Frontend setup  
cd ../frontend
yarn install
yarn start
```

### Environment Variables

**Backend (.env)**
```
MONGO_URL=mongodb://localhost:27017
DB_NAME=tegalsec_lab
JWT_SECRET=your-secret-key
CORS_ORIGINS=*
```

**Frontend (.env)**
```
REACT_APP_BACKEND_URL=http://localhost:8001
```

---

## 👥 Default Accounts

**Admin Access**
- Username: `admin`
- Password: `admin123`
- Role: Full CRUD + Analytics

**Demo User**
- Username: `demouser`
- Password: `demo123`
- Role: Standard user

---

## 📖 API Documentation

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `POST /api/auth/forgot-password` - Request reset code
- `POST /api/auth/reset-password` - Reset password
- `GET /api/auth/me` - Get current user (with streak update)

### Challenges
- `GET /api/challenges` - List all challenges (with filters)
- `GET /api/challenges/{id}` - Get challenge detail
- `POST /api/challenges/{id}/attempt` - Submit answers (multi-question + time bonus)
- `GET /api/daily-challenge` - Get today's challenge (2x points)

### Courses
- `GET /api/courses` - List all courses
- `GET /api/courses/{id}` - Get course with modules & slides
- `POST /api/courses/{id}/progress` - Update progress
- `GET /api/courses/{id}/progress` - Get user progress

### Quiz
- `GET /api/quiz/random` - Generate random 10-question quiz
- `POST /api/quiz/submit` - Submit quiz answers

### Gamification
- `GET /api/leaderboard` - Top 10 users
- `GET /api/badges` - Available badges
- `GET /api/user/badges` - User's earned badges
- `GET /api/certificates` - User certificates (auto-issue)

### Admin (Requires admin role)
- `POST /api/admin/challenges` - Create challenge
- `PUT /api/admin/challenges/{id}` - Update challenge
- `DELETE /api/admin/challenges/{id}` - Delete challenge
- `GET /api/admin/users` - List all users
- `GET /api/admin/stats` - Platform statistics
- Endpoints untuk Education & Courses CRUD

---

## 🎯 Learning Outcomes

Setelah menyelesaikan lab ini, user akan mampu:

✅ Mengidentifikasi 6 prinsip psikologi Cialdini yang dieksploitasi
✅ Mendeteksi red flags dari berbagai jenis social engineering  
✅ Memahami modus penipuan umum di Indonesia (crypto, MLM, romance, job scam)
✅ Menerapkan defense strategies dalam kehidupan sehari-hari
✅ Melakukan analisis kritis terhadap permintaan informasi
✅ Menggunakan tools & techniques untuk verify legitimacy

---

## 🏆 Gamification Features

**Daily Challenge**: Random challenge setiap hari dengan 2x points bonus

**Streak System**: Track consecutive days active dengan fire icon 🔥

**Speed Bonus**:
- Finish <30% time limit = 2.0x multiplier
- Finish <50% time limit = 1.5x multiplier  
- Finish <70% time limit = 1.2x multiplier

**Level Progression**:
- Beginner: 0-199 points
- Intermediate: 200-499 points
- Advanced: 500-999 points
- Expert: 1000+ points

**Certificates**: Auto-issued untuk major achievements (complete all challenges, expert level, course completion)

**Badges**: First Blood, Perfectionist, Speed Demon, Phishing Hunter, Social Expert

---

## 🎓 Course Content

### 1. Fundamental Social Engineering (120 min)
- Module 1: Pengenalan Social Engineering
- Module 2: 6 Prinsip Cialdini (detail per prinsip)
- Module 3: Defense Strategies & Incident Response

### 2. Advanced Phishing Techniques (90 min)
- Modern Phishing Landscape (2024-2025)
- Anatomy of Phishing Emails
- Detection & Investigation

**Expandable**: Admin dapat create unlimited courses

---

## 🔧 Development

### Project Structure
```
/app
├── backend/
│   ├── server.py (FastAPI app)
│   ├── seed_data.py (Initial data)
│   ├── seed_courses.py (Course content)
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── pages/ (All pages)
│   │   ├── components/ (Reusable components + Shadcn UI)
│   │   ├── App.js (Routes & Auth)
│   │   └── App.css (Styles)
│   └── package.json
└── README.md
```

### Key Technologies
- **UI Components**: Shadcn/UI (Radix UI primitives)
- **Styling**: Tailwind CSS + Custom CSS (glass-morphism, cyber theme)
- **Icons**: Lucide React
- **Toast**: Sonner
- **Animations**: Framer Motion patterns + CSS animations
- **Charts**: (ready for integration)

---

## 🤝 Contributing

Kami welcome contributions! Area yang bisa dikontribusi:

1. **New Challenges**: Submit challenge baru dengan format existing
2. **Course Content**: Buat module baru untuk topics advanced
3. **UI/UX Improvements**: Enhance user experience
4. **Bug Fixes**: Report dan fix bugs
5. **Documentation**: Improve docs dan tutorials

### Contribution Guidelines
1. Fork repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## ⚠️ Disclaimer

Platform ini dibuat untuk **tujuan edukasi** cybersecurity awareness. Pengetahuan yang diperoleh HARUS digunakan secara etis dan bertanggung jawab.

**Tegalsec Community tidak bertanggung jawab atas penyalahgunaan informasi dari platform ini.**

---

## 📞 Contact & Links

- **Website**: [tegalsec.org](https://tegalsec.org)
- **Telegram**: [@tegalsec](https://t.me/tegalsec)
- **Email**: info@tegalsec.org
- **GitHub**: [github.com/tegalsec](https://github.com/tegalsec)

---

## 📄 License

Educational Purpose - Tegalsec Community © 2025

---

## 🙏 Acknowledgments

- Inspired by DVWA (Damn Vulnerable Web Application)
- Based on Robert Cialdini's "Influence: The Psychology of Persuasion"
- Kasus-kasus dibuat berdasarkan real incidents di Indonesia
- Built with ❤️ by Tegalsec Community untuk cybersecurity awareness

---

**Made with 🔐 by Tegalsec Community** | Meningkatkan Cyber Awareness Indonesia 🇮🇩
