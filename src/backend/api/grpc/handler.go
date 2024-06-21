package grpc

import (
	"alibi_backend/config"
	apb "alibi_backend/protobuf"
	"fmt"
	"google.golang.org/grpc"
	"log"
	"net"
)

// GrpcH Global reference
var GrpcH *AlibiGRPCHandler

// init function
func init() {
	GrpcH = NewAlibiGRPCHandler()
}

// AlibiGRPCHandler Structure
type AlibiGRPCHandler struct {
	lis    net.Listener
	server *grpc.Server

	iuss *ImageHandler
}

// NewAlibiGRPCHandler Function
func NewAlibiGRPCHandler() *AlibiGRPCHandler {
	return &AlibiGRPCHandler{
		iuss: new(ImageHandler),
	}
}

// Start Function
func Start() error {
	var err error

	// listen gRPC
	listenAddr := fmt.Sprintf("%s:%d", config.Host, config.GRPCPort)
	GrpcH.lis, err = net.Listen("tcp", listenAddr)
	if err != nil {
		return err
	}

	log.Printf("[gRPC] Listening Alibi gRPC Services at %s", listenAddr)

	// init gRPC server and services
	GrpcH.server = grpc.NewServer()
	GrpcH.registerGRPCServices()

	// start serving
	log.Printf("[gRPC] Serving Alibi gRPC Services %s", listenAddr)
	go func() {
		err := GrpcH.server.Serve(GrpcH.lis)
		if err != nil {
			log.Printf("[gRPC] Failed to serve gRPC: %v", err)
		}
	}()

	return nil
}

// registerGRPCServices Function
func (ah *AlibiGRPCHandler) registerGRPCServices() {
	// image upload service
	apb.RegisterImageUploadServiceServer(ah.server, *ah.iuss)
	log.Printf("[gRPC] Initialized Alibi Image upload service")
}
