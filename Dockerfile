FROM data_science:9949

WORKDIR /app

COPY . /app/

RUN pip install -r requirements.txt

CMD [ "python", "app.py" ]