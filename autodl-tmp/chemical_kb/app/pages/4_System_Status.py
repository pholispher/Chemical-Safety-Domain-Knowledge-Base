import streamlit as st

import json
import faiss



BASE="/root/autodl-tmp/chemical_kb"



st.title(
    "📊 知识库系统状态"
)



index = faiss.read_index(
    BASE+
    "/data/vector_store/faiss.index"
)



with open(
    BASE+
    "/data/vector_store/index_metadata.json",
    "r",
    encoding="utf-8"
) as f:

    metadata=json.load(f)



col1,col2,col3=st.columns(3)



with col1:

    st.metric(
        "向量数量",
        index.ntotal
    )


with col2:

    st.metric(
        "Chunk数量",
        len(metadata)
    )


with col3:

    st.metric(
        "向量维度",
        index.d
    )



st.divider()



st.success(
    "知识库运行正常"
)



st.info(
"""
Embedding模型:

BGE-M3


Reranker模型:

BGE-Reranker-v2-m3


向量数据库:

FAISS

"""
)