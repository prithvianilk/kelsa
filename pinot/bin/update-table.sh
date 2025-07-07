docker run \
    --rm \
    --network=pinot-demo \
    -v $(pwd):/app \
    --name pinot-streaming-table-schema-update \
    apachepinot/pinot:latest AddSchema \
    -schemaFile /app/schemas/work.json \
    -controllerHost pinot-controller \
    -controllerPort 9000 \
    -override \
    -exec

curl -X POST localhost:9000/segments/work/reload
