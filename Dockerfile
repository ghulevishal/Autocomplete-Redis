FROM python:alpine
COPY . /usr/src/app
WORKDIR /usr/src/app
ENV FLASK_APP /usr/src/app/autocomplete.py
RUN pip3 install -r requirements.txt
CMD python autocomplete.py
