FROM eclipse-temurin:21

WORKDIR /app

RUN apt-get update && apt-get install -y unzip

RUN mkdir api_gateway && cd api_gateway && \
    curl -O https://download2.interactivebrokers.com/portal/clientportal.gw.zip && \
    unzip clientportal.gw.zip && rm clientportal.gw.zip

RUN mkdir -p api_gateway/root

COPY conf.yaml api_gateway/root/conf.yaml

COPY run_gateway.sh /app/run_gateway.sh

RUN chmod +x /app/run_gateway.sh

COPY healthcheck.sh /usr/local/bin/healthcheck.sh

RUN chmod +x /usr/local/bin/healthcheck.sh

COPY tickler.sh /app/tickler.sh

RUN chmod +x /app/tickler.sh

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

EXPOSE 5055

ENTRYPOINT ["/app/run_gateway.sh", "api_gateway/root/conf.yaml"]

CMD api_gateway/bin/run.sh api_gateway/root/conf.yaml
