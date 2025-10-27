FROM postgres:15-alpine

# Set environment variables
ENV POSTGRES_DB=personal_finances
ENV POSTGRES_USER=finance_user
ENV POSTGRES_PASSWORD=finance_password

# Expose PostgreSQL port
EXPOSE 5432

# Copy initialization scripts (optional)
# COPY init.sql /docker-entrypoint-initdb.d/

# Default command
CMD ["postgres"]