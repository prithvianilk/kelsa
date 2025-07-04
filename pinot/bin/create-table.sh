docker run \
    --rm \
    --network=pinot-demo \
    -v $(pwd):/app \
    --name pinot-streaming-table-creation \
    apachepinot/pinot:latest AddTable \
    -schemaFile /app/schemas/work.json \
    -tableConfigFile /app/tables/work.json \
    -controllerHost pinot-controller \
    -controllerPort 9000 \
    -exec