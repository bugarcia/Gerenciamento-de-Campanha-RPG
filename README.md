# 📜 Grimório do Mestre v23

O **Grimório do Mestre** é uma ferramenta de gerenciamento de campanhas para TTRPG (RPG de Mesa) desenvolvida em Python. Projetado para oferecer agilidade ao Game Master, o software centraliza o controle de combate, a organização de NPCs, o desenvolvimento de enredo e a descrição de ambientes em uma interface unificada e intuitiva.

---

## ✨ Funcionalidades Principais

### ⚔️ Painel de Combate Ativo
* **Iniciativa e HP:** Gerencie monstros em tempo real com botões de ajuste rápido de PV (Pontos de Vida).
* **Cards Dinâmicos:** Visualize estatísticas de combate (CA, Atributos e Notas) sem sair da tela principal.
* **Ordem de Combate:** Organize a sequência de turnos movendo os cards para a esquerda ou direita.

### 🌍 Construção de Mundo (Worldbuilding)
* **Ambientes:** Registre cidades, masmorras e tavernas com descrições detalhadas.
* **Bestiário:** Cadastro completo de criaturas com suporte a todos os atributos clássicos (FOR, DES, CON, INT, SAB, CAR).
* **Gestão de NPCs:** Organize personagens não-jogáveis por vínculo (Aliado, Inimigo, Neutro).

### 📖 Narrativa e Organização
* **Fluxo de Enredo:** Estruture capítulos e cenas para manter a cronologia da história.
* **Sistema de Busca:** Localize rapidamente qualquer entrada no banco de dados.
* **Cards Expansíveis:** Função "🔍 VER" para leitura confortável de textos longos durante a sessão.

---

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3.x
* **Interface Gráfica:** Tkinter (Customizada com tema Dark)
* **Persistência de Dados:** SQLite3 (Relacional)

---

## 🚀 Como Executar o Projeto

1. **Pré-requisitos:**
   Certifique-se de ter o Python instalado em sua máquina. O `tkinter` e o `sqlite3` fazem parte da biblioteca padrão do Python.

2. **Clonagem:**
   ```bash
   git clone [https://github.com/seu-usuario/grimorio-mestre-rpg.git](https://github.com/seu-usuario/grimorio-mestre-rpg.git)
   cd grimorio-mestre-rpg
