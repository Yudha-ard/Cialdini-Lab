#!/usr/bin/env python3
"""
Backend API Testing for Course CRUD Endpoints
Testing the Course management system with comprehensive scenarios
"""

import requests
import json
import sys
from datetime import datetime

# Configuration
BASE_URL = "https://secsim-lab.preview.emergentagent.com/api"
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

class CourseAPITester:
    def __init__(self):
        self.base_url = BASE_URL
        self.token = None
        self.created_course_id = None
        self.test_results = []
        
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
    
    def authenticate(self):
        """Test authentication and get token"""
        print("\n=== AUTHENTICATION TEST ===")
        
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
                self.token = data.get("token")
                user = data.get("user", {})
                
                if self.token and user.get("role") == "admin":
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
                        f"Token: {bool(self.token)}, Role: {user.get('role')}"
                    )
                    return False
            else:
                self.log_result(
                    "Admin Authentication", 
                    False, 
                    f"Login failed with status {response.status_code}",
                    response.text
                )
                return False
                
        except Exception as e:
            self.log_result(
                "Admin Authentication", 
                False, 
                f"Authentication request failed: {str(e)}"
            )
            return False
    
    def get_headers(self):
        """Get headers with authorization"""
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
    
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