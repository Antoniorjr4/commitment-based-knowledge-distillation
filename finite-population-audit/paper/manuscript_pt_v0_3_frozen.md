# Auditoria de fidelidade Teacher–Student com compromisso de resultados, aleatoriedade pública e certificação em população finita

**Antônio Rufino**  
**Manuscrito de trabalho — versão 0.3, 31 de outubro de 2026 (horário de Brasília)**  
Versão em português para revisão científica. Sem submissão ou publicação realizada.

## Resumo

A adoção de modelos menores ajustados com respostas de um modelo de referência exige uma forma verificável de medir a fidelidade comportamental, sem consultar a referência para cada entrada. Apresentamos uma implementação de auditoria que combina o compromisso por SHA256 de uma população finita e das respostas do Student, uma rodada futura de um beacon público de aleatoriedade e um limite superior unilateral obtido pela inversão da distribuição hipergeométrica. Aplicamos o protocolo à classificação de relatos de manutenção industrial entre as especialidades elétrica e mecânica. Um Qwen2.5-1.5B-Instruct ajustado por LoRA foi executado localmente em CPU e teve suas 2.048 respostas fixadas antes do sorteio. A amostra principal, predefinida em 768 relatos, apresentou 64 divergências em relação ao Teacher servido por API, resultando em limite superior de 9,7656% e atendendo à meta previamente fixada de 10%, com confiança nominal de 95% sob a hipótese de uma tabela fixa de divergências e amostragem uniforme sem reposição. O censo posterior encontrou 158 divergências em 2.048 relatos, ou 7,7148%, abaixo do limite primário. A etapa de certificação utilizou 37,5% das consultas e 37,6653% dos tokens observados no censo; o complemento foi realizado para avaliação do procedimento. Todos os relatos já possuíam rótulos revisados por humano: a comparação de esforço refere-se à aquisição das respostas do Teacher, e não à avaliação contra um gabarito já disponível. Os artefatos permitem reconstruir o sorteio, conferir a integridade das respostas e reproduzir os cálculos. A contribuição é uma demonstração operacional de certificação de fidelidade com referência externa, com distinção explícita entre integridade documental, validade amostral e estabilidade da referência.

**Palavras-chave:** auditoria de modelos; fidelidade comportamental; destilação por respostas; amostragem sem reposição; limite hipergeométrico; aleatoriedade pública; reprodutibilidade.

## 1. Introdução

Modelos de linguagem compactos podem ser ajustados para executar tarefas delimitadas a partir de respostas produzidas por um modelo de referência. Essa estratégia permite executar o modelo ajustado em infraestrutura local, mas introduz uma questão de verificação: quanto seu comportamento diverge da referência no conjunto de entradas que se pretende processar?

Uma taxa de concordância calculada em exemplos escolhidos informalmente oferece evidência descritiva. Uma auditoria exige também especificar a população, impedir escolhas oportunistas da amostra, preservar as saídas avaliadas e associar o resultado a uma regra de decisão definida antes da observação. Quando a referência é acessada por API, a auditoria precisa ainda registrar as condições de consulta e distinguir o identificador comercial do serviço de uma revisão de pesos efetivamente controlada pelo pesquisador.

Este trabalho estuda uma pergunta operacional: **é possível certificar uma taxa de divergência Teacher–Student de, no máximo, 10% em uma população finita de 2.048 relatos, consultando o Teacher em uma amostra predefinida de 768 entradas?** A resposta experimental foi positiva: o limite primário foi 9,7656%. Uma avaliação posterior de toda a população mediu divergência de 7,7148%.

O protocolo foi organizado em três etapas. Primeiro, a população, o Student e suas respostas foram identificados por hashes. Depois, uma rodada futura do drand determinou a amostra. Finalmente, as respostas do Teacher nos itens selecionados produziram o certificado estatístico. A avaliação complementar foi iniciada após a emissão do certificado primário e preservou esse resultado.

A implementação contribui com: (i) uma sequência auditável que conecta compromissos de arquivos, sorteio reproduzível e análise estatística; (ii) uma demonstração em 2.048 relatos técnicos revisados, executada com Student local em CPU; e (iii) uma conferência censitária e diagnósticos que permitem examinar tanto a fidelidade quanto a relação de ambos os modelos com os rótulos revisados. As ferramentas estatísticas e criptográficas empregadas são estabelecidas; a contribuição aqui documentada está em sua integração experimental e na rastreabilidade dos resultados.

## 2. Fundamentação e trabalhos relacionados

### 2.1. Destilação e adaptação de modelos

A destilação transfere comportamento de modelos de referência para modelos mais compactos [1]. Neste estudo, a transferência utiliza rótulos textuais produzidos pelo Teacher. O Student é treinado com a perda de predição dos tokens da resposta; não há acesso aos logits do Teacher. Denominamos essa estratégia **destilação por respostas**, reconhecendo sua proximidade com ajuste supervisionado por rótulos sintéticos.

A adaptação utiliza LoRA [2], mantendo os pesos base congelados e atualizando matrizes de baixo posto. Os modelos Student pertencem à família Qwen2.5 [3]. O objetivo experimental é obter um comportamento de classificação auditável em uma tarefa restrita, utilizando equipamento pessoal.

### 2.2. Amostragem finita e avaliação eficiente

A amostragem sem reposição permite inferir propriedades de uma população fixa sem examinar todos os seus elementos. Desigualdades de concentração, incluindo resultados de Serfling e seus refinamentos, tratam esse cenário [4]. Para uma característica binária e uma população de tamanho conhecido, a distribuição hipergeométrica permite construir um limite unilateral por inversão de testes, incorporando diretamente a informação sobre o tamanho finito da população.

A inferência auxiliada por predições também investiga como combinar avaliações caras com predições mais abundantes [5]. Sua aplicação à avaliação de modelos de linguagem inclui métodos estratificados [6]. Nosso estimando é especificamente a fração de divergências entre Student e referência na população comprometida. Não aplicamos os estimadores de correção da prediction-powered inference neste experimento.

Métodos de controle conformal de risco oferecem outra abordagem para vincular decisões a garantias estatísticas [7]. O procedimento aqui utilizado é um limite de confiança para um total finito com tamanho amostral fixo; sua garantia e seu objeto diferem daqueles de controle do risco esperado de uma regra calibrada.

### 2.3. Auditorias com limite de risco e inferência sequencial

As auditorias eleitorais com limite de risco fornecem antecedentes diretos para transformar amostragem e uma trilha documental em decisões com risco máximo predefinido. Lindeman e Stark [11] apresentam esse princípio; CAST [12] organiza etapas de amostragem e testes; ALPHA [13] contempla desenhos com e sem reposição e atualização baseada nos itens já auditados. Compartilhamos a ideia de examinar uma fração dos registros sob uma regra estatística verificável. Nosso estimando é uma taxa de divergência entre classificadores, enquanto essas auditorias tratam da correção do resultado eleitoral e de regras de escalonamento até recontagem. O censo do presente experimento foi uma validação complementar planejada, não uma escalada necessária após reprovação.

Em particular, a regra atual pode ser vista como um teste de \(H_0:K\ge205\): sob cada tabela fixa que excede a meta, a probabilidade de aprovação é no máximo 5%. Isso decorre da cobertura unilateral e não é um princípio novo de auditoria. A contribuição examinada é a implementação dessa lógica em uma tarefa Teacher–Student, com preservação das respostas e sorteio derivado de beacon.

Para permitir parada dependente dos dados em trabalhos futuros, a referência diretamente pertinente são as sequências de confiança sem reposição de Waudby-Smith e Ramdas [14]. Elas controlam a cobertura simultaneamente ao longo da coleta. Essa garantia não seria obtida simplesmente recalculando o limite hipergeométrico de tamanho fixo após cada consulta.

### 2.4. Identidade e estabilidade de uma API

Gao, Liang e Guestrin [10] formulam *Model Equality Testing* como um problema de comparação entre distribuições de respostas de uma API e de uma referência. O problema é próximo da identificação operacional do Teacher: um nome de modelo não basta para estabelecer que a distribuição servida corresponde à referência pretendida. Nosso diagnóstico compara rótulos em entradas repetidas, sem implementar o teste distribucional desse trabalho. A fidelidade binária em uma população delimitada e a igualdade de distribuições de geração são objetos distintos. Essa literatura fornece uma base para ampliar o monitoramento de mudanças na referência.

### 2.5. Aleatoriedade verificável

O NIST descreve o compromisso antecipado de uma operação determinística e o uso de um valor futuro de beacon como procedimento genérico de aleatorização publicamente verificável, incluindo seleção de itens para auditoria [15]. Esse encadeamento constitui um antecedente explícito do desenho adotado. O ZkAudit [16] combina compromissos de dados e modelos com provas de conhecimento zero para auditar propriedades sem revelar os objetos privados. Aqui, os registros são examináveis e o certificado é estatístico; não implementamos as garantias de execução privada do ZkAudit. O problema de selecionar desafios favoráveis também aparece em *Seal, Then Sample* [17], que discute grinding e a necessidade de ordenação externa do desafio em seu próprio protocolo de provas de inferência.

O drand produz valores públicos de aleatoriedade acompanhados de assinaturas verificáveis [8,9]. No protocolo implementado, a rodada é reservada após a fixação dos artefatos, e seu valor determina a amostra por um algoritmo previamente identificado. Isso torna o sorteio reconstruível a partir de dados públicos e do compromisso registrado.

A função dos hashes é identificar versões exatas dos arquivos. A função do beacon é fornecer a entrada pública do sorteador. A prova estatística descreve a cobertura sob o desenho amostral assumido. Essas funções são complementares: a assinatura do beacon não autentica as respostas da API, e um hash local, isoladamente, não estabelece uma data de publicação perante terceiros.

## 3. Objeto da auditoria e protocolo estatístico

### 3.1. Estimando

Seja uma população ordenada de entradas \(x_1,\ldots,x_N\). Denotamos por \(s_i\) a resposta fixada do Student e por \(t_i\) o rótulo de referência associado à entrada sob as condições de consulta especificadas. Definimos

\[
D_i=\mathbf{1}\{s_i\ne t_i\},\qquad K=\sum_{i=1}^{N}D_i,\qquad p=K/N.
\]

A auditoria busca limitar \(p\), a divergência na população comprometida. Os rótulos manuais são utilizados em uma análise separada de concordância com a revisão técnica.

O resultado teórico a seguir pressupõe uma tabela binária de divergências fixa e uma amostra aleatória simples sem reposição. Sua aplicação à referência externa requer que a forma de obtenção dos rótulos não introduza dependência entre o resultado potencial de um item e sua inclusão ou ordem de consulta. A estabilidade observada do Teacher fornece evidência operacional relevante para essa hipótese, sem substituir sua formulação.

### 3.2. Limite unilateral exato

Se a amostra contém \(n\) itens, o número observado de divergências \(X\), condicionado a \(K\), segue

\[
X\sim\operatorname{Hypergeom}(N,K,n).
\]

Para o valor observado \(k\), definimos

\[
K_U(k)=\max\left\{K'\in\{0,\ldots,N\}:\Pr_{K'}(X\le k)>\delta\right\},
\qquad U(k)=K_U(k)/N.
\]

Para \(K'<k\), a probabilidade pontual da observação \(X=k\) é zero, mas a CDF \(\Pr_{K'}(X\le k)\) vale 1: esses valores entram no conjunto e apenas não alteram seu máximo. Pode-se restringir a busca ao suporte compatível \(k\le K'\le N-n+k\). Esse suporte contém \(K'=k\), cuja CDF vale 1; para \(K'>N-n+k\), a CDF é zero. A restrição preserva, portanto, o máximo definido acima.

**Proposição.** Sob uma tabela fixa e amostragem aleatória simples sem reposição, \(\Pr_K\{K\le K_U(X)\}\ge1-\delta\), para todo \(K\).

**Justificativa.** A função \(\Pr_{K'}(X\le k)\) é não crescente em \(K'\). O evento de subcobertura implica que a função de distribuição avaliada no valor observado sob o verdadeiro \(K\) é menor ou igual a \(\delta\). Para uma variável discreta, a probabilidade desse evento é, no máximo, \(\delta\). A inversão preserva, portanto, cobertura de pelo menos \(1-\delta\). A discretização pode produzir cobertura superior à nominal. No censo, \(n=N\), a observação determina \(K\), e o limite coincide com a taxa conhecida.

O termo “exato” refere-se à distribuição finita utilizada, em oposição a uma aproximação assintótica. A implementação calcula sua CDF numericamente com SciPy.

### 3.3. Regra primária

O desenho fixou \(N=2.048\), \(n=768\), \(\delta=0,05\) e a meta \(U\le0,10\). Como o total é inteiro, a meta equivale a \(K_U\le204\). O código conferiu previamente que até 65 divergências na amostra atendem ao critério, enquanto 66 não atendem.

O tamanho de 768 e a meta foram registrados no desenho antes da construção da população ampliada, segundo a sequência documental preservada. O estudo de dimensionamento considerou taxas de 3%, 5%, 7% e 10%. A escolha ocorreu depois dos resultados dos experimentos anteriores, incluindo o censo de 256 relatos com 17 divergências (6,6406%). Assim, o cenário de aproximadamente 7% foi informado por experiência prévia; não era uma previsão independente dos resultados anteriores.

| Momento registrado | Informação disponível ou etapa realizada |
|---|---|
| Escolha de N, n e meta | Adapter já selecionado; resultados anteriores conhecidos, incluindo 17/256; nova população ainda em construção futura |
| Congelamento da população e execução do Student | Textos e rótulos revisados completos; geração posterior das 2.048 respostas do Student |
| Compromisso pré-beacon | Rótulos revisados e tabela completa do Student disponíveis; nenhum Teacher da população ampliada consultado segundo os registros |
| Após o sorteio | Teacher consultado nos 768 itens; emissão do resultado primário |
| Após o resultado primário | Teacher consultado no complemento; obtenção do total censitário K = 158 |

Antes do beacon, seria possível calcular o erro do Student contra os rótulos revisados, pois ambas as tabelas já existiam. Isso não equivale a conhecer o total de divergências com o Teacher. Os artefatos examinados não oferecem uma trilha completa de toda inspeção informal ou cálculo fora dos scripts; a afirmação de anterioridade é documental e não constitui um registro público independente de pré-registro. Os registros situam a fixação de n e da meta antes da própria disponibilidade da tabela ampliada do Student. A concordância posterior Teacher–revisão de 99,4141% também não era uma medição disponível nessa escolha.

No cenário de planejamento \(K=143\), a probabilidade exata de aprovação era 98,2510% com n = 768 e 87,4397% com n = 512. Depois do censo, podemos caracterizar o mesmo desenho condicionalmente a \(K=158\):

| Total fixo de divergências | Taxa | n = 512, aprovação até k = 41 | n = 768, aprovação até k = 65 |
|---|---:|---:|---:|
| K = 143 — cenário de planejamento | 6,9824% | 87,4397% | 98,2510% |
| K = 158 — caracterização posterior ao censo | 7,7148% | 65,3156% | 85,7332% |

As probabilidades são \(\Pr_K(X\le c_n)\), com \(X\sim\operatorname{Hypergeom}(2.048,K,n)\) e corte \(c_n\) de cada tamanho. O cálculo para K = 158 descreve a chance de aprovação em novos sorteios sobre a tabela censitária fixa; não constitui uma nova estimativa de cobertura nem uma justificação retrospectiva para selecionar n. A aprovação observada não era garantida.

O procedimento utiliza uma única análise primária com tamanho fixo. Os cálculos exploratórios de outros tamanhos não constituem uma regra de parada adaptativa nem uma garantia simultânea entre múltiplas análises. A cobertura para cada tabela fixa não depende de a taxa escolhida no planejamento acertar a taxa censitária; depende de preservar as condições do desenho e a regra de análise.

## 4. Modelos, dados e execução

### 4.1. Desenvolvimento do Student

O desenvolvimento comparou Qwen2.5-0.5B-Instruct e Qwen2.5-1.5B-Instruct. Na etapa que originou o Student de 1,5B, o conjunto de desenvolvimento continha 96 relatos de treino, em 24 famílias, e 32 relatos de validação, em oito famílias. Cada família continha quatro redações. As classes eram balanceadas em cada divisão.

Foram examinadas duas taxas de aprendizado, \(5\times10^{-5}\) e \(2\times10^{-4}\), com checkpoints nas épocas 1 e 3. Cada taxa partiu do modelo original. A configuração LoRA utilizou posto 4, alpha 8, dropout zero e os módulos `q_proj` e `v_proj`; 544.768 parâmetros eram treináveis. O ajuste empregou AdamW, lote unitário e semente 42, em CPU/FP32. O checkpoint selecionado foi o da terceira época com taxa \(2\times10^{-4}\), identificado por hashes antes das avaliações subsequentes.

Os rótulos do Teacher coincidiram com os rótulos revisados nos dados de desenvolvimento. Assim, essa etapa demonstra a viabilidade do ajuste por respostas, mas não isola um benefício exclusivo dos rótulos do Teacher em relação aos mesmos rótulos fornecidos manualmente.

### 4.2. População ampliada

A população da auditoria ampliada contém 2.048 relatos em português, organizados em 1.024 famílias cadastradas, com duas redações por situação. Há 1.024 relatos elétricos e 1.024 mecânicos, distribuídos em oito grupos técnicos de 256 relatos cada.

As situações e redações foram elaboradas com assistência de IA e revisadas pelo pesquisador responsável. Foram registrados 32 lotes e suas aprovações. Duas emendas anteriores ao congelamento refinaram textos e delimitações técnicas; os arquivos originais foram preservados. A conferência final detectou ausência de duplicatas textuais após normalização de caixa e espaços.

As famílias registram situações técnicas relacionadas; componentes e mecanismos de falha podem reaparecer em famílias distintas. O universo inferencial principal é a tabela finita de 2.048 relatos. Essa definição permite analisar o desenho amostral sem presumir que as famílias representem mecanismos independentes ou uma amostra probabilística da manutenção industrial em produção.

### 4.3. Referência e respostas

O Teacher foi acessado pela Groq, com identificador `openai/gpt-oss-20b`, temperatura zero, limite de 1.024 tokens de conclusão, timeout de 90 segundos e repetição automática desativada. O prompt solicitava somente `ELETRICA` ou `MECANICA`.

As respostas brutas, os pedidos e os metadados retornados foram preservados. A normalização do Teacher remove espaços periféricos e admite as formas acentuadas previstas. O Student foi avaliado por correspondência exata após remoção de espaços periféricos. A configuração de geração utilizou `do_sample=False`, até 12 novos tokens e o template de chat do tokenizer identificado.

Duas interrupções HTTP 429 ocorreram na coleta complementar. Os erros foram arquivados, e a coleta foi retomada explicitamente nos itens sem resposta salva. O executor e o certificado primário foram preservados. O conjunto final contém uma resposta utilizada por item, além do histórico das tentativas interrompidas.

### 4.4. Infraestrutura local

O Student foi executado em um notebook com processador Intel Core i7-8565U, 16 GB de memória física e Ubuntu sob WSL2, com teto de memória de 10 GB. A configuração utilizou CPU, FP32 e quatro threads. A revisão dos pesos base foi `989aa7980e4cf806f80c7fef2b1adb7bc71aa306`.

A geração das 2.048 respostas levou 4 h 19 min 09 s, com pico de memória residente registrado de 9.465.320 KiB. Esse tempo caracteriza a execução local específica. O registro de consultas e tokens do Teacher é apresentado separadamente, sem convertê-lo em uma comparação de energia ou de custo computacional entre infraestruturas.

## 5. Compromisso, sorteio e rastreabilidade

A sequência operacional foi:

1. Consolidar a população, registrar revisões e congelar os textos.
2. Fixar configurações, sorteador, análise e executores.
3. Gerar e fixar as 2.048 respostas do Student.
4. Registrar o compromisso dos artefatos e reservar uma rodada futura do drand.
5. Verificar a assinatura do beacon e reconstruir a amostra de 768 itens.
6. Consultar o Teacher na amostra e emitir o certificado primário.
7. Preservar o certificado e consultar os 1.280 itens restantes para o censo.

O compromisso utiliza SHA256 dos bytes exatos dos arquivos. A implementação usa hashes de arquivos completos; não emprega árvore de Merkle. A rodada escolhida foi 33.515.062 da rede quicknet, prevista para 30 de outubro de 2026, às 08:22:30 UTC.

O sorteador deriva uma semente do domínio do experimento, do hash da população e da aleatoriedade do beacon. Um fluxo de blocos SHA256 com contador alimenta uma permutação Fisher–Yates, utilizando rejeição para evitar viés de redução modular. Os primeiros 768 IDs da permutação formam a amostra.

O resultado estatístico assume amostragem uniforme. Na implementação, a geração pseudoaleatória por SHA256 representa essa idealização sob hipóteses criptográficas; rejeitar o viés modular não transforma um espaço finito de sementes em uniformidade informacional exata sobre todas as permutações possíveis.

A verificação independente dos artefatos recebidos reconstruiu a amostra, verificou as assinaturas BLS e um teste negativo de rodada, conferiu os 6.336 arquivos inventariados e reproduziu as contagens e o limite principal. Essa revisão foi realizada por processamento dos registros arquivados, sem reexecutar treinamento ou inferência. O pacote registra que não foi estabelecido um carimbo temporal público independente do compromisso. Seu uso futuro em uma disputa entre partes exige um canal de publicação ou registro temporal verificável anterior à rodada.

### 5.1. Modelo de ameaça: grinding e seleção de execuções

Um adversário pode preparar várias populações ou compromissos candidatos, observar o beacon e apresentar apenas o candidato cujo sorteio pareça favorável. Também pode escolher entre rodadas ou abandonar seletivamente auditorias depois do resultado. Na implementação atual, a semente depende do hash da população e do beacon: variar a população candidata ou a rodada altera o sorteio. A mera existência de um hash não demonstra que um candidato era o único elegível antes da revelação, e gerar muitos candidatos offline não é, por si só, detectável nos arquivos publicados.

A defesa prospectiva precisa vincular uma identidade de auditoria a um compromisso elegível e à rodada futura por meio de um registro público ordenado, antes da disponibilidade do beacon. Deve especificar prazo, regra de escolha entre registros, tratamento de alterações e obrigação de preservar e reportar resultados e abandonos. Um carimbo temporal de vários candidatos sem regra de elegibilidade ainda permite escolha posterior. O registro ordenado evita essa escolha apenas no modelo de participação definido; identidades múltiplas ou auditorias ocultadas exigem controles adicionais.

A auditoria realizada preserva a sequência local e o compromisso recebido, mas não estabeleceu esse registro público independente nem uma prova de resistência a grinding. O beacon verificável e os hashes conferidos são evidências de reconstrução e integridade, não uma demonstração de unicidade prévia do compromisso. O padrão do NIST [15] e o ataque discutido em [17] motivam essa extensão sem atribuir à implementação uma proteção ainda não realizada.

## 6. Resultados

### 6.1. Certificado primário e censo

| Medida | Amostra principal | Complemento | Censo |
|---|---:|---:|---:|
| Relatos consultados | 768 | 1.280 | 2.048 |
| Divergências Teacher–Student | 64 | 94 | 158 |
| Divergência observada | 8,3333% | 7,3438% | 7,7148% |
| Limite superior primário | 9,7656% | — | Taxa censitária conhecida |
| Tokens reportados | 168.640 | 279.093 | 447.733 |

**A auditoria atingiu a meta previamente fixada.** As 64 divergências observadas produziram \(K_U=200\), ou 9,765625%, abaixo de 10%. O censo posterior encontrou 158 divergências, 42 a menos que o total superior certificado. A taxa censitária ficou 2,0508 pontos percentuais abaixo do limite primário.

O certificado foi emitido com 37,5% das consultas requeridas pelo censo. Os tokens correspondentes representaram 37,6653% do total observado, uma diferença de 62,3347%. Essa comparação mede o esforço da etapa de certificação em relação à referência completa. Como o censo foi efetivamente realizado para examinar o procedimento, o experimento utilizou os 447.733 tokens reportados nas 2.048 respostas.

A cobertura nominal descreve o procedimento em repetições do desenho sob suas hipóteses. O fato de o censo estar abaixo do limite confirma a cobertura nesta realização específica; a garantia de 95% decorre da construção estatística, não de uma frequência estimada a partir desta única rodada.

### 6.2. Concordância com a revisão técnica

| Medida no censo | Contagem | Percentual |
|---|---:|---:|
| Student em acordo com Teacher | 1.890/2.048 | 92,2852% |
| Student em acordo com rótulos revisados | 1.892/2.048 | 92,3828% |
| Teacher em desacordo com rótulos revisados | 12/2.048 | 0,5859% |
| Student com formato inválido | 0/2.048 | 0% |

Nos 12 casos em que Teacher e rótulo revisado diferiram, o Student concordou com a revisão em sete e com o Teacher em cinco. Esses casos mostram por que fidelidade e concordância com a referência técnica precisam ser reportadas separadamente.

Entre os exemplos estão a palavra “corrente” em relatos de transmissão mecânica, cabos de sustentação e falhas mecânicas em componentes cuja função principal é elétrica. O diagnóstico posterior identifica pontos de ambiguidade ou fronteira disciplinar para investigação. As classificações e os textos originais foram mantidos no cálculo oficial.

### 6.3. Resultados por classe e grupo técnico

| Classe revisada | Relatos | Divergências com Teacher | Student de acordo com revisão |
|---|---:|---:|---:|
| ELETRICA | 1.024 | 46 | 982 — 95,8984% |
| MECANICA | 1.024 | 112 | 910 — 88,8672% |

A maior parte das divergências ocorreu nos relatos mecânicos. A decomposição por grupo localiza essa diferença com maior detalhe.

| Grupo técnico — 256 relatos por grupo | Divergências com Teacher | Concordância Teacher–Student |
|---|---:|---:|
| Acionamentos e eletrônica de potência | 7 | 97,2656% |
| Motores, geradores e ligações | 9 | 96,4844% |
| Distribuição, proteção e aterramento | 14 | 94,5313% |
| Transmissões, eixos e mancais | 14 | 94,5313% |
| Comando, instrumentação e sensores | 16 | 93,7500% |
| Bombas, tubulações e válvulas | 30 | 88,2813% |
| Hidráulica e pneumática | 31 | 87,8906% |
| Transportadores, estruturas e mecanismos | 37 | 85,5469% |

Esses resultados são diagnósticos descritivos do censo. O certificado primário controla a divergência global; não estabelece limites de 10% para cada subgrupo.

### 6.4. Redações da mesma situação

Das 1.024 famílias cadastradas, 890 não apresentaram divergência com o Teacher, 110 apresentaram uma e 24 apresentaram divergência nas duas redações. O Student mudou de resposta entre as redações A/B em 106 famílias; o Teacher mudou de rótulo em dez.

Essa comparação examina sensibilidade à formulação de entradas semanticamente relacionadas. Como A e B são textos diferentes, ela se distingue do diagnóstico de repetição de uma mesma consulta.

## 7. Evidências auxiliares de desenvolvimento e validação

### 7.1. Desenvolvimento e escala do Student

Em um benchmark anterior de 128 relatos, a comparação na mesma tabela encontrou 64 acertos normalizados para o modelo original de 0,5B, 90 para seu primeiro adapter e 103 para o adapter v2. O Student de 1,5B ajustado alcançou 124 acertos, enquanto sua versão original alcançou 76. Essa comparação de escala é exploratória, pois o benchmark já havia sido inspecionado.

Uma auditoria posterior em uma população de 256 relatos utilizou o adapter de 1,5B congelado. A amostra de 128 apresentou 12 divergências e limite superior de 12,8906%; o censo encontrou 17/256, ou 6,6406%. Essa experiência motivou estudar a relação entre tamanho amostral e precisão do certificado e fundamentou a preparação da auditoria ampliada.

Esses resultados anteriores explicam a seleção do sistema e do desenho. As diferentes populações não devem ser tratadas como uma série homogênea de desempenho: a evidência principal deste manuscrito é a auditoria ampliada, com população e meta próprias.

### 7.2. Estabilidade observada do Teacher

Um diagnóstico anterior utilizou 32 entradas fixas, de 27 famílias, em cinco novas rodadas: 160 respostas. Nenhuma apresentou mudança de texto ou rótulo entre as repetições, e todas coincidiram com as respectivas respostas históricas. Os metadados continham 34 fingerprints distintos.

Se as 160 comparações com as respostas históricas fossem ensaios Bernoulli independentes com probabilidade comum q de mudança, zero eventos produziriam o limite unilateral de 95% \(q_U=1-0,05^{1/160}=1,8549\%\). Esse é um cálculo condicional ilustrativo. As chamadas repetem entradas e compartilham infraestrutura e tempo; o experimento não estabelece a independência nem a probabilidade comum exigidas para tratá-lo como um limite empírico geral do serviço. Os 320 pares formados dentro das entradas também não são ensaios independentes. O escopo observado permanece restrito às 32 entradas e às ocasiões consultadas.

Esse resultado sustenta estabilidade observada de classificação nessas condições e entradas. A recontagem diretamente dos 2.048 arquivos de resposta da auditoria ampliada identificou **36 fingerprints distintos**, sem campos ausentes; esse número não foi importado da auditoria de 256 relatos. Os 36 aparecem tanto na amostra como no complemento. O Apêndice C apresenta contagens e divergências por fingerprint e etapa.

| Etapa e dia UTC das chamadas bem-sucedidas | Respostas | Divergências Teacher–Student | Taxa |
|---|---:|---:|---:|
| Amostra — 30/10/2026 | 768 | 64 | 8,3333% |
| Complemento — 30/10/2026 | 636 | 50 | 7,8616% |
| Complemento — 01/11/2026 | 644 | 44 | 6,8323% |
| Complemento — total | 1.280 | 94 | 7,3438% |

Os inícios de chamadas da amostra vão de 30/10, 08:24:22 a 09:09:36 UTC; no complemento, de 30/10, 19:10:57 a 01/11, 00:46:25 UTC. Datas UTC são usadas para reproduzir os registros, incluindo chamadas de 31/10 no horário de Brasília.

Essas tabulações são diagnósticos posteriores, sem novas consultas. O fingerprint não foi atribuído aleatoriamente, e os textos diferem entre etapas e períodos. Portanto, diferenças de taxa não identificam causalmente mudança do Teacher, nem a proximidade das taxas demonstra estabilidade. A variação do fingerprint também não determina a quantidade de modelos ou revisões de pesos. O diagnóstico repetido anterior não mede a estabilidade de cada uma das 2.048 entradas durante todo o intervalo de coleta.

### 7.2.1. Diagnósticos posteriores de heterogeneidade

A tabela fingerprint × divergência do censo produz χ² de Pearson = 28,5528, com 35 graus de liberdade e p assintótico = 0,7712. Como 17 das 72 células esperadas são menores que cinco, calculamos também uma permutação condicional: fixamos os tamanhos dos 36 grupos e o total de 158 divergências e redistribuímos os indicadores sob uma hipótese de permutabilidade. Foram 100.000 redistribuições, gerador NumPy `default_rng`, semente 20261031, estatística de Pearson e cauda superior com empates. A estimativa corrigida por uma unidade, (b + 1)/(B + 1), foi p = 0,7726, com erro-padrão Monte Carlo aproximado de 0,0013.

| Comparação posterior | Teste | Resultado |
|---|---|---:|
| 36 fingerprints × divergência | Pearson, 35 gl | χ² = 28,5528; p = 0,7712 |
| Mesma tabela, margens fixas | Permutação Monte Carlo | p = 0,7726 |
| Amostra × complemento | Fisher bilateral | p = 0,4416 |
| Amostra × complemento | Pearson sem correção, 1 gl | p = 0,4165 |
| Três janelas: amostra de 30/10 e complementos de 30/10 e 01/11, em UTC | Pearson, 2 gl | χ² = 1,1364; p = 0,5665 |

Não se detectou evidência de heterogeneidade de taxas nesses diagnósticos. Isso não é um teste de equivalência nem uma demonstração de estabilidade. O poder não foi dimensionado, os textos e as famílias diferem entre grupos e a permutabilidade dos indicadores é uma hipótese auxiliar, não assegurada pelo roteamento da API. A correlação entre variantes de uma família também não é removida por esses testes. Os valores-p são exploratórios, sem controle conjunto de múltiplas comparações, e não modificam o certificado primário.

Todos os 36 fingerprints aparecem na coleta primária de 45 min 15 s, com pelo menos seis respostas por fingerprint. Os intervalos entre primeira e última ocorrência se sobrepõem: a mais tardia primeira ocorrência foi às 08:39:52 UTC e a mais precoce última ocorrência às 08:57:28 UTC. Essa intercalação é compatível com roteamento por uma frota de réplicas ou configurações coexistentes, mas não identifica a arquitetura ou revisões de pesos sem informação do provedor. Uma sucessão simples de versões em blocos temporais exclusivos não descreve o padrão registrado.

A aquisição das referências do certificado primário concentrou-se nessa janela curta; o censo se estendeu por aproximadamente 29 h 36 min. A exposição primária a mudanças temporais é, assim, menor, mas o alvo continua sendo a população completa de 2.048 entradas sob a referência especificada, não apenas os itens ou instantes consultados. O intervalo curto favorece operacionalmente a hipótese de referência estável sem demonstrá-la; estender a interpretação para todo o período do censo requer cuidado adicional.

### 7.3. Validação dos cálculos e do sorteador

No estudo anterior com \(N=256\) e \(n=128\), a enumeração dos 257 totais possíveis encontrou cobertura mínima de 95,0069%, com \(\delta=0,05\). A bateria de verificação do sorteador reuniu 47 verificações aprovadas, incluindo testes de rejeição e uma população pequena com 120 permutações.

Para a auditoria ampliada, a revisão dos artefatos reproduziu a amostra real e calculou por enumeração dos totais candidatos o limite \(200/2.048\), concordando com a implementação registrada. Os testes numéricos conferem a aplicação das regras; sua função é complementar a justificativa estatística e a conferência da execução.

## 8. Discussão

### 8.1. O que foi alcançado

O experimento conectou uma meta definida antecipadamente a uma decisão reproduzível. O Student foi executado em equipamento pessoal, suas respostas foram comprometidas antes do sorteio e uma entrada pública de aleatoriedade determinou quais exemplos seriam consultados no Teacher. O limite calculado com 768 consultas atendeu à meta de 10%, e o censo posterior forneceu uma referência completa para examinar o resultado.

A redução da necessidade de consultas é particularmente relevante quando o Student processa uma tabela extensa e as classificações de referência precisam ser adquiridas. Neste experimento, porém, todos os relatos já possuíam rótulos revisados: medir a concordância Student–revisão custaria zero novas consultas à API. A geração e revisão desses rótulos exigiram trabalho humano, que não foi quantificado em horas ou custo monetário. A redução reportada compara aquisição amostral e censitária de respostas do Teacher; não demonstra superioridade econômica sobre um gabarito humano já disponível.

Essa distinção também é quantitativa. Para a tabela censitária observada, sejam \(p_{ST}\), \(p_{SY}\) e \(p_{TY}\) as divergências Student–Teacher, Student–revisão e Teacher–revisão. A desigualdade triangular fornece \(|p_{ST}-p_{SY}|\le p_{TY}\). Obtivemos \(p_{SY}=156/2.048=7,6172\%\), \(p_{ST}=158/2.048=7,7148\%\) e \(p_{TY}=12/2.048=0,5859\%\). O gabarito permite conhecer a primeira taxa sem API, mas substituí-la pela segunda requer informação sobre a relação Teacher–revisão; a proximidade entre elas foi medida com as consultas.

Em aplicações sem gabarito completo, a auditoria pode reduzir consultas à referência, enquanto uma subamostra com revisão humana independente é necessária para avaliar correção técnica e viés compartilhado, caso se pretendam essas afirmações. Essa avaliação humana complementar tem seu próprio desenho, incerteza e custo. A garantia de fidelidade ao Teacher, isoladamente, não exige nem fornece uma garantia de correção.

### 8.2. Dimensão econômica

Como referência de dimensionamento, a margem unilateral de Hoeffding requer \(n\ge\ln(1/\delta)/(2\varepsilon^2)\). Para margem aditiva de cinco pontos percentuais e \(\delta=0,05\), o valor arredondado é 600 consultas, sem dependência explícita de \(N\). Essa é uma referência de precisão, não o tamanho automaticamente suficiente para certificar qualquer meta de divergência.

A decisão \(U\le10\%\) depende também da taxa real e do número observado de divergências. A auditoria ampliada foi dimensionada para essa decisão específica e incorporou o tamanho finito da população pela distribuição hipergeométrica. O esforço empírico foi medido em consultas e tokens; uma análise econômica de implantação deve incorporar também o custo do Student, sua execução local e as condições de uso da API.

### 8.3. Referência externa e validade do certificado

A inferência para uma tabela finita fixa é clara quando todos os rótulos de referência são determinados antes da amostragem ou definidos por uma função estável. Aqui, o Teacher foi consultado depois do sorteio, e o complemento foi obtido posteriormente. O alias da API e temperatura zero não estabelecem, por si, uma função determinística imutável.

A interpretação formal do certificado é, portanto, condicional à referência estável ou a um mecanismo de respostas potenciais independente do desenho amostral. Os registros brutos e o teste de estabilidade dão suporte empírico a essa interpretação. Uma mudança da referência associada ao tempo, à ordem de consulta ou à seleção dos itens exigiria outra modelagem estatística.

Para uma referência estocástica, outro alvo possível é \(\bar q=N^{-1}\sum_i\Pr\{s_i\ne T(x_i)\}\), a divergência esperada sobre chamadas, e não o total K de uma única tabela realizada. Condicionar a resultados potenciais pré-gerados e independentes do sorteio pode justificar inferência sobre a tabela realizada, mas não transfere automaticamente o mesmo limite para \(\bar q\). A inversão hipergeométrica aplicada nesta auditoria não estabelece essa segunda garantia.

Limites de concentração para esse alvo exigem explicitar e demonstrar as condições sobre seleção, independência entre chamadas, heterogeneidade por entrada e variação temporal. Uma correção de população finita que zera no censo elimina incerteza de seleção dos itens, mas não elimina variabilidade de futuras chamadas. Assim, extensões do tipo Hoeffding/Serfling para o alvo esperado permanecem trabalho futuro; não assumimos que suas fórmulas se transfiram sem modificação.

Para tornar quantitativa a dependência das hipóteses, recalculamos os seguintes limites unilaterais com os mesmos n = 768, k = 64 e δ = 0,05:

| Construção | Alvo e hipótese usados nesta comparação | Limite superior | Atinge 10%? |
|---|---|---:|---:|
| Hipergeométrica exata | Fração da tabela fixa; amostra uniforme sem reposição | 9,7656% | Sim |
| Binomial exata, Clopper–Pearson | Probabilidade q de divergência em ensaios Bernoulli iid | 10,1608% | Não |
| Chernoff–KL | Probabilidade q no mesmo modelo iid | 10,9906% | Não |
| Hoeffding | Probabilidade q no mesmo modelo iid | 12,7496% | Não |

As três últimas linhas são referências sob um modelo homogêneo iid explícito, não novos certificados para o serviço real nem limites já demonstrados para a média heterogênea \(\bar q\). As fórmulas e justificativas nesse modelo estão no Apêndice D. A primeira linha é o resultado primário registrado; as demais foram calculadas depois do censo como análise de sensibilidade à interpretação.

A aprovação obtida depende do alvo de tabela fixa e do desenho sem reposição que justificam a primeira linha. Nesta comparação iid, nenhum dos três limites para a probabilidade de divergência fica abaixo de 10%. Isso não demonstra que todo Teacher estocástico necessariamente reprovaria a meta, nem que o binomial domine os demais desenhos: diferentes modelos, dependências ou procedimentos podem gerar outros limites. A extensão a probabilidades por entrada, réplicas e variação temporal continua exigindo demonstração própria.

Uma evolução do protocolo pode usar referência local com pesos e condições de execução identificados, uma tabela de referência comprometida por outra parte antes do sorteio, ou um desenho que modele explicitamente a aleatoriedade do serviço. O monitoramento distribucional sugerido por Model Equality Testing [10] é uma alternativa de diagnóstico adicional. A escolha deve acompanhar o objeto a certificar: fidelidade a uma referência fixa ou comportamento médio de um serviço variável.

### 8.4. Escopo e expansão

Os resultados se referem a relatos construídos e revisados em uma classificação binária. A elaboração assistida por IA dos textos, a proposta inicial de rótulos e o uso de outro modelo como Teacher podem compartilhar convenções de linguagem ou marcas de geração que favoreçam concordância. A revisão humana registrada melhora a rastreabilidade técnica, mas não exclui viés compartilhado; não houve validação cega por avaliadores independentes nem mensuração desse efeito. Uma avaliação de implantação deve incorporar dados operacionais coletados por um desenho adequado, casos ambíguos, outras especialidades e revisão técnica independente. A repetição com novas populações e sementes de ajuste permitiria separar variação de dados, de treinamento e de serviço.

A possibilidade de diferentes partes compartilharem população, compromisso, regra de sorteio e regra de decisão constitui uma base técnica para acordos de avaliação de IA. Essa perspectiva motiva o projeto. Sua avaliação institucional exige pesquisa adicional sobre governança, participação dos avaliadores e autenticação da origem dos resultados.

## 9. Reprodutibilidade e disponibilidade dos artefatos

O pacote de revisão contém a população e sua proveniência, aprovações e emendas, configurações, código registrado, 2.048 registros do Student, 2.048 respostas do Teacher, histórico de interrupções, beacon, amostra, certificados e diagnósticos. O adapter está incluído; os pesos base são identificados por modelo e revisão e não foram duplicados.

A reprodução documental consiste em verificar o inventário, reconstruir a permutação a partir do beacon, conferir a associação dos IDs aos pedidos e respostas, recomputar os indicadores de divergência e inverter a distribuição hipergeométrica. Essa reprodução dispensa novas consultas à API. Reexecutar os modelos constitui um procedimento distinto, sujeito ao ambiente e à disponibilidade da referência externa.

O pacote foi compartilhado privadamente para revisão. Um endereço público persistente, as condições de redistribuição e o ambiente instalável devem integrar a preparação da versão de submissão. Os identificadores completos dos artefatos principais estão no Apêndice A.

## 10. Conclusão

Demonstramos uma auditoria de fidelidade Teacher–Student que integra compromisso de respostas, aleatoriedade pública e inferência em população finita. Em uma população de 2.048 relatos, 768 consultas ao Teacher produziram limite superior unilateral de 9,7656%, atendendo à meta predefinida de 10% sob as hipóteses do protocolo. O censo posterior mediu divergência de 7,7148% e permitiu conferir a decisão e localizar os principais grupos de divergência.

O resultado estabelece uma demonstração reproduzível de como converter concordância entre modelos em uma decisão de auditoria documentada. A próxima etapa é testar o protocolo em novas populações operacionais e fortalecer a identificação da referência e a publicação verificável dos compromissos, preservando a separação entre fidelidade, qualidade técnica e integridade da execução.

## Declaração de uso de assistência de IA

Houve uso de assistência de IA no planejamento, na elaboração de scripts e relatos, na análise dos artefatos e na redação. O pesquisador responsável revisou e aprovou as situações técnicas e executou os experimentos em seu equipamento. A responsabilidade pela verificação e pelas afirmações da versão submetida deve permanecer com os autores humanos. A versão final deverá identificar as ferramentas de assistência utilizadas conforme as regras do destino de publicação.

## Referências

[1] Hinton, G.; Vinyals, O.; Dean, J. **Distilling the Knowledge in a Neural Network.** 2015. https://arxiv.org/abs/1503.02531.

[2] Hu, E. J. et al. **LoRA: Low-Rank Adaptation of Large Language Models.** 2021. https://arxiv.org/abs/2106.09685.

[3] Qwen Team. **Qwen2.5 Technical Report.** arXiv:2412.15115, disponibilizado em 2024. https://arxiv.org/abs/2412.15115.

[4] Bardenet, R.; Maillard, O.-A. **Concentration inequalities for sampling without replacement.** Bernoulli, 21(3), 1361–1385, 2015. https://arxiv.org/abs/1309.4029. DOI: 10.3150/14-BEJ605.

[5] Angelopoulos, A. N.; Bates, S.; Fannjiang, C.; Jordan, M. I.; Zrnic, T. **Prediction-powered inference.** Science, 382(6671), 669–674, 2023. DOI: https://doi.org/10.1126/science.adi6000. Preprint: https://arxiv.org/abs/2301.09633.

[6] Fisch, A.; Maynez, J.; Hofer, R. A.; Dhingra, B.; Globerson, A.; Cohen, W. W. **Stratified Prediction-Powered Inference for Effective Hybrid Evaluation of Language Models.** Advances in Neural Information Processing Systems, 37, 2024. https://papers.nips.cc/paper_files/paper/2024/hash/c9fcd02e6445c7dfbad6986abee53d0d-Abstract-Conference.html.

[7] Angelopoulos, A. N.; Bates, S.; Fisch, A.; Lei, L.; Schuster, T. **Conformal Risk Control.** ICLR, 2024; preprint de 2022. https://arxiv.org/abs/2208.02814.

[8] drand. **Protocol Specification.** Documentação técnica. https://docs.drand.love/docs/specification/. Consultada em 31 de outubro de 2026 (horário de Brasília).

[9] drand. **Cryptography.** Documentação técnica. https://drand.love/docs/cryptography/. Consultada em 31 de outubro de 2026 (horário de Brasília).

[10] Gao, I.; Liang, P.; Guestrin, C. **Model Equality Testing: Which Model is this API Serving?** ICLR, 2025. https://proceedings.iclr.cc/paper_files/paper/2025/hash/d73234a13815fc1f9779dd17d89be9b4-Abstract-Conference.html. Preprint: https://arxiv.org/abs/2410.20247.

[11] Lindeman, M.; Stark, P. B. **A Gentle Introduction to Risk-Limiting Audits.** IEEE Security & Privacy, 10(5), 42–49, 2012. Versão dos autores: https://www.stat.berkeley.edu/~stark/Preprints/gentle12.pdf.

[12] Stark, P. B. **CAST: Canvass Audits by Sampling and Testing.** IEEE Transactions on Information Forensics and Security, 4(4), 708–717, 2009. Versão do autor: https://www.stat.berkeley.edu/~stark/Preprints/cast09.pdf.

[13] Stark, P. B. **ALPHA: Audit that Learns from Previously Hand-Audited Ballots.** Annals of Applied Statistics, 17(1), 641–679, 2023. DOI: https://doi.org/10.1214/22-AOAS1646. Preprint: https://arxiv.org/abs/2201.02707.

[14] Waudby-Smith, I.; Ramdas, A. **Confidence sequences for sampling without replacement.** Advances in Neural Information Processing Systems, 33, 2020. https://proceedings.neurips.cc/paper/2020/hash/e96c7de8f6390b1e6c71556e4e0a4959-Abstract.html.

[15] NIST. **Interoperable Randomness Beacons — Applications.** Documentação institucional. https://csrc.nist.gov/projects/interoperable-randomness-beacons/apps. Consultada em 31/10/2026, horário de Brasília.

[16] Waiwitlikhit, S.; Stoica, I.; Sun, Y.; Hashimoto, T.; Kang, D. **Trustless Audits without Revealing Data or Models.** Proceedings of the 41st International Conference on Machine Learning, PMLR 235, 49808–49821, 2024. https://proceedings.mlr.press/v235/waiwitlikhit24a.html. Preprint: https://arxiv.org/abs/2404.04500.

[17] Lim, Y.; Yong, S. **Seal, Then Sample: Sampled Layerwise Proofs for Verifiable LLM Inference from GPT-2 to 70B.** Preprint, 2026. https://arxiv.org/abs/2609.27367.

[18] Clopper, C. J.; Pearson, E. S. **The Use of Confidence or Fiducial Limits Illustrated in the Case of the Binomial.** Biometrika, 26(4), 404–413, 1934. https://doi.org/10.1093/biomet/26.4.404.

[19] Hoeffding, W. **Probability Inequalities for Sums of Bounded Random Variables.** Journal of the American Statistical Association, 58(301), 13–30, 1963. https://doi.org/10.1080/01621459.1963.10500830.

## Apêndice A. Identificadores dos artefatos

Os valores abaixo são SHA256 dos bytes dos arquivos arquivados.

```text
population.json
719f66a571b90bd2cb7429d859b391ca0b66bc177e5c56c63d85f8aab8dd52f3

execution_settings.json
7eee96fd3fba6a6d740ce24a1be85775508ef938a15a8df6d889b425d819c738

student_table.json
d8e79ce6f2bc3586cb08f7e76e18f10c033f484ec863cabbd2047d285d2ff3cf

pre_beacon_commitment.json
da33afecc5fad0bc2edbf1beaf72dba9484965030acbcf776819da8f29e4f5c2

beacon_plan.json
ea9bd5b0cedf25c9ede26b4b579b47d45f6f7670c56afb8d13df42bb173dcf38

sample.json
b8844711818b2c3e59f11f61c437275f976c58532540ba576ed8cf3a347b9ae2

primary_certificate.json
e18b66541f302f55050439715364286e60557eb2fecefd57ef0f51e2b380b831

full_reference.json
d7f8d919f35a1486ef0fcc7a4a109e627b20b01cb5439b8ad180f33fcae66eff

adapter_model.safetensors
445fd312e4fa6d6363b93ca20626b32fc1416a4466b8265f0c4f40e695641cf5

Pacote completo de revisão recebido
92a6fcedc7561c78e9159c50a2709862d0b2b86e22c25c466ece38bb49b4c2a4
```

## Apêndice B. Estado editorial desta versão

O corpo do artigo constitui uma redação científica em português, revisada na versão 0.3 após conferência adicional de diagnósticos de heterogeneidade, interpretação estocástica, ameaças e literatura. Antes da submissão, a revisão editorial deverá confirmar a forma do nome do autor, afiliação e contato, completar os metadados bibliográficos, ampliar a busca de trabalhos diretamente próximos e preparar a versão em inglês no formato escolhido. A descrição atual não afirma prioridade histórica ou revisão sistemática da literatura.

As ações de pesquisa prioritárias são a formalização do tratamento da referência externa, a repetição em dados operacionais e a disponibilização de um ambiente de reprodução. Nenhuma delas deve ser descrita como concluída com base apenas neste manuscrito. O Student e as populações já avaliadas devem permanecer preservados; eventuais ajustes futuros exigem novas avaliações claramente identificadas.

### Convenção de datas e histórico editorial

As datas editoriais seguem `America/Sao_Paulo` (Brasília, UTC−03:00 nas datas registradas). Datas de chamadas e do beacon permanecem em UTC, sempre identificadas, para correspondência com os registros brutos.

| Versão | Data editorial em Brasília | Observação |
|---|---|---|
| 0.1 | 31/10/2026 | Criada às 22:03 de Brasília, correspondendo a 01/11/2026, 01:03 UTC; o cabeçalho original utilizou a data UTC |
| 0.2 | 31/10/2026 | Revisão preservada no histórico às 22:28 de Brasília |
| 0.3 | 31/10/2026 | Adota esta convenção e registra os esclarecimentos posteriores |

A data originalmente exibida na v0.1 foi uma diferença de fuso, não inversão da ordem das versões. O arquivo histórico não foi alterado retroativamente.

## Apêndice C. Fingerprints na auditoria ampliada

Tabulação descritiva recalculada a partir do campo `response.system_fingerprint` dos 2.048 registros brutos, associando IDs à amostra registrada e às divergências do censo. n é o número de respostas; d é o número de divergências Teacher–Student. As colunas de cada etapa permitem calcular d/n. Não se interpretam taxas por fingerprint como desempenho de versões distintas ou efeito causal da infraestrutura.

| Fingerprint | n amostra | d amostra | n complemento | d complemento | d/n no censo |
|---|---:|---:|---:|---:|---:|
| `fp_228717f27c` | 8 | 1 | 5 | 0 | 7,6923% |
| `fp_3023a70d60` | 13 | 2 | 8 | 0 | 9,5238% |
| `fp_334cc21c60` | 6 | 0 | 11 | 0 | 0,0000% |
| `fp_34cb00738d` | 16 | 2 | 18 | 1 | 8,8235% |
| `fp_565badff47` | 31 | 3 | 50 | 7 | 12,3457% |
| `fp_5979a0e1b7` | 32 | 2 | 51 | 1 | 3,6145% |
| `fp_63473661d7` | 23 | 1 | 16 | 2 | 7,6923% |
| `fp_75c733514d` | 23 | 1 | 54 | 5 | 7,7922% |
| `fp_80501ff3a1` | 29 | 2 | 36 | 3 | 7,6923% |
| `fp_816fc87d18` | 22 | 3 | 66 | 7 | 11,3636% |
| `fp_84bb35977d` | 8 | 0 | 11 | 1 | 5,2632% |
| `fp_8b41efc9a3` | 24 | 0 | 45 | 6 | 8,6957% |
| `fp_8d13edce1d` | 22 | 4 | 37 | 2 | 10,1695% |
| `fp_92d51d08e5` | 9 | 0 | 14 | 1 | 4,3478% |
| `fp_9340e7d14d` | 31 | 3 | 34 | 3 | 9,2308% |
| `fp_976a85d17a` | 15 | 2 | 13 | 1 | 10,7143% |
| `fp_996f667773` | 12 | 1 | 13 | 0 | 4,0000% |
| `fp_9b8528b477` | 35 | 3 | 49 | 3 | 7,1429% |
| `fp_a12402de73` | 21 | 2 | 43 | 5 | 10,9375% |
| `fp_a4315eb300` | 31 | 0 | 39 | 2 | 2,8571% |
| `fp_a8c584dda7` | 26 | 2 | 50 | 5 | 9,2105% |
| `fp_bb6a356524` | 27 | 1 | 49 | 3 | 5,2632% |
| `fp_c5a89987dc` | 19 | 2 | 52 | 3 | 7,0423% |
| `fp_ce54c53bd5` | 34 | 2 | 43 | 2 | 5,1948% |
| `fp_d23c14756c` | 19 | 2 | 55 | 3 | 6,7568% |
| `fp_d3e146e1a5` | 28 | 1 | 37 | 3 | 6,1538% |
| `fp_d6de37e6be` | 9 | 1 | 19 | 4 | 17,8571% |
| `fp_e11c8bbf69` | 14 | 1 | 40 | 2 | 5,5556% |
| `fp_e189667b30` | 34 | 6 | 48 | 5 | 13,4146% |
| `fp_e23fc997ca` | 25 | 3 | 55 | 5 | 10,0000% |
| `fp_e2cb7a84ec` | 7 | 1 | 11 | 1 | 11,1111% |
| `fp_e99e93f2ac` | 23 | 2 | 37 | 3 | 8,3333% |
| `fp_ed70b23331` | 13 | 2 | 43 | 3 | 8,9286% |
| `fp_ef00694abe` | 24 | 2 | 39 | 0 | 3,1746% |
| `fp_f102a3179c` | 29 | 1 | 45 | 2 | 4,0541% |
| `fp_feb9b278f1` | 26 | 3 | 44 | 0 | 4,2857% |
| **Total** | **768** | **64** | **1.280** | **94** | **7,7148%** |


## Apêndice D. Comparação ilustrativa sob modelo binomial iid

Considere \(Z_1,\ldots,Z_n\) independentes, com \(Z_j\sim\operatorname{Bernoulli}(q)\), e \(X=\sum_j Z_j\). A probabilidade q é comum a todos os ensaios, estacionária e não depende da seleção ou ordem das entradas. Esse modelo é mais específico que um serviço com probabilidades de resposta heterogêneas e dependência temporal.

**Binomial exato.** A inversão unilateral de Clopper–Pearson [18] encontra \(q_U\) tal que \(\Pr_{q_U}\{X\le k\}=\delta\). Para \(k<n\), o valor é o quantil \(1-\delta\) da distribuição Beta(k + 1, n − k). A monotonicidade da CDF em q e a validade do teste de cauda inferior garantem cobertura de pelo menos 95% nesse modelo. Para k = 64 e n = 768, \(q_U=0,1016076404\).

**Chernoff–KL.** Para \(a=k/n<q\), a função geradora de momentos binomial e a desigualdade de Markov, otimizadas sobre parâmetro negativo, fornecem \(\Pr_q(X/n\le a)\le\exp[-n\,\operatorname{kl}(a,q)]\), onde

\[
\operatorname{kl}(a,q)=a\log(a/q)+(1-a)\log[(1-a)/(1-q)].
\]

Invertendo \(n\,\operatorname{kl}(a,q_U)=\log(1/\delta)\) no ramo \(q_U>a\), obtemos \(q_U=0,1099060144\). A rejeição baseada nessa cauda tem probabilidade de erro no máximo δ sob o modelo indicado.

**Hoeffding.** A desigualdade unilateral para variáveis independentes em [0,1] [19] fornece \(\Pr_q(q-X/n\ge\varepsilon)\le\exp(-2n\varepsilon^2)\). Logo,

\[
q_U=\min\{1,\,k/n+\sqrt{\log(1/\delta)/(2n)}\}=0,1274960612.
\]

Essas justificativas valem para o modelo iid aqui definido. A transferência do limite binomial para amostragem sem reposição de entradas com probabilidades diferentes exigiria uma desigualdade de cauda na direção e faixa corretas; uma ordem de momentos ou convexidade, isoladamente, não demonstra dominância de todas as caudas. O manuscrito não afirma essa transferência. O tratamento de \(\bar q\) com heterogeneidade ou dependência permanece separado do resultado primário e desta ilustração.
