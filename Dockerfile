FROM python:3.11.7-slim
COPY . /app
WORKDIR /app
RUN python3 -m venv /opt/venv
RUN /opt/venv/bin/pip install pip --upgrade && \
    /opt/venv/bin/pip install -r requirements_prod.txt && \
    chmod +x entrypoint.sh
CMD ["/app/entrypoint.sh"]