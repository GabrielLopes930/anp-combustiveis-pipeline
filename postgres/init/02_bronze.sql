CREATE TABLE IF NOT EXISTS bronze.precos_combustiveis (
    regiao_sigla    TEXT,
    estado_sigla    TEXT,
    municipio       TEXT,
    revenda         TEXT,
    cnpj_revenda    TEXT,
    nome_rua        TEXT,
    numero_rua      TEXT,
    complemento     TEXT,
    bairro          TEXT,
    cep             TEXT,
    produto         TEXT,
    data_coleta     TEXT,
    valor_venda     TEXT,
    valor_compra    TEXT,
    unidade_medida  TEXT,
    bandeira        TEXT,
    arquivo_origem  TEXT NOT NULL,
    carregado_em    TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_bronze_arquivo_origem
    ON bronze.precos_combustiveis (arquivo_origem);