package core

var AlibiH Alibi

// init Function
func init() {
	AlibiH = Alibi{}
}

// Alibi struct
type Alibi struct {
	host string `yaml:"host"`
	port int    `yaml:"port"`
}

// NewAlibi Function
func NewAlibi() *Alibi {

}

// DestroyAlibi Function
func (ah *Alibi) DestroyAlibi() {
	// @todo add close logic

}
