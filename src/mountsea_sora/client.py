"""
Sora 2 API Client

Generate AI videos using OpenAI Sora 2, Sora Pro via Mountsea AI.
Supports text-to-video and image-to-video generation.

Documentation: https://docs.mountsea.ai/api-reference/sora/introduction
Platform: https://offoff.ai/
"""

import time
import requests


class SoraClient:
    """Client for Mountsea Sora 2 API.

    Args:
        api_key: Your Mountsea AI API key. Get one at https://offoff.ai/
        base_url: API base URL (default: https://api.mountsea.ai)
        timeout: Request timeout in seconds (default: 30)

    Example:
        >>> client = SoraClient("your-api-key")
        >>> task = client.generate("A sunset over the ocean, 4K cinematic")
        >>> result = client.wait(task["taskId"])
        >>> print(result["videoUrl"])
    """

    def __init__(self, api_key: str, base_url: str = "https://api.mountsea.ai", timeout: int = 30):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._session = requests.Session()
        self._session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        })

    def generate(self, prompt: str, duration: int = 5, resolution: str = "1080p", **kwargs) -> dict:
        """Generate a video from a text prompt using Sora 2.

        Args:
            prompt: Text description of the video to generate
            duration: Video duration in seconds (default: 5)
            resolution: Video resolution (default: "1080p")
            **kwargs: Additional parameters (e.g., imageUrl for image-to-video)

        Returns:
            dict with taskId for tracking the generation

        Example:
            >>> task = client.generate("A drone shot of a tropical island")
            >>> print(task["taskId"])
        """
        payload = {"prompt": prompt, "duration": duration, "resolution": resolution, **kwargs}
        resp = self._session.post(f"{self.base_url}/sora/generate", json=payload, timeout=self.timeout)
        resp.raise_for_status()
        return resp.json()

    def image_to_video(self, prompt: str, image_url: str, duration: int = 5, **kwargs) -> dict:
        """Generate a video from an image using Sora 2.

        Args:
            prompt: Text description of the animation
            image_url: URL of the source image
            duration: Video duration in seconds (default: 5)

        Returns:
            dict with taskId for tracking the generation
        """
        return self.generate(prompt=prompt, imageUrl=image_url, duration=duration, **kwargs)

    def get_task(self, task_id: str) -> dict:
        """Get the status of a generation task.

        Args:
            task_id: The task ID returned by generate()

        Returns:
            dict with status, videoUrl (if completed), error (if failed)
        """
        resp = self._session.get(
            f"{self.base_url}/sora/task", params={"taskId": task_id}, timeout=self.timeout
        )
        resp.raise_for_status()
        return resp.json()

    def wait(self, task_id: str, timeout: int = 600, interval: int = 10) -> dict:
        """Wait for a generation task to complete.

        Args:
            task_id: The task ID returned by generate()
            timeout: Maximum wait time in seconds (default: 600)
            interval: Polling interval in seconds (default: 10)

        Returns:
            dict with videoUrl and other result data

        Raises:
            TimeoutError: If the task doesn't complete within timeout
            RuntimeError: If the task fails
        """
        start = time.time()
        while time.time() - start < timeout:
            result = self.get_task(task_id)
            if result.get("status") == "completed":
                return result
            if result.get("status") == "failed":
                raise RuntimeError(f"Sora generation failed: {result.get('error', 'Unknown error')}")
            time.sleep(interval)
        raise TimeoutError(f"Sora task {task_id} timed out after {timeout}s")

