#!/bin/bash
psql -U admin -d sila -c "CREATE TABLE IF NOT EXISTS atestado (id SERIAL PRIMARY KEY, user_id INT, data TEXT);"
psql -U admin -d sila -c "CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, username TEXT UNIQUE, hashed_password TEXT);"
psql -U admin -d sila -c "CREATE TABLE IF NOT EXISTS taxa (id SERIAL PRIMARY KEY, user_id INT, valor FLOAT, tipo TEXT);"
psql -U admin -d sila -c "CREATE TABLE IF NOT EXISTS denuncia (id SERIAL PRIMARY KEY, user_id INT, descricao TEXT, localizacao TEXT);"
psql -U admin -d sila -c "CREATE TABLE IF NOT EXISTS matricula (id SERIAL PRIMARY KEY, user_id INT, escola TEXT, ano_letivo TEXT);"
psql -U admin -d sila -c "CREATE TABLE IF NOT EXISTS inscricao (id SERIAL PRIMARY KEY, user_id INT, tipo TEXT, instituicao TEXT);"
psql -U admin -d sila -c "INSERT INTO users (username, hashed_password) VALUES ('admin', '/$2b/$12/$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjP9Qxk7y6') ON CONFLICT DO NOTHING;"

