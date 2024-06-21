package config

import (
	"os"
	"strconv"
)

var Host string
var GRPCPort int
var RESTPort int
var MongoDB string
var EngagementEngine string

// init Function
func init() {
	loadEnv()
}

// loadEnv Function
func loadEnv() {
	host, hostExists := os.LookupEnv("HOST")
	gRPCPort, portExists := os.LookupEnv("GRPC_PORT")
	restPort, portExists := os.LookupEnv("REST_PORT")
	mongodb, mongodbExists := os.LookupEnv("MONGODB_HOST")
	engagement, engagementExists := os.LookupEnv("AI_ENGINE_HOST")

	// parse host
	if !hostExists || host == "" {
		Host = "0.0.0.0"
	} else {
		Host = host
	}

	// parse mongodb
	if !mongodbExists || mongodb == "" {
		MongoDB = "mongodb://127.0.0.1:27018"
	} else {
		MongoDB = mongodb
	}

	// parse engagement engine
	if !engagementExists || engagement == "" {
		EngagementEngine = "http://127.0.0.1:9092"
	} else {
		EngagementEngine = engagement
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
