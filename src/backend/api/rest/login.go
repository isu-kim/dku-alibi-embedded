package rest

import (
	"encoding/json"
	"log"
	"net/http"
)

// login Function
func login(w http.ResponseWriter, r *http.Request) {
	log.Printf("[REST] %s /login", r.RemoteAddr)

	// Struct to hold incoming JSON data
	request := struct {
		Username string `json:"username"`
		Password string `json:"password"`
	}{}

	// Decode JSON body from request
	err := json.NewDecoder(r.Body).Decode(&request)
	if err != nil {
		http.Error(w, "Failed to parse JSON body", http.StatusBadRequest)
		return
	}

	// Struct to hold outgoing JSON response
	response := struct {
		Result  string `json:"result"`
		Success bool   `json:"success"`
	}{}

	// Perform login check
	if request.Username == "isu" && request.Password == "32190984" {
		response.Success = true
		response.Result = "login success"
	} else {
		response.Success = false
		response.Result = "login failed"
		// Set HTTP status code for unauthorized access
		w.WriteHeader(http.StatusUnauthorized) // 401 Unauthorized
	}

	// Encode response as JSON and send it
	err = json.NewEncoder(w).Encode(response)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
}
