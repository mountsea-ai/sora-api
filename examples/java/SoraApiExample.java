/**
 * Sora 2 API - Video Generation Example (Java)
 * Generate videos using OpenAI Sora 2 via Mountsea AI
 *
 * Documentation: https://docs.mountsea.ai/api-reference/sora/introduction
 * Platform: https://offoff.ai/
 *
 * Dependencies: Java 11+ (uses java.net.http)
 */

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

public class SoraApiExample {

    private static final String API_KEY = System.getenv("MOUNTSEA_API_KEY") != null
            ? System.getenv("MOUNTSEA_API_KEY") : "your-api-key";
    private static final String BASE_URL = "https://api.mountsea.ai";

    public static void main(String[] args) throws Exception {
        HttpClient client = HttpClient.newHttpClient();

        // 1. Submit text-to-video generation task (Sora 2 / Sora Pro)
        System.out.println("🎬 Generating video with Sora 2...");

        String requestBody = """
                {
                    "prompt": "A beautiful sunset over the ocean with waves crashing on rocks, cinematic 4K",
                    "duration": 5,
                    "resolution": "1080p"
                }
                """;

        HttpRequest generateRequest = HttpRequest.newBuilder()
                .uri(URI.create(BASE_URL + "/sora/generate"))
                .header("Authorization", "Bearer " + API_KEY)
                .header("Content-Type", "application/json")
                .POST(HttpRequest.BodyPublishers.ofString(requestBody))
                .build();

        HttpResponse<String> generateResponse = client.send(generateRequest,
                HttpResponse.BodyHandlers.ofString());

        System.out.println("Response: " + generateResponse.body());

        // Extract taskId (simple parsing - use a JSON library in production)
        String taskId = extractJsonValue(generateResponse.body(), "taskId");
        System.out.println("Task ID: " + taskId);

        // 2. Poll for results
        System.out.println("⏳ Waiting for completion...");
        while (true) {
            HttpRequest statusRequest = HttpRequest.newBuilder()
                    .uri(URI.create(BASE_URL + "/sora/task?taskId=" + taskId))
                    .header("Authorization", "Bearer " + API_KEY)
                    .GET()
                    .build();

            HttpResponse<String> statusResponse = client.send(statusRequest,
                    HttpResponse.BodyHandlers.ofString());
            String body = statusResponse.body();
            String status = extractJsonValue(body, "status");

            System.out.println("Status: " + status);

            if ("completed".equals(status)) {
                String videoUrl = extractJsonValue(body, "videoUrl");
                System.out.println("✅ Video URL: " + videoUrl);
                break;
            } else if ("failed".equals(status)) {
                System.out.println("❌ Generation failed");
                break;
            }

            Thread.sleep(10000); // Wait 10 seconds
        }

        System.out.println("\n📘 Docs: https://docs.mountsea.ai/api-reference/sora/introduction");
        System.out.println("🏠 Platform: https://offoff.ai/");
    }

    // Simple JSON value extractor (use Gson/Jackson in production)
    private static String extractJsonValue(String json, String key) {
        int start = json.indexOf("\"" + key + "\"");
        if (start == -1) return "";
        start = json.indexOf(":", start) + 1;
        int valueStart = json.indexOf("\"", start) + 1;
        int valueEnd = json.indexOf("\"", valueStart);
        return json.substring(valueStart, valueEnd);
    }
}

