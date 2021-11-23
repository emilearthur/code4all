FROM golang:alpine

LABEL maintainer="Emile Bondzie-Arthur"

WORKDIR /go/src/app

ADD . .

RUN go mod init

RUN go build -o helloworld

EXPOSE 6111

CMD ["./helloworld"]