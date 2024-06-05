package api

import "net/http"

// Server structure
type Server struct {
	Host string
	Port string
	server
}

// NewServer Function
func NewServer(host string, port string) *Server {
	return &Server{
		Host: host,
		Port: port,
	}
}

// Init Function
func (s *Server) Init() {

}

// Start Function
func (s *Server) Start() error {
	s.server.
}