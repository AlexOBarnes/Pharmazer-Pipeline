FROM python:latest

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN python -m spacy download en_core_web_md

COPY aliases.csv .
COPY message.py .
COPY pipeline.py .
COPY extract.py .
COPY transform.py .
COPY load.py .

CMD ["python","pipeline.py"]