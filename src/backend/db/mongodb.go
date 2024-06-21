package db

import (
	"alibi_backend/common"
	"alibi_backend/config"
	"context"
	"go.mongodb.org/mongo-driver/bson"
	"log"
	"time"

	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

// DBH Global Reference
var DBH *MongoDBHandler

// MongoDBHandler Structure
type MongoDBHandler struct {
	client *mongo.Client
	cancel context.CancelFunc

	database *mongo.Database

	attendanceCol *mongo.Collection
}

// init Function
func init() {
	DBH = NewMongoDBHandler()
}

// NewMongoDBHandler Function
func NewMongoDBHandler() *MongoDBHandler {
	var err error
	ret := MongoDBHandler{}

	// create a MongoDB client
	ret.client, err = mongo.NewClient(options.Client().ApplyURI(config.MongoDB))
	if err != nil {
		log.Printf("[MongoDB] Unable to initialize a monogoDB client (%s): %v", config.MongoDB, err)
		return nil
	}

	// set timeout (10 sec)
	var ctx context.Context
	ctx, ret.cancel = context.WithTimeout(context.Background(), 10*time.Second)

	// connect to the MongoDB server
	err = ret.client.Connect(ctx)
	if err != nil {
		log.Printf("[MongoDB] Unable to connect the mongoDB server (%s): %v", config.MongoDB, err)
		return nil
	}

	// create 'Alibi' database
	ret.database = ret.client.Database("Alibi")

	// Create APILogs and Metrics collections
	ret.attendanceCol = ret.database.Collection("Attendance")

	return &ret
}

// Disconnect Function
func (handler *MongoDBHandler) Disconnect() {
	err := handler.client.Disconnect(context.Background())
	if err != nil {
		log.Printf("[MongoDB] Unable to properly disconnect: %v", err)
	}
}

// InsertAttendance Function
func (handler *MongoDBHandler) InsertAttendance(data *common.Attendance) error {
	_, err := handler.attendanceCol.InsertOne(context.Background(), data)
	if err != nil {
		return err
	}

	return nil
}

// GetAllAttendances Function
func (handler *MongoDBHandler) GetAllAttendances() ([]common.Attendance, error) {
	var attendances []common.Attendance

	cursor, err := handler.attendanceCol.Find(context.Background(), bson.D{})
	if err != nil {
		return nil, err
	}
	defer cursor.Close(context.Background())

	for cursor.Next(context.Background()) {
		var attendance common.Attendance
		if err = cursor.Decode(&attendance); err != nil {
			return nil, err
		}
		attendances = append(attendances, attendance)
	}

	if err := cursor.Err(); err != nil {
		return nil, err
	}

	return attendances, nil
}
