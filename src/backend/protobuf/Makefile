PROTO:=alibi.proto
PB_GO:=$(PROTO:.proto=.pb.go)

.PHONY: build
build: $(PB_GO) go.sum

%.pb.go: %.proto
ifeq (, $(shell which protoc))
	sudo cp bin/protoc /usr/local/bin/protoc
endif
ifeq (, $(shell which protoc-gen-go))
	go install google.golang.org/protobuf/cmd/protoc-gen-go@latest
endif
ifeq (, $(shell which protoc-gen-go-grpc))
	go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@latest
endif
	go mod tidy
	protoc -I . --go_out=. alibi.proto
	protoc -I . --go-grpc_out=. alibi.proto
	python -m grpc_tools.protoc --python_out=. --grpc_python_out=. --proto_path=. alibi.proto
go.sum: go.mod
	go get .

.PHONY: clean
clean:
	rm -f go.sum *.pb.go