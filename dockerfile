# 
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

# 
WORKDIR /services/apis/film_backend

# 
COPY ./requirements.txt /services/apis/film_backend/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /services/apis/film_backend/requirements.txt

# 
COPY . /services/apis/film_backend

# 
CMD ["uvicorn", "src.main:app", "--reload","--host", "0.0.0.0", "--port", "80"]