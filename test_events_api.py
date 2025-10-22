#!/usr/bin/env python
"""
Comprehensive test script for Events API endpoints
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000/api/auth"

def print_header(text):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def print_result(success, message):
    """Print a formatted result"""
    status = "✅" if success else "❌"
    print(f"{status} {message}")

def test_list_all_events():
    """Test GET /api/auth/events/"""
    print_header("TEST 1: List All Events")
    
    try:
        response = requests.get(f"{BASE_URL}/events/")
        
        if response.status_code == 200:
            data = response.json()
            print_result(True, f"Status: {response.status_code}")
            print(f"   Total events: {data.get('count', 0)}")
            print(f"   Results returned: {len(data.get('results', []))}")
            
            # Show first event details
            if data.get('results'):
                first_event = data['results'][0]
                print(f"\n   First Event:")
                print(f"   - Name: {first_event.get('name')}")
                print(f"   - Type: {first_event.get('event_type')}")
                print(f"   - Category: {first_event.get('category')}")
                print(f"   - Date: {first_event.get('formatted_date')}")
                print(f"   - Location: {first_event.get('location')}")
        else:
            print_result(False, f"Status: {response.status_code}")
            print(f"   Error: {response.text}")
    except Exception as e:
        print_result(False, f"Exception: {str(e)}")

def test_events_by_type():
    """Test GET /api/auth/events/type/<type>/"""
    print_header("TEST 2: Get Events by Type")
    
    for event_type in ['past', 'recent', 'upcoming']:
        try:
            response = requests.get(f"{BASE_URL}/events/type/{event_type}/")
            
            if response.status_code == 200:
                data = response.json()
                print_result(True, f"{event_type.upper()}: {len(data)} events")
                
                if data:
                    print(f"   Events:")
                    for event in data:
                        print(f"   - {event.get('name')} ({event.get('formatted_date')})")
            else:
                print_result(False, f"{event_type.upper()}: Status {response.status_code}")
        except Exception as e:
            print_result(False, f"{event_type.upper()}: {str(e)}")

def test_featured_events():
    """Test GET /api/auth/events/featured/"""
    print_header("TEST 3: Get Featured Events")
    
    try:
        response = requests.get(f"{BASE_URL}/events/featured/")
        
        if response.status_code == 200:
            data = response.json()
            print_result(True, f"Status: {response.status_code}")
            print(f"   Featured events: {len(data)}")
            
            if data:
                print(f"\n   Featured Events:")
                for event in data:
                    print(f"   - {event.get('name')} ({event.get('event_type')})")
                    print(f"     Benefits: {len(event.get('benefits', []))} items")
        else:
            print_result(False, f"Status: {response.status_code}")
    except Exception as e:
        print_result(False, f"Exception: {str(e)}")

def test_categories():
    """Test GET /api/auth/events/categories/"""
    print_header("TEST 4: Get Event Categories")
    
    try:
        response = requests.get(f"{BASE_URL}/events/categories/")
        
        if response.status_code == 200:
            data = response.json()
            print_result(True, f"Status: {response.status_code}")
            print(f"   Categories: {len(data)}")
            
            print(f"\n   Category Distribution:")
            for cat in data:
                print(f"   - {cat['name']}: {cat['count']} events")
        else:
            print_result(False, f"Status: {response.status_code}")
    except Exception as e:
        print_result(False, f"Exception: {str(e)}")

def test_single_event():
    """Test GET /api/auth/events/<slug>/"""
    print_header("TEST 5: Get Single Event Details")
    
    # First, get a slug from the list
    try:
        response = requests.get(f"{BASE_URL}/events/")
        if response.status_code == 200:
            data = response.json()
            if data.get('results'):
                slug = data['results'][0]['slug']
                
                # Now test the detail endpoint
                detail_response = requests.get(f"{BASE_URL}/events/{slug}/")
                
                if detail_response.status_code == 200:
                    event = detail_response.json()
                    print_result(True, f"Retrieved event: {event.get('name')}")
                    print(f"\n   Event Details:")
                    print(f"   - Slug: {event.get('slug')}")
                    print(f"   - Description: {event.get('description')[:100]}...")
                    print(f"   - Details: {event.get('details')[:100]}...")
                    print(f"   - Location: {event.get('location')}")
                    print(f"   - Date: {event.get('formatted_date')}")
                    print(f"   - Time: {event.get('formatted_time')}")
                    print(f"   - Timezone: {event.get('event_timezone')}")
                    print(f"   - Benefits: {len(event.get('benefits', []))} items")
                    print(f"   - Key Highlights: {len(event.get('key_highlights', []))} items")
                    print(f"   - Is Featured: {event.get('is_featured')}")
                    print(f"   - View Count: {event.get('view_count')}")
                    print(f"   - Registration Open: {event.get('is_registration_open')}")
                    
                    if event.get('benefits'):
                        print(f"\n   Benefits:")
                        for benefit in event.get('benefits', []):
                            print(f"   • {benefit}")
                else:
                    print_result(False, f"Status: {detail_response.status_code}")
            else:
                print_result(False, "No events found to test detail endpoint")
    except Exception as e:
        print_result(False, f"Exception: {str(e)}")

def test_filters():
    """Test filtering and pagination"""
    print_header("TEST 6: Test Filters and Pagination")
    
    # Test filtering by category
    try:
        response = requests.get(f"{BASE_URL}/events/?category=conference")
        if response.status_code == 200:
            data = response.json()
            print_result(True, f"Filter by category='conference': {data.get('count', 0)} events")
        else:
            print_result(False, f"Category filter failed: {response.status_code}")
    except Exception as e:
        print_result(False, f"Category filter: {str(e)}")
    
    # Test filtering by featured
    try:
        response = requests.get(f"{BASE_URL}/events/?featured=true")
        if response.status_code == 200:
            data = response.json()
            print_result(True, f"Filter by featured=true: {data.get('count', 0)} events")
        else:
            print_result(False, f"Featured filter failed: {response.status_code}")
    except Exception as e:
        print_result(False, f"Featured filter: {str(e)}")
    
    # Test pagination
    try:
        response = requests.get(f"{BASE_URL}/events/?page=1&page_size=3")
        if response.status_code == 200:
            data = response.json()
            print_result(True, f"Pagination (page=1, size=3): {len(data.get('results', []))} results")
            print(f"   Next page: {data.get('next') is not None}")
            print(f"   Previous page: {data.get('previous') is not None}")
        else:
            print_result(False, f"Pagination failed: {response.status_code}")
    except Exception as e:
        print_result(False, f"Pagination: {str(e)}")

def test_response_structure():
    """Validate response structure matches serializer"""
    print_header("TEST 7: Validate Response Structure")
    
    try:
        response = requests.get(f"{BASE_URL}/events/")
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('results'):
                event = data['results'][0]
                
                # Check required fields from EventListSerializer
                required_fields = [
                    'id', 'name', 'slug', 'description', 'event_type', 
                    'category', 'location', 'event_date', 'formatted_date',
                    'featured_image', 'thumbnail_image', 'benefits',
                    'is_featured', 'is_published'
                ]
                
                missing_fields = []
                present_fields = []
                
                for field in required_fields:
                    if field in event:
                        present_fields.append(field)
                    else:
                        missing_fields.append(field)
                
                print_result(len(missing_fields) == 0, "Response structure validation")
                print(f"   Present fields: {len(present_fields)}/{len(required_fields)}")
                
                if missing_fields:
                    print(f"   ❌ Missing fields: {', '.join(missing_fields)}")
                else:
                    print(f"   ✅ All expected fields present")
                    
                # Show data types
                print(f"\n   Field Types:")
                for field in ['id', 'name', 'slug', 'benefits', 'is_featured']:
                    if field in event:
                        print(f"   - {field}: {type(event[field]).__name__}")
        else:
            print_result(False, f"Failed to fetch events: {response.status_code}")
    except Exception as e:
        print_result(False, f"Exception: {str(e)}")

def run_all_tests():
    """Run all API tests"""
    print("\n" + "🚀 "*30)
    print("   NEOSHARX EVENTS API - COMPREHENSIVE TEST SUITE")
    print("🚀 "*30)
    print(f"\nBase URL: {BASE_URL}")
    print(f"Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    test_list_all_events()
    test_events_by_type()
    test_featured_events()
    test_categories()
    test_single_event()
    test_filters()
    test_response_structure()
    
    print("\n" + "🎉 "*30)
    print("   ALL TESTS COMPLETED!")
    print("🎉 "*30 + "\n")

if __name__ == '__main__':
    try:
        run_all_tests()
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
