
# EPX Entregas - Sistema de Rastreamento de Entregas

Sistema web para gerenciamento e rastreamento de entregas em tempo real.

## 🚚 Funcionalidades

- **Painel de Rastreamento**
  - Consulta de entregas por código de rastreio
  - Visualização do histórico de status
  - Interface amigável para clientes

- **Painel Administrativo**
  - Login seguro para administradores
  - Geração automática de códigos de rastreio
  - Gerenciamento completo de entregas
  - Atualização de status em tempo real
  - Exclusão de registros

## 🛠️ Tecnologias

- Python 3.11+
- FastAPI
- Jinja2 Templates
- JSON para armazenamento
- HTML/CSS/JavaScript
- Font Awesome Icons

## 📦 Instalação

1. Clone o repositório
2. Instale as dependências:
```bash
pip install fastapi jinja2 uvicorn
```

## 🚀 Como Executar

Execute o servidor com:
```bash
python main.py
```

Acesse:
- 🌐 Interface de Rastreamento: `http://localhost:5000`
- ⚙️ Painel Administrativo: `http://localhost:5000/admin`

## 📋 Fluxo de Status

1. Pacote recebido pela transportadora
2. Pacote está a caminho
3. Pacote chegou na cidade destinada
4. Pacote em rota de entrega
5. Pacote entregue

## 👥 Credenciais Admin (Demo)

- Usuário: admin
- Senha: 123456

## 📁 Estrutura do Projeto

```
├── templates/
│   ├── admin.html    # Painel administrativo
│   └── index.html    # Página de rastreamento
├── main.py          # Servidor FastAPI
└── deliveries.json  # Banco de dados JSON
```
# Rastreio-de-Encomenda
