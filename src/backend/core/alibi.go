package core

import "main/api"

var AlibiH *Alibi

// init Function
func init() {
	// @todo: add init logic
}

// Alibi struct
type Alibi struct {
	host      string `yaml:"host"`
	port      int    `yaml:"port"`
	apiServer *api.Server
}

// NewAlibi Function
func NewAlibi(host string, port int) *Alibi {
	ret := &Alibi{
		host: host,
		port: port,
	}

	ret.apiServer = api.NewServer(host, port)
	AlibiH = ret

	return ret
}

// DestroyAlibi Function
func (ah *Alibi) DestroyAlibi() {
	// @todo add close logic

}

// Run Function
func (ah *Alibi) Run() error {
	// @todo: add more run start function
	ah.apiServer.Start()

	return nil
}
