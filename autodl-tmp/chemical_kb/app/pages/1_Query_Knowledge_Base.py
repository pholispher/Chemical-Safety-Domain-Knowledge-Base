import streamlit as st

import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent.parent

sys.path.append(
    str(BASE_DIR)
)


from core.retriever import Retriever



st.title(
    "🔍 知识库查询"
)



@st.cache_resource
def load_kb():

    return Retriever()



with st.spinner(
    "正在加载知识库模型..."
):

    kb = load_kb()



question = st.text_input(
    "请输入安全问题",
    placeholder="例如：液氯泄漏事故应该如何处理？"
)



if st.button(
    "开始查询"
):

    if question.strip()=="":


        st.warning(
            "请输入问题"
        )


    else:


        with st.spinner(
            "正在检索相关知识..."
        ):


            results = kb.query(
                question
            )


        st.success(
            "检索完成"
        )


        st.divider()


        st.subheader(
            "相关知识依据"
        )


        for i,item in enumerate(
            results,
            1
        ):


            metadata=item["metadata"]


            with st.expander(
                f"依据 {i}: {metadata.get('title','')}"
            ):


                st.write(
                    "📘 **文档名称**"
                )

                st.write(
                    metadata.get(
                        "title",
                        ""
                    )
                )


                st.write(
                    "📌 **标准编号**"
                )

                st.write(
                    metadata.get(
                        "code",
                        ""
                    )
                )


                st.write(
                    "📂 **文档类型**"
                )

                st.write(
                    metadata.get(
                        "document_type",
                        ""
                    )
                )


                st.write(
                    "⭐ **相关评分**"
                )

                st.write(
                    round(
                        item.get(
                            "rerank_score",
                            0
                        ),
                        4
                    )
                )


                st.divider()


                st.write(
                    "📄 **原文内容**"
                )


                st.text(
                    metadata.get(
                        "text",
                        ""
                    )[:2000]
                )