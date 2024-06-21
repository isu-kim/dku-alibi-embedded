package _chan

import (
	"alibi_backend/ai"
	"alibi_backend/common"
	"alibi_backend/db"
	"errors"
	"log"
	"time"
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
			processImageUpload(imgUpload)
		}
	}
}

// processImageUpload Function
func processImageUpload(upload common.ImageUpload) {
	ret := common.Attendance{
		StudentName: upload.StudentName,
		ImageBase64: upload.Pixels,
		Timestamp:   time.Now(),
	}

	// check engagement of a specific face
	err := ai.CheckEngagement(upload, &ret)
	if err != nil {
		log.Printf("[AI] Unable to check engagement: %v", err)
	}

	err = db.DBH.InsertAttendance(&ret)
	if err != nil {
		log.Printf("[Chan] Unable to store attendance to DB: %v", err)
		return
	}

	log.Printf("[Chan] Successfully stored attendance check to DB")
}
