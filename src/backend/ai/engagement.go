package ai

import (
	"alibi_backend/common"
	"alibi_backend/config"
	"bytes"
	"encoding/json"
	"errors"
	"net/http"
)

// CheckEngagement Function
func CheckEngagement(data common.ImageUpload, attendance *common.Attendance) error {
	request := struct {
		PixelsB64 string `json:"pixels_b_64"`
	}{
		PixelsB64: data.Pixels,
	}

	requestBody, err := json.Marshal(request)
	if err != nil {
		return err
	}

	url := config.EngagementEngine + "/engagement"
	resp, err := http.Post(url, "application/json", bytes.NewBuffer(requestBody))
	if err != nil {
		return err
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return errors.New("failed to get a successful response from the engagement engine")
	}

	var responsePayload struct {
		Status   string `json:"status"`
		Sleeping bool   `json:"sleeping"`
		Yawning  bool   `json:"yawning"`
	}

	err = json.NewDecoder(resp.Body).Decode(&responsePayload)
	if err != nil {
		return err
	}

	if responsePayload.Status != "success" {
		return errors.New("engagement engine returned a failure status")
	}

	attendance.Yawning = responsePayload.Yawning
	attendance.Sleeping = responsePayload.Sleeping
	return nil
}
