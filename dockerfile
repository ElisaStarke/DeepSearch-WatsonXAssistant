FROM python:3.9
ENV PYTHONUNBUFFERED=1

# Install Dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY ./ /

# CMD python manage.py migrate
CMD [ "uvicorn", "main:app", "--host 0.0.0.0",]