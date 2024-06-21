package main

import (
	"log"
	"main/core"
)

// main Function
func main() {
	core.NewAlibi("0.0.0.0", 8080)
	err := core.AlibiH.Run()
	if err != nil {
		log.Fatalf("%v", err)
	}
}
