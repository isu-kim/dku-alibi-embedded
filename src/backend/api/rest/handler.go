package rest

import (
	"alibi_backend/config"
	"fmt"
	"github.com/gorilla/mux"
	"log"
	"net/http"
)

// RestH Global reference
var RestH *AlibiRestHandler

// init Function
func init() {
	RestH = NewAlibiRestHandler()
}

// AlibiRestHandler Function
type AlibiRestHandler struct {
	server *http.Server
	router *mux.Router
}

// NewAlibiRestHandler Function
func NewAlibiRestHandler() *AlibiRestHandler {
	return &AlibiRestHandler{}
}

// Start Function
func Start() error {
	// register endpoints
	RestH.registerEndpoints()

	// listen REST API
	listenAddr := fmt.Sprintf("%s:%d", config.Host, config.RESTPort)
	RestH.server = &http.Server{
		Addr:    listenAddr,
		Handler: RestH.router,
	}

	log.Printf("[REST] Listening Alibi REST Services at %s", listenAddr)
	log.Printf("[REST] Serving Alibi REST Services at %s", listenAddr)

	go func() {
		err := RestH.server.ListenAndServe()
		if err != nil {
			log.Printf("[REST] Failed to serve REST API: %v", err)
		}
	}()

	return nil
}

// registerEndpoints Function
func (ah *AlibiRestHandler) registerEndpoints() {
	ah.router = mux.NewRouter()

	// /health endpoint
	ah.router.HandleFunc("/health", func(writer http.ResponseWriter, request *http.Request) {
		healthCheck(writer, request)
	}).Methods("GET")

	// /login endpoint
	ah.router.HandleFunc("/login", func(writer http.ResponseWriter, request *http.Request) {
		login(writer, request)
	}).Methods("POST")
}
