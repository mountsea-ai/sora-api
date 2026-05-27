/**
 * Mountsea Sora SDK - Generate videos with OpenAI Sora 2 API
 *
 * @example
 * const { SoraClient } = require('mountsea-sora');
 * const client = new SoraClient('your-api-key');
 * const task = await client.generate('A cat playing in autumn leaves, 4K');
 * const result = await client.wait(task.taskId);
 * console.log(result.videoUrl);
 *
 * Documentation: https://docs.mountsea.ai/api-reference/sora/introduction
 * Platform: https://offoff.ai/
 */

const https = require('https');
const http = require('http');
const { URL } = require('url');

class SoraClient {
  /**
   * @param {string} apiKey - Your Mountsea AI API key (get one at https://offoff.ai/)
   * @param {object} [options]
   * @param {string} [options.baseUrl='https://api.mountsea.ai'] - API base URL
   * @param {number} [options.timeout=30000] - Request timeout in ms
   */
  constructor(apiKey, options = {}) {
    this.apiKey = apiKey;
    this.baseUrl = (options.baseUrl || 'https://api.mountsea.ai').replace(/\/$/, '');
    this.timeout = options.timeout || 30000;
  }

  /**
   * Generate a video from a text prompt using Sora 2
   * @param {string} prompt - Text description
   * @param {object} [options] - { duration, resolution, imageUrl, ... }
   * @returns {Promise<{taskId: string}>}
   */
  async generate(prompt, options = {}) {
    return this._post('/sora/generate', { prompt, duration: 5, resolution: '1080p', ...options });
  }

  /**
   * Generate a video from an image
   * @param {string} prompt - Animation description
   * @param {string} imageUrl - Source image URL
   * @param {object} [options]
   * @returns {Promise<{taskId: string}>}
   */
  async imageToVideo(prompt, imageUrl, options = {}) {
    return this.generate(prompt, { imageUrl, ...options });
  }

  /**
   * Get task status
   * @param {string} taskId
   * @returns {Promise<{status: string, videoUrl?: string, error?: string}>}
   */
  async getTask(taskId) {
    return this._get(`/sora/task?taskId=${encodeURIComponent(taskId)}`);
  }

  /**
   * Wait for a task to complete
   * @param {string} taskId
   * @param {object} [options] - { timeout: 600000, interval: 10000 }
   * @returns {Promise<{videoUrl: string}>}
   */
  async wait(taskId, options = {}) {
    const timeout = options.timeout || 600000;
    const interval = options.interval || 10000;
    const start = Date.now();

    while (Date.now() - start < timeout) {
      const result = await this.getTask(taskId);
      if (result.status === 'completed') return result;
      if (result.status === 'failed') throw new Error(`Sora failed: ${result.error || 'Unknown'}`);
      await new Promise(r => setTimeout(r, interval));
    }
    throw new Error(`Sora task ${taskId} timed out after ${timeout}ms`);
  }

  /** @private */
  _post(path, body) {
    return this._request('POST', path, body);
  }

  /** @private */
  _get(path) {
    return this._request('GET', path);
  }

  /** @private */
  _request(method, path, body) {
    return new Promise((resolve, reject) => {
      const url = new URL(this.baseUrl + path);
      const mod = url.protocol === 'https:' ? https : http;
      const options = {
        method, hostname: url.hostname, port: url.port, path: url.pathname + url.search,
        headers: { 'Authorization': `Bearer ${this.apiKey}`, 'Content-Type': 'application/json' },
        timeout: this.timeout,
      };
      const req = mod.request(options, (res) => {
        let data = '';
        res.on('data', chunk => data += chunk);
        res.on('end', () => {
          try { resolve(JSON.parse(data)); } catch { reject(new Error(`Invalid JSON: ${data}`)); }
        });
      });
      req.on('error', reject);
      req.on('timeout', () => { req.destroy(); reject(new Error('Request timeout')); });
      if (body) req.write(JSON.stringify(body));
      req.end();
    });
  }
}

module.exports = { SoraClient };

