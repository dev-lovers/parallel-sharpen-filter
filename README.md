# Parallel Sharpen Filter

Este projeto implementa um sistema de **processamento paralelo de imagens** com aplicação do filtro **Sharpen**, utilizando a linguagem Python, com foco em **threads** e **desempenho**.

## 🖼️ Funcionalidades

- Interface gráfica com `tkinter` para carregamento e exibição de imagens.
- Aplicação do filtro **Sharpen** com divisão da imagem entre múltiplas threads.
- Medição de tempo de execução.
- Suporte a imagens RGB e RGBA.

## 🚀 Execução

### 1. Criação do ambiente virtual (recomendado)

```bash
python -m venv venv
```

### 2. Ativação do ambiente virtual

- **Windows**:
```bash
venv\Scripts\activate
```
- **Linux/macOS**:
```bash
source venv/bin/activate
```

### 3. Instalação dos requisitos

```bash
pip install -r requirements.txt
```

### 4. Execução da aplicação

```bash
python sharpen_parallel.py
```

## 🧩 Requisitos

- Python 3.8 ou superior
- Pillow
- NumPy

## 📁 Estrutura do Projeto

```
parallel-sharpen-filter/
├── venv/                  # Ambiente virtual
├── .gitignore             # Arquivo para ignorar dependências e temporários
├── README.md              # Descrição do projeto
├── requirements.txt       # Dependências do projeto
└── sharpen_parallel.py    # Código-fonte principal com a interface e lógica do filtro
```

## 👨‍💻 Autoria

Desenvolvido pela equipe do filtro Sharpen, composta por:

- Caio César
- Cláudio Zicri
- Emerson Okorie
- Joshua Strauss
- Rafael Sampaio
- Milena Constantino
- Renata Vaz

Como parte do projeto da disciplina **Programação e Plataformas de Alto Desempenho** - Unijorge.


## 🔁 Ativação e Desativação do Ambiente Virtual

### ▶️ Ativar

- **Windows**:
```bash
venv\Scripts\activate
```
- **Linux/macOS**:
```bash
source venv/bin/activate
```

### ⏹️ Sair do ambiente virtual

Em qualquer sistema, com o ambiente ativado, execute:

```bash
deactivate
```
