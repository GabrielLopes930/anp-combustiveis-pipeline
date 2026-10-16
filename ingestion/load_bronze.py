import os
from pathlib import Path
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sources import SOURCES

load_dotenv()

RAW_DIR = Path("data/raw")
TABELA = "precos_combustiveis"
SCHEMA = "bronze"

COLUNAS = {
    "Regiao - Sigla": "regiao_sigla",
    "Estado - Sigla": "estado_sigla",
    "Municipio": "municipio",
    "Revenda": "revenda",
    "CNPJ da Revenda": "cnpj_revenda",
    "Nome da Rua": "nome_rua",
    "Numero Rua": "numero_rua",
    "Complemento": "complemento",
    "Bairro": "bairro",
    "Cep": "cep",
    "Produto": "produto",
    "Data da Coleta": "data_coleta",
    "Valor de Venda": "valor_venda",
    "Valor de Compra": "valor_compra",
    "Unidade de Medida": "unidade_medida",
    "Bandeira": "bandeira",
}

usuario = os.environ["POSTGRES_USER"]
senha = os.environ["POSTGRES_PASSWORD"]
host = os.environ.get("POSTGRES_HOST", "localhost")
engine = create_engine(f"postgresql+psycopg://{usuario}:{senha}@{host}:5432/anp")

for nome in SOURCES:
    arquivo = RAW_DIR / f"{nome}.csv"

    if not arquivo.exists():
        print(f"arquivo não encontrado, rode o download antes: {arquivo}")
        continue

    df = pd.read_csv(
        arquivo,
        sep=";",
        dtype=str,
        encoding="utf-8-sig",
        keep_default_na=False,
        na_values=[""],
    )
    df = df.rename(columns=COLUNAS)
    df["arquivo_origem"] = arquivo.name

    with engine.begin() as conn:
        conn.execute(
            text(f"DELETE FROM {SCHEMA}.{TABELA} WHERE arquivo_origem = :arquivo"),
            {"arquivo": arquivo.name},
        )
        df.to_sql(
            TABELA,
            conn,
            schema=SCHEMA,
            if_exists="append",
            index=False,
            method="multi",
            chunksize=1000,
        )

    print(f"carregado: {arquivo.name} ({len(df)} linhas)")