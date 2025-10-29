#!/usr/bin/env python3
"""
Debug script to investigate course update issue
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

def debug_update_issue():
    """Debug the course update issue"""
    token = get_token()
    if not token:
        print("❌ Failed to get token")
        return
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Step 1: Create a simple course
    print("1. Creating test course...")
    create_payload = {
        "title": "Debug Test Course",
        "description": "Simple course for debugging update issue",
        "category": "social_engineering",
        "difficulty": "beginner",
        "total_duration_minutes": 30,
        "prerequisites": ["Basic Knowledge"],
        "learning_outcomes": ["Learn debugging"],
        "modules": [
            {
                "module_number": 1,
                "title": "Test Module",
                "description": "Test module description",
                "slides": [
                    {
                        "title": "Test Slide",
                        "content": "Test content",
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
        print(create_response.text)
        return
    
    course = create_response.json()
    course_id = course.get("id")
    print(f"✅ Created course with ID: {course_id}")
    
    # Step 2: Verify course exists
    print("2. Verifying course exists...")
    get_response = requests.get(f"{BASE_URL}/courses/{course_id}")
    if get_response.status_code == 200:
        print("✅ Course exists and is accessible")
    else:
        print(f"❌ Course not accessible: {get_response.status_code}")
        return
    
    # Step 3: Try to update with minimal changes
    print("3. Attempting minimal update...")
    
    # Get the current course data first
    current_course = get_response.json()
    
    # Make minimal update - just change title
    update_payload = current_course.copy()
    update_payload["title"] = "Debug Test Course - Updated"
    
    # Remove fields that might cause issues
    if "id" in update_payload:
        del update_payload["id"]
    if "created_at" in update_payload:
        del update_payload["created_at"]
    
    print(f"Update payload keys: {list(update_payload.keys())}")
    
    update_response = requests.put(
        f"{BASE_URL}/admin/courses/{course_id}",
        json=update_payload,
        headers=headers
    )
    
    print(f"Update response status: {update_response.status_code}")
    print(f"Update response: {update_response.text}")
    
    # Step 4: Check if course still exists
    print("4. Checking if course still exists after update...")
    verify_response = requests.get(f"{BASE_URL}/courses/{course_id}")
    print(f"Verification response status: {verify_response.status_code}")
    
    if verify_response.status_code == 200:
        updated_course = verify_response.json()
        print(f"✅ Course still exists. Title: {updated_course.get('title')}")
    else:
        print(f"❌ Course no longer exists after update: {verify_response.text}")
    
    # Step 5: Clean up if course still exists
    if verify_response.status_code == 200:
        print("5. Cleaning up...")
        delete_response = requests.delete(
            f"{BASE_URL}/admin/courses/{course_id}",
            headers=headers
        )
        print(f"Delete response: {delete_response.status_code}")

if __name__ == "__main__":
    debug_update_issue()