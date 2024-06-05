package api

import (
	"fmt"
	"net/http"
)

// Server structure
type Server struct {
	Host   string
	Port   int
	server *http.Server
}

// NewServer Function
func NewServer(host string, port int) *Server {
	return &Server{
		Host: host,
		Port: port,
	}
}

// Init Function
func (s *Server) Init() {
	s.server = &http.Server{
		Addr: fmt.Sprintf("%s:%d", s.Host, s.Port),
	}
}

// Start Function
func (s *Server) Start() {
	if s.server == nil {
		s.Init()
	}

	// run in other goroutine
	go func() {
		err := s.server.ListenAndServe()
		if err != nil {
			return
		}
	}()
}
