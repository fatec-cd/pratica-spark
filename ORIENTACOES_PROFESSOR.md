# Orientações para o Professor - Atividade PySpark

## Resumo das Mudanças

Este documento descreve as alterações realizadas no roteiro da atividade prática de PySpark.

### O que foi removido

As seguintes partes foram **removidas** do roteiro original:

- **Parte 6: Exercícios Práticos** - 5 exercícios adicionais de implementação
- **Parte 7: Comparação MapReduce vs Spark** - Exercício comparativo detalhado
- **Parte 8: Publicação e Documentação** - Instruções para Docker Hub e documentação adicional

### O que foi adicionado

Foi criada uma nova **Parte 6: Entregáveis da Atividade** que contém:

1. Estrutura clara do que deve ser entregue
2. Template detalhado do relatório (ENTREGA.md)
3. Lista de 13 screenshots obrigatórios
4. Critérios de avaliação objetivos
5. Checklist de pré-entrega
6. Orientações sobre formato e organização

### Arquivos criados

1. **ENTREGA_TEMPLATE.md** - Template para os alunos preencherem
2. **evidencias/README.md** - Instruções sobre os screenshots
3. **evidencias/** - Pasta onde alunos devem colocar os screenshots

---

## Estrutura da Entrega do Aluno

Cada aluno deve entregar:

### 1. Arquivo ENTREGA.md

Baseado no template fornecido, contendo:

- **Informações pessoais**: Nome, RA, data
- **Evidências de cada parte**: Screenshots e reflexões
- **Checklist de conclusão**: Marcado conforme concluído
- **Aprendizados**: Reflexões sobre a atividade
- **Declaração de autenticidade**: Assinatura digital

### 2. Pasta evidencias/

Contendo 13 screenshots obrigatórios:

1. `screenshot_fork.png` - Fork no GitHub
2. `screenshot_codespaces.png` - Ambiente de desenvolvimento
3. `screenshot_estrutura.png` - Estrutura do projeto
4. `screenshot_data_generator.png` - Geração de dados
5. `screenshot_wordcount.png` - Exemplo word count
6. `screenshot_schema.png` - Schema do DataFrame
7. `screenshot_receita_categoria.png` - Análise 1
8. `screenshot_top_produtos.png` - Análise 2
9. `screenshot_vendas_regiao.png` - Análise 3
10. `screenshot_docker_build.png` - Build Docker
11. `screenshot_docker_images.png` - Imagens Docker
12. `screenshot_docker_run.png` - Execução container
13. `screenshot_docker_compose.png` - Docker Compose

### 3. Repositório completo

- Código funcionando (todos os scripts .py)
- Dados gerados (arquivos CSV)
- Dockerfile e docker-compose.yml funcionais
- README.md original preservado

---

## Critérios de Avaliação

### Distribuição de Pontos (100 pontos)

| Critério | Pontos | Detalhamento |
|----------|--------|--------------|
| **Completude das Evidências** | 40 | Todos os 13 screenshots presentes e legíveis |
| **Execução Correta** | 30 | Evidências mostram execuções bem-sucedidas |
| **Documentação e Reflexão** | 20 | Respostas demonstram compreensão dos conceitos |
| **Organização** | 10 | Repositório bem estruturado e profissional |

### Rubricas Detalhadas

#### Completude das Evidências (40 pontos)

- **40 pontos**: Todos os 13 screenshots presentes, legíveis, completos
- **35 pontos**: 12 screenshots presentes e adequados
- **30 pontos**: 11 screenshots presentes e adequados
- **25 pontos**: 10 screenshots presentes e adequados
- **20 pontos**: 8-9 screenshots presentes
- **10 pontos**: 5-7 screenshots presentes
- **0 pontos**: Menos de 5 screenshots

#### Execução Correta (30 pontos)

- **30 pontos**: Todas as execuções funcionaram corretamente sem erros
- **25 pontos**: Uma pequena falha ou erro solucionado
- **20 pontos**: 2-3 problemas menores
- **15 pontos**: Várias falhas mas demonstra esforço
- **10 pontos**: Execuções parciais
- **0 pontos**: Não executou ou erros graves não tratados

#### Documentação e Reflexão (20 pontos)

- **20 pontos**: Reflexões profundas, demonstra total compreensão
- **17 pontos**: Boa compreensão, reflexões adequadas
- **14 pontos**: Compreensão básica, reflexões superficiais
- **10 pontos**: Compreensão parcial
- **5 pontos**: Respostas muito superficiais ou copiadas
- **0 pontos**: Seções de reflexão não preenchidas

#### Organização (10 pontos)

- **10 pontos**: Repositório impecável, screenshots bem nomeados, estrutura perfeita
- **8 pontos**: Bem organizado, pequenos desvios
- **6 pontos**: Organização adequada
- **4 pontos**: Desorganizado mas navegável
- **2 pontos**: Muito desorganizado
- **0 pontos**: Caótico ou arquivos faltando

---

## Checklist de Correção

Use este checklist ao avaliar cada entrega:

### Requisitos Obrigatórios

- [ ] Arquivo ENTREGA.md existe e está preenchido
- [ ] Pasta evidencias/ existe e contém screenshots
- [ ] Repositório é um fork válido do original
- [ ] Nome e RA do aluno estão claramente identificados
- [ ] Link do repositório está funcionando

### Screenshots (13 obrigatórios)

- [ ] Screenshot 1: Fork do repositório
- [ ] Screenshot 2: Codespaces em execução
- [ ] Screenshot 3: Estrutura do projeto
- [ ] Screenshot 4: Geração de dados
- [ ] Screenshot 5: Word count executado
- [ ] Screenshot 6: Schema do DataFrame
- [ ] Screenshot 7: Receita por categoria
- [ ] Screenshot 8: Top 10 produtos
- [ ] Screenshot 9: Vendas por região
- [ ] Screenshot 10: Docker build
- [ ] Screenshot 11: Docker images
- [ ] Screenshot 12: Container executando
- [ ] Screenshot 13: Docker compose

### Execuções

- [ ] data_generator.py foi executado (dados gerados)
- [ ] spark_word_count.py foi executado com sucesso
- [ ] spark_sales_analysis.py foi executado com sucesso
- [ ] Imagem Docker foi construída
- [ ] Container Docker executou corretamente

### Reflexões

- [ ] Parte 1: Reflexão sobre RDD vs DataFrame
- [ ] Parte 2: 3 perguntas de negócio propostas
- [ ] Parte 4: Principais descobertas descritas
- [ ] Seção final: Aprendizados descritos
- [ ] Seção final: Dificuldades e soluções
- [ ] Seção final: 2 aplicações práticas

### Organização

- [ ] Screenshots com nomes padronizados
- [ ] Imagens em formato PNG ou JPG
- [ ] ENTREGA.md formatado corretamente (Markdown)
- [ ] Declaração de autenticidade preenchida
- [ ] Commit SHA informado

---

## Dúvidas Frequentes (Respostas para o Professor)

### 1. E se o aluno não conseguir usar Codespaces?

**Resposta**: O aluno pode trabalhar localmente. O importante são as evidências de execução, independente do ambiente.

### 2. E se o Docker não funcionar no ambiente do aluno?

**Resposta**: O aluno pode usar Play with Docker (labs.play-with-docker.com) ou qualquer ambiente que suporte Docker. Screenshots devem demonstrar a execução.

### 3. Screenshots precisam ser do Codespaces especificamente?

**Resposta**: Não. Podem ser de ambiente local, Play with Docker, ou qualquer ambiente Linux/Mac/Windows que execute os comandos.

### 4. E se o aluno fizer mais do que o pedido?

**Resposta**: Pode conceder pontos extras (até 10% bônus) se o aluno:
- Implementar exercícios extras do EXERCICIOS_EXTRAS.md
- Criar visualizações (gráficos) dos resultados
- Otimizar o código ou Dockerfile
- Documentar insights de negócio profundos

### 5. Posso modificar os critérios de avaliação?

**Resposta**: Sim! A estrutura fornecida é uma sugestão. Ajuste conforme os objetivos da sua disciplina.

### 6. Como verificar se o trabalho é autêntico?

**Sugestões**:
- Verificar timestamp dos commits no GitHub
- Pedir que o aluno grave um vídeo curto (2-3 min) explicando uma parte
- Fazer perguntas sobre o código em uma apresentação oral
- Verificar se as reflexões são coerentes com o nível do aluno

---

## Sugestões de Uso

### Modalidade Presencial

1. **Aula 1**: Introdução ao Spark (Partes 1 e 2)
2. **Aula 2**: Hands-on - Configuração e primeira execução (Partes 3 e 4)
3. **Aula 3**: Docker e containerização (Parte 5)
4. **Aula 4**: Finalização e dúvidas
5. **Entrega**: 1 semana após Aula 4

### Modalidade EAD/Híbrida

1. **Semana 1**: Vídeo-aulas + leitura Partes 1 e 2
2. **Semana 2**: Tutorial guiado Partes 3 e 4 + fórum de dúvidas
3. **Semana 3**: Tutorial Docker Parte 5 + plantão online
4. **Semana 4**: Entrega do trabalho

### Modalidade Intensiva (Bootcamp)

1. **Dia 1 - Manhã**: Teoria (Partes 1 e 2)
2. **Dia 1 - Tarde**: Prática guiada (Partes 3 e 4)
3. **Dia 2 - Manhã**: Docker (Parte 5) + início entrega
4. **Dia 2 - Tarde**: Finalização da entrega + dúvidas
5. **Entrega**: Final do Dia 2

---

## Materiais Complementares Disponíveis

O repositório inclui materiais extras opcionais:

1. **EXERCICIOS_EXTRAS.md** - 10+ exercícios adicionais para alunos avançados
2. **COMPARACAO_MAPREDUCE_SPARK.md** - Comparação detalhada dos paradigmas
3. **PROJETO_OVERVIEW.md** - Visão geral do projeto

Estes podem ser usados para:
- Atividades extras (pontos bônus)
- Trabalhos de aprofundamento
- Material de estudo para provas
- Projetos finais da disciplina

---

## Contato e Suporte

Para dúvidas sobre o roteiro ou sugestões de melhorias:

- Abra uma issue no repositório original
- Entre em contato com o mantenedor
- Contribua com pull requests

---

**Versão**: 2.0  
**Data de atualização**: Novembro 2024  
**Alterações**: Remoção de Partes 6, 7 e 8 originais; Adição de Parte 6 (Entregáveis)
