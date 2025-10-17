# Use Debian-based image
FROM debian:stable-slim

# Install required packages
RUN apt-get update && apt-get install -y \
    bash \
    curl \
    cowsay \
    fortune-mod \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Copy app
WORKDIR /app
COPY wisecow.sh /app/wisecow.sh
RUN chmod +x /app/wisecow.sh

# Create non-root user and fix permissions
RUN useradd -m appuser && chown -R appuser:appuser /app

# Add /usr/games to PATH for cowsay/fortune
ENV PATH="/usr/games:${PATH}"

# Switch user AFTER fixing PATH
USER appuser

# Expose port
EXPOSE 4499

# Start app
CMD ["/app/wisecow.sh"]
