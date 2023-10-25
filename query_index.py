# query_index.py
import configparser
import openai
from llama_index import StorageContext, load_index_from_storage

# APIキーの設定
config = configparser.ConfigParser()
config.read('settings.ini')
openai.api_key = config['openai']['api_key']

# インデックスの読み込み
storage_context = StorageContext.from_defaults(persist_dir="./storage")
index = load_index_from_storage(storage_context)
query_engine = index.as_query_engine(streaming=True)

while True:
    user_query = input("\n質問を入力してください（終了するには'quit'と入力）: ")
    if user_query.lower() == 'quit':
        break
    response = query_engine.query(user_query)
    
    # 回答を表示
    # print("回答:", response.answer if hasattr(response, 'answer') else "回答が見つかりませんでした。")
    response.print_response_stream()
    
    # ソースノードを表示
    if hasattr(response, 'source_nodes'):
        print(f"\n[ソースノード（情報源）]:ノード数：{len(response.source_nodes)}\n")
        for i, source_node in enumerate(response.source_nodes):
            print(f"[ソース{i + 1}].{source_node.node.get_metadata_str()} [スコア]:{source_node.score}\n{source_node.node.get_text()}")
