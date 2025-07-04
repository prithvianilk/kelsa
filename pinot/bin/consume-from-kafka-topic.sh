docker exec \
  -t kafka \
  /bin/bash -c "
    /opt/bitnami/kafka/bin/kafka-console-consumer.sh \
    --bootstrap-server kafka:9092 \
    --topic work-topic \
    --from-beginning
  "