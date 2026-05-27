/**
 * Sora 2 API - Video Generation Example (Node.js)
 * Generate videos using OpenAI Sora 2 via Mountsea AI
 *
 * Documentation: https://docs.mountsea.ai/api-reference/sora/introduction
 * Platform: https://offoff.ai/
 */

const axios = require('axios');

const API_KEY = process.env.MOUNTSEA_API_KEY || 'your-api-key';
const BASE_URL = 'https://api.mountsea.ai';

const headers = {
  'Authorization': `Bearer ${API_KEY}`,
  'Content-Type': 'application/json'
};

/**
 * Generate video from text prompt (Sora 2 / Sora Pro)
 */
async function textToVideo(prompt, duration = 5, resolution = '1080p') {
  const { data } = await axios.post(`${BASE_URL}/sora/generate`, {
    prompt, duration, resolution
  }, { headers });
  return data;
}

/**
 * Generate video from image (Image-to-Video)
 */
async function imageToVideo(prompt, imageUrl, duration = 5) {
  const { data } = await axios.post(`${BASE_URL}/sora/generate`, {
    prompt, imageUrl, duration
  }, { headers });
  return data;
}

/**
 * Poll for task completion
 */
async function waitForResult(taskId, timeout = 600000, interval = 10000) {
  const start = Date.now();
  while (Date.now() - start < timeout) {
    const { data } = await axios.get(`${BASE_URL}/sora/task`, {
      headers, params: { taskId }
    });

    console.log(`Status: ${data.status}`);
    if (data.status === 'completed') return data;
    if (data.status === 'failed') throw new Error(data.error || 'Generation failed');

    await new Promise(r => setTimeout(r, interval));
  }
  throw new Error('Timeout waiting for video generation');
}

// --- Main ---
(async () => {
  try {
    // Text-to-Video
    console.log('🎬 Generating video with Sora 2...');
    const task = await textToVideo(
      'A drone flying over a tropical island with crystal clear water, cinematic 4K',
      5, '1080p'
    );
    console.log('Task ID:', task.taskId);

    const result = await waitForResult(task.taskId);
    console.log('✅ Video URL:', result.videoUrl);

    // Image-to-Video
    console.log('\n🖼️ Animating image...');
    const task2 = await imageToVideo(
      'The landscape slowly pans with clouds drifting across the sky',
      'https://example.com/landscape.jpg'
    );
    console.log('Task ID:', task2.taskId);

  } catch (err) {
    console.error('Error:', err.message);
  }

  console.log('\n📘 Docs: https://docs.mountsea.ai/api-reference/sora/introduction');
  console.log('🏠 Platform: https://offoff.ai/');
})();

