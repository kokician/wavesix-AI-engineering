def query_index(index, query_text):
    query_engine = index.as_query_engine()
    return query_engine.query(query_text)
