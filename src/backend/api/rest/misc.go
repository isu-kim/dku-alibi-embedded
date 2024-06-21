package rest

import (
	"encoding/json"
	"log"
	"net/http"
)

// healthCheck Function
func healthCheck(w http.ResponseWriter, r *http.Request) {
	log.Printf("[REST] %s /health_check", r.RemoteAddr)
	response := struct {
		Result  string `json:"result"`
		Success bool   `json:"success"`
	}{
		Success: true,
		Result:  "API running",
	}

	w.WriteHeader(http.StatusOK) // Set the status code to 200 OK

	err := json.NewEncoder(w).Encode(response)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
}
