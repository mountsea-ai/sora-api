<?php
/**
 * Sora 2 API - Video Generation Example (PHP)
 * Generate videos using OpenAI Sora 2 via Mountsea AI
 *
 * Documentation: https://docs.mountsea.ai/api-reference/sora/introduction
 * Platform: https://offoff.ai/
 */

$API_KEY = getenv('MOUNTSEA_API_KEY') ?: 'your-api-key';
$BASE_URL = 'https://api.mountsea.ai';

/**
 * Generate video from text prompt (Sora 2 / Sora Pro)
 */
function generateVideo(string $prompt, int $duration = 5, string $resolution = '1080p'): array
{
    global $API_KEY, $BASE_URL;

    $ch = curl_init("$BASE_URL/sora/generate");
    curl_setopt_array($ch, [
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_POST => true,
        CURLOPT_HTTPHEADER => [
            "Authorization: Bearer $API_KEY",
            'Content-Type: application/json',
        ],
        CURLOPT_POSTFIELDS => json_encode([
            'prompt' => $prompt,
            'duration' => $duration,
            'resolution' => $resolution,
        ]),
    ]);

    $response = curl_exec($ch);
    curl_close($ch);

    return json_decode($response, true);
}

/**
 * Check task status
 */
function getTaskStatus(string $taskId): array
{
    global $API_KEY, $BASE_URL;

    $ch = curl_init("$BASE_URL/sora/task?taskId=$taskId");
    curl_setopt_array($ch, [
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_HTTPHEADER => [
            "Authorization: Bearer $API_KEY",
        ],
    ]);

    $response = curl_exec($ch);
    curl_close($ch);

    return json_decode($response, true);
}

/**
 * Wait for task completion
 */
function waitForCompletion(string $taskId, int $timeout = 600, int $interval = 10): array
{
    $start = time();
    while (time() - $start < $timeout) {
        $result = getTaskStatus($taskId);
        echo "Status: {$result['status']}\n";

        if ($result['status'] === 'completed') {
            return $result;
        }
        if ($result['status'] === 'failed') {
            throw new Exception("Task failed: " . ($result['error'] ?? 'Unknown'));
        }

        sleep($interval);
    }
    throw new Exception("Timeout waiting for task $taskId");
}

// --- Main ---
echo "🎬 Generating video with Sora 2...\n";

$task = generateVideo(
    'A golden retriever playing in autumn leaves, cinematic lighting, 4K',
    5,
    '1080p'
);
echo "Task ID: {$task['taskId']}\n";

echo "⏳ Waiting for completion...\n";
$result = waitForCompletion($task['taskId']);
echo "✅ Video URL: {$result['videoUrl']}\n";

echo "\n📘 Docs: https://docs.mountsea.ai/api-reference/sora/introduction\n";
echo "🏠 Platform: https://offoff.ai/\n";

