
FROM python:latest
COPY ./run.py .
COPY ./scraper.py .
COPY requirements.txt .
RUN pip3 install -r requirements.txt --upgrade
ENTRYPOINT [ "python3" ]
CMD ["run.py"] 
