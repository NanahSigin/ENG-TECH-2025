-- Verificando se há outros bancos de dados
SHOW DATABASES;
-- excluindo banco de dados
DROP database eu_indico;

-- Criando um novo banco de dados
CREATE DATABASE eu_indico;

-- Selecionando o banco de dados que será usado
USE eu_indico;

-- Tabela de usuários
CREATE TABLE usuario (
    user_id INT AUTO_INCREMENT PRIMARY KEY,       -- Chave primária da tabela
    user_nome VARCHAR(150) NOT NULL,              -- Nome do usuário
    user_email VARCHAR(150) NOT NULL,             -- E-mail do usuário
    user_senha VARCHAR(150) NOT NULL             -- Senha do usuário
);

-- Tabela de gêneros
CREATE TABLE genero (
    gen_id INT AUTO_INCREMENT PRIMARY KEY,        -- Chave primária
    gen_nome VARCHAR(150) NOT NULL                -- Nome do gênero
);

-- Tabela de filmes
CREATE TABLE filmes (
    fil_id INT AUTO_INCREMENT PRIMARY KEY,        -- Chave primária
    genero_filme_id INT,                          -- Gênero do filme (genero_filme_id apenas para saber o nome da tabela filme )
    fil_nome VARCHAR(150) NOT NULL,               -- Nome do filme
    fil_diretor VARCHAR(150),                     -- Diretor do filme
    fil_duracao INT,                              -- Duração do filme em minutos
    fil_dtlancamento DATE,                        -- Data de lançamento
    FOREIGN KEY (genero_filme_id) REFERENCES genero(gen_id) -- Chave estrangeira para gênero
);

-- Tabela de livros
CREATE TABLE livros (
    liv_id INT AUTO_INCREMENT PRIMARY KEY,        -- Chave primária
    genero_livro_id INT,                          -- Gênero do livro
    liv_nome VARCHAR(150) NOT NULL,               -- Nome do livro
    liv_escritor VARCHAR(150),                    -- Autor do livro
    liv_paginas INT,                              -- Número de páginas
    liv_dtlancamento DATE,                        -- Data de lançamento
    FOREIGN KEY (genero_livro_id) REFERENCES genero(gen_id) -- Chave estrangeira para gênero
);

-- Tabela de avaliações
CREATE TABLE avaliacao (
    aval_id INT AUTO_INCREMENT PRIMARY KEY,       -- Chave primária
    usuario_id INT,                               -- Usuário que avaliou
    filme_id INT,                                 -- Filme avaliado (pode ser NULL se for livro)
    livro_id INT,                                 -- Livro avaliado (pode ser NULL se for filme)
    aval_nota INT NOT NULL,                       -- Nota da avaliação
    aval_texto TEXT,                    		  -- Texto/opinião
    aval_data TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, -- Data da avaliação
    FOREIGN KEY (usuario_id) REFERENCES usuario(user_id),   -- FK para usuário
    FOREIGN KEY (filme_id) REFERENCES filmes(fil_id),       -- FK para filme
    FOREIGN KEY (livro_id) REFERENCES livros(liv_id)        -- FK para livro
);