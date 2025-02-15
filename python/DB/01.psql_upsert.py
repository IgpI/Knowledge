from sqlalchemy import create_engine
import psycopg2
import json

# データベース接続情報
db_params = {
    "host": "localhost",
    "database": "[DB名]",
    "user": "[ユーザー名]",
    "password": "[パスワード]"
}
# データベース情報
table_name = "[テーブル名]"
column_name1 = "[カラム名]"
column_name2 = "[カラム名(作成日時)]"
column_name3 = "[カラム名(更新日時)]"
# JSONファイルパス
json_file_path = "[JSONファイル名]"

#既存データがいないならINSERT,キー重複ならUPDATE
def connect_to_db(db_params):
    """PostgreSQLデータベースに接続する
    Args:
        db_params (dict): データベース接続情報を格納した辞書
    Returns:
        connection: psycopg2.connectionオブジェクト
    """
    try:
        connection = psycopg2.connect(**db_params)
        return connection
    except psycopg2.Error as e:
        print(f"データベース接続エラー: {e}")
        return None

def insert_json_to_db(connection, json_file_path, table_name, column_name):
    """JSONファイルの内容をデータベースに挿入する

    Args:
        connection: psycopg2.connectionオブジェクト
        json_file_path (str): JSONファイルのパス
        table_name (str): 挿入先のテーブル名
        column_name (str): 挿入先のカラム名
    """
    try:
        with open(json_file_path, 'r',encoding='utf8') as f:
            json_data = json.load(f)

        # JSONデータを文字列に変換
        json_string = json.dumps(json_data)

        cursor = connection.cursor()
        #件数確認
        query = f"SELECT COUNT(*) FROM {table_name} WHERE  {column_name1} = %s;"
        cursor.execute(query, (json_string,))
        if cursor.fetchone()[0]==0:
            #追加
            query = f"INSERT INTO {table_name} ({column_name1}) VALUES (%s);"
            cursor.execute(query, (json_string,))
            query = f"UPDATE {table_name} SET {column_name2} = now(),{column_name3} = now() WHERE  {column_name1} = %s;"
            cursor.execute(query, (json_string,))
        else:
            #更新
            query = f"UPDATE {table_name} SET {column_name3} = now() WHERE  {column_name1} = %s;"
            cursor.execute(query, (json_string,))
        connection.commit()
        print("JSONデータがデータベースに挿入されました。")

    except (FileNotFoundError, json.JSONDecodeError, psycopg2.Error) as e:
        print(f"エラー: {e}")
        connection.rollback()
        
        
        
        
if __name__ == "__main__":
    connection = connect_to_db(db_params)
    if connection:
        insert_json_to_db(connection, json_file_path, table_name, column_name)
        connection.close()
