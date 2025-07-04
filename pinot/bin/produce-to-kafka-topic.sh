for i in {1..1000}; do
  docker exec \
    -t kafka \
    /bin/bash -c "
      /opt/bitnami/kafka/bin/kafka-console-producer.sh \
      --bootstrap-server kafka:9092 \
      --topic work-topic < /app/rawData/work.json
    "
  echo "Started iteration $i"
done

echo "All iterations complete"