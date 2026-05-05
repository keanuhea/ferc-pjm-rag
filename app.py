"""Streamlit chat interface for the FERC/PJM RAG pipeline."""

from __future__ import annotations

import streamlit as st

from src.query import ask, format_citations

st.set_page_config(page_title="FERC/PJM RAG", layout="wide")
st.title("FERC + PJM Interconnection RAG")
st.caption(
    "Ask questions across FERC Order 2023 filings and PJM cluster studies. "
    "Answers cite the source document and page."
)

if "history" not in st.session_state:
    st.session_state.history = []

for turn in st.session_state.history:
    with st.chat_message(turn["role"]):
        st.markdown(turn["content"])
        if turn.get("citations"):
            with st.expander("Sources"):
                for c in turn["citations"]:
                    loc = f"p.{c.page}" if c.page else "page ?"
                    st.markdown(
                        f"**{c.filename}** ({loc}, score={c.score:.3f})\n\n"
                        f"> {c.text}"
                    )

if prompt := st.chat_input("Ask about FERC Order 2023, cluster studies, queue mechanics..."):
    st.session_state.history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Retrieving + generating..."):
            try:
                result = ask(prompt)
            except RuntimeError as e:
                st.error(str(e))
                st.stop()
        st.markdown(result.answer)
        with st.expander("Sources"):
            for c in result.citations:
                loc = f"p.{c.page}" if c.page else "page ?"
                st.markdown(
                    f"**{c.filename}** ({loc}, score={c.score:.3f})\n\n"
                    f"> {c.text}"
                )
        st.session_state.history.append({
            "role": "assistant",
            "content": result.answer,
            "citations": result.citations,
        })
