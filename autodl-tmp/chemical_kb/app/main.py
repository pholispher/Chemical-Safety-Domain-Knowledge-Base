import streamlit as st


st.set_page_config(
    page_title="危险化学品安全知识库",
    page_icon="⚗️",
    layout="wide"
)


st.title(
    "⚗️ 危险化学品安全知识库系统"
)


st.markdown(
"""
## 系统简介


本系统面向危险化学品安全领域，

基于：

- BGE-M3语义向量模型
- FAISS向量数据库
- BGE-Reranker重排序模型


构建专业安全知识检索系统。


---

## 当前功能


### 🔍 知识库查询

支持：

- 标准查询
- 法规查询
- 安全要求检索
- 条款依据定位


### 📄 文档管理

支持：

- PDF文档上传
- 新知识补充
- 知识库更新


### 📊 系统状态

查看：

- 文档数量
- Chunk数量
- 向量数量
- 模型状态


---

请选择左侧功能开始使用。

"""
)