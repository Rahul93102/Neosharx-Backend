#!/bin/bash

# Comprehensive API Testing Script for Backend-Neosharx
# Run this after successful deployment to test all endpoints

BASE_URL="https://backend-neosharx.onrender.com"
echo "🧪 Testing Backend-Neosharx API Endpoints"
echo "=========================================="

# Function to test endpoint
test_endpoint() {
    local url="$1"
    local description="$2"
    echo -n "Testing $description: "

    # Get HTTP status code and response
    response=$(curl -s -w "\n%{http_code}" "$url" 2>/dev/null)
    http_code=$(echo "$response" | tail -n 1)
    content=$(echo "$response" | head -n -1)

    if [ "$http_code" = "200" ]; then
        echo "✅ SUCCESS ($http_code)"
        # Show first 100 chars of response for successful requests
        if [ ${#content} -gt 0 ] && [ "$content" != "" ]; then
            echo "   Response: ${content:0:100}..."
        fi
    elif [ "$http_code" = "404" ]; then
        echo "❌ NOT FOUND ($http_code)"
    elif [ "$http_code" = "500" ]; then
        echo "❌ SERVER ERROR ($http_code)"
    elif [ "$http_code" = "302" ]; then
        echo "✅ REDIRECT ($http_code)"
    else
        echo "⚠️  OTHER ($http_code)"
        if [ ${#content} -gt 0 ] && [ "$content" != "" ]; then
            echo "   Response: ${content:0:100}..."
        fi
    fi
    echo ""
}

echo "1. HEALTH CHECK"
echo "---------------"
test_endpoint "$BASE_URL/healthz/" "Health Check"

echo "2. CONTENT ENDPOINTS"
echo "-------------------"
test_endpoint "$BASE_URL/api/auth/stories/" "Startup Stories"
test_endpoint "$BASE_URL/api/auth/neo-stories/" "Neo Stories"
test_endpoint "$BASE_URL/api/auth/neo-projects/" "Neo Projects"
test_endpoint "$BASE_URL/api/auth/hackathons/" "Hackathons"
test_endpoint "$BASE_URL/api/auth/tech-news/" "Tech News"
test_endpoint "$BASE_URL/api/auth/robotics-news/" "Robotics News"
test_endpoint "$BASE_URL/api/auth/talk-episodes/" "Talk Episodes"

echo "3. FEATURED CONTENT"
echo "------------------"
test_endpoint "$BASE_URL/api/auth/stories/featured/" "Featured Stories"
test_endpoint "$BASE_URL/api/auth/neo-stories/featured/" "Featured Neo Stories"
test_endpoint "$BASE_URL/api/auth/neo-projects/featured/" "Featured Neo Projects"
test_endpoint "$BASE_URL/api/auth/hackathons/featured/" "Featured Hackathons"
test_endpoint "$BASE_URL/api/auth/tech-news/featured/" "Featured Tech News"
test_endpoint "$BASE_URL/api/auth/robotics-news/featured/" "Featured Robotics News"

echo "4. COMMENTS & SOCIAL"
echo "-------------------"
test_endpoint "$BASE_URL/api/auth/comments/" "Comments"
test_endpoint "$BASE_URL/api/auth/events/" "Events"
test_endpoint "$BASE_URL/api/auth/youtube-videos/" "YouTube Videos"

echo "5. OAUTH ENDPOINTS"
echo "-----------------"
test_endpoint "$BASE_URL/api/auth/google/login-url/" "Google OAuth URL"
test_endpoint "$BASE_URL/api/auth/linkedin/login-url/" "LinkedIn OAuth URL"

echo "6. FILTERS & CATEGORIES"
echo "----------------------"
test_endpoint "$BASE_URL/api/auth/stories/filters/" "Story Filters"
test_endpoint "$BASE_URL/api/auth/tech-news/categories/" "Tech News Categories"
test_endpoint "$BASE_URL/api/auth/hackathons/filters/" "Hackathon Filters"

echo "7. STATIC FILES"
echo "--------------"
echo -n "Testing Admin Interface: "
admin_response=$(curl -s -I "$BASE_URL/admin/" | grep "HTTP/" | cut -d' ' -f2)
if [ "$admin_response" = "302" ]; then
    echo "✅ SUCCESS (302 - Redirect to login)"
else
    echo "❌ FAILED ($admin_response)"
fi

echo ""
echo -n "Testing Google Callback: "
callback_response=$(curl -s -I "$BASE_URL/auth/google/callback.html" | grep "HTTP/" | cut -d' ' -f2)
if [ "$callback_response" = "200" ]; then
    echo "✅ SUCCESS"
else
    echo "❌ FAILED ($callback_response)"
fi

echo ""
echo "🎉 Testing Complete!"
echo "==================="
echo "If you see mostly ✅ SUCCESS messages, your API is working correctly!"
echo "If you see ❌ SERVER ERROR (500), the database migrations haven't run yet."