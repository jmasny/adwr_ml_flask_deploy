FROM python:3.9.0

WORKDIR /app

COPY app.py .
COPY create_and_train_model.py .
COPY requirements.txt .
COPY /data/diamonds_cleaned.csv data/
COPY /templates/home.html templates/

RUN pip install -r requirements.txt
RUN python3 create_and_train_model.py

EXPOSE 5010

ENTRYPOINT ["python3"]
CMD ["app.py"]
