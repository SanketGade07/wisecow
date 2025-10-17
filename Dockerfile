# Use Debian-based image for easier package availability
FROM debian:stable-slim

# Install required packages
RUN apt-get update && apt-get install -y \
    bash \
    curl \
    cowsay \
    fortune-mod \
    && rm -rf /var/lib/apt/lists/*

# Copy app
WORKDIR /app
COPY wisecow.sh /app/wisecow.sh
RUN chmod +x /app/wisecow.sh

# Expose the port used by wisecow
EXPOSE 4499

# Create non-root user
RUN useradd -m appuser
USER appuser

# Start the app
CMD ["/app/wisecow.sh"]
