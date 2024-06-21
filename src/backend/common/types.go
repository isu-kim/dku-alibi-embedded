package common

import "time"

// ImageUpload structure
type ImageUpload struct {
	StudentName string
	Accuracy    float32
	Pixels      string
}

// Attendance Structure
type Attendance struct {
	StudentName string    `json:"student_name" bson:"student_name"`
	Yawning     bool      `json:"yawning" bson:"'yawning'"`
	Sleeping    bool      `json:"sleeping" bson:"sleeping"`
	Timestamp   time.Time `json:"timestamp" bson:"timestamp"`
	ClassName   string    `json:"class_name" bson:"class_name"`
	ImageBase64 string    `json:"image_base_64" bson:"image_base_64"`
}
