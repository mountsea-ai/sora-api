# 🎬 Sora 2 API - OpenAI Sora API | Sora Pro | Text-to-Video API

[English](#english) | [中文](#中文)

> Access **OpenAI Sora 2** (Sora Pro, Sora2, Sora-2) text-to-video and image-to-video generation through a simple, affordable API. The cheapest Sora 2 API access available.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![API Status](https://img.shields.io/badge/API-Online-green.svg)](https://offoff.ai/)
[![Documentation](https://img.shields.io/badge/Docs-Available-blue.svg)](https://docs.mountsea.ai/api-reference/sora/introduction)

<!-- Banner Image - replace with actual banner -->
<!-- ![Sora 2 API Banner](assets/banner.png) -->

---

<a name="english"></a>

## 🤔 What is Sora 2 API?

**Sora 2** (also known as Sora Pro, Sora2, OpenAI Sora) is OpenAI's latest AI video generation model. This project provides the **cheapest and easiest way** to access Sora 2 API through [Mountsea AI](https://offoff.ai/).

### Supported Models

| Model | Also Known As | Description |
|-------|--------------|-------------|
| **Sora 2** | Sora-2, Sora2, OpenAI Sora 2 | Latest text-to-video model |
| **Sora Pro** | Sora-Pro, SoraPro | High-quality production model |

## ✨ Features

- 🎥 **Text-to-Video** – Generate stunning videos from text descriptions
- 🖼️ **Image-to-Video** – Animate static images into dynamic videos
- ⚡ **Fast Generation** – Optimized infrastructure for quick results
- 💰 **Affordable Pricing** – Up to 50% cheaper than alternatives
- 🔄 **Task Management** – Easy-to-use async task system

## 🚀 Quick Start

### Install SDK

```bash
# Python
pip install mountsea-sora

# Node.js
npm install mountsea-sora
```

### Get Your API Key

1. Visit [Mountsea AI Platform](https://offoff.ai/)
2. Sign up and get your API key
3. Start generating videos!

### Python SDK Example

```python
from mountsea_sora import SoraClient

client = SoraClient("your-api-key")
task = client.generate("A golden retriever playing in autumn leaves, cinematic 4K")
result = client.wait(task["taskId"])
print(result["videoUrl"])
```

### Node.js SDK Example

```javascript
const { SoraClient } = require('mountsea-sora');

const client = new SoraClient('your-api-key');
const task = await client.generate('A golden retriever in autumn leaves, 4K');
const result = await client.wait(task.taskId);
console.log(result.videoUrl);
```

### Python Example (requests)

```python
import requests
import time

API_KEY = "your-api-key"
BASE_URL = "https://api.mountsea.ai"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Text-to-Video Generation
response = requests.post(
    f"{BASE_URL}/sora/generate",
    headers=headers,
    json={
        "prompt": "A golden retriever playing in autumn leaves in a park, cinematic lighting, 4K",
        "duration": 5,
        "resolution": "1080p"
    }
)

task = response.json()
task_id = task['taskId']
print(f"Task ID: {task_id}")

# Poll for results
while True:
    status = requests.get(
        f"{BASE_URL}/sora/task",
        headers=headers,
        params={"taskId": task_id}
    ).json()
    
    if status['status'] == 'completed':
        print(f"Video URL: {status['videoUrl']}")
        break
    elif status['status'] == 'failed':
        print(f"Error: {status['error']}")
        break
    
    print(f"Status: {status['status']}...")
    time.sleep(10)
```

### Image-to-Video

```python
# Animate an image
response = requests.post(
    f"{BASE_URL}/sora/generate",
    headers=headers,
    json={
        "prompt": "The person in the image slowly turns and smiles",
        "imageUrl": "https://example.com/your-image.jpg",
        "duration": 5
    }
)

task = response.json()
print(f"Task ID: {task['taskId']}")
```

### JavaScript / Node.js

```javascript
const axios = require('axios');

const API_KEY = process.env.MOUNTSEA_API_KEY || 'your-api-key';
const BASE_URL = 'https://api.mountsea.ai';

async function generateVideo(prompt, options = {}) {
  const response = await axios.post(`${BASE_URL}/sora/generate`, {
    prompt,
    duration: options.duration || 5,
    resolution: options.resolution || '1080p',
    ...options
  }, {
    headers: {
      'Authorization': `Bearer ${API_KEY}`,
      'Content-Type': 'application/json'
    }
  });

  return response.data;
}

async function waitForResult(taskId) {
  while (true) {
    const { data } = await axios.get(`${BASE_URL}/sora/task`, {
      headers: { 'Authorization': `Bearer ${API_KEY}` },
      params: { taskId }
    });

    if (data.status === 'completed') return data;
    if (data.status === 'failed') throw new Error(data.error);
    
    console.log(`Status: ${data.status}...`);
    await new Promise(r => setTimeout(r, 10000));
  }
}

// Usage
(async () => {
  const task = await generateVideo(
    'A timelapse of a city skyline from day to night, 4K cinematic'
  );
  console.log('Task created:', task.taskId);

  const result = await waitForResult(task.taskId);
  console.log('Video URL:', result.videoUrl);
})();
```

### cURL

```bash
# Text-to-Video
curl -X POST https://api.mountsea.ai/sora/generate \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A beautiful sunset over the ocean with waves crashing on the shore",
    "duration": 5,
    "resolution": "1080p"
  }'

# Image-to-Video
curl -X POST https://api.mountsea.ai/sora/generate \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "The landscape slowly pans from left to right with clouds moving",
    "imageUrl": "https://example.com/landscape.jpg",
    "duration": 5
  }'

# Check Task Status
curl -X GET "https://api.mountsea.ai/sora/task?taskId=YOUR_TASK_ID" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

## 📖 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/sora/generate` | POST | Generate video from text or image |
| `/sora/task` | GET | Get task status and results |

## 🎯 Use Cases

- 🎬 **Content Creation** – Generate marketing videos, social media content
- 🎨 **Creative Projects** – Bring artistic visions to life
- 📱 **App Development** – Add AI video generation to your app
- 🏢 **Enterprise** – Automate video production workflows
- 📚 **Education** – Create educational video content

## 💰 Pricing

Mountsea AI offers the most competitive pricing for Sora API:

| Package | Credits | Price |
|---------|---------|-------|
| Starter | 10,000 | ¥100 |
| Basic | 50,000 | ¥500 |
| Pro | 200,000 | ¥2,000 |
| Business | 500,000 | ¥4,500 (10% OFF) |
| Enterprise | 1,000,000 | ¥8,000 (20% OFF) |

👉 [View Full Pricing](https://offoff.ai/)

## 📚 Documentation

- 📘 [Sora API Documentation](https://docs.mountsea.ai/api-reference/sora/introduction)
- 🏠 [Mountsea AI Platform](https://offoff.ai/)

## 🔗 Related Projects

- [Suno API](https://github.com/mountsea-ai/suno-api) - AI Music Generation API
- [Veo API](https://github.com/mountsea-ai/veo-api) - Google Veo Video Generation API
- [Gemini API](https://github.com/mountsea-ai/gemini-api) - Google Gemini API
- [OpenAI Compatible API](https://github.com/mountsea-ai/openai-compatible-api) - OpenAI-compatible Chat API

---

<a name="中文"></a>

## 🇨🇳 中文文档

# 🎬 Sora 2 API - OpenAI Sora API | Sora Pro | AI 视频生成

> 通过简单、实惠的 API 访问 **OpenAI Sora 2**（Sora Pro、Sora2、Sora-2）视频生成能力。最便宜的 Sora 2 API 接入方案。

## ✨ 功能特点

- 🎥 **文本生成视频** – 从文字描述生成精彩视频
- 🖼️ **图片生成视频** – 将静态图片动态化
- ⚡ **快速生成** – 优化的基础设施，快速出结果
- 💰 **价格实惠** – 比竞品便宜高达 50%
- 🔄 **任务管理** – 简单易用的异步任务系统

## 🚀 快速开始

### 获取 API 密钥

1. 访问 [Mountsea AI 平台](https://offoff.ai/)
2. 注册账号并获取 API 密钥
3. 开始生成视频！

### Python 示例

```python
import requests

API_KEY = "your-api-key"
BASE_URL = "https://api.mountsea.ai"

# 文本生成视频
response = requests.post(
    f"{BASE_URL}/sora/generate",
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    },
    json={
        "prompt": "一只金毛犬在秋叶中玩耍，电影级光影，4K",
        "duration": 5,
        "resolution": "1080p"
    }
)

task = response.json()
print(f"任务 ID: {task['taskId']}")
```

## 📖 API 接口

| 接口 | 方法 | 描述 |
|------|------|------|
| `/sora/generate` | POST | 从文本或图片生成视频 |
| `/sora/task` | GET | 获取任务状态和结果 |

## 📚 文档

- 📘 [Sora API 完整文档](https://docs.mountsea.ai/api-reference/sora/introduction)
- 🏠 [Mountsea AI 官网](https://offoff.ai/)

## ⭐ Star History

如果这个项目对你有帮助，请给我们一个 Star ⭐

## 📄 License

[MIT License](LICENSE)

---

**Powered by [Mountsea AI](https://offoff.ai/) – 全球顶级 AI 视频和音乐生成器 API 一体化平台**

<!-- Auto-updated by CI -->
> Last API Check: 2026-03-06 | Status: online
