import pinotdb

conn = pinotdb.connect(
    host="localhost",
    port=8099,
    path="/query/sql"
)