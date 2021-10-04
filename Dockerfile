FROM python:3.8-slim-buster

RUN pip3 install fastapi
RUN pip3 install uvicorn
RUN pip3 install requests
RUN pip3 install python-multipart
RUN pip3 install pyjwt

COPY fast-api .

EXPOSE 8000

CMD ["python3", "main.py"]