# 1. Use slim base image for small size
FROM python:3.11-slim

# 2. Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 3. Create and switch to a non-root user
RUN addgroup --system appgroup && \
    adduser --system --ingroup appgroup appuser

# 4. Set working directory
WORKDIR /app

# 5. Copy ONLY requirements first (leverage Docker cache)
COPY requirements.txt .

# 6. Install dependencies (no cache, as root temporarily)
RUN pip install --no-cache-dir -r requirements.txt

# 7. Copy the rest of the application code
COPY app/ .

# 8. Change ownership of /app to the non-root user
RUN chown -R appuser:appgroup /app

# 9. Switch to non-root user
USER appuser

# 10. Define the default command
CMD ["python", "main.py"]
