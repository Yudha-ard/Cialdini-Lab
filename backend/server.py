from fastapi import FastAPI, APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import List, Optional
import uuid
from datetime import datetime, timezone, timedelta
from passlib.context import CryptContext
import jwt

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Security
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()
SECRET_KEY = os.environ.get('JWT_SECRET', 'tegalsec-secret-key-2025')
ALGORITHM = "HS256"

app = FastAPI()
api_router = APIRouter(prefix="/api")

# ===== MODELS =====
class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str
    full_name: str

class UserLogin(BaseModel):
    username: str
    password: str

class User(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    username: str
    email: str
    full_name: str
    role: str = "user"  # user or admin
    points: int = 0
    level: str = "Beginner"
    completed_challenges: List[str] = []
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class QuestionItem(BaseModel):
    question: str
    options: List[str]
    correct_answer: int
    explanation: str

class Challenge(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    category: str  # phishing, pretexting, baiting, quid_pro_quo, tailgating, money_app, indonesian_case
    difficulty: str  # beginner, intermediate, advanced
    cialdini_principle: str  # reciprocity, commitment, social_proof, authority, liking, scarcity
    challenge_type: str = "multi_choice"  # multi_choice, chat_simulation, email_analysis, spot_difference, timeline_ordering
    description: str
    scenario: str
    questions: List[QuestionItem]  # Multi-question support
    points: int
    tips: List[str]
    real_case_reference: Optional[str] = None
    time_limit_seconds: Optional[int] = None
    interactive_data: Optional[dict] = None  # For chat, email, etc simulations
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ChallengeAttempt(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    challenge_id: str
    answers: List[int]  # Multiple answers for multi-question
    correct_count: int
    total_questions: int
    is_completed: bool
    points_earned: int
    time_taken_seconds: Optional[int] = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ChallengeFeedback(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    challenge_id: str
    rating: int  # 1-5
    comment: str
    username: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class EducationContent(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    content_type: str  # cialdini_principle, prevention_tips, case_study
    content: str
    principle: Optional[str] = None

# ===== AUTH HELPERS =====
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=7)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        user = await db.users.find_one({"id": user_id}, {"_id": 0})
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

# ===== AUTH ROUTES =====
@api_router.post("/auth/register")
async def register(user_data: UserRegister):
    # Check if username exists
    existing = await db.users.find_one({"username": user_data.username})
    if existing:
        raise HTTPException(status_code=400, detail="Username sudah digunakan")
    
    # Check if email exists
    existing_email = await db.users.find_one({"email": user_data.email})
    if existing_email:
        raise HTTPException(status_code=400, detail="Email sudah terdaftar")
    
    # Create user
    user = User(
        username=user_data.username,
        email=user_data.email,
        full_name=user_data.full_name
    )
    
    user_dict = user.model_dump()
    user_dict['password'] = hash_password(user_data.password)
    user_dict['created_at'] = user_dict['created_at'].isoformat()
    
    await db.users.insert_one(user_dict)
    
    token = create_access_token({"sub": user.id})
    return {"token": token, "user": user.model_dump()}

@api_router.post("/auth/login")
async def login(login_data: UserLogin):
    user = await db.users.find_one({"username": login_data.username}, {"_id": 0})
    if not user or not verify_password(login_data.password, user['password']):
        raise HTTPException(status_code=401, detail="Username atau password salah")
    
    token = create_access_token({"sub": user['id']})
    user.pop('password')
    return {"token": token, "user": user}

@api_router.get("/auth/me")
async def get_me(current_user: dict = Depends(get_current_user)):
    return current_user

# ===== CHALLENGE ROUTES =====
@api_router.get("/challenges", response_model=List[Challenge])
async def get_challenges(category: Optional[str] = None, difficulty: Optional[str] = None):
    query = {}
    if category:
        query['category'] = category
    if difficulty:
        query['difficulty'] = difficulty
    
    challenges = await db.challenges.find(query, {"_id": 0}).to_list(1000)
    for ch in challenges:
        if isinstance(ch['created_at'], str):
            ch['created_at'] = datetime.fromisoformat(ch['created_at'])
    return challenges

@api_router.get("/challenges/{challenge_id}")
async def get_challenge(challenge_id: str):
    challenge = await db.challenges.find_one({"id": challenge_id}, {"_id": 0})
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge tidak ditemukan")
    if isinstance(challenge['created_at'], str):
        challenge['created_at'] = datetime.fromisoformat(challenge['created_at'])
    return challenge

@api_router.post("/challenges/{challenge_id}/attempt")
async def attempt_challenge(challenge_id: str, answer: dict, current_user: dict = Depends(get_current_user)):
    challenge = await db.challenges.find_one({"id": challenge_id}, {"_id": 0})
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge tidak ditemukan")
    
    answers = answer.get('answers', [])
    time_taken = answer.get('time_taken_seconds', 0)
    
    # Calculate correct answers
    correct_count = 0
    total_questions = len(challenge['questions'])
    results = []
    
    for idx, (user_ans, question) in enumerate(zip(answers, challenge['questions'])):
        is_correct = user_ans == question['correct_answer']
        if is_correct:
            correct_count += 1
        results.append({
            "question_index": idx,
            "is_correct": is_correct,
            "explanation": question['explanation']
        })
    
    # Calculate points (partial credit for getting some right)
    base_points = challenge['points']
    points_per_question = base_points / total_questions
    points_earned = int(correct_count * points_per_question)
    is_completed = correct_count == total_questions
    
    # Save attempt
    attempt = ChallengeAttempt(
        user_id=current_user['id'],
        challenge_id=challenge_id,
        answers=answers,
        correct_count=correct_count,
        total_questions=total_questions,
        is_completed=is_completed,
        points_earned=points_earned,
        time_taken_seconds=time_taken
    )
    attempt_dict = attempt.model_dump()
    attempt_dict['timestamp'] = attempt_dict['timestamp'].isoformat()
    await db.attempts.insert_one(attempt_dict)
    
    # Update user progress if completed and not already completed
    if is_completed and challenge_id not in current_user.get('completed_challenges', []):
        new_points = current_user.get('points', 0) + points_earned
        completed = current_user.get('completed_challenges', [])
        completed.append(challenge_id)
        
        # Update level based on points
        level = "Beginner"
        if new_points >= 500:
            level = "Advanced"
        elif new_points >= 200:
            level = "Intermediate"
        
        await db.users.update_one(
            {"id": current_user['id']},
            {"$set": {
                "points": new_points,
                "completed_challenges": completed,
                "level": level
            }}
        )
    
    return {
        "correct_count": correct_count,
        "total_questions": total_questions,
        "is_completed": is_completed,
        "points_earned": points_earned,
        "results": results,
        "tips": challenge['tips']
    }

# ===== LEADERBOARD =====
@api_router.get("/leaderboard")
async def get_leaderboard():
    users = await db.users.find({}, {"_id": 0, "password": 0}).to_list(1000)
    sorted_users = sorted(users, key=lambda x: x.get('points', 0), reverse=True)[:10]
    return sorted_users

# ===== CHALLENGE FEEDBACK =====
@api_router.post("/challenges/{challenge_id}/feedback")
async def add_feedback(challenge_id: str, feedback_data: dict, current_user: dict = Depends(get_current_user)):
    challenge = await db.challenges.find_one({"id": challenge_id}, {"_id": 0})
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge tidak ditemukan")
    
    feedback = ChallengeFeedback(
        user_id=current_user['id'],
        challenge_id=challenge_id,
        rating=feedback_data.get('rating', 5),
        comment=feedback_data.get('comment', ''),
        username=current_user['username']
    )
    
    feedback_dict = feedback.model_dump()
    feedback_dict['created_at'] = feedback_dict['created_at'].isoformat()
    await db.feedbacks.insert_one(feedback_dict)
    
    return {"message": "Feedback berhasil dikirim"}

@api_router.get("/challenges/{challenge_id}/feedback")
async def get_feedback(challenge_id: str):
    feedbacks = await db.feedbacks.find({"challenge_id": challenge_id}, {"_id": 0}).sort("created_at", -1).to_list(100)
    for fb in feedbacks:
        if isinstance(fb['created_at'], str):
            fb['created_at'] = datetime.fromisoformat(fb['created_at'])
    return feedbacks

# ===== USER PROGRESS =====
@api_router.get("/progress")
async def get_progress(current_user: dict = Depends(get_current_user)):
    total_challenges = await db.challenges.count_documents({})
    completed = len(current_user.get('completed_challenges', []))
    attempts = await db.attempts.find({"user_id": current_user['id']}, {"_id": 0}).to_list(1000)
    
    return {
        "total_challenges": total_challenges,
        "completed_challenges": completed,
        "points": current_user.get('points', 0),
        "level": current_user.get('level', 'Beginner'),
        "recent_attempts": attempts[-5:] if len(attempts) > 5 else attempts
    }

# ===== EDUCATION CONTENT =====
@api_router.get("/education", response_model=List[EducationContent])
async def get_education_content(content_type: Optional[str] = None):
    query = {}
    if content_type:
        query['content_type'] = content_type
    contents = await db.education.find(query, {"_id": 0}).to_list(1000)
    return contents

# ===== ADMIN ROUTES =====
@api_router.post("/admin/challenges")
async def create_challenge(challenge: Challenge, current_user: dict = Depends(get_current_user)):
    if current_user.get('role') != 'admin':
        raise HTTPException(status_code=403, detail="Akses ditolak")
    
    challenge_dict = challenge.model_dump()
    challenge_dict['created_at'] = challenge_dict['created_at'].isoformat()
    await db.challenges.insert_one(challenge_dict)
    return challenge

@api_router.get("/admin/stats")
async def get_admin_stats(current_user: dict = Depends(get_current_user)):
    if current_user.get('role') != 'admin':
        raise HTTPException(status_code=403, detail="Akses ditolak")
    
    total_users = await db.users.count_documents({})
    total_challenges = await db.challenges.count_documents({})
    total_attempts = await db.attempts.count_documents({})
    
    return {
        "total_users": total_users,
        "total_challenges": total_challenges,
        "total_attempts": total_attempts
    }

app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()