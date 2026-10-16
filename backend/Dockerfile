FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN useradd --create-home --uid 10001 appuser

COPY requirements.txt .
# pip is removed after installing: it isn't needed at runtime and its vendored
# libraries (urllib3, msgpack, setuptools) carry HIGH CVEs flagged by Trivy.
RUN pip install --no-cache-dir -r requirements.txt \
 && pip uninstall -y pip

COPY . .

USER 10001
EXPOSE 8000

CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]