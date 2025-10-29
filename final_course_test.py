#!/usr/bin/env python3
"""
Final comprehensive Course CRUD API test
"""

import requests
import json

BASE_URL = "https://secsim-lab.preview.emergentagent.com/api"
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

def run_final_test():
    """Run final comprehensive test"""
    print("🚀 FINAL COMPREHENSIVE COURSE CRUD TEST")
    print("="*50)
    
    # Get token
    auth_response = requests.post(
        f"{BASE_URL}/auth/login",
        json={"username": ADMIN_USERNAME, "password": ADMIN_PASSWORD}
    )
    
    if auth_response.status_code != 200:
        print("❌ Authentication failed")
        return False
    
    token = auth_response.json().get("token")
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    print("✅ Authentication successful")
    
    # Test 1: Create course with multiple modules
    print("\n1. Testing CREATE with multiple modules...")
    create_payload = {
        "title": "Advanced Social Engineering Defense",
        "description": "Comprehensive course covering advanced social engineering defense techniques",
        "category": "social_engineering",
        "difficulty": "advanced",
        "total_duration_minutes": 180,
        "prerequisites": ["Basic Security", "Network Fundamentals", "Psychology Basics"],
        "learning_outcomes": [
            "Identify advanced SE techniques",
            "Implement comprehensive defense strategies",
            "Train others in SE awareness",
            "Conduct security assessments"
        ],
        "modules": [
            {
                "module_number": 1,
                "title": "Advanced Phishing Techniques",
                "description": "Deep dive into sophisticated phishing attacks",
                "slides": [
                    {
                        "title": "Spear Phishing Evolution",
                        "content": "Understanding how spear phishing has evolved with AI and social media intelligence",
                        "code_example": "# Email analysis script\nimport re\n\ndef analyze_phishing_indicators(email_content):\n    indicators = ['urgent', 'verify', 'suspended', 'click here']\n    return [ind for ind in indicators if ind in email_content.lower()]",
                        "image_url": ""
                    },
                    {
                        "title": "Business Email Compromise",
                        "content": "How attackers compromise business communications and impersonate executives",
                        "code_example": "",
                        "image_url": ""
                    }
                ]
            },
            {
                "module_number": 2,
                "title": "Physical Social Engineering",
                "description": "Understanding physical security breaches through social engineering",
                "slides": [
                    {
                        "title": "Tailgating and Piggybacking",
                        "content": "How attackers gain physical access through social manipulation",
                        "code_example": "",
                        "image_url": ""
                    },
                    {
                        "title": "Pretexting Scenarios",
                        "content": "Common pretexting scenarios used to gain information or access",
                        "code_example": "",
                        "image_url": ""
                    }
                ]
            },
            {
                "module_number": 3,
                "title": "Defense Strategies",
                "description": "Implementing effective defenses against social engineering",
                "slides": [
                    {
                        "title": "Security Awareness Training",
                        "content": "Designing and implementing effective security awareness programs",
                        "code_example": "",
                        "image_url": ""
                    }
                ]
            }
        ],
        "created_by": "admin"
    }
    
    create_response = requests.post(
        f"{BASE_URL}/admin/courses",
        json=create_payload,
        headers=headers
    )
    
    if create_response.status_code != 200:
        print(f"❌ CREATE failed: {create_response.status_code}")
        return False
    
    course = create_response.json()
    course_id = course.get("id")
    print(f"✅ CREATE successful - Course ID: {course_id}")
    print(f"   - Modules: {len(course.get('modules', []))}")
    print(f"   - Total slides: {sum(len(m.get('slides', [])) for m in course.get('modules', []))}")
    
    # Test 2: Read the created course
    print("\n2. Testing READ (GET single course)...")
    get_response = requests.get(f"{BASE_URL}/courses/{course_id}")
    
    if get_response.status_code != 200:
        print(f"❌ READ failed: {get_response.status_code}")
        return False
    
    retrieved_course = get_response.json()
    print("✅ READ successful")
    print(f"   - Title: {retrieved_course.get('title')}")
    print(f"   - Difficulty: {retrieved_course.get('difficulty')}")
    print(f"   - Modules: {len(retrieved_course.get('modules', []))}")
    
    # Test 3: Update the course
    print("\n3. Testing UPDATE...")
    update_payload = retrieved_course.copy()
    
    # Remove fields that shouldn't be in update
    for field in ['id', 'created_at']:
        if field in update_payload:
            del update_payload[field]
    
    # Make changes
    update_payload["title"] = "Advanced Social Engineering Defense - Updated Edition"
    update_payload["difficulty"] = "expert"
    update_payload["total_duration_minutes"] = 240
    
    # Add a new module
    update_payload["modules"].append({
        "module_number": 4,
        "title": "Incident Response",
        "description": "Responding to social engineering incidents",
        "slides": [
            {
                "title": "Incident Detection",
                "content": "How to detect when a social engineering attack has occurred",
                "code_example": "",
                "image_url": ""
            },
            {
                "title": "Response Procedures",
                "content": "Step-by-step procedures for responding to SE incidents",
                "code_example": "",
                "image_url": ""
            }
        ]
    })
    
    update_response = requests.put(
        f"{BASE_URL}/admin/courses/{course_id}",
        json=update_payload,
        headers=headers
    )
    
    if update_response.status_code != 200:
        print(f"❌ UPDATE failed: {update_response.status_code}")
        print(update_response.text)
        return False
    
    print("✅ UPDATE successful")
    
    # Verify update
    verify_response = requests.get(f"{BASE_URL}/courses/{course_id}")
    if verify_response.status_code == 200:
        updated_course = verify_response.json()
        print(f"   - New title: {updated_course.get('title')}")
        print(f"   - New difficulty: {updated_course.get('difficulty')}")
        print(f"   - New duration: {updated_course.get('total_duration_minutes')} minutes")
        print(f"   - Modules after update: {len(updated_course.get('modules', []))}")
        
        if len(updated_course.get('modules', [])) == 4:
            print("✅ Module addition verified")
        else:
            print("❌ Module addition failed")
            return False
    else:
        print("❌ UPDATE verification failed")
        return False
    
    # Test 4: List all courses
    print("\n4. Testing LIST (GET all courses)...")
    list_response = requests.get(f"{BASE_URL}/courses")
    
    if list_response.status_code != 200:
        print(f"❌ LIST failed: {list_response.status_code}")
        return False
    
    courses = list_response.json()
    print(f"✅ LIST successful - Found {len(courses)} courses")
    
    # Find our course in the list
    our_course = next((c for c in courses if c.get('id') == course_id), None)
    if our_course:
        print("✅ Our course found in list")
    else:
        print("❌ Our course not found in list")
        return False
    
    # Test 5: Delete the course
    print("\n5. Testing DELETE...")
    delete_response = requests.delete(
        f"{BASE_URL}/admin/courses/{course_id}",
        headers=headers
    )
    
    if delete_response.status_code != 200:
        print(f"❌ DELETE failed: {delete_response.status_code}")
        return False
    
    print("✅ DELETE successful")
    
    # Verify deletion
    verify_delete_response = requests.get(f"{BASE_URL}/courses/{course_id}")
    if verify_delete_response.status_code == 404:
        print("✅ DELETE verification successful - course no longer exists")
    else:
        print(f"❌ DELETE verification failed - course still exists: {verify_delete_response.status_code}")
        return False
    
    print("\n" + "="*50)
    print("🎉 ALL COURSE CRUD OPERATIONS SUCCESSFUL!")
    print("✅ CREATE - Multiple modules with slides")
    print("✅ READ - Single course retrieval")
    print("✅ UPDATE - Adding modules and modifying fields")
    print("✅ DELETE - Complete removal")
    print("✅ LIST - All courses retrieval")
    
    return True

if __name__ == "__main__":
    success = run_final_test()
    if not success:
        print("\n❌ Final test failed!")
        exit(1)
    else:
        print("\n🎉 Final test passed!")
        exit(0)