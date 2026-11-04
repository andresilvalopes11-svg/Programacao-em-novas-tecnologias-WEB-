DROP TABLE IF EXISTS produto;
DROP TABLE IF EXISTS categoria;
DROP TABLE IF EXISTS usuario;

CREATE TABLE categoria(
    id integer primary key autoincrement,
    nome varchar(50) not null,
    descricao text,
    ativo boolean,
    imagem blob,
    img varchar(100)
);

CREATE TABLE produto(
    id integer primary key autoincrement,
    nome varchar(50) not null,
    preco float,
    ativo boolean,
    imagem blob,
    img varchar(100),
    id_categoria integer,
    foreign key ('id_categoria') references categoria(id)
);

CREATE TABLE usuario(
    id integer primary key autoincrement,
    nome varchar(50) not null,
    senha varchar(50) not null,
    ativo boolean


);


insert into categoria(nome, descricao, ativo) 
values ('vodka', 'orlof', True),
       ('Coca Cola','Lata', True);