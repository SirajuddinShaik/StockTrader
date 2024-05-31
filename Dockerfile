FROM tensorflow/tensorflow:nightly

WORKDIR /app

COPY . /app/

RUN pip install --upgrade pip && \
pip install --ignore-installed blinker && \
pip install -r requirements.txt

CMD [ "python", "app.py" ]