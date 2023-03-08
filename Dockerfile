FROM python:3.10

ADD ./EF_NFCS/package /code

WORKDIR /code

RUN pip install -i http://pypi.doubanio.com/simple/ --trusted-host pypi.doubanio.com --upgrade -r requirements.txt

CMD ["flask", "run","--host=0.0.0.0"]