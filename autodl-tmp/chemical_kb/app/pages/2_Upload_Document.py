import streamlit as st

import sys
from pathlib import Path


# ==================================================
# 添加项目根目录
# ==================================================

BASE_DIR = Path(__file__).resolve().parent.parent.parent

sys.path.append(
    str(BASE_DIR)
)


# ==================================================
# 导入核心模块
# ==================================================

from core.parser import PDFParser
from core.chunker import ChunkBuilder
from core.updater import KnowledgeUpdater
from core.document_manager import DocumentManager



# ==================================================
# 页面设置
# ==================================================

st.set_page_config(
    page_title="文档上传",
    page_icon="📄",
    layout="wide"
)



st.title(
    "📄 知识文档上传"
)


st.markdown(
"""
上传新的危险化学品安全标准或法规。

处理流程：

PDF文件

↓

OCR解析

↓

文本切分

↓

Embedding生成

↓

FAISS更新

↓

文档登记


"""
)



st.divider()



# ==================================================
# 上传目录
# ==================================================

UPLOAD_DIR = (
    BASE_DIR /
    "data/pdf/upload"
)


UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True
)



# ==================================================
# 上传文件
# ==================================================

uploaded_file = st.file_uploader(
    "选择PDF文件",
    type=["pdf"]
)



if uploaded_file:


    st.success(
        f"已选择：{uploaded_file.name}"
    )



    # ==============================
    # 文档信息
    # ==============================


    st.subheader(
        "📌 文档信息"
    )


    title = st.text_input(
        "文档标题",
        value=uploaded_file.name.replace(
            ".pdf",
            ""
        )
    )



    document_type = st.selectbox(
        "文档类型",
        [
            "标准",
            "法规"
        ]
    )



    code = st.text_input(
        "编号",
        placeholder="例如 AQ3011-2007"
    )



    source = st.text_input(
        "来源",
        value="web_upload"
    )



    # ==============================
    # 开始处理
    # ==============================


    if st.button(
        "🚀 加入知识库"
    ):


        try:


            # --------------------------
            # 1 保存PDF
            # --------------------------


            pdf_path = (
                UPLOAD_DIR /
                uploaded_file.name
            )


            with open(
                pdf_path,
                "wb"
            ) as f:

                f.write(
                    uploaded_file.getbuffer()
                )



            st.info(
                "PDF保存完成"
            )



            # --------------------------
            # 生成doc_id
            # --------------------------


            doc_id = (
                Path(
                    uploaded_file.name
                )
                .stem
            )



            # --------------------------
            # 2 PDF解析
            # --------------------------


            with st.spinner(
                "正在OCR解析..."
            ):


                parser = PDFParser()


                pages = parser.parse(
                    pdf_path
                )



            st.success(
                f"OCR完成，共 {len(pages)} 页"
            )



            # --------------------------
            # 3 Chunk
            # --------------------------


            with st.spinner(
                "正在生成文本块..."
            ):


                chunk_builder = ChunkBuilder()


                chunks = chunk_builder.build(
                    pages=pages,
                    doc_id=doc_id,
                    title=title,
                    document_type=document_type,
                    code=code,
                    source=source,
                    pdf_path=pdf_path
                )



            st.success(
                f"生成 {len(chunks)} 个Chunk"
            )



            # --------------------------
            # 4 更新FAISS
            # --------------------------


            with st.spinner(
                "正在更新向量数据库..."
            ):


                updater = KnowledgeUpdater()


                updater.update(
                    chunks
                )



            st.success(
                "向量库更新完成"
            )



            # --------------------------
            # 5 登记文档
            # --------------------------


            manager = DocumentManager()



            manager.add_document(
                {
                    "doc_id":
                        doc_id,


                    "title":
                        title,


                    "document_type":
                        document_type,


                    "code":
                        code,


                    "source":
                        source,


                    "pdf_path":
                        str(pdf_path),


                    "pages":
                        len(pages),


                    "chunks":
                        len(chunks)

                }
            )



            st.success(
                "文档管理信息保存完成"
            )



            # ==========================
            # 结果展示
            # ==========================


            st.divider()


            st.subheader(
                "🎉 处理结果"
            )


            col1,col2,col3 = st.columns(3)



            with col1:

                st.metric(
                    "PDF页数",
                    len(pages)
                )


            with col2:

                st.metric(
                    "Chunk数量",
                    len(chunks)
                )


            with col3:

                st.metric(
                    "状态",
                    "成功"
                )



            st.info(
                f"""
文档ID:

{doc_id}


标题:

{title}


类型:

{document_type}

"""
            )



        except Exception as e:


            st.error(
                "处理失败"
            )


            st.exception(
                e
            )