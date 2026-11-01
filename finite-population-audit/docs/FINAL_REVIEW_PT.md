# Revisão final e preparação de submissão — RC1

Data editorial: 31/10/2026, America/Sao_Paulo. Situação: candidato preparado para revisão do autor; nada publicado ou submetido.

## Parecer

O trabalho está em condição de ser apresentado como **preprint técnico de uma demonstração reproduzível**, após fechamento dos metadados de autoria e das condições de publicação. A afirmação principal permanece condicional à tabela fixa e ao desenho amostral. O tratamento de Teacher estocástico não foi promovido a resultado demonstrado para a API real.

Não é necessário acrescentar um novo experimento para sustentar esse escopo delimitado. O estudo futuro de divergência esperada deve continuar em separado, sem alterar os resultados ou a população já examinados.

## O que foi preparado

- Base portuguesa v0.3 preservada, sem alterações de bytes.
- Versão científica em inglês, com edição de concisão e organização, 12 páginas, 19 referências e figura científica. É uma adaptação editorial fiel às afirmações da v0.3, não uma tradução literal linha a linha.
- Fonte Markdown, LaTeX e comando de compilação incluídos.
- Arquivo de evidência original preservado, sem sanitização que invalidasse seus hashes.
- Verificador novo e independente dos executores arquivados: lê dados, não executa código do arquivo, não chama API e não carrega modelos.
- Resultados do replay e varredura de padrões de credenciais incluídos.

## Conferências realizadas

O replay passou em 46.095 verificações de integridade, consistência e cálculos. Essa contagem é de condições verificadas no código, não de testes estatísticos independentes nem de evidências independentes de segurança.

| Item | Resultado |
|---|---|
| Arquivo de evidência | SHA256 original confirmado |
| Inventário | 6.336 arquivos conferidos; arquivo também contém inventário e README |
| Registros de modelos | 2.048 Teacher + 2.048 Student reconstruídos |
| Compromisso e vínculos | Conferidos |
| Adapter e seleção | Hashes conferidos |
| Beacon observado e reservado | Assinaturas BLS e controles de rodada errada conferidos |
| Sorteio | Permutação reconstruída independentemente |
| Certificado | k = 64; limite superior = 200/2.048; aprovação preservada |
| Censo | K = 158; dentro do limite primário |
| Gabarito revisado | Student 1.892 acertos; Teacher 12 discordâncias |
| Tokens | 168.640 na amostra; 447.733 no censo |
| Fingerprints | 36; pelo menos seis registros de cada um na amostra |
| Fronteira da decisão | 65 aprova; 66 não aprova |
| Risco de falsa aprovação | Enumeração dos totais K ≥ 205: máximo 0,0407935426 |
| Alteração de um byte no arquivo | Rejeitada antes de gerar resultados |
| Repetição do replay | Mesmo resumo em venv separada |

O ambiente de reprodução usa Python 3.12.14, NumPy 2.3.5, SciPy 1.17.0 e py-ecc 8.0.0. Os registros históricos identificam seu próprio ambiente, incluindo SciPy 1.18.1 nos estudos de planejamento. Esses ambientes não foram confundidos. A venv de conferência reutiliza NumPy/SciPy do ambiente instalado e possui py-ecc instalado nela; não é uma validação de contêiner isolado ou de todos os sistemas operacionais.

O PDF foi compilado e suas 12 páginas foram renderizadas para inspeção visual. Não restaram avisos de texto excedendo margens na compilação final. Os números principais foram conferidos também no texto extraído do PDF.

## Ajustes editoriais em inglês

- “Revisão independente” foi especificada como replay computacional separado, assistido por IA; não é auditoria institucional ou revisão por pares externa.
- Resumo e discussão mantêm a hipótese de tabela fixa e a existência de rótulos revisados por humano.
- Economia mantém o denominador e o escopo corretos; como houve censo, não se afirma economia efetivamente retida nas consultas totais.
- Comparações binomial/KL/Hoeffding estão explicitamente condicionadas ao modelo iid.
- Os testes por fingerprint e tempo permanecem exploratórios, sem afirmação de equivalência ou estabilidade comprovada.
- A sequência é evidência local, não carimbo temporal público; a ameaça de grinding permanece declarada.
- A inovação é apresentada como integração e demonstração experimental; não se afirma prioridade histórica ou um teorema novo.

## Inspeção de informações para publicação

Foram varridos os 6.338 arquivos do arquivo de revisão, com exclusão dos bytes binários do adapter na pesquisa textual, para padrões de chaves Groq, GitHub, OpenAI e chaves privadas. Nenhum padrão foi encontrado. Não foram encontrados caminhos `/home/asus` no conteúdo textual conferido. Essa é uma varredura delimitada, não prova de ausência de qualquer informação sensível.

IDs de requisição do provedor, fingerprints, horários e textos sintéticos permanecem na evidência original. Não foram adicionados e-mail, ORCID, vínculo com empregador ou patrocínio presumidos.

## O que resta antes de publicação

1. Confirmar a forma do nome do autor, afiliação e contato; nenhum vínculo empresarial foi atribuído.
2. Adotar as licenças propostas, respeitando o material de terceiros e as condições aplicáveis às respostas arquivadas.
3. Aprovar a publicação deste candidato em uma pasta separada do repositório existente e criar uma versão pública identificável. Ainda não há DOI de lançamento.
4. Atualizar a declaração de disponibilidade com a URL pública real e concluir os metadados de submissão.

As opções concretas estão em `PUBLICATION_DECISIONS.md`. O pacote não foi enviado ao GitHub ou ao arXiv. Os arquivos originais no Ubuntu do autor também não foram alterados por esta preparação.
