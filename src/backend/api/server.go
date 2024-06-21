package api

import (
	"alibi_backend/api/grpc"
	"alibi_backend/api/rest"
)

// ApiS global reference
var ApiS *Server

// init Function
func init() {
	ApiS = NewServer()
}

// Server structure
type Server struct {
	restServer *rest.AlibiRestHandler
	gRPCServer *grpc.AlibiGRPCHandler
}

// NewServer Function
func NewServer() *Server {
	return &Server{
		restServer: rest.RestH,
		gRPCServer: grpc.GrpcH,
	}
}

// Start Function
func (s *Server) Start() {
	// run gRPC Server
	err := grpc.Start()
	if err != nil {
		return
	}

	// run REST API Server
	err = rest.Start()
	if err != nil {
		return
	}
}
