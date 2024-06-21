FROM ubuntu
RUN apt-get update && apt-get install python3 cmake build-essential -y

RUN mkdir app
WORKDIR /app
COPY ./ /app

RUN chmod +x install.sh
RUN ./install.sh

CMD ["./run.sh"]