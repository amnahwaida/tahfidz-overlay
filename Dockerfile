FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Salin semua file proyek ke dalam container
COPY . .

# Expose port yang digunakan oleh server.py
EXPOSE 8000

# Jalankan server
# Menggunakan -u untuk unbuffered output agar log terlihat di docker logs
CMD ["python", "-u", "server.py"]
