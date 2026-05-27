#!/bin/bash
# Sora 2 API - Video Generation Examples (cURL)
#
# Documentation: https://docs.mountsea.ai/api-reference/sora/introduction
# Platform: https://offoff.ai/

API_KEY="${MOUNTSEA_API_KEY:-your-api-key}"
BASE_URL="https://api.mountsea.ai"

echo "🎬 Sora 2 API - Video Generation Examples"
echo "==========================================="
echo ""

# 1. Text-to-Video (Sora 2 / Sora Pro)
echo "📌 Text-to-Video:"
echo "---"
curl -s -X POST "${BASE_URL}/sora/generate" \
  -H "Authorization: Bearer ${API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A beautiful sunset over the ocean with waves crashing on the shore, cinematic 4K",
    "duration": 5,
    "resolution": "1080p"
  }' | python3 -m json.tool 2>/dev/null || echo "(install python3 for pretty output)"
echo ""

# 2. Image-to-Video
echo "📌 Image-to-Video:"
echo "---"
echo 'curl -X POST "${BASE_URL}/sora/generate" \'
echo '  -H "Authorization: Bearer YOUR_API_KEY" \'
echo '  -H "Content-Type: application/json" \'
echo '  -d '"'"'{'
echo '    "prompt": "The landscape slowly pans from left to right",'
echo '    "imageUrl": "https://example.com/landscape.jpg",'
echo '    "duration": 5'
echo '  }'"'"''
echo ""

# 3. Check Task Status
echo "📌 Check Task Status:"
echo "---"
echo 'curl -X GET "${BASE_URL}/sora/task?taskId=YOUR_TASK_ID" \'
echo '  -H "Authorization: Bearer YOUR_API_KEY"'
echo ""

echo "🔗 Full Documentation: https://docs.mountsea.ai/api-reference/sora/introduction"
echo "🏠 Platform: https://offoff.ai/"

