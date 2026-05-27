"""
Sora API - Video Generation Example
Generate videos using Mountsea AI's Sora API

Documentation: https://docs.mountsea.ai/api-reference/sora/introduction
Platform: https://offoff.ai/
"""

import requests
import time
import os

API_KEY = os.environ.get("MOUNTSEA_API_KEY", "your-api-key")
BASE_URL = "https://api.mountsea.ai"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}


def text_to_video(prompt: str, duration: int = 5, resolution: str = "1080p") -> dict:
    """
    Generate a video from text description.
    
    Args:
        prompt: Description of the video to generate
        duration: Duration in seconds
        resolution: Video resolution (720p, 1080p, 4K)
    
    Returns:
        Task information including taskId
    """
    response = requests.post(
        f"{BASE_URL}/sora/generate",
        headers=HEADERS,
        json={
            "prompt": prompt,
            "duration": duration,
            "resolution": resolution
        }
    )
    response.raise_for_status()
    return response.json()


def image_to_video(prompt: str, image_url: str, duration: int = 5) -> dict:
    """
    Generate a video from an image.
    
    Args:
        prompt: Description of the animation/motion
        image_url: URL of the source image
        duration: Duration in seconds
    
    Returns:
        Task information including taskId
    """
    response = requests.post(
        f"{BASE_URL}/sora/generate",
        headers=HEADERS,
        json={
            "prompt": prompt,
            "imageUrl": image_url,
            "duration": duration
        }
    )
    response.raise_for_status()
    return response.json()


def wait_for_completion(task_id: str, timeout: int = 600, interval: int = 15) -> dict:
    """
    Wait for a video generation task to complete.
    
    Args:
        task_id: The task ID to monitor
        timeout: Maximum wait time in seconds
        interval: Polling interval in seconds
    
    Returns:
        Completed task results
    """
    start_time = time.time()
    while time.time() - start_time < timeout:
        response = requests.get(
            f"{BASE_URL}/sora/task",
            headers=HEADERS,
            params={"taskId": task_id}
        )
        result = response.json()
        status = result.get("status", "unknown")
        
        print(f"Status: {status}")
        
        if status == "completed":
            return result
        elif status == "failed":
            raise Exception(f"Task failed: {result.get('error', 'Unknown error')}")
        
        time.sleep(interval)
    
    raise TimeoutError(f"Task {task_id} did not complete within {timeout} seconds")


if __name__ == "__main__":
    # Example 1: Text-to-Video
    print("🎬 Generating video from text...")
    task = text_to_video(
        prompt="A golden retriever running through a field of sunflowers at sunset, cinematic, 4K",
        duration=5,
        resolution="1080p"
    )
    print(f"Task created: {task['taskId']}")
    
    print("⏳ Waiting for generation...")
    result = wait_for_completion(task['taskId'])
    print(f"✅ Video generated! URL: {result.get('videoUrl')}")
    
    # Example 2: Image-to-Video
    print("\n🖼️ Generating video from image...")
    task2 = image_to_video(
        prompt="The landscape slowly pans from left to right with clouds drifting",
        image_url="https://example.com/landscape.jpg",
        duration=5
    )
    print(f"Task created: {task2['taskId']}")
    
    print("\n🔗 Documentation: https://docs.mountsea.ai/api-reference/sora/introduction")
    print("🏠 Platform: https://offoff.ai/")

