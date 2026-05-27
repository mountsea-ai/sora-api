"""
Mountsea Sora SDK - Generate videos with OpenAI Sora 2 API

Quick Start:
    >>> from mountsea_sora import SoraClient
    >>> client = SoraClient("your-api-key")
    >>> task = client.generate("A cat playing in autumn leaves, cinematic 4K")
    >>> result = client.wait(task["taskId"])
    >>> print(result["videoUrl"])

Documentation: https://docs.mountsea.ai/api-reference/sora/introduction
Platform: https://offoff.ai/
"""

from .client import SoraClient

__version__ = "1.0.0"
__all__ = ["SoraClient"]

