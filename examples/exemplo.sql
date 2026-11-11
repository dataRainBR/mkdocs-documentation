-- exemplo.sql — criação de tabela e consulta simples incorporada na
-- documentação.
CREATE TABLE medias (
    id SERIAL PRIMARY KEY,
    valor NUMERIC NOT NULL
);

SELECT AVG(valor) AS media
FROM medias;
