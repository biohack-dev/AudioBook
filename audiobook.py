"""
===============================================================================
 File...........: book.py
 Title..........: GERADOR PROFISSIONAL DE AUDIOBOOKS - VERSÃO OTIMIZADA
 Program........: Shell Template Code - GNU/Linux

 Description....: Gera livro formatado para audiobook (Natural Reader 11)

 Copyright......: Copyright(c) 2026 / @B10H4Ck - HackLab
 License........: GNU GENERAL PUBLIC LICENSE - Version 3, 29 June 2007

 Author.........: B10H4Ck
 E-Mail.........: b10h4ck.br@proton.me

 Dependency.....: OpenRouter

 Date...........: 09/05/2026
 Version........: 0.2.0

===============================================================================
"""

import json, requests, os, re, time, sys
from datetime import datetime

API_KEY = "_SUA_KEY_AKI_"
API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "openai/gpt-oss-120b"

ARQUIVOS = {"base": "livro_base.txt", "topicos": "topicos.txt", "tema": "tema.txt", "livro": "livro.txt"}

def p(texto=""):
    print(texto)

def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")

def limpar_texto(texto):
    if not texto:
        return ""
    texto = re.sub(r'[#*_~`]', '', texto)
    texto = re.sub(r'\s+', ' ', texto)
    return texto.strip()

def req_api(mensagens, max_tokens=2000, temp=0.7):
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    payload = {"model": MODEL, "messages": mensagens, "temperature": temp, "max_tokens": max_tokens}
    try:
        resp = requests.post(API_URL, headers=headers, json=payload, timeout=90)
        return resp.json()["choices"][0]["message"]["content"] if resp.status_code == 200 else ""
    except:
        return ""

def ler_base():
    if not os.path.exists(ARQUIVOS["base"]):
        with open(ARQUIVOS["base"], "w", encoding="utf-8") as f:
            f.write("""TITULO: Celular Sobrevivencialista
ASSUNTO: Guia definitivo de apps e recursos para sobrevivência urbana e campo de batalha.""")
        p(f"Criado {ARQUIVOS['base']} como exemplo. Edite e execute novamente.")
        return None, None
    with open(ARQUIVOS["base"], "r", encoding="utf-8") as f:
        conteudo = f.read()
    titulo = re.search(r'TITULO:?\s*(.+?)(?:\n|$)', conteudo, re.I)
    assunto = re.search(r'ASSUNTO:?\s*(.+?)$', conteudo, re.I | re.DOTALL)
    return (titulo.group(1).strip() if titulo else None), (assunto.group(1).strip() if assunto else None)

def testar_conexao():
    if not API_KEY.startswith("sk-or-"):
        return False
    headers = {"Authorization": "Bearer " + API_KEY, "Content-Type": "application/json"}
    try:
        resp = requests.post(API_URL, headers=headers, json={"model": MODEL, "messages": [{"role": "user", "content": "Teste"}], "max_tokens": 5}, timeout=10)
        return resp.status_code == 200
    except:
        return False

def gerar_topicos(titulo, assunto):
    p(f"Gerando 30-40 capítulos para: {titulo}")
    prompt = f"""Crie 30-40 capítulos para o livro "{titulo}" sobre: {assunto}

REGRAS:
- Apenas número e título: "1. Título do Capítulo"
- Sem subcapítulos (1.1, 1a, etc.)
- Sem caracteres especiais
- Títulos com 5-15 palavras
- Português brasileiro

Liste APENAS os capítulos:"""
    
    resposta = req_api([
        {"role": "system", "content": "Você é um planejador editorial. Gere apenas capítulos numerados sequencialmente."},
        {"role": "user", "content": prompt}
    ], 2500, 0.8)
    
    topicos = []
    for linha in resposta.split('\n'):
        linha = limpar_texto(linha)
        if re.match(r'^\d+\.\s+', linha):
            topico = re.sub(r'^\d+\.\s+', '', linha)
            if topico and len(topico) > 3:
                topicos.append(topico)
    
    if len(topicos) < 30:
        padroes = ["Fundamentos do Tema", "Conceitos Básicos", "História e Evolução", "Princípios Teóricos",
                   "Metodologias Práticas", "Ferramentas e Recursos", "Aplicações no Mundo Real", "Estudos de Caso",
                   "Desafios e Soluções", "Melhores Práticas", "Tendências e Inovações", "Aspectos Éticos",
                   "Desenvolvimento de Habilidades", "Planejamento Estratégico", "Implementação Efetiva",
                   "Avaliação de Resultados", "Otimização Contínua", "Sustentabilidade", "Perspectivas Futuras",
                   "Considerações Finais"]
        for padrao in padroes:
            if len(topicos) < 40:
                topicos.append(padrao)
    
    with open(ARQUIVOS["topicos"], "w", encoding="utf-8") as f:
        for i, t in enumerate(topicos, 1):
            f.write(f"{i}. {limpar_texto(t)}\n")
    return topicos

def gerar_tema(titulo, assunto, topicos):
    p("Gerando introdução do livro...")
    prompt = f"""TÍTULO: {titulo}
ASSUNTO: {assunto}

Crie uma INTRODUÇÃO para o livro com:
- Parágrafos curtos de 2 a 3 frases
- Texto fluido para leitura em voz alta
- Tom profissional e envolvente
- Sem marcadores, listas ou caracteres especiais

Escreva APENAS a introdução em parágrafos separados por linha em branco:"""
    
    tema = req_api([
        {"role": "system", "content": "Você é um escritor profissional. Escreva apenas texto corrido em parágrafos curtos para narração."},
        {"role": "user", "content": prompt}
    ], 2500, 0.7)
    
    if not tema or len(tema) < 100:
        tema = f"""Bem-vindo ao {titulo}.

Este guia foi criado para ajudá-lo a transformar seu celular em uma ferramenta essencial de sobrevivência.

{assunto}

Ao longo deste livro, você aprenderá a selecionar os melhores aplicativos e recursos para situações de emergência.

Prepare-se para descobrir como seu smartphone pode ser seu maior aliado em momentos críticos."""
    
    with open(ARQUIVOS["tema"], "w", encoding="utf-8") as f:
        f.write(tema)
    return tema

def quebrar_paragrafos_audio(texto):
    """Formata texto em parágrafos curtos para audiobook"""
    if not texto:
        return ""
    
    texto = limpar_texto(texto)
    
    texto = re.sub(r'\*\*.*?\*\*', '', texto)
    texto = re.sub(r'[•·]', '', texto)
    
    frases = re.split(r'(?<=[.!?])\s+', texto)
    
    paragrafos = []
    buffer = []
    frases_por_paragrafo = 3
    
    for i, frase in enumerate(frases):
        frase = frase.strip()
        if frase:
            buffer.append(frase)
            if len(buffer) >= frases_por_paragrafo or i == len(frases)-1:
                paragrafos.append(' '.join(buffer))
                buffer = []
    
    return '\n\n'.join(paragrafos)

def gerar_capitulo_audio(titulo, num, total, tema, introducao):
    """Gera capítulo otimizado para audiobook"""
    p(f"Capítulo {num}/{total}: {titulo[:50]}...")
    
    prompt = f"""INTRODUÇÃO DO LIVRO:
{introducao[:500]}

CAPÍTULO {num}: {titulo}

Escreva este capítulo para AUDIOBOOK seguindo estas regras:

1. Português brasileiro natural e fluido
2. Parágrafos com APENAS 2 a 3 frases cada
3. Comece diretamente com o conteúdo
4. Use frases curtas e diretas
5. NÃO use listas, marcadores, negritos ou itálico
6. NÃO use asteriscos, hashtags ou caracteres especiais
7. Separe cada parágrafo por uma linha em branco
8. Evite palavras de transição como "neste capítulo"
9. Mantenha ritmo agradável para narração

Escreva o capítulo:"""
    
    conteudo = req_api([
        {"role": "system", "content": "Você é um escritor de audiobooks. Escreva apenas texto corrido em parágrafos de 2 a 3 frases. Não use formatação especial."},
        {"role": "user", "content": prompt}
    ], 2000, 0.7)
    
    if conteudo:
        return quebrar_paragrafos_audio(conteudo)
    return f"Capítulo {num}. {titulo}. Conteúdo não disponível."

def criar_audiobook(titulo, topicos, introducao):
    """Gera audiobook formatado para Natural Reader 11"""
    p(f"Gerando audiobook com {len(topicos)} capítulos...")
    
    linhas = []
    
    titulo_limpo = limpar_texto(titulo)
    linhas.append(titulo_limpo.upper())
    linhas.append("")
    
    for paragrafo in introducao.split('\n\n'):
        if paragrafo.strip():
            linhas.append(limpar_texto(paragrafo))
            linhas.append("")
    
    linhas.append("")
    
    for i, topico in enumerate(topicos, 1):
        linhas.append(f"Capítulo {i}")
        linhas.append("")
        linhas.append(limpar_texto(topico))
        linhas.append("")
        
        conteudo = gerar_capitulo_audio(topico, i, len(topicos), introducao, introducao)
        
        for paragrafo in conteudo.split('\n\n'):
            if paragrafo.strip():
                linhas.append(limpar_texto(paragrafo))
                linhas.append("")
        
        if i < len(topicos):
            linhas.append("")
        
        progresso = int((i / len(topicos)) * 100)
        p(f"Progresso: {progresso}%")
        time.sleep(2)
    
    linhas.append("Fim do livro.")
    
    with open(ARQUIVOS["livro"], "w", encoding="utf-8") as f:
        for linha in linhas:
            if linha.strip():
                f.write(linha + "\n")
            else:
                f.write("\n")
    
    return len(linhas)

def exibir_preview_audio():
    if os.path.exists(ARQUIVOS["livro"]):
        with open(ARQUIVOS["livro"], "r", encoding="utf-8") as f:
            linhas = f.readlines()
        p("\n" + "="*60)
        p("PRÉVIA DO AUDIOBOOK (primeiras 25 linhas)")
        p("="*60)
        for i, linha in enumerate(linhas[:25]):
            if linha.strip():
                linha_curta = linha.strip()[:80]
                p(linha_curta)
            else:
                p("")
        p("="*60)
        p(f"Total de linhas: {len(linhas)}")
        p(f"Arquivo salvo: {ARQUIVOS['livro']}")
        p("")
        p("Para usar no Natural Reader 11:")
        p("1. Abra o arquivo livro.txt")
        p("2. Selecione a voz em português brasileiro")
        p("3. Ajuste velocidade para 1.0x ou 1.2x")
        p("4. Clique em Play")
    else:
        p("Erro: Arquivo do audiobook não foi criado")

def main():
    limpar_tela()
    p("="*60)
    p("GERADOR PROFISSIONAL DE AUDIOBOOKS")
    p("Otimizado para Natural Reader 11")
    p("="*60)
    p()
    
    titulo, assunto = ler_base()
    if not titulo or not assunto:
        input("Pressione Enter para sair...")
        return
    
    p(f"Título: {titulo}")
    p(f"Assunto: {assunto[:80]}...")
    p()
    
    p("Testando conexão com a API...")
    if not testar_conexao():
        p("ERRO: Não foi possível conectar à API.")
        input("Pressione Enter para sair...")
        return
    p("Conexão OK")
    p()
    
    inicio = time.time()
    
    if os.path.exists(ARQUIVOS["topicos"]) and os.path.getsize(ARQUIVOS["topicos"]) > 100:
        resp = input("Arquivo de tópicos já existe. Gerar novo? (s/N): ").lower()
        if resp != 's':
            with open(ARQUIVOS["topicos"], "r", encoding="utf-8") as f:
                topicos = []
                for linha in f:
                    linha = linha.strip()
                    if linha and '.' in linha and not linha.startswith('#'):
                        partes = linha.split('.', 1)
                        if len(partes) > 1:
                            topicos.append(limpar_texto(partes[1].strip()))
            p(f"Usando {len(topicos)} tópicos existentes")
        else:
            topicos = gerar_topicos(titulo, assunto)
    else:
        topicos = gerar_topicos(titulo, assunto)
    
    if not topicos:
        p("ERRO: Não foi possível gerar tópicos")
        input("Pressione Enter...")
        return
    
    p(f"{len(topicos)} capítulos gerados")
    p()
    
    if os.path.exists(ARQUIVOS["tema"]) and os.path.getsize(ARQUIVOS["tema"]) > 200:
        resp = input("Arquivo de introdução já existe. Gerar novo? (s/N): ").lower()
        if resp != 's':
            with open(ARQUIVOS["tema"], "r", encoding="utf-8") as f:
                introducao = f.read()
            p("Usando introdução existente")
        else:
            introducao = gerar_tema(titulo, assunto, topicos)
    else:
        introducao = gerar_tema(titulo, assunto, topicos)
    
    p()
    p("Iniciando geração do audiobook...")
    p("="*60)
    
    linhas_total = criar_audiobook(titulo, topicos, introducao)
    
    tempo = time.time() - inicio
    minutos = int(tempo // 60)
    segundos = int(tempo % 60)
    
    p()
    p("="*60)
    p("AUDIOBOOK GERADO COM SUCESSO!")
    p("="*60)
    p(f"Arquivo: {ARQUIVOS['livro']}")
    p(f"Título: {titulo}")
    p(f"Capítulos: {len(topicos)}")
    p(f"Tamanho: {linhas_total} linhas")
    p(f"Tempo: {minutos}m{segundos}s")
    p("="*60)
    
    exibir_preview_audio()
    
    p()
    p("INSTRUÇÕES PARA NATURAL READER 11:")
    p("1. Abra o arquivo livro.txt no Natural Reader")
    p("2. Selecione voz brasileira (ex: Ricardo, Maria)")
    p("3. Velocidade recomendada: 0.9x a 1.1x")
    p("4. Clique em Play para começar a narração")
    p()
    p("DICAS:")
    p("- O texto já está formatado com pausas naturais")
    p("- Parágrafos curtos = respiração correta do narrador")
    p("- Sem formatação especial = leitura mais fluida")
    p()
    input("Pressione Enter para sair...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        p("\nPrograma interrompido pelo usuário.")
    except Exception as e:
        p(f"Erro: {str(e)}")
        input("Pressione Enter para sair...")