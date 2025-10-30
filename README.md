# Tegalsec Social Engineering Lab 🎯

**Platform pembelajaran cybersecurity pertama di Indonesia** yang fokus pada social engineering dengan kasus nyata Indonesia.

![Version](https://img.shields.io/badge/version-5.0-emerald) ![By Tegalsec](https://img.shields.io/badge/by-Tegalsec%20Community-cyan) ![Challenges](https://img.shields.io/badge/challenges-36%2B-yellow)

---

## 🌟 Tentang Project

Tegalsec Social Engineering Lab adalah platform edukasi hands-on untuk memahami, mendeteksi, dan mencegah serangan social engineering. Terinspirasi dari DVWA (Damn Vulnerable Web Application) namun fokus pada aspek psikologi dan manipulasi manusia berdasarkan **6 Prinsip Cialdini**.

Platform ini dirancang untuk memberikan pengalaman belajar interaktif dengan kasus-kasus nyata yang sering terjadi di Indonesia.

---

## 🚀 Quick Start dengan Docker

### Prerequisites
- Docker & Docker Compose installed
- 4GB RAM minimum
- Port 3000, 8001, 27017 tersedia

### Installation

```bash
# Clone repository
git clone <repository-url>
cd tegalsec-lab

# Run dengan Docker Compose
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

# Create & activate virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# OR venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Setup MongoDB
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

---

## ✨ Fitur Utama

### 🎯 Challenge System
- **36+ challenges** komprehensif dengan 200+ pertanyaan
- **Grouped by Cialdini's 6 Principles**:
  * **Reciprocity** (Timbal Balik) - 6 challenges
  * **Commitment & Consistency** - 5 challenges  
  * **Social Proof** (Bukti Sosial) - 5 challenges
  * **Authority** (Otoritas) - 5 challenges
  * **Liking** (Kesukaan) - 5 challenges
  * **Scarcity** (Kelangkaan) - 5 challenges
  * **Advanced Topics** - 5+ challenges

- **Single-Play System**: Setiap challenge hanya bisa diselesaikan sekali
- **Time-based Scoring**: Speed bonus untuk jawaban cepat
- **Multi-question Format**: 10-20 soal per challenge
- **Previous Results Display**: Lihat hasil sebelumnya jika sudah diselesaikan

**Kasus Indonesia yang Dibahas:**
- Pinjol predatory practices & terror collector
- E-commerce & marketplace scams
- Crypto ponzi schemes & NFT rugpull
- MLM traps & pyramid schemes
- Romance scams & fake profiles
- Phishing bank & SIM swap
- Job scams & fake recruiters
- Money game applications
- Deepfake attacks
- Supply chain security
- Insider threats

### ⚡ Quiz Mode (Rapid Fire)
- **Single-Play Global**: Hanya bisa mengikuti quiz sekali
- 10 random questions dari quiz question pool
- 60 seconds time limit
- 1.5x speed bonus
- Confetti animation untuk skor tinggi
- Admin dapat mengelola quiz questions

### 🎮 Mini Game: "Spot the Phishing"
- **Single-Play**: Hanya bisa bermain sekali per game
- Interactive phishing detection game
- Real-world email examples (legitimate vs phishing)
- 60 seconds, 3 lives system
- Streak bonus (+2pts per streak)
- Red flags education
- Admin dapat mengelola phishing scenarios

### 📚 Course System
- Interactive slide-based learning
- Module-by-module progression
- Progress tracking per user
- Auto-generated certificates
- **Admin CRUD**: Full course management dengan modules & slides

### 🏆 Achievement & Gamification
- **Daily Challenge**: 2x points bonus
- **Streak System**: Track consecutive days active
- **8 Achievements**: Common, Rare, Epic, Legendary
- **Progress Heatmap**: GitHub-style activity calendar
- **Real-time Leaderboard**
- **Social Sharing**: Share certificates ke social media

### 👨‍💼 Admin Panel (Full CRUD)
- **Challenges**: Create, Edit, Delete dengan multi-question
- **Quiz Questions**: Manage quiz question pool
- **Mini Game Scenarios**: Manage phishing scenarios
- **Courses**: Module & slide management
- **Education**: Content management by Cialdini principle
- **Users**: Edit, Delete, Reset completions
- **Analytics Dashboard**: Platform statistics & recent activity

### 🔐 Security Features
- **Single-Play Enforcement**: Quiz, mini games, dan challenges hanya bisa diselesaikan sekali
- **RBAC** (Role-Based Access Control)
- **Rate Limiting**: Login (5/5min), Register (3/hour)
- JWT authentication
- Password hashing (bcrypt)
- Admin-only endpoints protection
- Input validation & sanitization

---

## 📊 Challenge Statistics

| Prinsip Cialdini | Challenges | Pertanyaan | Level Distribution |
|------------------|------------|------------|-------------------|
| Reciprocity | 6 | 60+ | 2 Beginner, 2 Intermediate, 2 Advanced |
| Commitment | 5 | 50+ | 1 Beginner, 2 Intermediate, 2 Advanced |
| Social Proof | 5 | 50+ | 1 Beginner, 2 Intermediate, 2 Advanced |
| Authority | 5 | 50+ | 1 Beginner, 2 Intermediate, 2 Advanced |
| Liking | 5 | 40+ | 2 Beginner, 2 Intermediate, 1 Advanced |
| Scarcity | 5 | 40+ | 2 Beginner, 2 Intermediate, 1 Advanced |
| Advanced | 5+ | 30+ | All Advanced |
| **TOTAL** | **36+** | **320+** | **Balanced Mix** |

---

## 🔧 Troubleshooting

### Challenges tidak muncul
```bash
cd backend
python seed_data.py
python seed_indonesia_challenges.py
python seed_massive_challenges.py
python seed_final_10.py
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

# Restart services
sudo supervisorctl restart backend
```

---

## 📖 API Documentation

Access interactive API docs: **http://localhost:8001/docs**

### Key Endpoints

**Authentication:**
- `POST /api/auth/register` - Register user
- `POST /api/auth/login` - Login user
- `POST /api/auth/forgot-password` - Request reset
- `POST /api/auth/reset-password` - Reset password

**Challenges:**
- `GET /api/challenges` - List all challenges
- `GET /api/challenges/{id}` - Get challenge detail
- `POST /api/challenges/{id}/attempt` - Submit attempt
- `GET /api/challenges/{id}/completion` - Check completion status

**Quiz:**
- `GET /api/quiz/random` - Get random quiz
- `POST /api/quiz/submit` - Submit quiz
- `GET /api/quiz/completion-status` - Check if completed

**Mini Game:**
- `GET /api/minigame/scenarios/{game_type}` - Get scenarios
- `POST /api/minigame/complete` - Record completion
- `GET /api/minigame/completion-status/{game_type}` - Check status

**Admin (Requires admin role):**
- `GET /api/admin/stats` - Platform statistics
- `POST /api/admin/challenges` - Create challenge
- `POST /api/admin/quiz-questions` - Create quiz question
- `POST /api/admin/minigame-scenarios` - Create scenario
- `POST /api/admin/reset-completion` - Reset user completions
- `PUT /api/admin/users/{id}` - Update user
- `DELETE /api/admin/users/{id}` - Delete user

---

## 🎯 Learning Outcomes

Setelah menyelesaikan lab ini, peserta akan mampu:

✅ **Memahami** 6 prinsip psikologi Cialdini yang dieksploitasi dalam social engineering  
✅ **Mengidentifikasi** red flags dari berbagai jenis serangan  
✅ **Mendeteksi** modus penipuan umum di Indonesia (crypto, MLM, romance, job scam)  
✅ **Menerapkan** defense strategies dalam kehidupan sehari-hari  
✅ **Melakukan** analisis kritis terhadap permintaan informasi  
✅ **Menggunakan** teknik verifikasi untuk memvalidasi legitimacy

---

## 🛠️ Tech Stack

- **Frontend**: React 19 + Tailwind CSS + Shadcn/UI
- **Backend**: FastAPI (Python 3.11+)
- **Database**: MongoDB 7.0
- **Authentication**: JWT dengan bcrypt
- **Deployment**: Docker + Docker Compose
- **Icons**: Lucide React
- **Animations**: Canvas Confetti + CSS animations

---

## 🤝 Contributing

Contributions welcome! Areas untuk improvement:
- More Indonesian case studies
- Additional Cialdini principle challenges
- Course content expansion
- Quiz questions & mini game scenarios
- UI/UX enhancements
- Security hardening

---

## ⚠️ Disclaimer

Platform ini dibuat untuk **tujuan edukasi cybersecurity awareness**. Pengetahuan yang diperoleh HARUS digunakan secara etis dan bertanggung jawab.

**Tegalsec Community tidak bertanggung jawab atas penyalahgunaan informasi dari platform ini.**

---

## 📞 Contact & Support

- **Website**: https://tegalsec.org
- **GitHub**: https://github.com/tegal1337
- **Discord**: Join our community (link on website)
- **Email**: info@tegalsec.org

---

## 📄 License

Educational Purpose - © Tegalsec Community 2024-2025

---

## 🙏 Credits

**Developed by:** Tegalsec Community (tegalsec.org)  
**Inspiration:** DVWA, Cialdini's "Influence: The Psychology of Persuasion"  
**Framework:** React + FastAPI + MongoDB

Kasus-kasus dibuat berdasarkan real incidents di Indonesia untuk meningkatkan cyber awareness 🇮🇩

---

**Made with 🔐 by Tegalsec Community** | Version 5.0 - Single-Play System & Enhanced Admin Control
