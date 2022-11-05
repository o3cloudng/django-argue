# start from an official image
FROM python:3.10.6-alpine


# USER devops
# arbitrary location choice: you can change the directory
RUN mkdir -p /opt/services/djangoapp/src

WORKDIR /opt/services/djangoapp/src

# install our dependencies
# we use --system flag because we don't need an extra virtualenv
COPY Pipfile Pipfile.lock /opt/services/djangoapp/src/

RUN pip install --upgrade pip 

RUN pip install pipenv && pipenv install --system

# copy our project code
COPY . /opt/services/djangoapp/src

# RUN pipenv shell
RUN python manage.py migrate --no-input && python manage.py collectstatic --no-input -v 2

# expose the port 8000
EXPOSE 80

RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser ./
USER appuser

# define the default command to run when starting the container
CMD ["gunicorn", "--chdir", "core", "--bind", ":80", "core.wsgi:application", "--reload"]
