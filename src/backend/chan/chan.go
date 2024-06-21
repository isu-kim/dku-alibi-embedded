package _chan

import (
	"alibi_backend/common"
	"errors"
	"log"
)

var Mc *MainChan

// MainChan structure
type MainChan struct {
	ImageUploadChan chan common.ImageUpload
}

// init Function
func init() {
	Mc = NewMainChan()
}

// NewMainChan Function
func NewMainChan() *MainChan {
	return &MainChan{
		ImageUploadChan: make(chan common.ImageUpload),
	}
}

// InsertData Function
func (mc *MainChan) InsertData(data interface{}) error {
	switch data.(type) {
	case common.ImageUpload: // image upload from gRPC
		converted := data.(common.ImageUpload)
		mc.ImageUploadChan <- converted
	default:
		return errors.New("unsupported type")
	}

	return nil
}

// Start Function
func (mc *MainChan) Start() {
	for {
		select {
		case imgUpload := <-mc.ImageUploadChan:
			log.Printf("[Chan] Received Image Upload, (%s, %f)", imgUpload.StudentName, imgUpload.Accuracy)
			// @todo, make this be added
		}
	}
}
