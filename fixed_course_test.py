#!/usr/bin/env python3
"""
Fixed Course CRUD API Test - addressing the update issue
"""

import requests
import json

BASE_URL = "https://secsim-lab.preview.emergentagent.com/api"
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

def get_token():
    """Get admin token"""
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={"username": ADMIN_USERNAME, "password": ADMIN_PASSWORD}
    )
    if response.status_code == 200:
        return response.json().get("token")
    return None

def test_course_update_properly():
    """Test course update with proper payload structure"""
    token = get_token()
    if not token:
        print("❌ Failed to get token")
        return False
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    print("=== TESTING COURSE UPDATE WITH PROPER PAYLOAD ===")
    
    # Step 1: Create course
    print("1. Creating test course...")
    create_payload = {
        "title": "Original Course Title",
        "description": "Original description",
        "category": "social_engineering",
        "difficulty": "beginner",
        "total_duration_minutes": 60,
        "prerequisites": ["Basic Knowledge"],
        "learning_outcomes": ["Original outcome"],
        "modules": [
            {
                "module_number": 1,
                "title": "Original Module",
                "description": "Original module description",
                "slides": [
                    {
                        "title": "Original Slide",
                        "content": "Original content",
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
        print(f"❌ Failed to create course: {create_response.status_code}")
        return False
    
    course = create_response.json()
    course_id = course.get("id")
    original_created_at = course.get("created_at")
    print(f"✅ Created course with ID: {course_id}")
    
    # Step 2: Update course with proper payload (preserving original structure)
    print("2. Updating course with proper payload...")
    
    # Create update payload that matches the original structure but with changes
    update_payload = {
        "title": "Updated Course Title",
        "description": "Updated description with more details",
        "category": "social_engineering",
        "difficulty": "intermediate",  # Changed
        "total_duration_minutes": 90,  # Changed
        "prerequisites": ["Basic Knowledge", "Advanced Security"],  # Added item
        "learning_outcomes": ["Original outcome", "New advanced outcome"],  # Added item
        "modules": [
            {
                "module_number": 1,
                "title": "Updated Module",  # Changed
                "description": "Updated module description",
                "slides": [
                    {
                        "title": "Updated Slide",  # Changed
                        "content": "Updated content with more information",
                        "code_example": "# Example code\nprint('Hello Security')",  # Added
                        "image_url": ""
                    }
                ]
            },
            {
                "module_number": 2,  # New module
                "title": "Additional Module",
                "description": "This is a new module added during update",
                "slides": [
                    {
                        "title": "New Slide",
                        "content": "Content for the new slide",
                        "code_example": "",
                        "image_url": ""
                    }
                ]
            }
        ],
        "created_by": "admin"
    }
    
    update_response = requests.put(
        f"{BASE_URL}/admin/courses/{course_id}",
        json=update_payload,
        headers=headers
    )
    
    print(f"Update response status: {update_response.status_code}")
    print(f"Update response: {update_response.text}")
    
    if update_response.status_code != 200:
        print(f"❌ Update failed")
        return False
    
    # Step 3: Verify the update
    print("3. Verifying update...")
    verify_response = requests.get(f"{BASE_URL}/courses/{course_id}")
    
    if verify_response.status_code == 200:
        updated_course = verify_response.json()
        
        # Check if updates were applied
        checks = [
            ("Title updated", updated_course.get("title") == "Updated Course Title"),
            ("Description updated", "more details" in updated_course.get("description", "")),
            ("Difficulty updated", updated_course.get("difficulty") == "intermediate"),
            ("Duration updated", updated_course.get("total_duration_minutes") == 90),
            ("Prerequisites added", len(updated_course.get("prerequisites", [])) == 2),
            ("Learning outcomes added", len(updated_course.get("learning_outcomes", [])) == 2),
            ("Modules count", len(updated_course.get("modules", [])) == 2),
            ("ID preserved", updated_course.get("id") == course_id)
        ]
        
        all_passed = True
        for check_name, result in checks:
            status = "✅" if result else "❌"
            print(f"   {status} {check_name}")
            if not result:
                all_passed = False
        
        if all_passed:
            print("✅ All update verifications passed!")
        else:
            print("❌ Some update verifications failed")
            print(f"Updated course ID: {updated_course.get('id')}")
            print(f"Original course ID: {course_id}")
        
        # Step 4: Clean up
        print("4. Cleaning up...")
        delete_response = requests.delete(
            f"{BASE_URL}/admin/courses/{course_id}",
            headers=headers
        )
        print(f"Delete response: {delete_response.status_code}")
        
        return all_passed
    else:
        print(f"❌ Course not found after update: {verify_response.status_code}")
        print(verify_response.text)
        return False

if __name__ == "__main__":
    success = test_course_update_properly()
    if success:
        print("\n🎉 Course update test passed!")
    else:
        print("\n⚠️ Course update test failed!")