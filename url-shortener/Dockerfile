FROM python:3.8-alpine AS compile-image


RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install -r requirements.txt
 

FROM python:3.8-alpine AS build-image

COPY --from=compile-image /opt/venv /opt/venv

COPY . .
ENV PATH="/opt/venv/bin:$PATH"

CMD ["python", "./app.py"]


