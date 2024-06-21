FROM golang:1.21-alpine3.17 as builder

RUN mkdir app
WORKDIR /app
COPY ./* /app

RUN go mod tidy
RUN go build

FROM alpine:3.17 as alibi_backend
COPY --from=builder /app/cloud-side /
CMD ["/alibi_backend"]