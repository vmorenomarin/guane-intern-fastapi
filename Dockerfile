FROM python:3.8 
RUN pip install -r ./requirements
COPY ./app /app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]