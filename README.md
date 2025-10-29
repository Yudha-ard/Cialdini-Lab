# Tegalsec Social Engineering Lab

🎯 **Platform pembelajaran cybersecurity pertama di Indonesia** yang fokus pada social engineering dengan kasus nyata Indonesia.

![Version](https://img.shields.io/badge/version-2.0-emerald) ![By Tegalsec](https://img.shields.io/badge/by-Tegalsec%20Community-cyan) ![Challenges](https://img.shields.io/badge/challenges-25%2B-yellow)

## 🌟 Tentang Project

Tegalsec Social Engineering Lab adalah platform edukasi hands-on untuk memahami, mendeteksi, dan mencegah serangan social engineering. Terinspirasi dari DVWA (Damn Vulnerable Web Application) namun fokus pada aspek psikologi dan manipulasi manusia.

### ✨ Fitur Utama

**🎯 Challenge System**
- 25+ challenges interaktif dengan kasus nyata Indonesia
- Multi-question per challenge (3-4 pertanyaan mendalam)
- Organized by Cialdini's 6 principles
- Time-based scoring dengan speed multipliers
- Partial credit system

**📚 Course System**
- Interactive slide-based learning
- Module-by-module progression
- Progress tracking per user
- Admin CRUD untuk create/edit courses

**⚡ Quiz Mode (Rapid Fire)**
- 10 random questions
- 60 seconds time limit
- 1.5x speed bonus
- Confetti animation untuk high score

**🔥 Gamification**
- Daily Challenge (2x points bonus)
- Streak system (consecutive days)
- Badge & Achievement system
- Certificate auto-generation
- Leaderboard real-time

**👨‍💼 Admin Panel**
- Full CRUD: Challenges, Education, Courses
- User management & statistics
- Recent activity monitoring
- Platform analytics dashboard

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
