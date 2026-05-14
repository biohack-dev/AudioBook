# 📚 Professional Audiobook Generator

**Gerador profissional de audiobooks otimizado para Natural Reader 11**  
*Crie livros completos com capítulos fluidos, parágrafos curtos e formatação ideal para narração por voz.*

---

## ✨ Funcionalidades

- 🤖 **Geração automática de conteúdo** via API OpenRouter (modelo `openai/gpt-oss-120b`)
- 📖 **Criação estruturada**: tópicos, introdução e capítulos sequenciais
- 🎧 **Otimizado para audiobook**:
  - Parágrafos de 2 a 3 frases (ritmo natural de narração)
  - Remoção automática de caracteres especiais, markdown e listas
  - Pausas estratégicas para respiração do narrador
- 💾 **Armazenamento local** de progresso (tópicos e introdução são reaproveitáveis)
- 📊 **Preview final** com estatísticas e instruções para uso no Natural Reader 11
- 🔌 **Suporte a fallback** caso a API falhe (gera conteúdo básico)

---

## 🗂️ Estrutura do Projeto

| Arquivo               | Descrição                                                                 |
|-----------------------|----------------------------------------------------------------------------|
| `audiobook.py`        | Script principal                                                          |
| `livro_base.txt`      | Arquivo de configuração com **TITULO** e **ASSUNTO** do livro             |
| `topicos.txt`         | Lista dos capítulos gerados (pode ser reutilizada)                        |
| `tema.txt`            | Introdução do livro (pode ser reutilizada)                                |
| `livro.txt`           | Audiobook final pronto para o Natural Reader 11                           |

---

## 🚀 Como Usar

### 1. Pré‑requisitos

- Python 3.8+
- Uma chave de API da [OpenRouter](https://openrouter.ai/)
- Instalar as dependências (se necessário):
  ```bash
  pip install requests
