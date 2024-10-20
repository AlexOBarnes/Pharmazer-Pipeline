'''Loads static alias data to mysql database'''
from os import environ as ENV
from dotenv import load_dotenv
from pymysql import connect
import pandas as pd


def get_connection():
    '''Returns a connection to a given mysql database'''
    return connect(host=ENV['DB_HOST'],
                   user=ENV['DB_USER'],
                   password=ENV['DB_PW'],
                   database=ENV['DB_NAME'],
                   port=int(ENV['DB_PORT']))

def get_alias_data() -> list:
    '''Uses pandas to read in the alias data and return a list of the values'''
    alias_df = pd.read_csv('../pipeline/aliases.csv')
    return alias_df.values.tolist()

def insert_alias_data(aliases: list[list]) -> None:
    '''Inserts a list of aliases into a given database'''
    q ='''INSERT INTO pubmed_db.affiliation (grid_id,affiliate_name)
    VALUES (%s, %s)
    ON DUPLICATE KEY UPDATE grid_id = grid_id'''
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.executemany(q, aliases)
            conn.commit()
            print(f"Inserted {cur.rowcount} rows.")

def get_keywords() -> list:
    keyword_df = pd.read_csv('../pipeline/cleaned_sjogren_data.csv')['keywords'].dropna()
    keyword_list = [keywords.replace('"','').replace('[','').replace(']','').replace('\\','').replace("'",'').lower() 
                    for keywords in [word for word in keyword_df.values.tolist()]]
    clean_keywords = []
    for word in keyword_list:
        clean_keywords.extend(word.split(','))
    return clean_keywords

def insert_keywords(words: list[str]) -> None:
    q = '''INSERT INTO pubmed_db.keywords (keyword)
    VALUES (%s)
    ON DUPLICATE KEY UPDATE keyword = keyword'''
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.executemany(q, words)
            conn.commit()
            print(f"Inserted {cur.rowcount} rows.")

def get_mesh()-> list:
    mesh_df = pd.read_csv('../pipeline/cleaned_sjogren_data.csv')['mesh'].dropna()
    mesh_list = [mesh.replace('"', '').replace('[', '').replace(']', '').replace('\\', '').replace("'", '').strip()
                    for mesh in [meshes for meshes in mesh_df.values.tolist()]]
    clean_mesh = []
    for word in mesh_list:
        clean_mesh.extend(word.split(','))
    return clean_mesh

def insert_mesh(words:list[str]) -> None:
    q = '''INSERT INTO pubmed_db.mesh (mesh_word)
    VALUES (%s)
    ON DUPLICATE KEY UPDATE mesh_word = mesh_word'''
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.executemany(q, words)
            conn.commit()
            print(f"Inserted {cur.rowcount} rows.")

def main() -> None:
    '''Calls the other functions in sequence'''
    load_dotenv()
    df = get_alias_data()
    insert_alias_data(df)
    keywords = get_keywords()
    insert_keywords(list(set(keywords)))
    mesh = get_mesh()
    insert_mesh(list(set(mesh)))


if __name__ == '__main__':
    main()