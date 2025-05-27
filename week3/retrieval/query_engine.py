def query_index(index, query_text, mode="vector"):
    if mode == "hybrid":
        chroma_collection = index.vector_store._collection 

        results = chroma_collection.query(
            query_texts=[query_text],
            n_results=5,
            include=["documents", "metadatas", "distances"],
            search_type="hybrid"  
        )

        print("\nSources:")
        for metadata in results["metadatas"][0]:
            print(f"- {metadata.get('file_path', 'unknown source')}")
        return "\n".join(results["documents"][0])

    else:
        query_engine = index.as_query_engine(response_mode="compact", return_source=True)
        response = query_engine.query(query_text)

        print("\nSources:")
        for node in response.source_nodes:
            print(f"- {node.metadata.get('file_path', 'unknown source')}")

        return response
