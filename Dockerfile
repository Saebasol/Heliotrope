# first stage
FROM python:3.9 AS builder
COPY ./requirements/deps.txt .

# install dependencies to the local user directory (eg. /root/.local)
RUN pip install --user -r deps.txt

# second unnamed stage
FROM python:3.9-slim
WORKDIR /code

# copy only the dependencies installation from the 1st stage image
COPY --from=builder /root/.local /root/.local
COPY ./heliotrope ./heliotrope

# update PATH environment variable
ENV PATH=/root/.local:$PATH

EXPOSE 8000 8001

ENTRYPOINT [ "python", "-m", "heliotrope" ]


