#!/usr/bin/env python3
"""
Backend API Testing for Single-Play Restriction System
Testing Quiz, Mini Games, Challenges, and Admin CRUD endpoints
"""

import requests
import json
import sys
import uuid
from datetime import datetime

# Configuration
BASE_URL = "https://securitytrainer-5.preview.emergentagent.com/api"
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"
TEST_USER_USERNAME = f"testuser_{str(uuid.uuid4())[:8]}"
TEST_USER_EMAIL = f"test_{str(uuid.uuid4())[:8]}@example.com"
TEST_USER_PASSWORD = "testpass123"

class SinglePlayRestrictionTester:
    def __init__(self):
        self.base_url = BASE_URL
        self.admin_token = None
        self.user_token = None
        self.user_id = None
        self.test_results = []
        self.created_quiz_question_id = None
        self.created_minigame_scenario_id = None
        self.challenge_id = None
        
    def log_result(self, test_name, success, message, details=None):
        """Log test result"""
        result = {
            "test": test_name,
            "success": success,
            "message": message,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {message}")
        if details and not success:
            print(f"   Details: {details}")
    
    def authenticate_admin(self):
        """Test admin authentication and get token"""
        print("\n=== ADMIN AUTHENTICATION TEST ===")
        
        try:
            response = requests.post(
                f"{self.base_url}/auth/login",
                json={
                    "username": ADMIN_USERNAME,
                    "password": ADMIN_PASSWORD
                },
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                self.admin_token = data.get("token")
                user = data.get("user", {})
                
                if self.admin_token and user.get("role") == "admin":
                    self.log_result(
                        "Admin Authentication", 
                        True, 
                        f"Successfully authenticated as admin user: {user.get('username')}"
                    )
                    return True
                else:
                    self.log_result(
                        "Admin Authentication", 
                        False, 
                        "Login successful but missing token or admin role",
                        f"Token: {bool(self.admin_token)}, Role: {user.get('role')}"
                    )
                    return False
            else:
                self.log_result(
                    "Admin Authentication", 
                    False, 
                    f"Admin login failed with status {response.status_code}",
                    response.text
                )
                return False
                
        except Exception as e:
            self.log_result(
                "Admin Authentication", 
                False, 
                f"Admin authentication request failed: {str(e)}"
            )
            return False
    
    def create_test_user(self):
        """Create a test user for testing"""
        print("\n=== CREATE TEST USER ===")
        
        try:
            response = requests.post(
                f"{self.base_url}/auth/register",
                json={
                    "username": TEST_USER_USERNAME,
                    "email": TEST_USER_EMAIL,
                    "password": TEST_USER_PASSWORD,
                    "full_name": "Test User for Single Play Testing"
                },
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                self.user_token = data.get("token")
                user = data.get("user", {})
                self.user_id = user.get("id")
                
                if self.user_token and self.user_id:
                    self.log_result(
                        "Create Test User", 
                        True, 
                        f"Successfully created test user: {user.get('username')} (ID: {self.user_id})"
                    )
                    return True
                else:
                    self.log_result(
                        "Create Test User", 
                        False, 
                        "User created but missing token or user ID",
                        f"Token: {bool(self.user_token)}, User ID: {self.user_id}"
                    )
                    return False
            else:
                self.log_result(
                    "Create Test User", 
                    False, 
                    f"User creation failed with status {response.status_code}",
                    response.text
                )
                return False
                
        except Exception as e:
            self.log_result(
                "Create Test User", 
                False, 
                f"User creation request failed: {str(e)}"
            )
            return False
    
    def get_admin_headers(self):
        """Get headers with admin authorization"""
        return {
            "Authorization": f"Bearer {self.admin_token}",
            "Content-Type": "application/json"
        }
    
    def get_user_headers(self):
        """Get headers with user authorization"""
        return {
            "Authorization": f"Bearer {self.user_token}",
            "Content-Type": "application/json"
        }
    
    def get_challenge_id(self):
        """Get a challenge ID for testing"""
        print("\n=== GET CHALLENGE FOR TESTING ===")
        
        try:
            response = requests.get(f"{self.base_url}/challenges", timeout=10)
            
            if response.status_code == 200:
                challenges = response.json()
                if challenges:
                    self.challenge_id = challenges[0]["id"]
                    self.log_result(
                        "Get Challenge ID", 
                        True, 
                        f"Found challenge for testing: {self.challenge_id}"
                    )
                    return True
                else:
                    self.log_result(
                        "Get Challenge ID", 
                        False, 
                        "No challenges available for testing"
                    )
                    return False
            else:
                self.log_result(
                    "Get Challenge ID", 
                    False, 
                    f"Failed to get challenges: {response.status_code}",
                    response.text
                )
                return False
                
        except Exception as e:
            self.log_result(
                "Get Challenge ID", 
                False, 
                f"Request failed: {str(e)}"
            )
            return False

    def test_quiz_completion_tracking(self):
        """Test Quiz GLOBAL completion restriction"""
        print("\n=== QUIZ COMPLETION TRACKING TEST ===")
        
        if not self.user_token:
            self.log_result("Quiz Completion Test", False, "No user token available")
            return False
        
        # Step 1: Check initial completion status
        try:
            response = requests.get(
                f"{self.base_url}/quiz/completion-status",
                headers=self.get_user_headers(),
                timeout=10
            )
            
            if response.status_code == 200:
                status = response.json()
                if not status.get("completed", True):
                    self.log_result(
                        "Quiz Initial Status", 
                        True, 
                        "Quiz not completed initially - correct"
                    )
                else:
                    self.log_result(
                        "Quiz Initial Status", 
                        False, 
                        "Quiz already completed for new user"
                    )
                    return False
            else:
                self.log_result(
                    "Quiz Initial Status", 
                    False, 
                    f"Failed to check quiz status: {response.status_code}"
                )
                return False
        except Exception as e:
            self.log_result("Quiz Initial Status", False, f"Request failed: {str(e)}")
            return False
        
        # Step 2: Get quiz questions
        try:
            response = requests.get(f"{self.base_url}/quiz/random", timeout=10)
            
            if response.status_code == 200:
                quiz_data = response.json()
                questions = quiz_data.get("questions", [])
                if questions:
                    self.log_result(
                        "Get Quiz Questions", 
                        True, 
                        f"Retrieved {len(questions)} quiz questions"
                    )
                else:
                    self.log_result("Get Quiz Questions", False, "No questions in quiz")
                    return False
            else:
                self.log_result(
                    "Get Quiz Questions", 
                    False, 
                    f"Failed to get quiz: {response.status_code}"
                )
                return False
        except Exception as e:
            self.log_result("Get Quiz Questions", False, f"Request failed: {str(e)}")
            return False
        
        # Step 3: Submit quiz (first time - should work)
        try:
            # Create realistic answers
            answers = [q.get("correct_answer", 0) for q in questions]
            
            response = requests.post(
                f"{self.base_url}/quiz/submit",
                json={
                    "answers": answers,
                    "questions": questions,
                    "time_taken": 45
                },
                headers=self.get_user_headers(),
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                self.log_result(
                    "Quiz First Submission", 
                    True, 
                    f"Successfully submitted quiz - Score: {result.get('correct')}/{result.get('total')}"
                )
            else:
                self.log_result(
                    "Quiz First Submission", 
                    False, 
                    f"Failed to submit quiz: {response.status_code}",
                    response.text
                )
                return False
        except Exception as e:
            self.log_result("Quiz First Submission", False, f"Request failed: {str(e)}")
            return False
        
        # Step 4: Check completion status after submission
        try:
            response = requests.get(
                f"{self.base_url}/quiz/completion-status",
                headers=self.get_user_headers(),
                timeout=10
            )
            
            if response.status_code == 200:
                status = response.json()
                if status.get("completed", False):
                    completion_data = status.get("completion_data", {})
                    self.log_result(
                        "Quiz Completion Status", 
                        True, 
                        f"Quiz marked as completed - Accuracy: {completion_data.get('accuracy', 0)}%"
                    )
                else:
                    self.log_result(
                        "Quiz Completion Status", 
                        False, 
                        "Quiz not marked as completed after submission"
                    )
                    return False
            else:
                self.log_result(
                    "Quiz Completion Status", 
                    False, 
                    f"Failed to check completion status: {response.status_code}"
                )
                return False
        except Exception as e:
            self.log_result("Quiz Completion Status", False, f"Request failed: {str(e)}")
            return False
        
        # Step 5: Try to submit quiz again (should fail with GLOBAL restriction)
        try:
            response = requests.post(
                f"{self.base_url}/quiz/submit",
                json={
                    "answers": answers,
                    "questions": questions,
                    "time_taken": 30
                },
                headers=self.get_user_headers(),
                timeout=10
            )
            
            if response.status_code == 400:
                error_detail = response.json().get("detail", "")
                if "sudah pernah diselesaikan" in error_detail or "hanya bisa mengikuti quiz sekali" in error_detail:
                    self.log_result(
                        "Quiz Replay Prevention", 
                        True, 
                        "Successfully prevented quiz replay with proper error message"
                    )
                    return True
                else:
                    self.log_result(
                        "Quiz Replay Prevention", 
                        False, 
                        f"Got 400 but wrong error message: {error_detail}"
                    )
                    return False
            else:
                self.log_result(
                    "Quiz Replay Prevention", 
                    False, 
                    f"Expected 400 for replay attempt, got {response.status_code}",
                    response.text
                )
                return False
        except Exception as e:
            self.log_result("Quiz Replay Prevention", False, f"Request failed: {str(e)}")
            return False

    def test_minigame_completion_tracking(self):
        """Test Mini Game completion tracking"""
        print("\n=== MINI GAME COMPLETION TRACKING TEST ===")
        
        if not self.user_token:
            self.log_result("Mini Game Test", False, "No user token available")
            return False
        
        game_type = "spot_the_phishing"
        
        # Step 1: Check initial completion status
        try:
            response = requests.get(
                f"{self.base_url}/minigame/completion-status/{game_type}",
                headers=self.get_user_headers(),
                timeout=10
            )
            
            if response.status_code == 200:
                status = response.json()
                if not status.get("completed", True):
                    self.log_result(
                        "Mini Game Initial Status", 
                        True, 
                        f"Mini game {game_type} not completed initially - correct"
                    )
                else:
                    self.log_result(
                        "Mini Game Initial Status", 
                        False, 
                        f"Mini game {game_type} already completed for new user"
                    )
                    return False
            else:
                self.log_result(
                    "Mini Game Initial Status", 
                    False, 
                    f"Failed to check mini game status: {response.status_code}"
                )
                return False
        except Exception as e:
            self.log_result("Mini Game Initial Status", False, f"Request failed: {str(e)}")
            return False
        
        # Step 2: Complete mini game (first time - should work)
        try:
            response = requests.post(
                f"{self.base_url}/minigame/complete",
                json={
                    "game_type": game_type,
                    "score": 85,
                    "time_taken_seconds": 120,
                    "details": {
                        "correct_identifications": 4,
                        "total_scenarios": 5,
                        "accuracy": 80.0
                    }
                },
                headers=self.get_user_headers(),
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                self.log_result(
                    "Mini Game First Completion", 
                    True, 
                    f"Successfully completed mini game - Points earned: {result.get('points_earned', 0)}"
                )
            else:
                self.log_result(
                    "Mini Game First Completion", 
                    False, 
                    f"Failed to complete mini game: {response.status_code}",
                    response.text
                )
                return False
        except Exception as e:
            self.log_result("Mini Game First Completion", False, f"Request failed: {str(e)}")
            return False
        
        # Step 3: Check completion status after completion
        try:
            response = requests.get(
                f"{self.base_url}/minigame/completion-status/{game_type}",
                headers=self.get_user_headers(),
                timeout=10
            )
            
            if response.status_code == 200:
                status = response.json()
                if status.get("completed", False):
                    completion_data = status.get("completion_data", {})
                    self.log_result(
                        "Mini Game Completion Status", 
                        True, 
                        f"Mini game marked as completed - Score: {completion_data.get('score', 0)}"
                    )
                else:
                    self.log_result(
                        "Mini Game Completion Status", 
                        False, 
                        "Mini game not marked as completed after submission"
                    )
                    return False
            else:
                self.log_result(
                    "Mini Game Completion Status", 
                    False, 
                    f"Failed to check completion status: {response.status_code}"
                )
                return False
        except Exception as e:
            self.log_result("Mini Game Completion Status", False, f"Request failed: {str(e)}")
            return False
        
        # Step 4: Try to complete mini game again (should fail)
        try:
            response = requests.post(
                f"{self.base_url}/minigame/complete",
                json={
                    "game_type": game_type,
                    "score": 95,
                    "time_taken_seconds": 90,
                    "details": {"attempt": "second"}
                },
                headers=self.get_user_headers(),
                timeout=10
            )
            
            if response.status_code == 400:
                error_detail = response.json().get("detail", "")
                if "sudah pernah diselesaikan" in error_detail or "hanya bisa bermain sekali" in error_detail:
                    self.log_result(
                        "Mini Game Replay Prevention", 
                        True, 
                        "Successfully prevented mini game replay with proper error message"
                    )
                    return True
                else:
                    self.log_result(
                        "Mini Game Replay Prevention", 
                        False, 
                        f"Got 400 but wrong error message: {error_detail}"
                    )
                    return False
            else:
                self.log_result(
                    "Mini Game Replay Prevention", 
                    False, 
                    f"Expected 400 for replay attempt, got {response.status_code}",
                    response.text
                )
                return False
        except Exception as e:
            self.log_result("Mini Game Replay Prevention", False, f"Request failed: {str(e)}")
            return False

    def test_challenge_completion_tracking(self):
        """Test Challenge single-play restriction"""
        print("\n=== CHALLENGE COMPLETION TRACKING TEST ===")
        
        if not self.user_token or not self.challenge_id:
            self.log_result("Challenge Test", False, "No user token or challenge ID available")
            return False
        
        # Step 1: Check initial completion status
        try:
            response = requests.get(
                f"{self.base_url}/challenges/{self.challenge_id}/completion",
                headers=self.get_user_headers(),
                timeout=10
            )
            
            if response.status_code == 200:
                status = response.json()
                if not status.get("completed", True):
                    self.log_result(
                        "Challenge Initial Status", 
                        True, 
                        f"Challenge {self.challenge_id} not completed initially - correct"
                    )
                else:
                    self.log_result(
                        "Challenge Initial Status", 
                        False, 
                        f"Challenge {self.challenge_id} already completed for new user"
                    )
                    return False
            else:
                self.log_result(
                    "Challenge Initial Status", 
                    False, 
                    f"Failed to check challenge status: {response.status_code}"
                )
                return False
        except Exception as e:
            self.log_result("Challenge Initial Status", False, f"Request failed: {str(e)}")
            return False
        
        # Step 2: Get challenge details
        try:
            response = requests.get(f"{self.base_url}/challenges/{self.challenge_id}", timeout=10)
            
            if response.status_code == 200:
                challenge = response.json()
                questions = challenge.get("questions", [])
                if questions:
                    self.log_result(
                        "Get Challenge Details", 
                        True, 
                        f"Retrieved challenge with {len(questions)} questions"
                    )
                else:
                    self.log_result("Get Challenge Details", False, "No questions in challenge")
                    return False
            else:
                self.log_result(
                    "Get Challenge Details", 
                    False, 
                    f"Failed to get challenge: {response.status_code}"
                )
                return False
        except Exception as e:
            self.log_result("Get Challenge Details", False, f"Request failed: {str(e)}")
            return False
        
        # Step 3: Attempt challenge (first time - should work)
        try:
            # Create realistic answers
            answers = [q.get("correct_answer", 0) for q in questions]
            
            response = requests.post(
                f"{self.base_url}/challenges/{self.challenge_id}/attempt",
                json={
                    "answers": answers,
                    "time_taken_seconds": 180
                },
                headers=self.get_user_headers(),
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                self.log_result(
                    "Challenge First Attempt", 
                    True, 
                    f"Successfully attempted challenge - Score: {result.get('correct_count')}/{result.get('total_questions')}"
                )
            else:
                self.log_result(
                    "Challenge First Attempt", 
                    False, 
                    f"Failed to attempt challenge: {response.status_code}",
                    response.text
                )
                return False
        except Exception as e:
            self.log_result("Challenge First Attempt", False, f"Request failed: {str(e)}")
            return False
        
        # Step 4: Check completion status after attempt
        try:
            response = requests.get(
                f"{self.base_url}/challenges/{self.challenge_id}/completion",
                headers=self.get_user_headers(),
                timeout=10
            )
            
            if response.status_code == 200:
                status = response.json()
                if status.get("completed", False):
                    completion_data = status.get("completion_data", {})
                    self.log_result(
                        "Challenge Completion Status", 
                        True, 
                        f"Challenge marked as completed - Points: {completion_data.get('points_earned', 0)}"
                    )
                else:
                    self.log_result(
                        "Challenge Completion Status", 
                        False, 
                        "Challenge not marked as completed after successful attempt"
                    )
                    return False
            else:
                self.log_result(
                    "Challenge Completion Status", 
                    False, 
                    f"Failed to check completion status: {response.status_code}"
                )
                return False
        except Exception as e:
            self.log_result("Challenge Completion Status", False, f"Request failed: {str(e)}")
            return False
        
        # Step 5: Try to attempt challenge again (should fail with previous results)
        try:
            response = requests.post(
                f"{self.base_url}/challenges/{self.challenge_id}/attempt",
                json={
                    "answers": answers,
                    "time_taken_seconds": 120
                },
                headers=self.get_user_headers(),
                timeout=10
            )
            
            if response.status_code == 400:
                error_data = response.json()
                error_detail = error_data.get("detail", {})
                
                if isinstance(error_detail, dict) and "previous_result" in error_detail:
                    previous_result = error_detail["previous_result"]
                    self.log_result(
                        "Challenge Replay Prevention", 
                        True, 
                        f"Successfully prevented challenge replay and returned previous results: {previous_result.get('points_earned', 0)} points"
                    )
                    return True
                else:
                    self.log_result(
                        "Challenge Replay Prevention", 
                        False, 
                        f"Got 400 but missing previous results: {error_detail}"
                    )
                    return False
            else:
                self.log_result(
                    "Challenge Replay Prevention", 
                    False, 
                    f"Expected 400 for replay attempt, got {response.status_code}",
                    response.text
                )
                return False
        except Exception as e:
            self.log_result("Challenge Replay Prevention", False, f"Request failed: {str(e)}")
            return False

    def test_admin_reset_functionality(self):
        """Test Admin reset completion functionality"""
        print("\n=== ADMIN RESET FUNCTIONALITY TEST ===")
        
        if not self.admin_token or not self.user_id:
            self.log_result("Admin Reset Test", False, "No admin token or user ID available")
            return False
        
        # Test 1: Reset quiz completion
        try:
            response = requests.post(
                f"{self.base_url}/admin/reset-completion",
                json={
                    "user_id": self.user_id,
                    "type": "quiz"
                },
                headers=self.get_admin_headers(),
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                self.log_result(
                    "Admin Reset Quiz", 
                    True, 
                    f"Successfully reset quiz completion - Deleted {result.get('deleted_count', 0)} records"
                )
            else:
                self.log_result(
                    "Admin Reset Quiz", 
                    False, 
                    f"Failed to reset quiz: {response.status_code}",
                    response.text
                )
                return False
        except Exception as e:
            self.log_result("Admin Reset Quiz", False, f"Request failed: {str(e)}")
            return False
        
        # Test 2: Verify quiz can be taken again after reset
        try:
            response = requests.get(
                f"{self.base_url}/quiz/completion-status",
                headers=self.get_user_headers(),
                timeout=10
            )
            
            if response.status_code == 200:
                status = response.json()
                if not status.get("completed", True):
                    self.log_result(
                        "Quiz Reset Verification", 
                        True, 
                        "Quiz completion successfully reset - user can take quiz again"
                    )
                else:
                    self.log_result(
                        "Quiz Reset Verification", 
                        False, 
                        "Quiz still marked as completed after reset"
                    )
                    return False
            else:
                self.log_result(
                    "Quiz Reset Verification", 
                    False, 
                    f"Failed to verify quiz reset: {response.status_code}"
                )
                return False
        except Exception as e:
            self.log_result("Quiz Reset Verification", False, f"Request failed: {str(e)}")
            return False
        
        # Test 3: Reset mini game completion
        try:
            response = requests.post(
                f"{self.base_url}/admin/reset-completion",
                json={
                    "user_id": self.user_id,
                    "type": "minigame",
                    "specific_id": "spot_the_phishing"
                },
                headers=self.get_admin_headers(),
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                self.log_result(
                    "Admin Reset Mini Game", 
                    True, 
                    f"Successfully reset mini game completion - Deleted {result.get('deleted_count', 0)} records"
                )
            else:
                self.log_result(
                    "Admin Reset Mini Game", 
                    False, 
                    f"Failed to reset mini game: {response.status_code}",
                    response.text
                )
                return False
        except Exception as e:
            self.log_result("Admin Reset Mini Game", False, f"Request failed: {str(e)}")
            return False
        
        # Test 4: Reset challenge completion
        if self.challenge_id:
            try:
                response = requests.post(
                    f"{self.base_url}/admin/reset-completion",
                    json={
                        "user_id": self.user_id,
                        "type": "challenge",
                        "specific_id": self.challenge_id
                    },
                    headers=self.get_admin_headers(),
                    timeout=10
                )
                
                if response.status_code == 200:
                    result = response.json()
                    self.log_result(
                        "Admin Reset Challenge", 
                        True, 
                        f"Successfully reset challenge completion - Deleted {result.get('deleted_count', 0)} records"
                    )
                    return True
                else:
                    self.log_result(
                        "Admin Reset Challenge", 
                        False, 
                        f"Failed to reset challenge: {response.status_code}",
                        response.text
                    )
                    return False
            except Exception as e:
                self.log_result("Admin Reset Challenge", False, f"Request failed: {str(e)}")
                return False
        
        return True

    def test_admin_quiz_questions_crud(self):
        """Test Admin CRUD for Quiz Questions"""
        print("\n=== ADMIN QUIZ QUESTIONS CRUD TEST ===")
        
        if not self.admin_token:
            self.log_result("Quiz Questions CRUD", False, "No admin token available")
            return False
        
        # Test 1: Get all quiz questions
        try:
            response = requests.get(
                f"{self.base_url}/admin/quiz-questions",
                headers=self.get_admin_headers(),
                timeout=10
            )
            
            if response.status_code == 200:
                questions = response.json()
                self.log_result(
                    "Get Quiz Questions", 
                    True, 
                    f"Successfully retrieved {len(questions)} quiz questions"
                )
            else:
                self.log_result(
                    "Get Quiz Questions", 
                    False, 
                    f"Failed to get quiz questions: {response.status_code}",
                    response.text
                )
                return False
        except Exception as e:
            self.log_result("Get Quiz Questions", False, f"Request failed: {str(e)}")
            return False
        
        # Test 2: Create new quiz question
        try:
            question_data = {
                "question": "What is the most common type of social engineering attack?",
                "options": [
                    "Phishing emails",
                    "Physical tailgating", 
                    "Phone pretexting",
                    "USB baiting"
                ],
                "correct_answer": 0,
                "explanation": "Phishing emails are the most widespread form of social engineering, targeting millions of users daily through deceptive messages.",
                "category": "phishing",
                "difficulty": "beginner"
            }
            
            response = requests.post(
                f"{self.base_url}/admin/quiz-questions",
                json=question_data,
                headers=self.get_admin_headers(),
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                self.created_quiz_question_id = result.get("question_id")
                self.log_result(
                    "Create Quiz Question", 
                    True, 
                    f"Successfully created quiz question with ID: {self.created_quiz_question_id}"
                )
            else:
                self.log_result(
                    "Create Quiz Question", 
                    False, 
                    f"Failed to create quiz question: {response.status_code}",
                    response.text
                )
                return False
        except Exception as e:
            self.log_result("Create Quiz Question", False, f"Request failed: {str(e)}")
            return False
        
        # Test 3: Update quiz question
        if self.created_quiz_question_id:
            try:
                updated_data = {
                    "question": "What is the MOST common type of social engineering attack in 2024?",
                    "options": [
                        "Phishing emails",
                        "Smishing (SMS phishing)",
                        "Physical tailgating", 
                        "Voice phishing (vishing)"
                    ],
                    "correct_answer": 0,
                    "explanation": "Phishing emails remain the most widespread form of social engineering, with billions of malicious emails sent daily.",
                    "category": "phishing",
                    "difficulty": "intermediate"
                }
                
                response = requests.put(
                    f"{self.base_url}/admin/quiz-questions/{self.created_quiz_question_id}",
                    json=updated_data,
                    headers=self.get_admin_headers(),
                    timeout=10
                )
                
                if response.status_code == 200:
                    self.log_result(
                        "Update Quiz Question", 
                        True, 
                        "Successfully updated quiz question"
                    )
                else:
                    self.log_result(
                        "Update Quiz Question", 
                        False, 
                        f"Failed to update quiz question: {response.status_code}",
                        response.text
                    )
                    return False
            except Exception as e:
                self.log_result("Update Quiz Question", False, f"Request failed: {str(e)}")
                return False
        
        # Test 4: Delete quiz question
        if self.created_quiz_question_id:
            try:
                response = requests.delete(
                    f"{self.base_url}/admin/quiz-questions/{self.created_quiz_question_id}",
                    headers=self.get_admin_headers(),
                    timeout=10
                )
                
                if response.status_code == 200:
                    self.log_result(
                        "Delete Quiz Question", 
                        True, 
                        "Successfully deleted quiz question"
                    )
                    return True
                else:
                    self.log_result(
                        "Delete Quiz Question", 
                        False, 
                        f"Failed to delete quiz question: {response.status_code}",
                        response.text
                    )
                    return False
            except Exception as e:
                self.log_result("Delete Quiz Question", False, f"Request failed: {str(e)}")
                return False
        
        return True

    def test_admin_minigame_scenarios_crud(self):
        """Test Admin CRUD for Mini Game Scenarios"""
        print("\n=== ADMIN MINI GAME SCENARIOS CRUD TEST ===")
        
        if not self.admin_token:
            self.log_result("Mini Game Scenarios CRUD", False, "No admin token available")
            return False
        
        # Test 1: Get all mini game scenarios
        try:
            response = requests.get(
                f"{self.base_url}/admin/minigame-scenarios",
                headers=self.get_admin_headers(),
                timeout=10
            )
            
            if response.status_code == 200:
                scenarios = response.json()
                self.log_result(
                    "Get Mini Game Scenarios", 
                    True, 
                    f"Successfully retrieved {len(scenarios)} mini game scenarios"
                )
            else:
                self.log_result(
                    "Get Mini Game Scenarios", 
                    False, 
                    f"Failed to get scenarios: {response.status_code}",
                    response.text
                )
                return False
        except Exception as e:
            self.log_result("Get Mini Game Scenarios", False, f"Request failed: {str(e)}")
            return False
        
        # Test 2: Create new mini game scenario
        try:
            scenario_data = {
                "game_type": "spot_the_phishing",
                "title": "Suspicious Banking Email",
                "description": "A realistic phishing email targeting bank customers",
                "image_url": "https://example.com/phishing-email.png",
                "is_phishing": True,
                "indicators": [
                    "Generic greeting instead of personal name",
                    "Urgent language creating false sense of emergency",
                    "Suspicious sender domain not matching bank",
                    "Request for sensitive information via email"
                ],
                "difficulty": "intermediate"
            }
            
            response = requests.post(
                f"{self.base_url}/admin/minigame-scenarios",
                json=scenario_data,
                headers=self.get_admin_headers(),
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                self.created_minigame_scenario_id = result.get("scenario_id")
                self.log_result(
                    "Create Mini Game Scenario", 
                    True, 
                    f"Successfully created scenario with ID: {self.created_minigame_scenario_id}"
                )
            else:
                self.log_result(
                    "Create Mini Game Scenario", 
                    False, 
                    f"Failed to create scenario: {response.status_code}",
                    response.text
                )
                return False
        except Exception as e:
            self.log_result("Create Mini Game Scenario", False, f"Request failed: {str(e)}")
            return False
        
        # Test 3: Update mini game scenario
        if self.created_minigame_scenario_id:
            try:
                updated_data = {
                    "game_type": "spot_the_phishing",
                    "title": "Advanced Banking Phishing Email",
                    "description": "A sophisticated phishing email with advanced social engineering techniques",
                    "image_url": "https://example.com/advanced-phishing-email.png",
                    "is_phishing": True,
                    "indicators": [
                        "Generic greeting instead of personal name",
                        "Urgent language creating false sense of emergency",
                        "Suspicious sender domain not matching bank",
                        "Request for sensitive information via email",
                        "Poor grammar and spelling mistakes",
                        "Mismatched URLs in links"
                    ],
                    "difficulty": "advanced"
                }
                
                response = requests.put(
                    f"{self.base_url}/admin/minigame-scenarios/{self.created_minigame_scenario_id}",
                    json=updated_data,
                    headers=self.get_admin_headers(),
                    timeout=10
                )
                
                if response.status_code == 200:
                    self.log_result(
                        "Update Mini Game Scenario", 
                        True, 
                        "Successfully updated mini game scenario"
                    )
                else:
                    self.log_result(
                        "Update Mini Game Scenario", 
                        False, 
                        f"Failed to update scenario: {response.status_code}",
                        response.text
                    )
                    return False
            except Exception as e:
                self.log_result("Update Mini Game Scenario", False, f"Request failed: {str(e)}")
                return False
        
        # Test 4: Delete mini game scenario
        if self.created_minigame_scenario_id:
            try:
                response = requests.delete(
                    f"{self.base_url}/admin/minigame-scenarios/{self.created_minigame_scenario_id}",
                    headers=self.get_admin_headers(),
                    timeout=10
                )
                
                if response.status_code == 200:
                    self.log_result(
                        "Delete Mini Game Scenario", 
                        True, 
                        "Successfully deleted mini game scenario"
                    )
                    return True
                else:
                    self.log_result(
                        "Delete Mini Game Scenario", 
                        False, 
                        f"Failed to delete scenario: {response.status_code}",
                        response.text
                    )
                    return False
            except Exception as e:
                self.log_result("Delete Mini Game Scenario", False, f"Request failed: {str(e)}")
                return False
        
        return True

    def test_edge_cases(self):
        """Test edge cases and unauthorized access"""
        print("\n=== EDGE CASES AND SECURITY TEST ===")
        
        # Test 1: Unauthorized access to admin endpoints
        try:
            response = requests.get(f"{self.base_url}/admin/quiz-questions", timeout=10)
            
            if response.status_code in [401, 403]:
                self.log_result(
                    "Unauthorized Admin Access", 
                    True, 
                    f"Correctly rejected unauthorized access with status {response.status_code}"
                )
            else:
                self.log_result(
                    "Unauthorized Admin Access", 
                    False, 
                    f"Expected 401/403, got {response.status_code}"
                )
                return False
        except Exception as e:
            self.log_result("Unauthorized Admin Access", False, f"Request failed: {str(e)}")
            return False
        
        # Test 2: Non-existent challenge completion check
        try:
            fake_challenge_id = "non-existent-challenge-12345"
            response = requests.get(
                f"{self.base_url}/challenges/{fake_challenge_id}/completion",
                headers=self.get_user_headers(),
                timeout=10
            )
            
            if response.status_code == 404:
                self.log_result(
                    "Non-existent Challenge", 
                    True, 
                    "Correctly returned 404 for non-existent challenge"
                )
            else:
                self.log_result(
                    "Non-existent Challenge", 
                    False, 
                    f"Expected 404, got {response.status_code}"
                )
                return False
        except Exception as e:
            self.log_result("Non-existent Challenge", False, f"Request failed: {str(e)}")
            return False
        
        # Test 3: Invalid reset completion type
        if self.admin_token and self.user_id:
            try:
                response = requests.post(
                    f"{self.base_url}/admin/reset-completion",
                    json={
                        "user_id": self.user_id,
                        "type": "invalid_type"
                    },
                    headers=self.get_admin_headers(),
                    timeout=10
                )
                
                if response.status_code == 400:
                    self.log_result(
                        "Invalid Reset Type", 
                        True, 
                        "Correctly rejected invalid reset type with 400"
                    )
                    return True
                else:
                    self.log_result(
                        "Invalid Reset Type", 
                        False, 
                        f"Expected 400, got {response.status_code}"
                    )
                    return False
            except Exception as e:
                self.log_result("Invalid Reset Type", False, f"Request failed: {str(e)}")
                return False
        
        return True

    def test_get_all_courses(self):
        """Test GET /api/courses"""
        print("\n=== GET ALL COURSES TEST ===")
        
        try:
            response = requests.get(f"{self.base_url}/courses", timeout=10)
            
            if response.status_code == 200:
                courses = response.json()
                self.log_result(
                    "Get All Courses", 
                    True, 
                    f"Successfully retrieved {len(courses)} courses"
                )
                
                # Validate response structure
                if isinstance(courses, list):
                    for course in courses[:3]:  # Check first 3 courses
                        required_fields = ["id", "title", "description", "category", "difficulty"]
                        missing_fields = [field for field in required_fields if field not in course]
                        if missing_fields:
                            self.log_result(
                                "Course Structure Validation", 
                                False, 
                                f"Missing required fields in course: {missing_fields}"
                            )
                            return False
                    
                    self.log_result(
                        "Course Structure Validation", 
                        True, 
                        "Course objects have required fields"
                    )
                return True
            else:
                self.log_result(
                    "Get All Courses", 
                    False, 
                    f"Failed with status {response.status_code}",
                    response.text
                )
                return False
                
        except Exception as e:
            self.log_result(
                "Get All Courses", 
                False, 
                f"Request failed: {str(e)}"
            )
            return False
    
    def test_create_course(self):
        """Test POST /api/admin/courses"""
        print("\n=== CREATE COURSE TEST ===")
        
        if not self.token:
            self.log_result(
                "Create Course", 
                False, 
                "No authentication token available"
            )
            return False
        
        # Test payload with complete structure
        course_payload = {
            "title": "Test Course Social Engineering Advanced",
            "description": "Comprehensive course untuk testing CRUD operations dengan advanced scenarios",
            "category": "social_engineering",
            "difficulty": "beginner",
            "total_duration_minutes": 90,
            "prerequisites": ["Basic Security Knowledge", "Understanding of Psychology"],
            "learning_outcomes": [
                "Understand advanced SE techniques", 
                "Identify sophisticated threats",
                "Implement defense strategies"
            ],
            "modules": [
                {
                    "module_number": 1,
                    "title": "Introduction to Social Engineering",
                    "description": "Learn the fundamentals of social engineering attacks",
                    "slides": [
                        {
                            "title": "Welcome to Social Engineering",
                            "content": "Social engineering is the art of manipulating people to divulge confidential information or perform actions that compromise security.",
                            "code_example": "",
                            "image_url": ""
                        },
                        {
                            "title": "Types of Social Engineering",
                            "content": "Common types include phishing, pretexting, baiting, and tailgating.",
                            "code_example": "# Example phishing detection\ndef is_suspicious_email(sender, subject):\n    suspicious_keywords = ['urgent', 'verify', 'suspended']\n    return any(keyword in subject.lower() for keyword in suspicious_keywords)",
                            "image_url": ""
                        }
                    ]
                }
            ],
            "created_by": "admin"
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/admin/courses",
                json=course_payload,
                headers=self.get_headers(),
                timeout=15
            )
            
            if response.status_code == 200:
                course = response.json()
                self.created_course_id = course.get("id")
                
                # Validate response structure
                required_fields = ["id", "title", "description", "category", "difficulty", "modules"]
                missing_fields = [field for field in required_fields if field not in course]
                
                if missing_fields:
                    self.log_result(
                        "Create Course", 
                        False, 
                        f"Course created but missing fields: {missing_fields}"
                    )
                    return False
                
                # Validate modules structure
                modules = course.get("modules", [])
                if len(modules) != 1:
                    self.log_result(
                        "Create Course", 
                        False, 
                        f"Expected 1 module, got {len(modules)}"
                    )
                    return False
                
                module = modules[0]
                if len(module.get("slides", [])) != 2:
                    self.log_result(
                        "Create Course", 
                        False, 
                        f"Expected 2 slides in module, got {len(module.get('slides', []))}"
                    )
                    return False
                
                self.log_result(
                    "Create Course", 
                    True, 
                    f"Successfully created course with ID: {self.created_course_id}"
                )
                return True
            else:
                self.log_result(
                    "Create Course", 
                    False, 
                    f"Failed with status {response.status_code}",
                    response.text
                )
                return False
                
        except Exception as e:
            self.log_result(
                "Create Course", 
                False, 
                f"Request failed: {str(e)}"
            )
            return False
    
    def test_get_single_course(self):
        """Test GET /api/courses/{course_id}"""
        print("\n=== GET SINGLE COURSE TEST ===")
        
        if not self.created_course_id:
            self.log_result(
                "Get Single Course", 
                False, 
                "No course ID available from create test"
            )
            return False
        
        try:
            response = requests.get(
                f"{self.base_url}/courses/{self.created_course_id}",
                timeout=10
            )
            
            if response.status_code == 200:
                course = response.json()
                
                # Validate complete structure
                if course.get("id") != self.created_course_id:
                    self.log_result(
                        "Get Single Course", 
                        False, 
                        f"Course ID mismatch: expected {self.created_course_id}, got {course.get('id')}"
                    )
                    return False
                
                # Check modules and slides
                modules = course.get("modules", [])
                if len(modules) == 1 and len(modules[0].get("slides", [])) == 2:
                    self.log_result(
                        "Get Single Course", 
                        True, 
                        f"Successfully retrieved course with complete structure"
                    )
                    return True
                else:
                    self.log_result(
                        "Get Single Course", 
                        False, 
                        f"Course structure incomplete: {len(modules)} modules, {len(modules[0].get('slides', [])) if modules else 0} slides"
                    )
                    return False
            else:
                self.log_result(
                    "Get Single Course", 
                    False, 
                    f"Failed with status {response.status_code}",
                    response.text
                )
                return False
                
        except Exception as e:
            self.log_result(
                "Get Single Course", 
                False, 
                f"Request failed: {str(e)}"
            )
            return False
    
    def test_update_course(self):
        """Test PUT /api/admin/courses/{course_id}"""
        print("\n=== UPDATE COURSE TEST ===")
        
        if not self.created_course_id or not self.token:
            self.log_result(
                "Update Course", 
                False, 
                "No course ID or token available"
            )
            return False
        
        # Updated payload with additional module
        updated_payload = {
            "title": "Test Course Social Engineering Advanced - Updated",
            "description": "Updated comprehensive course dengan additional module",
            "category": "social_engineering", 
            "difficulty": "intermediate",
            "total_duration_minutes": 120,
            "prerequisites": ["Basic Security Knowledge", "Understanding of Psychology", "Network Fundamentals"],
            "learning_outcomes": [
                "Understand advanced SE techniques", 
                "Identify sophisticated threats",
                "Implement defense strategies",
                "Conduct security awareness training"
            ],
            "modules": [
                {
                    "module_number": 1,
                    "title": "Introduction to Social Engineering",
                    "description": "Learn the fundamentals of social engineering attacks",
                    "slides": [
                        {
                            "title": "Welcome to Social Engineering",
                            "content": "Social engineering is the art of manipulating people to divulge confidential information.",
                            "code_example": "",
                            "image_url": ""
                        }
                    ]
                },
                {
                    "module_number": 2,
                    "title": "Advanced Attack Vectors",
                    "description": "Deep dive into sophisticated social engineering techniques",
                    "slides": [
                        {
                            "title": "Spear Phishing Techniques",
                            "content": "Targeted phishing attacks using personal information to increase success rates.",
                            "code_example": "",
                            "image_url": ""
                        },
                        {
                            "title": "Business Email Compromise",
                            "content": "Understanding how attackers compromise business communications.",
                            "code_example": "",
                            "image_url": ""
                        }
                    ]
                }
            ],
            "created_by": "admin"
        }
        
        try:
            response = requests.put(
                f"{self.base_url}/admin/courses/{self.created_course_id}",
                json=updated_payload,
                headers=self.get_headers(),
                timeout=15
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Verify update by fetching the course
                get_response = requests.get(f"{self.base_url}/courses/{self.created_course_id}")
                if get_response.status_code == 200:
                    updated_course = get_response.json()
                    
                    if (updated_course.get("title") == updated_payload["title"] and 
                        len(updated_course.get("modules", [])) == 2):
                        self.log_result(
                            "Update Course", 
                            True, 
                            "Successfully updated course with additional module"
                        )
                        return True
                    else:
                        self.log_result(
                            "Update Course", 
                            False, 
                            "Update response OK but changes not reflected"
                        )
                        return False
                else:
                    self.log_result(
                        "Update Course", 
                        False, 
                        "Update OK but verification fetch failed"
                    )
                    return False
            else:
                self.log_result(
                    "Update Course", 
                    False, 
                    f"Failed with status {response.status_code}",
                    response.text
                )
                return False
                
        except Exception as e:
            self.log_result(
                "Update Course", 
                False, 
                f"Request failed: {str(e)}"
            )
            return False
    
    def test_edge_cases(self):
        """Test edge cases and error conditions"""
        print("\n=== EDGE CASES TEST ===")
        
        # Test 1: Create course with empty modules
        empty_modules_payload = {
            "title": "Empty Modules Test Course",
            "description": "Testing course creation with empty modules array",
            "category": "social_engineering",
            "difficulty": "beginner", 
            "total_duration_minutes": 30,
            "prerequisites": [],
            "learning_outcomes": ["Test empty modules"],
            "modules": [],
            "created_by": "admin"
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/admin/courses",
                json=empty_modules_payload,
                headers=self.get_headers(),
                timeout=10
            )
            
            if response.status_code == 200:
                course = response.json()
                empty_course_id = course.get("id")
                self.log_result(
                    "Empty Modules Course", 
                    True, 
                    "Successfully created course with empty modules array"
                )
                
                # Clean up
                requests.delete(
                    f"{self.base_url}/admin/courses/{empty_course_id}",
                    headers=self.get_headers()
                )
            else:
                self.log_result(
                    "Empty Modules Course", 
                    False, 
                    f"Failed to create course with empty modules: {response.status_code}"
                )
        except Exception as e:
            self.log_result(
                "Empty Modules Course", 
                False, 
                f"Request failed: {str(e)}"
            )
        
        # Test 2: Access admin endpoint without token
        try:
            response = requests.post(
                f"{self.base_url}/admin/courses",
                json=empty_modules_payload,
                timeout=10
            )
            
            if response.status_code == 403 or response.status_code == 401:
                self.log_result(
                    "Unauthorized Access Protection", 
                    True, 
                    f"Correctly rejected unauthorized request with status {response.status_code}"
                )
            else:
                self.log_result(
                    "Unauthorized Access Protection", 
                    False, 
                    f"Expected 401/403, got {response.status_code}"
                )
        except Exception as e:
            self.log_result(
                "Unauthorized Access Protection", 
                False, 
                f"Request failed: {str(e)}"
            )
        
        # Test 3: Get non-existent course
        try:
            fake_id = "non-existent-course-id-12345"
            response = requests.get(f"{self.base_url}/courses/{fake_id}", timeout=10)
            
            if response.status_code == 404:
                self.log_result(
                    "Non-existent Course Handling", 
                    True, 
                    "Correctly returned 404 for non-existent course"
                )
            else:
                self.log_result(
                    "Non-existent Course Handling", 
                    False, 
                    f"Expected 404, got {response.status_code}"
                )
        except Exception as e:
            self.log_result(
                "Non-existent Course Handling", 
                False, 
                f"Request failed: {str(e)}"
            )
    
    def test_delete_course(self):
        """Test DELETE /api/admin/courses/{course_id}"""
        print("\n=== DELETE COURSE TEST ===")
        
        if not self.created_course_id or not self.token:
            self.log_result(
                "Delete Course", 
                False, 
                "No course ID or token available"
            )
            return False
        
        try:
            response = requests.delete(
                f"{self.base_url}/admin/courses/{self.created_course_id}",
                headers=self.get_headers(),
                timeout=10
            )
            
            if response.status_code == 200:
                # Verify deletion by trying to fetch the course
                get_response = requests.get(f"{self.base_url}/courses/{self.created_course_id}")
                
                if get_response.status_code == 404:
                    self.log_result(
                        "Delete Course", 
                        True, 
                        "Successfully deleted course - confirmed by 404 on fetch"
                    )
                    return True
                else:
                    self.log_result(
                        "Delete Course", 
                        False, 
                        f"Delete OK but course still accessible with status {get_response.status_code}"
                    )
                    return False
            else:
                self.log_result(
                    "Delete Course", 
                    False, 
                    f"Failed with status {response.status_code}",
                    response.text
                )
                return False
                
        except Exception as e:
            self.log_result(
                "Delete Course", 
                False, 
                f"Request failed: {str(e)}"
            )
            return False
    
    def run_all_tests(self):
        """Run all course CRUD tests"""
        print("🚀 Starting Course CRUD API Testing...")
        print(f"Backend URL: {self.base_url}")
        print(f"Admin Credentials: {ADMIN_USERNAME}")
        
        # Test sequence
        tests = [
            self.authenticate,
            self.test_get_all_courses,
            self.test_create_course,
            self.test_get_single_course,
            self.test_update_course,
            self.test_edge_cases,
            self.test_delete_course
        ]
        
        passed = 0
        total = 0
        
        for test in tests:
            try:
                if test():
                    passed += 1
                total += 1
            except Exception as e:
                print(f"❌ Test {test.__name__} crashed: {str(e)}")
                total += 1
        
        # Summary
        print(f"\n{'='*60}")
        print(f"📊 COURSE CRUD API TEST SUMMARY")
        print(f"{'='*60}")
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        
        # Detailed results
        print(f"\n📋 DETAILED RESULTS:")
        for result in self.test_results:
            status = "✅" if result["success"] else "❌"
            print(f"{status} {result['test']}: {result['message']}")
        
        return passed == total

if __name__ == "__main__":
    tester = CourseAPITester()
    success = tester.run_all_tests()
    
    if success:
        print(f"\n🎉 All Course CRUD API tests passed!")
        sys.exit(0)
    else:
        print(f"\n⚠️  Some Course CRUD API tests failed!")
        sys.exit(1)