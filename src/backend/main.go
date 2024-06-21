package main

import (
	"alibi_backend/core"
	"log"
)

// main Function
func main() {
	err := core.AlibiH.Run()
	if err != nil {
		log.Fatalf("%v", err)
	}
}
