package rest

import (
	"alibi_backend/db"
	"encoding/json"
	"log"
	"net/http"
)

// getStudents Function
func getStudents(w http.ResponseWriter, r *http.Request) {
	log.Printf("[REST] %s /get_students", r.RemoteAddr)

	students, err := db.DBH.GetAllAttendances()
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	err = json.NewEncoder(w).Encode(students)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	w.WriteHeader(http.StatusOK)
}
