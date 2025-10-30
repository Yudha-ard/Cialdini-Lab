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
    streak_days: int = 0
    last_active_date: Optional[str] = None
    daily_challenge_completed: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    email: EmailStr
    reset_code: str
    new_password: str

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

class Badge(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str
    name: str
    description: str
    icon: str
    requirement: str

class UserBadge(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    badge_id: str
    earned_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class HintRequest(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    challenge_id: str
    question_index: int
    hint_cost: int = 10
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class CourseSlide(BaseModel):
    title: str
    content: str
    code_example: Optional[str] = None
    image_url: Optional[str] = None

class CourseModule(BaseModel):
    module_number: int
    title: str
    description: str
    slides: List[CourseSlide]

class Course(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: str
    category: str
    difficulty: str
    modules: List[CourseModule]
    total_duration_minutes: int
    prerequisites: List[str] = []
    learning_outcomes: List[str] = []
    created_by: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class CourseProgress(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    course_id: str
    completed_modules: List[int] = []
    current_slide: int = 0
    completed: bool = False
    started_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    completed_at: Optional[datetime] = None

class Certificate(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    username: str
    full_name: str
    achievement_type: str  # course_completion, all_challenges, expert_level
    achievement_title: str
    issued_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    certificate_code: str = Field(default_factory=lambda: str(uuid.uuid4())[:8].upper())

class QuizCompletion(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    quiz_data: dict  # Store the quiz questions and answers
    correct_count: int
    total_questions: int
    points_earned: int
    time_taken_seconds: int
    accuracy: float
    completed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class MiniGameCompletion(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    game_type: str  # spot_the_phishing, etc
    score: int
    time_taken_seconds: int
    details: dict  # Store game-specific data
    completed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class QuizQuestion(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    question: str
    options: List[str]
    correct_answer: int
    explanation: str
    category: str
    difficulty: str
    created_by: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class MiniGameScenario(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    game_type: str  # spot_the_phishing
    title: str
    description: str
    image_url: str
    is_phishing: bool
    indicators: List[str]
    difficulty: str
    created_by: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

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


# ===== RBAC HELPER =====
async def require_admin(current_user: dict = Depends(get_current_user)):
    """Dependency untuk memastikan user adalah admin"""
    if current_user.get('role') != 'admin':
        raise HTTPException(
            status_code=403, 
            detail="Forbidden: Admin access required"
        )
    return current_user

# ===== RATE LIMITING =====
from collections import defaultdict
from time import time

# Simple in-memory rate limiter
rate_limit_store = defaultdict(list)
RATE_LIMIT_LOGIN = 5  # 5 attempts
RATE_LIMIT_WINDOW = 300  # 5 minutes

def check_rate_limit(identifier: str, limit: int = RATE_LIMIT_LOGIN, window: int = RATE_LIMIT_WINDOW):
    """Check if request is within rate limit"""
    now = time()
    # Clean old entries
    rate_limit_store[identifier] = [
        timestamp for timestamp in rate_limit_store[identifier]
        if now - timestamp < window
    ]
    
    if len(rate_limit_store[identifier]) >= limit:
        oldest = rate_limit_store[identifier][0]
        wait_time = int(window - (now - oldest))
        raise HTTPException(
            status_code=429,
            detail=f"Too many requests. Try again in {wait_time} seconds"
        )
    
    rate_limit_store[identifier].append(now)


# ===== AUTH ROUTES =====
@api_router.post("/auth/register")
async def register(user_data: UserRegister):
    # Rate limiting by username
    check_rate_limit(f"register_{user_data.username}", limit=3, window=3600)  # 3 attempts per hour
    
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
    # Rate limiting by username
    check_rate_limit(f"login_{login_data.username}", limit=5, window=300)  # 5 attempts per 5 minutes
    
    user = await db.users.find_one({"username": login_data.username}, {"_id": 0})
    if not user or not verify_password(login_data.password, user['password']):
        raise HTTPException(status_code=401, detail="Username atau password salah")
    
    token = create_access_token({"sub": user['id']})
    user.pop('password')
    return {"token": token, "user": user}

@api_router.get("/auth/me")
async def get_me(current_user: dict = Depends(get_current_user)):
    # Update streak
    today = datetime.now(timezone.utc).date().isoformat()
    last_active = current_user.get('last_active_date')
    
    if last_active != today:
        yesterday = (datetime.now(timezone.utc).date() - timedelta(days=1)).isoformat()
        if last_active == yesterday:
            # Continue streak
            new_streak = current_user.get('streak_days', 0) + 1
        else:
            # Reset streak
            new_streak = 1
        
        await db.users.update_one(
            {"id": current_user['id']},
            {"$set": {
                "last_active_date": today,
                "streak_days": new_streak,
                "daily_challenge_completed": False
            }}
        )
        current_user['streak_days'] = new_streak
        current_user['last_active_date'] = today
        current_user['daily_challenge_completed'] = False
    
    return current_user

@api_router.post("/auth/forgot-password")
async def forgot_password(request: ForgotPasswordRequest):
    user = await db.users.find_one({"email": request.email})
    if not user:
        # Don't reveal if email exists (security)
        return {"message": "Jika email terdaftar, kode reset telah dikirim"}
    
    # Generate 6-digit code
    import random
    reset_code = str(random.randint(100000, 999999))
    
    # Save reset code (expires in 10 minutes)
    await db.password_resets.insert_one({
        "email": request.email,
        "code": reset_code,
        "expires_at": (datetime.now(timezone.utc) + timedelta(minutes=10)).isoformat(),
        "created_at": datetime.now(timezone.utc).isoformat()
    })
    
    # In production, send email here. For demo, return code
    return {"message": "Kode reset telah dikirim ke email", "reset_code": reset_code}

@api_router.post("/auth/reset-password")
async def reset_password(request: ResetPasswordRequest):
    # Find valid reset code
    reset_record = await db.password_resets.find_one({
        "email": request.email,
        "code": request.reset_code
    })
    
    if not reset_record:
        raise HTTPException(status_code=400, detail="Kode reset tidak valid")
    
    # Check expiration
    expires_at = datetime.fromisoformat(reset_record['expires_at'])
    if datetime.now(timezone.utc) > expires_at:
        raise HTTPException(status_code=400, detail="Kode reset sudah expired")
    
    # Update password
    hashed = hash_password(request.new_password)
    await db.users.update_one(
        {"email": request.email},
        {"$set": {"password": hashed}}
    )
    
    # Delete used reset code
    await db.password_resets.delete_one({"_id": reset_record['_id']})
    
    return {"message": "Password berhasil direset"}

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
    
    # Check if challenge already completed (SINGLE-PLAY RESTRICTION)
    if challenge_id in current_user.get('completed_challenges', []):
        # Get previous attempt
        previous_attempt = await db.challenge_attempts.find_one(
            {"user_id": current_user['id'], "challenge_id": challenge_id, "is_completed": True},
            {"_id": 0},
            sort=[("timestamp", -1)]
        )
        if previous_attempt:
            raise HTTPException(
                status_code=400,
                detail={
                    "message": "Challenge ini sudah pernah diselesaikan. Kamu hanya bisa menyelesaikan challenge sekali.",
                    "previous_result": {
                        "correct_count": previous_attempt['correct_count'],
                        "total_questions": previous_attempt['total_questions'],
                        "points_earned": previous_attempt['points_earned'],
                        "time_taken_seconds": previous_attempt.get('time_taken_seconds'),
                        "completed_at": previous_attempt['timestamp']
                    }
                }
            )
    
    answers = answer.get('answers', [])
    time_taken = answer.get('time_taken_seconds', 0)
    is_daily = answer.get('is_daily_challenge', False)
    
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
    
    # Calculate points with TIME BONUS
    base_points = challenge['points']
    points_per_question = base_points / total_questions
    earned_points = correct_count * points_per_question
    
    # Time bonus calculation
    time_limit = challenge.get('time_limit_seconds', 300)
    time_bonus = 0
    speed_multiplier = 1.0
    
    if time_taken > 0 and time_taken < time_limit:
        # Speed bonus: finish under 50% time = 1.5x, under 30% = 2x
        time_ratio = time_taken / time_limit
        if time_ratio < 0.3:
            speed_multiplier = 2.0
            time_bonus = int(earned_points * 1.0)  # 100% bonus
        elif time_ratio < 0.5:
            speed_multiplier = 1.5
            time_bonus = int(earned_points * 0.5)  # 50% bonus
        elif time_ratio < 0.7:
            speed_multiplier = 1.2
            time_bonus = int(earned_points * 0.2)  # 20% bonus
    
    final_points = int(earned_points + time_bonus)
    
    # Daily challenge bonus (2x points)
    if is_daily and not current_user.get('daily_challenge_completed', False):
        final_points = final_points * 2
        await db.users.update_one(
            {"id": current_user['id']},
            {"$set": {"daily_challenge_completed": True}}
        )
    
    is_completed = correct_count == total_questions
    
    # Save attempt
    attempt = ChallengeAttempt(
        user_id=current_user['id'],
        challenge_id=challenge_id,
        answers=answers,
        correct_count=correct_count,
        total_questions=total_questions,
        is_completed=is_completed,
        points_earned=final_points,
        time_taken_seconds=time_taken
    )
    attempt_dict = attempt.model_dump()
    attempt_dict['timestamp'] = attempt_dict['timestamp'].isoformat()
    await db.challenge_attempts.insert_one(attempt_dict)
    
    # Update user progress if completed and not already completed
    if is_completed and challenge_id not in current_user.get('completed_challenges', []):
        new_points = current_user.get('points', 0) + final_points
        completed = current_user.get('completed_challenges', [])
        completed.append(challenge_id)
        
        # Update level based on points
        level = "Beginner"
        if new_points >= 1000:
            level = "Expert"
        elif new_points >= 500:
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
        "points_earned": final_points,
        "time_bonus": time_bonus,
        "speed_multiplier": speed_multiplier,
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


# ===== USER PROFILE =====
@api_router.put("/user/profile")
async def update_user_profile(
    full_name: str,
    email: str,
    current_user: dict = Depends(get_current_user)
):
    await db.users.update_one(
        {"id": current_user['id']},
        {"$set": {"full_name": full_name, "email": email}}
    )
    return {"message": "Profile updated successfully"}

@api_router.put("/user/change-password")
async def change_password(
    current_password: str,
    new_password: str,
    current_user: dict = Depends(get_current_user)
):
    # Verify current password
    if not pwd_context.verify(current_password, current_user['password']):
        raise HTTPException(status_code=400, detail="Password saat ini salah")
    
    # Hash and update new password
    hashed_password = pwd_context.hash(new_password)
    await db.users.update_one(
        {"id": current_user['id']},
        {"$set": {"password": hashed_password}}
    )
    return {"message": "Password changed successfully"}


# ===== EDUCATION CONTENT =====
@api_router.get("/education", response_model=List[EducationContent])
async def get_education_content(content_type: Optional[str] = None):
    query = {}
    if content_type:
        query['content_type'] = content_type
    contents = await db.education.find(query, {"_id": 0}).to_list(1000)
    return contents

@api_router.post("/admin/education")
async def create_education(content: EducationContent, admin_user: dict = Depends(require_admin)):
    content_dict = content.model_dump()
    await db.education.insert_one(content_dict)
    return content

@api_router.put("/admin/education/{content_id}")
async def update_education(content_id: str, content: EducationContent, admin_user: dict = Depends(require_admin)):
    content_dict = content.model_dump()
    result = await db.education.update_one(
        {"id": content_id},
        {"$set": content_dict}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Content tidak ditemukan")
    
    return {"message": "Content berhasil diupdate"}

@api_router.delete("/admin/education/{content_id}")
async def delete_education(content_id: str, admin_user: dict = Depends(require_admin)):
    result = await db.education.delete_one({"id": content_id})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Content tidak ditemukan")
    
    return {"message": "Content berhasil dihapus"}

# ===== DAILY CHALLENGE =====
@api_router.get("/daily-challenge")
async def get_daily_challenge():
    # Get a random challenge for today (same challenge for everyone today)
    import hashlib
    today = datetime.now(timezone.utc).date().isoformat()
    seed = int(hashlib.md5(today.encode()).hexdigest(), 16)
    
    all_challenges = await db.challenges.find({}, {"_id": 0}).to_list(1000)
    if not all_challenges:
        raise HTTPException(status_code=404, detail="Tidak ada challenge tersedia")
    
    # Deterministic random based on date
    daily_index = seed % len(all_challenges)
    daily_challenge = all_challenges[daily_index]
    
    if isinstance(daily_challenge['created_at'], str):
        daily_challenge['created_at'] = datetime.fromisoformat(daily_challenge['created_at'])
    
    return {
        "challenge": daily_challenge,
        "bonus_multiplier": 2,
        "expires_in_hours": 24
    }

# ===== ADMIN ROUTES =====
@api_router.post("/admin/challenges")
async def create_challenge(challenge: Challenge, current_user: dict = Depends(get_current_user)):
    if current_user.get('role') != 'admin':
        raise HTTPException(status_code=403, detail="Akses ditolak")
    
    challenge_dict = challenge.model_dump()
    challenge_dict['created_at'] = challenge_dict['created_at'].isoformat()
    await db.challenges.insert_one(challenge_dict)
    return challenge

@api_router.put("/admin/challenges/{challenge_id}")
async def update_challenge(challenge_id: str, challenge: Challenge, current_user: dict = Depends(get_current_user)):
    if current_user.get('role') != 'admin':
        raise HTTPException(status_code=403, detail="Akses ditolak")
    
    challenge_dict = challenge.model_dump()
    challenge_dict['created_at'] = challenge_dict['created_at'].isoformat()
    
    result = await db.challenges.update_one(
        {"id": challenge_id},
        {"$set": challenge_dict}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Challenge tidak ditemukan")
    
    return {"message": "Challenge berhasil diupdate"}

@api_router.delete("/admin/challenges/{challenge_id}")
async def delete_challenge(challenge_id: str, current_user: dict = Depends(get_current_user)):
    if current_user.get('role') != 'admin':
        raise HTTPException(status_code=403, detail="Akses ditolak")
    
    result = await db.challenges.delete_one({"id": challenge_id})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Challenge tidak ditemukan")
    
    return {"message": "Challenge berhasil dihapus"}

@api_router.get("/admin/users")
async def get_all_users(admin_user: dict = Depends(require_admin)):
    users = await db.users.find({}, {"_id": 0, "password": 0}).to_list(1000)
    return users

@api_router.get("/admin/stats")
async def get_admin_stats(admin_user: dict = Depends(require_admin)):
    total_users = await db.users.count_documents({})
    total_challenges = await db.challenges.count_documents({})
    total_attempts = await db.challenge_attempts.count_documents({})
    total_feedbacks = await db.feedbacks.count_documents({})
    
    # Recent activity
    recent_attempts = await db.challenge_attempts.find(
        {}, 
        {"_id": 0}
    ).sort("timestamp", -1).limit(10).to_list(10)
    
    recent_feedbacks = await db.feedbacks.find(
        {}, 
        {"_id": 0}
    ).sort("created_at", -1).limit(10).to_list(10)
    
    return {
        "total_users": total_users,
        "total_challenges": total_challenges,
        "total_attempts": total_attempts,
        "total_feedbacks": total_feedbacks,
        "recent_attempts": recent_attempts,
        "recent_feedbacks": recent_feedbacks
    }

@api_router.put("/admin/users/{user_id}")
async def update_user_by_admin(
    user_id: str,
    full_name: str,
    email: str,
    password: Optional[str] = None,
    admin_user: dict = Depends(require_admin)
):
    update_data = {"full_name": full_name, "email": email}
    
    # Only update password if provided
    if password:
        update_data["password"] = pwd_context.hash(password)
    
    result = await db.users.update_one(
        {"id": user_id},
        {"$set": update_data}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="User tidak ditemukan")
    
    return {"message": "User updated successfully"}

@api_router.delete("/admin/users/{user_id}")
async def delete_user_by_admin(user_id: str, admin_user: dict = Depends(require_admin)):
    # Prevent deleting self
    if user_id == admin_user['id']:
        raise HTTPException(status_code=400, detail="Tidak bisa menghapus akun sendiri")
    
    result = await db.users.delete_one({"id": user_id})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User tidak ditemukan")
    
    return {"message": "User deleted successfully"}

# ===== HINTS SYSTEM =====
@api_router.post("/challenges/{challenge_id}/hint")
async def get_hint(challenge_id: str, hint_data: dict, current_user: dict = Depends(get_current_user)):
    question_index = hint_data.get('question_index')
    
    challenge = await db.challenges.find_one({"id": challenge_id}, {"_id": 0})
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge tidak ditemukan")
    
    if question_index >= len(challenge['questions']):
        raise HTTPException(status_code=400, detail="Question index invalid")
    
    # Check if user has enough points
    user_points = current_user.get('points', 0)
    hint_cost = 10
    
    if user_points < hint_cost:
        raise HTTPException(status_code=400, detail="Poin tidak cukup untuk hint")
    
    # Deduct points
    new_points = user_points - hint_cost
    await db.users.update_one(
        {"id": current_user['id']},
        {"$set": {"points": new_points}}
    )
    
    # Save hint request
    hint_req = HintRequest(
        user_id=current_user['id'],
        challenge_id=challenge_id,
        question_index=question_index,
        hint_cost=hint_cost
    )
    hint_dict = hint_req.model_dump()
    hint_dict['created_at'] = hint_dict['created_at'].isoformat()
    await db.hints.insert_one(hint_dict)
    
    # Generate hint (first 50% of explanation)
    explanation = challenge['questions'][question_index]['explanation']
    hint_text = explanation[:len(explanation)//2] + "..."
    
    return {
        "hint": hint_text,
        "points_remaining": new_points,
        "hint_cost": hint_cost
    }

# ===== BADGES/ACHIEVEMENTS =====
@api_router.get("/badges")
async def get_badges():
    badges = [
        {"id": "first_blood", "name": "First Blood", "description": "Selesaikan challenge pertama", "icon": "🎯", "requirement": "Complete 1 challenge"},
        {"id": "phishing_hunter", "name": "Phishing Hunter", "description": "Selesaikan 3 challenge phishing", "icon": "🎣", "requirement": "Complete 3 phishing challenges"},
        {"id": "social_expert", "name": "Social Expert", "description": "Selesaikan semua kategori challenge", "icon": "🏆", "requirement": "Complete all categories"},
        {"id": "speed_demon", "name": "Speed Demon", "description": "Selesaikan challenge dalam <1 menit", "icon": "⚡", "requirement": "Complete challenge in under 60 seconds"},
        {"id": "perfectionist", "name": "Perfectionist", "description": "Dapat 100% di 5 challenge", "icon": "💎", "requirement": "Get 100% on 5 challenges"},
    ]
    return badges

@api_router.get("/user/badges")
async def get_user_badges(current_user: dict = Depends(get_current_user)):
    # Check earned badges based on user progress
    attempts = await db.attempts.find({"user_id": current_user['id']}, {"_id": 0}).to_list(1000)
    completed = current_user.get('completed_challenges', [])
    
    earned_badges = []
    
    # First Blood
    if len(completed) >= 1:
        earned_badges.append("first_blood")
    
    # Perfectionist - 5 perfect scores
    perfect_count = sum(1 for att in attempts if att.get('is_completed', False))
    if perfect_count >= 5:
        earned_badges.append("perfectionist")
    
    return {"earned_badges": earned_badges}

# ===== COURSES SYSTEM =====
@api_router.get("/courses")
async def get_courses(category: Optional[str] = None):
    query = {}
    if category:
        query['category'] = category
    courses = await db.courses.find(query, {"_id": 0}).to_list(1000)
    for course in courses:
        if isinstance(course.get('created_at'), str):
            course['created_at'] = datetime.fromisoformat(course['created_at'])
    return courses

@api_router.get("/courses/{course_id}")
async def get_course(course_id: str):
    course = await db.courses.find_one({"id": course_id}, {"_id": 0})
    if not course:
        raise HTTPException(status_code=404, detail="Course tidak ditemukan")
    if isinstance(course.get('created_at'), str):
        course['created_at'] = datetime.fromisoformat(course['created_at'])
    return course

@api_router.post("/admin/courses")
async def create_course(course: Course, admin_user: dict = Depends(require_admin)):
    course_dict = course.model_dump()
    course_dict['created_at'] = course_dict['created_at'].isoformat()
    course_dict['created_by'] = admin_user['username']
    await db.courses.insert_one(course_dict)
    return course

@api_router.put("/admin/courses/{course_id}")
async def update_course(course_id: str, course: Course, admin_user: dict = Depends(require_admin)):
    course_dict = course.model_dump()
    course_dict['created_at'] = course_dict['created_at'].isoformat()
    
    # Remove id field to prevent overwriting the existing course ID
    if 'id' in course_dict:
        del course_dict['id']
    
    result = await db.courses.update_one(
        {"id": course_id},
        {"$set": course_dict}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Course tidak ditemukan")
    
    return {"message": "Course berhasil diupdate"}

@api_router.delete("/admin/courses/{course_id}")
async def delete_course(course_id: str, admin_user: dict = Depends(require_admin)):
    result = await db.courses.delete_one({"id": course_id})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Course tidak ditemukan")
    
    return {"message": "Course berhasil dihapus"}

@api_router.post("/courses/{course_id}/progress")
async def update_course_progress(course_id: str, progress_data: dict, current_user: dict = Depends(get_current_user)):
    module_number = progress_data.get('module_number')
    slide_number = progress_data.get('slide_number')
    
    # Get or create progress
    progress = await db.course_progress.find_one({
        "user_id": current_user['id'],
        "course_id": course_id
    })
    
    if not progress:
        new_progress = CourseProgress(
            user_id=current_user['id'],
            course_id=course_id
        )
        progress_dict = new_progress.model_dump()
        progress_dict['started_at'] = progress_dict['started_at'].isoformat()
        await db.course_progress.insert_one(progress_dict)
        progress = progress_dict
    
    # Update progress
    completed_modules = progress.get('completed_modules', [])
    if module_number not in completed_modules:
        completed_modules.append(module_number)
    
    await db.course_progress.update_one(
        {"user_id": current_user['id'], "course_id": course_id},
        {"$set": {
            "completed_modules": completed_modules,
            "current_slide": slide_number
        }}
    )
    
    return {"message": "Progress updated"}

@api_router.get("/courses/{course_id}/progress")
async def get_course_progress(course_id: str, current_user: dict = Depends(get_current_user)):
    progress = await db.course_progress.find_one({
        "user_id": current_user['id'],
        "course_id": course_id
    }, {"_id": 0})
    
    return progress or {"completed_modules": [], "current_slide": 0}

# ===== CERTIFICATES =====
@api_router.get("/certificates")
async def get_user_certificates(current_user: dict = Depends(get_current_user)):
    certificates = await db.certificates.find(
        {"user_id": current_user['id']},
        {"_id": 0}
    ).to_list(100)
    
    # Check for auto-issuable certificates
    completed = len(current_user.get('completed_challenges', []))
    total_challenges = await db.challenges.count_documents({})
    
    # Auto-issue certificate for completing all challenges
    if completed == total_challenges and completed > 0:
        existing = await db.certificates.find_one({
            "user_id": current_user['id'],
            "achievement_type": "all_challenges"
        })
        
        if not existing:
            cert = Certificate(
                user_id=current_user['id'],
                username=current_user['username'],
                full_name=current_user['full_name'],
                achievement_type="all_challenges",
                achievement_title="Master of Social Engineering Defense"
            )
            cert_dict = cert.model_dump()
            cert_dict['issued_at'] = cert_dict['issued_at'].isoformat()
            await db.certificates.insert_one(cert_dict)
            certificates.append(cert_dict)
    
    return certificates

@api_router.get("/certificates/{certificate_id}")
async def get_certificate(certificate_id: str):
    cert = await db.certificates.find_one({"id": certificate_id}, {"_id": 0})
    if not cert:
        raise HTTPException(status_code=404, detail="Certificate tidak ditemukan")
    return cert

# ===== QUIZ MODE (RAPID FIRE) =====
@api_router.get("/quiz/random")
async def get_random_quiz():
    # Get 10 random questions from quiz_questions collection
    # If no quiz questions exist, fallback to challenges
    quiz_questions_list = await db.quiz_questions.find({}, {"_id": 0}).to_list(1000)
    
    import random
    
    if quiz_questions_list and len(quiz_questions_list) >= 10:
        # Use dedicated quiz questions
        random.shuffle(quiz_questions_list)
        selected_questions = quiz_questions_list[:10]
        
        quiz_questions = []
        for q in selected_questions:
            quiz_questions.append({
                "challenge_title": q.get('category', 'Quiz'),
                "question": q['question'],
                "options": q['options'],
                "correct_answer": q['correct_answer'],
                "points": 10
            })
    else:
        # Fallback to challenges if no quiz questions
        challenges = await db.challenges.find({}, {"_id": 0}).to_list(1000)
        if not challenges:
            raise HTTPException(status_code=404, detail="Tidak ada quiz questions atau challenges tersedia")
        
        random.shuffle(challenges)
        
        quiz_questions = []
        for challenge in challenges[:10]:
            if challenge.get('questions'):
                q = random.choice(challenge['questions'])
                quiz_questions.append({
                    "challenge_title": challenge['title'],
                    "question": q['question'],
                    "options": q['options'],
                    "correct_answer": q['correct_answer'],
                    "points": 10
                })
    
    return {
        "questions": quiz_questions,
        "time_limit_seconds": 60,
        "total_points": len(quiz_questions) * 10
    }

@api_router.post("/quiz/submit")
async def submit_quiz(answers: dict, current_user: dict = Depends(get_current_user)):
    # Check if user has already completed a quiz (GLOBAL restriction)
    existing_completion = await db.quiz_completions.find_one(
        {"user_id": current_user['id']},
        {"_id": 0}
    )
    
    if existing_completion:
        raise HTTPException(
            status_code=400, 
            detail="Quiz sudah pernah diselesaikan. Kamu hanya bisa mengikuti quiz sekali."
        )
    
    user_answers = answers.get('answers', [])
    quiz_questions = answers.get('questions', [])
    time_taken = answers.get('time_taken', 60)
    
    correct = sum(1 for ua, q in zip(user_answers, quiz_questions) if ua == q.get('correct_answer'))
    total = len(quiz_questions)
    points = correct * 10
    
    # Bonus for speed
    if time_taken < 40:
        points = int(points * 1.5)
    
    # Update user points
    new_points = current_user.get('points', 0) + points
    await db.users.update_one(
        {"id": current_user['id']},
        {"$set": {"points": new_points}}
    )
    
    # Record completion
    completion_data = {
        "user_id": current_user['id'],
        "quiz_data": {
            "questions": quiz_questions,
            "answers": user_answers
        },
        "correct_count": correct,
        "total_questions": total,
        "points_earned": points,
        "time_taken_seconds": time_taken,
        "accuracy": round((correct / total) * 100, 1),
        "completed_at": datetime.now(timezone.utc).isoformat()
    }
    
    await db.quiz_completions.insert_one(completion_data)
    
    return {
        "correct": correct,
        "total": total,
        "points_earned": points,
        "accuracy": round((correct / total) * 100, 1)
    }

# ===== QUIZ COMPLETION STATUS =====
@api_router.get("/quiz/completion-status")
async def get_quiz_completion_status(current_user: dict = Depends(get_current_user)):
    """Check if user has completed any quiz (GLOBAL restriction)"""
    completion = await db.quiz_completions.find_one(
        {"user_id": current_user['id']},
        {"_id": 0}
    )
    
    if completion:
        return {
            "completed": True,
            "completion_data": {
                "correct_count": completion['correct_count'],
                "total_questions": completion['total_questions'],
                "points_earned": completion['points_earned'],
                "accuracy": completion['accuracy'],
                "time_taken_seconds": completion['time_taken_seconds'],
                "completed_at": completion['completed_at']
            }
        }
    
    return {"completed": False}

# ===== MINI GAME ENDPOINTS =====
@api_router.get("/minigame/completion-status/{game_type}")
async def get_minigame_completion_status(game_type: str, current_user: dict = Depends(get_current_user)):
    """Check if user has completed a specific mini game"""
    completion = await db.minigame_completions.find_one(
        {"user_id": current_user['id'], "game_type": game_type},
        {"_id": 0}
    )
    
    if completion:
        return {
            "completed": True,
            "completion_data": {
                "score": completion['score'],
                "time_taken_seconds": completion['time_taken_seconds'],
                "details": completion.get('details', {}),
                "completed_at": completion['completed_at']
            }
        }
    
    return {"completed": False}

@api_router.post("/minigame/complete")
async def complete_minigame(data: dict, current_user: dict = Depends(get_current_user)):
    """Record mini game completion"""
    game_type = data.get('game_type')
    score = data.get('score', 0)
    time_taken = data.get('time_taken_seconds', 0)
    details = data.get('details', {})
    
    # Check if already completed
    existing = await db.minigame_completions.find_one(
        {"user_id": current_user['id'], "game_type": game_type}
    )
    
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Mini game ini sudah pernah diselesaikan. Kamu hanya bisa bermain sekali."
        )
    
    completion_data = {
        "user_id": current_user['id'],
        "game_type": game_type,
        "score": score,
        "time_taken_seconds": time_taken,
        "details": details,
        "completed_at": datetime.now(timezone.utc).isoformat()
    }
    
    await db.minigame_completions.insert_one(completion_data)
    
    # Award points
    points_earned = score
    new_points = current_user.get('points', 0) + points_earned
    await db.users.update_one(
        {"id": current_user['id']},
        {"$set": {"points": new_points}}
    )
    
    return {
        "success": True,
        "points_earned": points_earned,
        "message": "Mini game berhasil diselesaikan!"
    }

@api_router.get("/minigame/scenarios/{game_type}")
async def get_minigame_scenarios(game_type: str):
    """Get all scenarios for a specific mini game type"""
    scenarios = await db.minigame_scenarios.find(
        {"game_type": game_type},
        {"_id": 0}
    ).to_list(1000)
    
    return scenarios

# ===== CHALLENGE COMPLETION STATUS =====
@api_router.get("/challenges/{challenge_id}/completion")
async def get_challenge_completion_status(challenge_id: str, current_user: dict = Depends(get_current_user)):
    """Check if user has completed a specific challenge"""
    attempt = await db.challenge_attempts.find_one(
        {"user_id": current_user['id'], "challenge_id": challenge_id, "is_completed": True},
        {"_id": 0}
    )
    
    if attempt:
        return {
            "completed": True,
            "completion_data": {
                "correct_count": attempt['correct_count'],
                "total_questions": attempt['total_questions'],
                "points_earned": attempt['points_earned'],
                "time_taken_seconds": attempt.get('time_taken_seconds'),
                "completed_at": attempt['timestamp']
            }
        }
    
    return {"completed": False}

# ===== ADMIN: RESET COMPLETION STATUS =====
@api_router.post("/admin/reset-completion")
async def reset_user_completion(data: dict, admin_user: dict = Depends(require_admin)):
    """Admin endpoint to reset user completion status"""
    user_id = data.get('user_id')
    completion_type = data.get('type')  # quiz, minigame, challenge
    specific_id = data.get('specific_id')  # For challenge_id or game_type
    
    if not user_id or not completion_type:
        raise HTTPException(status_code=400, detail="user_id and type are required")
    
    deleted_count = 0
    
    if completion_type == "quiz":
        result = await db.quiz_completions.delete_many({"user_id": user_id})
        deleted_count = result.deleted_count
    
    elif completion_type == "minigame":
        query = {"user_id": user_id}
        if specific_id:
            query["game_type"] = specific_id
        result = await db.minigame_completions.delete_many(query)
        deleted_count = result.deleted_count
    
    elif completion_type == "challenge":
        query = {"user_id": user_id}
        if specific_id:
            query["challenge_id"] = specific_id
        result = await db.challenge_attempts.delete_many(query)
        deleted_count = result.deleted_count
        
        # Also remove from user's completed_challenges
        if specific_id:
            await db.users.update_one(
                {"id": user_id},
                {"$pull": {"completed_challenges": specific_id}}
            )
        else:
            await db.users.update_one(
                {"id": user_id},
                {"$set": {"completed_challenges": []}}
            )
    
    else:
        raise HTTPException(status_code=400, detail="Invalid type. Must be: quiz, minigame, or challenge")
    
    return {
        "success": True,
        "message": f"Reset {deleted_count} completion record(s)",
        "deleted_count": deleted_count
    }

# ===== ADMIN: QUIZ QUESTIONS CRUD =====
@api_router.get("/admin/quiz-questions")
async def get_all_quiz_questions(admin_user: dict = Depends(require_admin)):
    """Get all quiz questions for admin management"""
    questions = await db.quiz_questions.find({}, {"_id": 0}).to_list(1000)
    return questions

@api_router.post("/admin/quiz-questions")
async def create_quiz_question(question: dict, admin_user: dict = Depends(require_admin)):
    """Create a new quiz question"""
    question_data = {
        "id": str(uuid.uuid4()),
        "question": question.get('question'),
        "options": question.get('options', []),
        "correct_answer": question.get('correct_answer'),
        "explanation": question.get('explanation', ''),
        "category": question.get('category', 'general'),
        "difficulty": question.get('difficulty', 'beginner'),
        "created_by": admin_user['username'],
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    
    await db.quiz_questions.insert_one(question_data)
    return {"success": True, "question_id": question_data['id']}

@api_router.put("/admin/quiz-questions/{question_id}")
async def update_quiz_question(question_id: str, question: dict, admin_user: dict = Depends(require_admin)):
    """Update a quiz question"""
    update_data = {k: v for k, v in question.items() if k != 'id'}
    
    result = await db.quiz_questions.update_one(
        {"id": question_id},
        {"$set": update_data}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Question not found")
    
    return {"success": True}

@api_router.delete("/admin/quiz-questions/{question_id}")
async def delete_quiz_question(question_id: str, admin_user: dict = Depends(require_admin)):
    """Delete a quiz question"""
    result = await db.quiz_questions.delete_one({"id": question_id})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Question not found")
    
    return {"success": True}

# ===== ADMIN: MINI GAME SCENARIOS CRUD =====
@api_router.get("/admin/minigame-scenarios")
async def get_all_minigame_scenarios(admin_user: dict = Depends(require_admin)):
    """Get all mini game scenarios for admin management"""
    scenarios = await db.minigame_scenarios.find({}, {"_id": 0}).to_list(1000)
    return scenarios

@api_router.post("/admin/minigame-scenarios")
async def create_minigame_scenario(scenario: dict, admin_user: dict = Depends(require_admin)):
    """Create a new mini game scenario"""
    scenario_data = {
        "id": str(uuid.uuid4()),
        "game_type": scenario.get('game_type', 'spot_the_phishing'),
        "title": scenario.get('title'),
        "description": scenario.get('description', ''),
        "image_url": scenario.get('image_url', ''),
        "is_phishing": scenario.get('is_phishing', False),
        "indicators": scenario.get('indicators', []),
        "difficulty": scenario.get('difficulty', 'beginner'),
        "created_by": admin_user['username'],
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    
    await db.minigame_scenarios.insert_one(scenario_data)
    return {"success": True, "scenario_id": scenario_data['id']}

@api_router.put("/admin/minigame-scenarios/{scenario_id}")
async def update_minigame_scenario(scenario_id: str, scenario: dict, admin_user: dict = Depends(require_admin)):
    """Update a mini game scenario"""
    update_data = {k: v for k, v in scenario.items() if k != 'id'}
    
    result = await db.minigame_scenarios.update_one(
        {"id": scenario_id},
        {"$set": update_data}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Scenario not found")
    
    return {"success": True}

@api_router.delete("/admin/minigame-scenarios/{scenario_id}")
async def delete_minigame_scenario(scenario_id: str, admin_user: dict = Depends(require_admin)):
    """Delete a mini game scenario"""
    result = await db.minigame_scenarios.delete_one({"id": scenario_id})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Scenario not found")
    
    return {"success": True}

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