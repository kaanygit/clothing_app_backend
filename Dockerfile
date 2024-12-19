# Uygulamanızın çalışması için uygun bir base image seçin
FROM python:3.10-slim

# Çalışma dizini oluşturun ve ayarlayın
WORKDIR /app

# Gereksinimleri yükleyin
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Uygulamanızı kopyalayın
COPY . .

# Flask uygulamanız için 8080 portunu expose edin
EXPOSE 8080

# Flask uygulamanızı başlatın
CMD ["python", "main.py"]
