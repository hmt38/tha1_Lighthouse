FROM golang:1.20.5

WORKDIR /app
# 设置 GOPROXY 环境变量
ENV GOPROXY=https://goproxy.cn,direct
# COPY go.mod .
# COPY go.sum .
# 将当前目录下的所有文件复制到容器的/app目录下
COPY . .
RUN go mod download

CMD ["go", "run", "."]
EXPOSE 8080