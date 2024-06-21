package grpc

import (
	"alibi_backend/chan"
	"alibi_backend/common"
	apb "alibi_backend/protobuf"
	"io"
	"log"
)

// ImageHandler Structure
type ImageHandler struct {
	is apb.ImageUploadServiceServer
	apb.UnimplementedImageUploadServiceServer
}

// UploadImage Function
func (i ImageHandler) UploadImage(stream apb.ImageUploadService_UploadImageServer) error {
	for {
		event, err := stream.Recv()
		if err == io.EOF {
			return nil
		} else if err != nil {
			log.Printf("[gRPC] Alibi failed to receive an image: %v", err)
			return err
		}

		// convert, and insert
		ims := parseImageStruct(event)
		err = _chan.Mc.InsertData(ims)
		if err != nil {
			log.Printf("[gRPC] Alibi failed to insert data into channel")
			return nil
		}
	}
}

// parseImageStruct Function
func parseImageStruct(request *apb.StudentFaceRequest) common.ImageUpload {
	return common.ImageUpload{
		StudentName: request.DetectedName,
		Accuracy:    request.Accuracy,
		Pixels:      request.ImageDataB64,
	}
}
