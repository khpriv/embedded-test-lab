FROM python:3.13-slim

WORKDIR /app

COPY pyproject.toml .
COPY src/ src/
COPY tests/ tests/
COPY robot/ robot/

RUN python -m pip install --no-cache-dir ".[test]"

CMD ["sh", "-c", "python -m pytest -m 'not hardware' -v && robot -d robot_results robot/smoke.robot robot/negative.robot"]