# csv_loader_chroma.py
import os
import glob
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import CSVLoader
from langchain_chroma import Chroma

load_dotenv()

def build_chroma_vector_store(data_dir: str = "SKN13-3rd-5Team/dataset",
                              persist_dir: str = "chroma_db",
                              chunk_size: int = 100):

    pattern = os.path.join(data_dir, "*.csv")
    csv_file_paths = glob.glob(pattern)

    all_csv_docs = []
    for path in csv_file_paths:
        loader = CSVLoader(
            file_path=path,
            source_column="상세페이지링크",
            metadata_columns=["종목", "명칭", "소재지", "관리자", "분류",
                              "수량/면적", "지정(등록)일", "소재지(상세)", "시대",
                              "소유자(소유단체)", "관리자(관리단체)"],
            csv_args={'delimiter': ","},
            encoding='utf-8',
            content_columns=["설명"]
        )
        docs = loader.load()
        all_csv_docs.extend(docs)

    embedding_model = OpenAIEmbeddings(model="text-embedding-3-large")

    # Chroma 생성 or 불러오기
    vector_store = Chroma(
        embedding_function=embedding_model,
        collection_name="heritage_collection",
        persist_directory=persist_dir
        )

    # 문서 삽입
    for i in range(0, len(all_csv_docs), chunk_size):
        chunk = all_csv_docs[i:i+chunk_size]
        vector_store.add_documents(chunk)
        print(f"🔹{i+1}~{min(i+chunk_size, len(all_csv_docs))} 문서 Chroma에 저장 완료")    # 14637

    # 디스크에 저장
    vector_store.persist()
    print(f"✅ 저장 완료 → {persist_dir}")


build_chroma_vector_store()