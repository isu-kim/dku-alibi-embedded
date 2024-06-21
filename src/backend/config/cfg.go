package config

import (
	"os"
	"strconv"
)

var Host string
var GRPCPort int
var RESTPort int

// init Function
func init() {
	loadEnv()
}

// loadEnv Function
func loadEnv() {
	host, hostExists := os.LookupEnv("HOST")
	gRPCPort, portExists := os.LookupEnv("GRPC_PORT")
	restPort, portExists := os.LookupEnv("REST_PORT")

	// parse host
	if !hostExists || host == "" {
		Host = "0.0.0.0"
	} else {
		Host = host
	}

	// parse gRPC Port
	if !portExists || gRPCPort == "" {
		GRPCPort = 9090
	} else {
		p, err := strconv.Atoi(gRPCPort)
		if err != nil {
			GRPCPort = 9090
		} else {
			GRPCPort = p
		}
	}

	// parse REST API port
	if !portExists || restPort == "" {
		RESTPort = 9091
	} else {
		p, err := strconv.Atoi(restPort)
		if err != nil {
			RESTPort = 9091
		} else {
			RESTPort = p
		}
	}
}
