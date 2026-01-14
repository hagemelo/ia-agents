# Every Money - Sistema de Controle Financeiro Pessoal

Sistema de controle financeiro pessoal desenvolvido com NestJS no backend e React no frontend.

## 🏗️ Modelo de Domínio

### 🔹 Usuário (Usuario)

**Atributos:**
- `id: number` - Identificador único
- `nome: string` - Nome do usuário
- `email: string` - E-mail do usuário
- `senha: string` - Senha criptografada
- `createdAt: Date` - Data de criação
- `updatedAt: Date` - Data da última atualização
- `contas: Conta[]` - Lista de contas do usuário
- `categorias: Categoria[]` - Lista de categorias do usuário

**Métodos:**
- `calcularSaldos(): void` - Atualiza os saldos de todas as contas
- `alterarSenha(senha: string): void` - Altera a senha do usuário
- `toModel(): UsuarioModel` - Converte para o modelo de dados

### 🔹 Conta

**Atributos:**
- `id: number` - Identificador único
- `nome: string` - Nome da conta (ex.: Conta Corrente, Poupança)
- `saldoRealizado: number` - Saldo atualizado
- `saldoPrevisto: number` - Saldo previsto baseado em orçamentos
- `tipoConta: TipoContaModel` - Tipo da conta (Corrente, Poupança, etc.)
- `usuario: Usuario` - Usuário dono da conta
- `orcamentos: Orcamento[]` - Orçamentos associados
- `transacoes: Transacao[]` - Transações realizadas

**Métodos:**
- `calcularSaldoRealizado(): void` - Calcula o saldo realizado
- `calcularSaldoPrevisto(): void` - Calcula o saldo previsto
- `addUsuario(usuario: Usuario): Usuario` - Associa um usuário à conta
- `toModel(): ContaModel` - Converte para o modelo de dados

### 🔹 Categoria

**Atributos:**
- `id: number` - Identificador único
- `nome: string` - Nome da categoria
- `tipo: TipoTransacaoModel` - Tipo (Entrada ou Saída)
- `usuario: Usuario` - Usuário dono da categoria
- `transacoes: Transacao[]` - Transações associadas
- `orcamentos: Orcamento[]` - Orçamentos associados

### 🔹 Transação

**Atributos:**
- `id: number` - Identificador único
- `descricao: string` - Descrição da transação
- `valor: number` - Valor da transação
- `tipo: TipoTransacaoModel` - Tipo (Entrada ou Saída)
- `data: Date` - Data da transação
- `conta: Conta` - Conta associada
- `categoria: Categoria` - Categoria da transação

### 🔹 Orçamento

**Atributos:**
- `id: number` - Identificador único
- `limite: number` - Limite orçamentário
- `mesReferencia: string` - Mês de referência (formato MM/YYYY)
- `conta: Conta` - Conta associada
- `categoria: Categoria` - Categoria do orçamento

## 🔗 Relacionamentos

- Um **Usuário** pode ter várias **Contas**, **Categorias**, **Transações** e **Orçamentos**
- Uma **Conta** pertence a um **Usuário** e pode ter várias **Transações** e **Orçamentos**
- Uma **Categoria** pertence a um **Usuário** e pode ter várias **Transações** e **Orçamentos**
- Uma **Transação** pertence a uma **Conta** e uma **Categoria**
- Um **Orçamento** pertence a uma **Conta** e uma **Categoria**

## 🛠️ Tecnologias Utilizadas

- **Backend**: NestJS, TypeScript, TypeORM
- **Frontend**: React, TypeScript
- **Banco de Dados**: PostgreSQL
- **Autenticação**: JWT

## 🚀 Como Executar

### Backend

```bash
cd every-money-backend
npm install
npm run start:dev
```

### Frontend

```bash
cd every-money-frontend
npm install
npm start
```

## 📄 Licença

Este projeto está licenciado sob a licença MIT.
