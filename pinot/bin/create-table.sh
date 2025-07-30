docker run \
    --rm \
    --network=pinot-demo \
    -v $(pwd):/app \
    --name pinot-streaming-table-creation \
    -e JAVA_OPTS="-Xmx1G -Xms512M" \
    apachepinot/pinot:latest AddTable \
    -schemaFile /app/schemas/work.json \
    -tableConfigFile /app/tables/work.json \
    -controllerHost pinot-controller \
    -controllerPort 9000 \
    -exec
