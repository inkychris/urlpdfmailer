FROM python:3-alpine

WORKDIR /usr/src

COPY httptextfileserver ./httptextfileserver

ENTRYPOINT ["python", "httptextfileserver/httptextfileserver.py"]
CMD ["0.0.0.0", "1234", "log/output.log"]
