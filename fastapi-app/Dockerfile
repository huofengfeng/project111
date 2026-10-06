FROM python:3.11-slim

WORKDIR /app

# 安装系统依赖（cryptography 需要）
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件并安装
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目代码
COPY . .

# 创建必要的目录
RUN mkdir -p static files

# 暴露端口
EXPOSE 9090

# 启动命令
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9090"]
