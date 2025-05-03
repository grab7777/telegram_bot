FROM python:3.13-alpine AS compiler
ENV PYTHONUNBUFFERED=1

WORKDIR /app/

RUN python -m venv /opt/venv
# Enable venv
ENV PATH="/opt/venv/bin:$PATH"

COPY ./requirements.txt /app/requirements.txt
RUN pip install -Ur requirements.txt

FROM python:3.13-alpine AS runner
WORKDIR /app/
COPY --from=compiler /opt/venv /opt/venv

# Enable venv
ENV PATH="/opt/venv/bin:$PATH"
ENV TELEGRAM_BOT_API_KEY=key
ENV OPENAI_API_KEY=key
COPY . /app/
CMD ["python", "-u", "main.py"]
