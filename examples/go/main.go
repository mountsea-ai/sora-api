// Sora 2 API - Video Generation Example (Go)
// Generate videos using OpenAI Sora 2 via Mountsea AI
//
// Documentation: https://docs.mountsea.ai/api-reference/sora/introduction
// Platform: https://offoff.ai/

package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"
	"time"
)

const baseURL = "https://api.mountsea.ai"

var apiKey = getEnv("MOUNTSEA_API_KEY", "your-api-key")

func getEnv(key, fallback string) string {
	if v := os.Getenv(key); v != "" {
		return v
	}
	return fallback
}

// GenerateRequest represents a video generation request
type GenerateRequest struct {
	Prompt     string `json:"prompt"`
	Duration   int    `json:"duration,omitempty"`
	Resolution string `json:"resolution,omitempty"`
	ImageURL   string `json:"imageUrl,omitempty"`
}

// TaskResponse represents the API response
type TaskResponse struct {
	TaskID   string `json:"taskId"`
	Status   string `json:"status"`
	VideoURL string `json:"videoUrl"`
	Error    string `json:"error"`
}

// generateVideo sends a video generation request
func generateVideo(req GenerateRequest) (*TaskResponse, error) {
	body, _ := json.Marshal(req)

	httpReq, _ := http.NewRequest("POST", baseURL+"/sora/generate", bytes.NewBuffer(body))
	httpReq.Header.Set("Authorization", "Bearer "+apiKey)
	httpReq.Header.Set("Content-Type", "application/json")

	resp, err := http.DefaultClient.Do(httpReq)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	data, _ := io.ReadAll(resp.Body)
	var result TaskResponse
	json.Unmarshal(data, &result)
	return &result, nil
}

// waitForCompletion polls until the task is done
func waitForCompletion(taskID string, timeout time.Duration) (*TaskResponse, error) {
	start := time.Now()
	for time.Since(start) < timeout {
		req, _ := http.NewRequest("GET", fmt.Sprintf("%s/sora/task?taskId=%s", baseURL, taskID), nil)
		req.Header.Set("Authorization", "Bearer "+apiKey)

		resp, err := http.DefaultClient.Do(req)
		if err != nil {
			return nil, err
		}

		data, _ := io.ReadAll(resp.Body)
		resp.Body.Close()

		var result TaskResponse
		json.Unmarshal(data, &result)

		fmt.Printf("Status: %s\n", result.Status)

		switch result.Status {
		case "completed":
			return &result, nil
		case "failed":
			return nil, fmt.Errorf("task failed: %s", result.Error)
		}

		time.Sleep(10 * time.Second)
	}
	return nil, fmt.Errorf("timeout waiting for task %s", taskID)
}

func main() {
	// Text-to-Video with Sora 2
	fmt.Println("🎬 Generating video with Sora 2...")
	task, err := generateVideo(GenerateRequest{
		Prompt:     "A golden retriever running through autumn leaves in a park, cinematic 4K",
		Duration:   5,
		Resolution: "1080p",
	})
	if err != nil {
		fmt.Printf("Error: %v\n", err)
		return
	}
	fmt.Printf("Task ID: %s\n", task.TaskID)

	// Wait for result
	result, err := waitForCompletion(task.TaskID, 10*time.Minute)
	if err != nil {
		fmt.Printf("Error: %v\n", err)
		return
	}
	fmt.Printf("✅ Video URL: %s\n", result.VideoURL)

	fmt.Println("\n📘 Docs: https://docs.mountsea.ai/api-reference/sora/introduction")
	fmt.Println("🏠 Platform: https://offoff.ai/")
}

