FROM golang:1.20
WORKDIR /usr/src/app
COPY mission .
RUN go mod init mission
RUN go get github.com/gin-gonic/gin
RUN go get gorm.io/driver/mysql
RUN go get gorm.io/gorm
RUN go get github.com/gin-contrib/cors
RUN go build -o main .
CMD ["./main"]