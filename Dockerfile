FROM python:3.9

EXPOSE 8000 8001

WORKDIR /usr

COPY requirements.txt .

RUN python -m pip install -U pip && \
    pip install -r requirements.txt

COPY /heliotrope ./heliotrope

ENTRYPOINT [ "python", "-m", "heliotrope" ]