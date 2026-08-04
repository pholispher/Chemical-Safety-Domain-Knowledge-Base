import streamlit as st

import sys
from pathlib import Path


# ==================================================
# 项目路径
# ==================================================

BASE_DIR = Path(__file__).resolve().parent.parent.parent

sys.path.append(
    str(BASE_DIR)
)



# ==================================================
# 导入模块
# ==================================================

from core.document_manager import DocumentManager



# ==================================================
# 页面配置
# ==================================================

st.set_page_config(
    page_title="知识库管理",
    page_icon="📚",
    layout="wide"
)



st.title(
    "📚 知识库管理"
)



st.markdown(
"""
管理当前知识库中的所有安全标准和法规文档。

功能：

- 查看已有文档
- 查询文档信息
- 查看文档详情
- 删除文档记录


"""
)



st.divider()



# ==================================================
# 初始化
# ==================================================

manager = DocumentManager()



documents = manager.get_all_documents()



# ==================================================
# 数据统计
# ==================================================

stats = manager.get_statistics()



col1,col2,col3 = st.columns(3)



with col1:

    st.metric(
        "文档总数",
        stats["total_documents"]
    )


with col2:

    st.metric(
        "有效文档",
        stats["active_documents"]
    )


with col3:

    st.metric(
        "Chunk数量",
        stats["total_chunks"]
    )



st.divider()



# ==================================================
# 搜索
# ==================================================

st.subheader(
    "🔍 文档查询"
)


keyword = st.text_input(
    "输入关键词",
    placeholder="例如：AQ3011 或 液氯"
)



filtered_docs=[]



for doc in documents:


    if keyword.strip()=="":


        filtered_docs.append(
            doc
        )


    else:


        text = (
            str(doc.get("title",""))
            +
            str(doc.get("code",""))
            +
            str(doc.get("document_type",""))
        )


        if keyword.lower() in text.lower():

            filtered_docs.append(
                doc
            )



st.write(
    f"找到 {len(filtered_docs)} 个文档"
)



st.divider()



# ==================================================
# 文档列表
# ==================================================

st.subheader(
    "📄 文档列表"
)



if len(filtered_docs)==0:


    st.warning(
        "没有找到文档"
    )



else:


    for doc in filtered_docs:


        title = doc.get(
            "title",
            "未知文档"
        )


        doc_id = doc.get(
            "doc_id",
            ""
        )


        with st.expander(
            f"📘 {title}"
        ):


            col1,col2 = st.columns(2)



            with col1:


                st.write(
                    "**文档ID**"
                )

                st.write(
                    doc_id
                )


                st.write(
                    "**文档类型**"
                )

                st.write(
                    doc.get(
                        "document_type",
                        ""
                    )
                )


                st.write(
                    "**编号**"
                )

                st.write(
                    doc.get(
                        "code",
                        ""
                    )
                )



            with col2:


                st.write(
                    "**来源**"
                )


                st.write(
                    doc.get(
                        "source",
                        ""
                    )
                )


                st.write(
                    "**页数**"
                )


                st.write(
                    doc.get(
                        "pages",
                        0
                    )
                )


                st.write(
                    "**Chunk数量**"
                )


                st.write(
                    doc.get(
                        "chunks",
                        0
                    )
                )



            st.write(
                "**PDF路径**"
            )


            st.code(
                doc.get(
                    "pdf_path",
                    ""
                )
            )



            st.write(
                "**上传时间**"
            )


            st.write(
                doc.get(
                    "upload_time",
                    ""
                )
            )



            st.divider()



            # 删除按钮

            if st.button(
                f"删除记录: {doc_id}",
                key=f"delete_{doc_id}"
            ):


                result = manager.delete_document(
                    doc_id
                )


                if result:


                    st.success(
                        "文档记录已删除"
                    )


                    st.rerun()



                else:


                    st.error(
                        "删除失败"
                    )



# ==================================================
# 底部提示
# ==================================================

st.divider()


st.info(
"""
注意：

当前删除功能只删除：

documents.json中的文档记录。


FAISS向量删除将在后续版本实现。


后续功能：

- 向量级删除
- 文档重新解析
- 文档重新Embedding
- 索引重建

"""
)