# build_index.py
import configparser
import openai
from llama_index import VectorStoreIndex, SimpleDirectoryReader

# APIキーの設定
config = configparser.ConfigParser()
config.read('settings.ini')
openai.api_key = config['openai']['api_key']

# インデックスの作成
documents = SimpleDirectoryReader('data').load_data()
index = VectorStoreIndex.from_documents(documents)
index.storage_context.persist()
