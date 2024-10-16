import os
import boto3
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_aws import BedrockEmbeddings
from langchain_chroma import Chroma

# 指定されたディレクトリ内にあるPDFファイルのリストを返す
def get_pdf_files(directory=".", specific_files=None):
    if specific_files:
        return [f for f in specific_files if f.endswith('.pdf') and os.path.isfile(os.path.join(directory, f))]
    else:
        return [f for f in os.listdir(directory) if f.endswith('.pdf')]

# PDFファイルを処理しChromaのベクトルデータベースに格納
def process_pdfs_to_chroma(pdf_files, collection_name = "pdf_embeddings", persist_directory = "./chroma_db"):
    # Amazon Bedrock clientの設定
    bedrock_client = boto3.client(
        service_name = 'bedrock-runtime',
        region_name = 'us-west-2'  
    )

    # Bedrock Embeddingsの設定
    embeddings = BedrockEmbeddings(
        client = bedrock_client,
        model_id = "cohere.embed-multilingual-v3"
    )

    # Chromaベクトルストアの初期化（ローカルに保存）
    vectorstore = Chroma(collection_name = collection_name, embedding_function = embeddings, persist_directory = persist_directory)

    # テキスト分割の設定
    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap = 200)

    # 指定されたPDFファイルをVectorDBに登録する
    for pdf_file in pdf_files:
        print(f"{pdf_file}を作業中です...")
        
        # PDFの読み込み
        loader = PyPDFLoader(pdf_file)
        pages = loader.load()
        
        # テキストの分割
        chunks = text_splitter.split_documents(pages)
        
        # Chromaに追加
        vectorstore.add_documents(chunks)


# 処理したい特定のPDFファイル名をリストで指定（引数がない場合は、ディレクトリ内のすべてを探索する）
specific_pdf_files = ["generativeAI-guideline-solxyz.pdf"]  
    
# 指定されたPDFファイル名のリストを取得（引数がない場合は、ディレクトリ内のすべてを探索する）
pdf_files = get_pdf_files(specific_files = specific_pdf_files)
if not pdf_files:
    print("指定されたファイルが見つかりませんでした")
else:
    print(f"{len(pdf_files)}件指定されたPDFファイルが見つかりました\nファイル名: {pdf_files}")
    process_pdfs_to_chroma(pdf_files)
    print(f"VectorDBの作成が完了し、'./chroma_db'ディレクトリ配下に保存されました")
