-- Tabela de categorias (ex: Eletrônicos, Alimentos, Limpeza)
CREATE TABLE categorias (
    id INT NOT NULL AUTO_INCREMENT,
    nome VARCHAR(50) NOT NULL,
    PRIMARY KEY (id)
);

-- Tabela de produtos
CREATE TABLE produtos (
    id INT NOT NULL AUTO_INCREMENT,
    nome VARCHAR(100) NOT NULL,
    descricao VARCHAR(255),
    preco DECIMAL(10,2) NOT NULL,
    quantidade_estoque INT NOT NULL DEFAULT 0,
    categoria_id INT,
    PRIMARY KEY (id),
    FOREIGN KEY (categoria_id) REFERENCES categorias(id)
);

-- Tabela de clientes
CREATE TABLE clientes (
    id INT NOT NULL AUTO_INCREMENT,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    telefone VARCHAR(20),
    PRIMARY KEY (id)
);

-- Tabela de pedidos (venda)
CREATE TABLE pedidos (
    id INT NOT NULL AUTO_INCREMENT,
    cliente_id INT NOT NULL,
    data_pedido DATETIME DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'pendente',
    PRIMARY KEY (id),
    FOREIGN KEY (cliente_id) REFERENCES clientes(id)
);

-- Tabela de itens do pedido (liga produtos com pedidos)
CREATE TABLE itens_pedido (
    id INT NOT NULL AUTO_INCREMENT,
    pedido_id INT NOT NULL,
    produto_id INT NOT NULL,
    quantidade INT NOT NULL,
    preco_unitario DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (pedido_id) REFERENCES pedidos(id),
    FOREIGN KEY (produto_id) REFERENCES produtos(id)
);