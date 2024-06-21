package core

import (
	"alibi_backend/api"
	"alibi_backend/chan"
)

var AlibiH *Alibi

// Alibi struct
type Alibi struct {
	apiServer *api.Server
	mc        *_chan.MainChan
}

func init() {
	AlibiH = NewAlibi()
}

// NewAlibi Function
func NewAlibi() *Alibi {
	return &Alibi{
		apiServer: api.ApiS,
		mc:        _chan.Mc,
	}
}

// DestroyAlibi Function
func (ah *Alibi) DestroyAlibi() {
	// @todo add close logic
}

// Run Function
func (ah *Alibi) Run() error {
	// run gRPC, REST API
	ah.apiServer.Start()

	// run channels
	ah.mc.Start()

	return nil
}
