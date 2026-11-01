---
title: "Commitment-Based Teacher-Student Fidelity Auditing with Public Randomness and Finite-Population Certification"
author: |
  Antonio Rufino  
  Independent Researcher, Brazil  
  ORCID: 0009-0004-1767-8165
date: "Version audit-large-v1.0.0 / 31 October 2026 (Brasília)"
abstract: |
  Deploying compact models trained on reference-model responses calls for a verifiable assessment of behavioral fidelity without querying the reference on every input. We implement an audit combining SHA256 commitments to a finite input population and the Student's outputs, a future public-randomness beacon, and an upper confidence bound obtained by exact hypergeometric inversion. We study binary classification of Portuguese industrial-maintenance reports into electrical and mechanical specialties. A LoRA-adapted Qwen2.5-1.5B-Instruct Student ran locally on a CPU and committed 2,048 responses before sampling. The prespecified primary sample of 768 reports contained 64 disagreements with an API-served Teacher. Its one-sided upper bound was 9.7656%, meeting the declared 10% target at nominal 95% confidence under a fixed disagreement table and uniform sampling without replacement. A subsequent census found 158 disagreements, or 7.7148%. The primary stage used 37.5% of census queries and 37.6653% of reported census tokens; the complement was actually queried for validation. Human-reviewed labels already existed for all inputs, so this comparison concerns acquiring Teacher responses rather than evaluation against an existing answer key. We provide a documentary-replay package that reconstructs the sample and calculations without model inference or API access. The contribution is an operational, reproducible integration of established tools, with explicit separation of record integrity, sampling validity, and reference stability.
---

**Keywords:** model auditing; behavioral fidelity; response-based distillation; sampling without replacement; hypergeometric confidence bound; randomness beacon; reproducibility.

# Introduction

A compact language model can be adapted to a restricted task using responses produced by a larger reference model. Local deployment then raises an evaluation question: how often does the deployed Student disagree with the Teacher on the inputs it is meant to process? A sample agreement score alone does not specify the population, rule out favorable sample selection, or establish which outputs were evaluated.

This study asks an operational question: **can a prespecified audit of 768 Teacher queries certify a disagreement rate of at most 10% in a committed population of 2,048 reports?** The primary upper bound was 9.7656%, satisfying that rule under the stated fixed-table assumptions. A later census measured 7.7148% disagreement.

The protocol first fixes the input population, selected Student adapter, execution settings, analysis, and Student response table. A reserved future drand round then supplies the randomness for a reproducible sample. Teacher queries on that sample produce the primary certificate. Only after preserving that certificate is the complement evaluated. This sequence links statistical evaluation to a specific set of records rather than to an informally selected demonstration.

Our contribution is a reproducible engineering case study: a complete implementation, a constructed and technically reviewed maintenance benchmark, a prespecified decision, and a census-based examination of the outcome. We do not introduce hypergeometric inversion, public randomness, or cryptographic commitments. We examine how these established elements work together when the reference is an external API, while distinguishing fidelity from technical correctness and identifying the conditions needed for a stronger deployment claim.

# Related work

## Distillation and efficient adaptation

Knowledge distillation transfers behavior from a reference system to a more compact model [1]. Our Student learns textual class labels produced by the Teacher, using a response-token training loss without access to Teacher logits. We use the term *response-based distillation*, recognizing its proximity to supervised fine-tuning on synthetic labels. LoRA [2] updates low-rank matrices while keeping base weights frozen. The Students belong to the Qwen2.5 family [3].

## Statistical evaluation and finite populations

Sampling without replacement supports inference about a fixed population without observing every item. Serfling-type inequalities and subsequent refinements address this setting [4]. For a binary attribute and a known population size, hypergeometric inversion directly incorporates the finite population into a one-sided confidence bound.

Prediction-powered inference combines expensive labeled observations with abundant predictions [5], and stratified variants address language-model evaluation [6]. Our estimand is the fraction of disagreements between a Student and its reference on a committed finite population. We do not implement a prediction-powered correction estimator. Conformal risk control [7] concerns controlling expected losses of calibrated rules; the fixed-size finite-total confidence procedure used here has a different target and guarantee.

Risk-limiting election audits are important antecedents for combining a documented population, random sampling, and a prespecified maximum risk. Lindeman and Stark [11] describe the principle, CAST [12] organizes sampling and testing in stages, and ALPHA [13] accommodates several designs, including sampling without replacement. Our decision can likewise be expressed as testing an unacceptable population total. Unlike election auditing, our target is classifier disagreement, and our census was a planned complementary validation rather than an escalation triggered by a failed primary audit.

Waudby-Smith and Ramdas [14] provide confidence sequences for sampling without replacement, with simultaneous coverage throughout collection. They are a natural foundation for a future data-dependent stopping rule. Repeatedly recomputing the present fixed-size confidence bound would not supply that sequential guarantee.

## Reference identity and verifiable randomness

Model Equality Testing [10] compares the output distribution served by an API with a reference distribution. This is directly relevant to identifying an external Teacher: a model alias does not pin the served weights or distribution. Our repeated-query diagnostic examines label stability and does not implement that distributional equality test.

The NIST describes upfront commitment to a deterministic operation followed by a future beacon value as a generic publicly verifiable randomization procedure, including audit sampling [15]. Drand supplies publicly verifiable randomness using threshold signatures [8,9]. ZkAudit [16] combines commitments with zero-knowledge proofs to audit private model and data properties; those execution and privacy guarantees are not implemented here. *Seal, Then Sample* [17] discusses sampled inference proofs and a grinding attack in its own challenge construction. These works inform the threat model and delimit the present contribution as an integration study rather than a new cryptographic protocol.

# Statistical target and primary decision

## Fixed-table estimand

Let $x_1,\ldots,x_N$ be the ordered input population. Let $s_i$ be the committed Student response and $t_i$ the reference label associated with input $i$ under the specified conditions. Define

$$
D_i=\mathbf{1}\{s_i\ne t_i\},\qquad K=\sum_{i=1}^{N}D_i,\qquad p=K/N.
$$

The primary target is $p$, the fraction of disagreements in the committed population. Human-reviewed labels are evaluated separately. The statistical theorem assumes a fixed binary table and a simple random sample without replacement. For an API reference queried after selection, its application requires a stable reference or a potential-response construction independent of sampling and query order. Label stability diagnostics provide evidence relevant to that assumption but do not establish it.

## Exact one-sided inversion

For a sample of size $n$, its disagreement count satisfies

$$X\mid K\sim\operatorname{Hypergeom}(N,K,n).$$

For observed count $k$, define

$$
K_U(k)=\max\{K'\in\{0,\ldots,N\}:\Pr_{K'}(X\le k)>\delta\},
\qquad U(k)=K_U(k)/N.
$$

For $K'<k$, the point probability of $X=k$ is zero but the CDF at $k$ equals one; these totals enter the set without affecting its maximum. Search can be restricted to the compatible support $k\le K'\le N-n+k$. At $K'=k$ the CDF equals one, and above $N-n+k$ it equals zero.

**Proposition.** For any fixed table and a simple random sample without replacement,

$$\Pr_K\{K\le K_U(X)\}\ge1-\delta.$$

**Argument.** The CDF $F_{K'}(k)$ is nonincreasing in $K'$. If $K>K_U(X)$, then $F_K(X)\le\delta$. A discrete CDF evaluated at its own random variable satisfies $\Pr\{F_K(X)\le\delta\}\le\delta$. Hence the undercoverage probability is at most $\delta$. Discreteness can make coverage conservative. At a census, $n=N$, the bound equals the observed total exactly.

“Exact” refers to using the finite sampling distribution, rather than an asymptotic approximation. The implementation evaluates its CDF numerically using SciPy.

## Prespecification and available information

The design fixed $N=2,048$, $n=768$, $\delta=0.05$, and acceptance when $U\le0.10$. The integer decision is $K_U\le204$. The registered analysis accepts up to 65 sample disagreements; 66 does not pass. Equivalently, it tests $H_0:K\ge205$, with false acceptance at most 5% under the fixed-table assumptions.

The documentary sequence places selection of the sample size and target before construction of the enlarged population. Earlier experiments, including a census with 17 disagreements in 256 reports (6.6406%), were already known. The approximately 7% planning scenario was therefore informed by prior experience. It was not a prediction independent of those earlier results.

| Recorded stage | Available information |
|---|---|
| Choice of population size, sample size and target | Frozen adapter and earlier results known; enlarged population not yet constructed |
| Population freeze and Student execution | Complete texts and reviewed labels; subsequent generation of all Student outputs |
| Pre-beacon commitment | Reviewed labels and Student table available; no enlarged-population Teacher query recorded |
| After sampling | Primary Teacher responses and certificate |
| After preserving the primary result | Complementary Teacher responses and census total |

Before the beacon, Student error against the reviewed labels could have been calculated from the available tables. That is not the same as knowing Teacher-Student disagreement. The records do not capture every possible informal inspection or off-script calculation. Prespecification is supported by the preserved local sequence rather than by an independently timestamped public preregistration. The eventual 99.4141% Teacher-review agreement was a later observation.

The planning study compared hypothetical rates of 3%, 5%, 7%, and 10%. For the approximately 7% scenario, represented by $K=143$, $n=768$ gave 98.2510% probability of acceptance, versus 87.4397% for $n=512$. After the census, the same design can be characterized at $K=158$:

| Fixed total | Rate | $n=512$, cutoff 41 | $n=768$, cutoff 65 |
|---|---:|---:|---:|
| $K=143$: planning scenario | 6.9824% | 87.4397% | 98.2510% |
| $K=158$: post-census characterization | 7.7148% | 65.3156% | 85.7332% |

These are hypergeometric probabilities of meeting each fixed rule. The second row describes repeated sampling from the observed census table; it is neither a coverage estimate nor a retrospective justification for selecting $n$. Acceptance was not guaranteed. There was one primary fixed-size analysis, with no outcome-dependent extension or reselection.

![Primary fixed-table certificate and post-census characterization of the unchanged sampling rule. Panel (b) is a repeated-sampling calculation, not empirical coverage.](figures/audit_summary.pdf){width=100%}

# Models, population and execution

## Student development

Development compared Qwen2.5-0.5B-Instruct and Qwen2.5-1.5B-Instruct. The development data used for the 1.5B Student contained 96 training reports from 24 families and 32 validation reports from eight families, with four variants per family and balanced classes. The two learning rates were $5\times10^{-5}$ and $2\times10^{-4}$, each starting from the original base model. Checkpoints after epochs 1 and 3 were evaluated on validation data.

LoRA used rank 4, alpha 8, zero dropout, and the `q_proj` and `v_proj` modules, with 544,768 trainable parameters. Training used AdamW, batch size one, seed 42, CPU and FP32. The selected checkpoint was epoch 3 at learning rate $2\times10^{-4}$ and was identified by hashes before subsequent evaluation. Teacher and reviewed development labels coincided, so the study does not isolate a benefit of Teacher labels over the same labels supplied directly by humans.

## Enlarged population

The audit population contains 2,048 Portuguese maintenance reports in 1,024 registered families, with two meaning-preserving descriptions per situation. There are 1,024 electrical and 1,024 mechanical reports, divided into eight technical groups of 256 reports each. The task concerns the main repair specialty for an explicitly described fault, not discovery of an unknown root cause.

Reports and proposed labels were developed with AI assistance and reviewed by the responsible researcher. Thirty-two batches and their approvals were preserved. Two amendments refined wording and technical delimitations before freezing; original drafts remained intact. No literal duplicates remained after normalizing case and whitespace. Related components and failure mechanisms still occur across registered families. These are constructed, reviewed scenarios, not a probability sample of production maintenance. The inferential universe is the committed finite table, and no independence of technical families is required for its design-based fixed-table bound.

## Teacher queries and scoring

The Teacher was served by Groq under the alias `openai/gpt-oss-20b`, with temperature zero, at most 1,024 completion tokens, a 90-second timeout, automatic SDK retries disabled, and a three-second pause after successful responses. The Portuguese prompt requests only `ELETRICA` or `MECANICA`. Requests, raw responses and returned metadata were archived.

Teacher normalization strips outer whitespace and maps the prespecified accented spellings `ELÉTRICA` and `MECÂNICA` to their unaccented labels. Student scoring is exact after stripping outer whitespace. Generation used `do_sample=False`, at most 12 new tokens, and the identified tokenizer's chat template.

Two HTTP 429 interruptions occurred during complementary collection. Attempts and errors were preserved, and collection was explicitly resumed for items without a saved successful response. The executor and primary certificate were unchanged. The final census uses one successful Teacher response per item and retains the unsuccessful-attempt history.

## Local resources

The Student ran on a notebook with an Intel Core i7-8565U and 16 GB of physical memory, using Ubuntu under WSL2 with a 10 GB memory ceiling, four CPU threads and FP32. Base weights were pinned to revision `989aa7980e4cf806f80c7fef2b1adb7bc71aa306` of Qwen2.5-1.5B-Instruct.

Generating the 2,048 responses took 4 h 19 min 09 s. Maximum recorded resident memory was 9,465,320 KiB. This measures the particular local run. API tokens and query counts are accounted for separately and are not converted into energy or hardware-compute comparisons.

# Commitment and sampling

The operational sequence was: freeze the population and code; execute and commit every Student response; register a commitment to the artifacts; reserve a future drand round; verify its signature and draw the sample; acquire the primary Teacher responses and issue the certificate; preserve that result; then acquire the complement.

The commitment identifies exact file bytes with SHA256. It does not use a Merkle tree. The target was quicknet round 33,515,062, scheduled for 30 October 2026 at 08:22:30 UTC, 100 rounds after the observed round. The sampler hashes the experiment domain, population hash and beacon randomness to derive its seed. SHA256 blocks with a counter drive descending Fisher-Yates swaps; rejection sampling avoids modular-reduction bias. The first 768 IDs form the sample.

The statistical proof assumes uniform sampling. SHA256-based generation implements a computational idealization under cryptographic assumptions; eliminating modular bias does not make a finite seed space information-theoretically uniform over all possible permutations.

A separate, AI-assisted computational replay of the received records checked the inventory, regenerated the sample, verified BLS signatures with a wrong-round negative control, reconstructed raw-record counts and recomputed the bound. This was a documentary replay, not an external institutional audit, a rerun of the models, or authentication of the API response origin. No independent public timestamp was established for the original commitment.

## Grinding threat model

An adversary could prepare several populations or commitments, observe the beacon, and reveal only a favorable candidate. It could also choose among rounds or suppress unfavorable runs. The present seed depends on the population hash and beacon; changing either changes the sample. An archived hash does not establish that its candidate was uniquely eligible before randomness became available.

A prospective defense needs an externally ordered public record binding a defined audit identity to an eligible commitment and future round before revelation, with deadlines, amendment rules, eligibility among multiple registrations, and disclosure of outcomes and abandonments. Timestamping many candidates without a selection rule still allows later choice. Multiple identities and hidden runs require further controls. These protections were not implemented retroactively. The present evidence supports reconstruction and integrity, not a proof of resistance to grinding.

# Results

## Primary certificate and census

| Quantity | Primary sample | Complement | Census |
|---|---:|---:|---:|
| Reports queried | 768 | 1,280 | 2,048 |
| Teacher-Student disagreements | 64 | 94 | 158 |
| Observed disagreement | 8.3333% | 7.3438% | 7.7148% |
| Primary upper bound | 9.7656% | - | Census rate known |
| Reported tokens | 168,640 | 279,093 | 447,733 |

**The prespecified primary rule passed.** The observed 64 disagreements yielded $K_U=200$, or 9.765625%. The census found 158 disagreements, 42 fewer than the upper total and 2.0508 percentage points below the bound. The census was inside the bound in this realization; the procedure's confidence guarantee comes from the sampling argument, not an empirical coverage frequency estimated from one audit.

The primary stage used 37.5% of census queries and 37.6653% of reported census tokens, a 62.3347% difference in tokens. Since the complement was actually queried, the experiment consumed all 447,733 reported tokens. This is a primary-audit versus census acquisition comparison, not a claim of savings retained after completing the census.

## Fidelity and reviewed-label agreement

| Census measure | Count | Percentage |
|---|---:|---:|
| Student agrees with Teacher | 1,890/2,048 | 92.2852% |
| Student agrees with reviewed label | 1,892/2,048 | 92.3828% |
| Teacher disagrees with reviewed label | 12/2,048 | 0.5859% |
| Invalid Student label format | 0/2,048 | 0% |

Among the 12 Teacher-review disagreements, the Student matched the reviewed label in seven and the Teacher in five. Examples involve the Portuguese word *corrente*, which can denote electric current or a mechanical chain, support cables, and mechanical damage in components with an electrical function. These are post-census diagnostic observations; texts and official labels were not changed after inspection.

| Reviewed class | Reports | Disagreements with Teacher | Student agrees with review |
|---|---:|---:|---:|
| Electrical | 1,024 | 46 | 982 (95.8984%) |
| Mechanical | 1,024 | 112 | 910 (88.8672%) |

| Technical group, 256 reports each | Disagreements | Teacher-Student agreement |
|---|---:|---:|
| Drives and power electronics | 7 | 97.2656% |
| Motors, generators and connections | 9 | 96.4844% |
| Distribution, protection and grounding | 14 | 94.5313% |
| Transmissions, shafts and bearings | 14 | 94.5313% |
| Control, instrumentation and sensors | 16 | 93.7500% |
| Pumps, piping and valves | 30 | 88.2813% |
| Hydraulics and pneumatics | 31 | 87.8906% |
| Conveyors, structures and mechanisms | 37 | 85.5469% |

These census breakdowns are descriptive. The primary certificate controls global disagreement, not a 10% bound for every group. Of 1,024 families, 890 had zero Teacher-Student disagreements, 110 had one, and 24 had two. The Student changed its label between variants in 106 families, and the Teacher in ten. These are different texts describing related situations, not repeated identical queries.

# Auxiliary evidence and diagnostics

## Development context

An earlier same-table comparison on 128 reports produced 64 normalized agreements for the original 0.5B model, 90 for its first adapter and 103 for its v2 adapter. The adapted 1.5B model obtained 124, compared with 76 for its original model. The scaling comparison is exploratory because that benchmark had already been inspected.

A subsequent 256-report audit of the frozen 1.5B adapter found 12 disagreements in a primary sample of 128, yielding an upper bound of 12.8906%; its census found 17/256, or 6.6406%. That experience motivated the precision and sample-size studies. These populations should not be pooled into a homogeneous performance time series. They explain development choices; the enlarged audit is the principal experiment.

## Repeated-query diagnostic

An earlier diagnostic queried 32 fixed inputs from 27 families in five new rounds, for 160 responses. No raw-text or normalized-label change occurred, and all responses matched the corresponding historical responses. There were 34 fingerprints. If the 160 comparisons were independent Bernoulli trials with a common change probability, zero changes would imply a one-sided 95% upper bound $1-0.05^{1/160}=1.8549\%$. The repeated inputs and shared infrastructure do not establish those assumptions, so this is a conditional illustration rather than a general service guarantee. The 320 within-input pairs are not independent trials either.

Direct recounting of the enlarged audit's 2,048 raw responses found 36 distinct fingerprints, with none missing. All 36 occurred in both the primary sample and the complement; the number was not copied from the smaller audit.

| Query window, UTC | Responses | Disagreements | Rate |
|---|---:|---:|---:|
| Primary, 30 October | 768 | 64 | 8.3333% |
| Complement, 30 October | 636 | 50 | 7.8616% |
| Complement, 1 November | 644 | 44 | 6.8323% |
| Complement, combined | 1,280 | 94 | 7.3438% |

The primary successful-query window lasted 45 min 15 s, from 08:24:22 to 09:09:37 UTC on 30 October. Every fingerprint had at least six primary responses. Their occurrence intervals overlapped: the latest first occurrence was 08:39:52, and the earliest last occurrence was 08:57:28. This is compatible with routing across coexisting replicas or configurations; provider metadata does not establish that architecture or identify weight revisions. A simple sequence of temporally exclusive versions does not describe the records.

The complementary starts span 30 October, 19:10:57 to 1 November, 00:46:25 UTC. The shorter primary collection reduces temporal exposure, but its target remains the full population under the specified reference. It does not prove that reference stable across unqueried inputs or across the longer census period.

## Exploratory heterogeneity tests

The fingerprint-by-disagreement table gives Pearson $\chi^2=28.5528$, 35 degrees of freedom, and asymptotic $p=0.7712$. Seventeen of its 72 expected cells are below five. We therefore also redistributed 158 disagreement indicators across the fixed group sizes under an exchangeability null: 100,000 multivariate-hypergeometric draws, NumPy `default_rng`, seed 20261031, Pearson statistic, upper tail including ties, and $(b+1)/(B+1)$ correction. This gave $p=0.7726$, with approximate Monte Carlo standard error 0.0013.

| Post-hoc comparison | Test | $p$ |
|---|---|---:|
| 36 fingerprints | Pearson, 35 df | 0.7712 |
| Same table, fixed margins | Conditional Monte Carlo | 0.7726 |
| Primary versus complement | Two-sided Fisher exact | 0.4416 |
| Primary versus complement | Uncorrected Pearson, 1 df | 0.4165 |
| Three query windows | Pearson, 2 df | 0.5665 |

These diagnostics detect no rate heterogeneity, but they are not equivalence tests or proof of stability. Power was not designed; inputs and families differ among groups; routing does not ensure indicator exchangeability; family dependence remains. The exploratory tests have no joint multiplicity control and do not alter the primary decision. Full fingerprint counts are in the replay results.

## Computational checks

Earlier enumeration at $N=256,n=128$ over all 257 possible totals found minimum coverage 95.0069%; an earlier sampler suite passed 47 checks. For the enlarged audit, the documentary replay reconstructs the actual sample and independently enumerates compatible totals to obtain 200/2,048. It also enumerates the prespecified acceptance probability for all $K\ge205$, with maximum 0.0407935 at the boundary. This is a numerical check of the fixed-table decision rule, not a test of API stationarity or cryptographic provenance.

# Interpretation and scope

## What the experiment establishes

The study connects an advance decision rule to a specific committed output table and a reproducible sample, and checks its outcome against a complete census. It demonstrates local CPU execution of the Student and separates local generation from external reference acquisition.

However, every input already had a human-reviewed label. Evaluating Student agreement against that answer key would require no additional API queries. Human effort in generating and reviewing the labels was not measured. The economic comparison is acquisition of sampled versus census Teacher responses, not superiority over an existing human answer key.

For the observed census tables, let $p_{ST},p_{SY},p_{TY}$ denote Student-Teacher, Student-review, and Teacher-review disagreement. Then $|p_{ST}-p_{SY}|\le p_{TY}$. We observed $p_{SY}=156/2,048=7.6172\%$, $p_{ST}=158/2,048=7.7148\%$, and $p_{TY}=12/2,048=0.5859\%$. The reviewed labels identify the first rate without Teacher queries, not the second. Their proximity was learned through the queries.

Where a complete answer key is unavailable, sampled reference acquisition can reduce query demand. Claims about correctness and shared bias additionally require independent human assessment with its own sampling design and cost. Fidelity to the Teacher alone is not correctness.

As a scale reference, the one-sided Hoeffding margin requires $n\ge\log(1/\delta)/(2\varepsilon^2)$; a five-percentage-point margin at $\delta=0.05$ gives 600 queries after rounding. This is a precision benchmark, not a universally sufficient sample for passing a 10% threshold. Acceptance also depends on the underlying rate and observed count. Deployment economics must include Student generation and service conditions, not only Teacher tokens.

## Fixed realization versus stochastic reference

An alias and temperature zero do not establish an immutable deterministic function. Here the Teacher was queried after sampling and the complement later. The primary confidence interpretation is conditional on a stable per-input reference or a potential-response table independent of selection and order. An API change associated with time or routing can require a different model.

A distinct stochastic target is

$$\bar q=\frac1N\sum_{i=1}^N\Pr\{s_i\ne T(x_i)\},$$

the mean disagreement probability over repeated calls under specified service conditions. A fixed realization of all potential responses can support inference about that realization; it does not automatically give the same bound for $\bar q$.

To show sensitivity to interpretation, we computed the following post-hoc references for the same $n=768,k=64,\delta=0.05$:

| Construction | Target and assumptions in this comparison | Upper bound |
|---|---|---:|
| Exact hypergeometric | Fixed table, uniform sampling without replacement | 9.7656% |
| Exact binomial (Clopper-Pearson) | Common probability $q$, iid Bernoulli trials | 10.1608% |
| Chernoff-KL | Same iid target | 10.9906% |
| Hoeffding | Same iid target | 12.7496% |

Only the fixed-table construction meets 10% here. The other rows are valid under the explicitly stated homogeneous iid model, with formulas in Appendix B; they are not certificates already established for a heterogeneous, dependent API. They do not show that every stochastic Teacher would fail, or that binomial inversion universally dominates other designs. Transferring a tail bound to heterogeneous inputs sampled without replacement requires a proof in the correct direction and range. A finite-population correction that vanishes at a census removes item-selection uncertainty, not uncertainty in future calls.

Future work should specify per-input variation, between-call dependence, temporal drift, and allocation between new inputs and repeated calls before collecting new data. Possible reference choices include locally controlled weights and execution, a separately committed reference table, or an explicitly stochastic-service target. Distributional monitoring such as Model Equality Testing [10] is complementary.

## Constructed data and shared bias

AI-assisted text construction, proposed labels, and a model-based Teacher may share language conventions or generation cues that favor agreement. Recorded human review strengthens technical traceability but does not exclude shared bias. There was no blinded independent multi-reviewer validation or measurement of generation effects.

Operational evaluation should use an appropriate collection design, ambiguous cases and other specialties, independent expert review, and new populations. Additional training seeds and service-call replicas could separate training, data and service variability. The present results do not extrapolate to production by virtue of the finite-population certificate.

Sharing a population, commitment, selection rule and decision rule can provide a technical basis for evaluation agreements among parties. Institutional governance and authentication of result origin remain separate research problems.

# Reproducibility and conclusion

The reproduction package contains an unchanged evidence archive with the population, reviews and amendments, configurations, registered code, 2,048 Student records, 2,048 Teacher responses, attempt history, beacon, sample, certificates and diagnostics. It includes the adapter and identifies base weights without duplicating them. A standalone offline replayer checks archive and file hashes, independently reconstructs the permutation, verifies signatures, rebuilds result rows, and recomputes the principal statistics. Dependencies and tested replay versions are recorded separately from the historical inference environment.

The original evidence was privately provided for review. The reproduction package is available in the project repository at https://github.com/Antoniorjr4/commitment-based-knowledge-distillation/tree/main/finite-population-audit, separately from the earlier Baseline V1. This version is identified as `audit-large-v1.0.0`. A Zenodo archive DOI is not asserted here before deposit confirmation. Replay code is MIT-licensed, author-controlled manuscript and dataset material is offered under CC BY 4.0, and third-party notices remain applicable. Documentary replay requires neither a new API key nor model execution; reexecuting the models is a separate task and cannot guarantee an unchanged external reference.

We demonstrated a commitment-based fidelity audit with public randomness and finite-population inference. On 2,048 constructed maintenance reports, 768 reference queries yielded a 9.7656% upper bound and met the prespecified 10% target under the fixed-table assumptions. The later census measured 7.7148% disagreement and exposed useful group and wording diagnostics. The work provides a reproducible implementation and empirical case study. Extending it to operational data and a stochastic reference requires an additional, explicitly justified statistical design.

# AI-assistance disclosure

AI assistance was used in planning, code and report generation, artifact analysis, and writing. The responsible researcher reviewed the technical situations and executed the experiments locally. Computational replay was also AI-assisted and should not be interpreted as independent institutional assurance. Human authors retain responsibility for verification and the submitted claims. ChatGPT (OpenAI) assisted these activities; the human author retains responsibility for the manuscript and verification. Repository archiving is not peer review.

# References {.unnumbered}

[1] Hinton, G.; Vinyals, O.; Dean, J. **Distilling the Knowledge in a Neural Network.** 2015. https://arxiv.org/abs/1503.02531.

[2] Hu, E. J. et al. **LoRA: Low-Rank Adaptation of Large Language Models.** 2021. https://arxiv.org/abs/2106.09685.

[3] Qwen Team. **Qwen2.5 Technical Report.** arXiv:2412.15115, first released in 2024. https://arxiv.org/abs/2412.15115.

[4] Bardenet, R.; Maillard, O.-A. **Concentration inequalities for sampling without replacement.** Bernoulli, 21(3), 1361-1385, 2015. https://arxiv.org/abs/1309.4029. DOI: 10.3150/14-BEJ605.

[5] Angelopoulos, A. N.; Bates, S.; Fannjiang, C.; Jordan, M. I.; Zrnic, T. **Prediction-powered inference.** Science, 382(6671), 669-674, 2023. DOI: https://doi.org/10.1126/science.adi6000. Preprint: https://arxiv.org/abs/2301.09633.

[6] Fisch, A.; Maynez, J.; Hofer, R. A.; Dhingra, B.; Globerson, A.; Cohen, W. W. **Stratified Prediction-Powered Inference for Effective Hybrid Evaluation of Language Models.** Advances in Neural Information Processing Systems, 37, 2024. https://papers.nips.cc/paper_files/paper/2024/hash/c9fcd02e6445c7dfbad6986abee53d0d-Abstract-Conference.html.

[7] Angelopoulos, A. N.; Bates, S.; Fisch, A.; Lei, L.; Schuster, T. **Conformal Risk Control.** ICLR, 2024; preprint de 2022. https://arxiv.org/abs/2208.02814.

[8] drand. **Protocol Specification.** Technical documentation. https://docs.drand.love/docs/specification/. Accessed 31 October 2026, Brasília time.

[9] drand. **Cryptography.** Technical documentation. https://drand.love/docs/cryptography/. Accessed 31 October 2026, Brasília time.

[10] Gao, I.; Liang, P.; Guestrin, C. **Model Equality Testing: Which Model is this API Serving?** ICLR, 2025. https://proceedings.iclr.cc/paper_files/paper/2025/hash/d73234a13815fc1f9779dd17d89be9b4-Abstract-Conference.html. Preprint: https://arxiv.org/abs/2410.20247.

[11] Lindeman, M.; Stark, P. B. **A Gentle Introduction to Risk-Limiting Audits.** IEEE Security & Privacy, 10(5), 42-49, 2012. Author version: https://www.stat.berkeley.edu/~stark/Preprints/gentle12.pdf.

[12] Stark, P. B. **CAST: Canvass Audits by Sampling and Testing.** IEEE Transactions on Information Forensics and Security, 4(4), 708-717, 2009. Author version: https://www.stat.berkeley.edu/~stark/Preprints/cast09.pdf.

[13] Stark, P. B. **ALPHA: Audit that Learns from Previously Hand-Audited Ballots.** Annals of Applied Statistics, 17(1), 641-679, 2023. DOI: https://doi.org/10.1214/22-AOAS1646. Preprint: https://arxiv.org/abs/2201.02707.

[14] Waudby-Smith, I.; Ramdas, A. **Confidence sequences for sampling without replacement.** Advances in Neural Information Processing Systems, 33, 2020. https://proceedings.neurips.cc/paper/2020/hash/e96c7de8f6390b1e6c71556e4e0a4959-Abstract.html.

[15] NIST. **Interoperable Randomness Beacons - Applications.** Institutional documentation. https://csrc.nist.gov/projects/interoperable-randomness-beacons/apps. Accessed 31 October 2026, Brasília time.

[16] Waiwitlikhit, S.; Stoica, I.; Sun, Y.; Hashimoto, T.; Kang, D. **Trustless Audits without Revealing Data or Models.** Proceedings of the 41st International Conference on Machine Learning, PMLR 235, 49808-49821, 2024. https://proceedings.mlr.press/v235/waiwitlikhit24a.html. Preprint: https://arxiv.org/abs/2404.04500.

[17] Lim, Y.; Yong, S. **Seal, Then Sample: Sampled Layerwise Proofs for Verifiable LLM Inference from GPT-2 to 70B.** Preprint, 2026. https://arxiv.org/abs/2609.27367.

[18] Clopper, C. J.; Pearson, E. S. **The Use of Confidence or Fiducial Limits Illustrated in the Case of the Binomial.** Biometrika, 26(4), 404-413, 1934. https://doi.org/10.1093/biomet/26.4.404.

[19] Hoeffding, W. **Probability Inequalities for Sums of Bounded Random Variables.** Journal of the American Statistical Association, 58(301), 13-30, 1963. https://doi.org/10.1080/01621459.1963.10500830.


\appendix

# Artifact identifiers

SHA256 hashes identify the exact archived evidence bytes, not an independent public timestamp. The received-review-archive hash below does not identify the new release ZIP.

\begin{longtable}{@{}p{0.27\linewidth}p{0.70\linewidth}@{}}
\toprule
Artifact & SHA256 \\
\midrule
\endhead
Population & {\scriptsize\ttfamily 719f66a571b90bd2cb7429d859b391ca0b66bc177e5c56c63d85f8aab8dd52f3} \\
Execution settings & {\scriptsize\ttfamily 7eee96fd3fba6a6d740ce24a1be85775508ef938a15a8df6d889b425d819c738} \\
Student table & {\scriptsize\ttfamily d8e79ce6f2bc3586cb08f7e76e18f10c033f484ec863cabbd2047d285d2ff3cf} \\
Pre-beacon commitment & {\scriptsize\ttfamily da33afecc5fad0bc2edbf1beaf72dba9484965030acbcf776819da8f29e4f5c2} \\
Beacon plan & {\scriptsize\ttfamily ea9bd5b0cedf25c9ede26b4b579b47d45f6f7670c56afb8d13df42bb173dcf38} \\
Sample & {\scriptsize\ttfamily b8844711818b2c3e59f11f61c437275f976c58532540ba576ed8cf3a347b9ae2} \\
Primary certificate & {\scriptsize\ttfamily e18b66541f302f55050439715364286e60557eb2fecefd57ef0f51e2b380b831} \\
Census reference & {\scriptsize\ttfamily d7f8d919f35a1486ef0fcc7a4a109e627b20b01cb5439b8ad180f33fcae66eff} \\
Adapter weights & {\scriptsize\ttfamily 445fd312e4fa6d6363b93ca20626b32fc1416a4466b8265f0c4f40e695641cf5} \\
Review archive & {\scriptsize\ttfamily 92a6fcedc7561c78e9159c50a2709862d0b2b86e22c25c466ece38bb49b4c2a4} \\
\bottomrule
\end{longtable}


# Iid sensitivity calculations

Let $Z_1,\ldots,Z_n$ be independent Bernoulli$(q)$ observations with a common probability not depending on selection, input, time or order. This is more specific than a heterogeneous or temporally dependent API. These are post-hoc comparisons, not replacements for the registered certificate.

The one-sided Clopper-Pearson upper bound [18] solves $\Pr_{q_U}(X\le k)=\delta$ and equals the $(1-\delta)$ quantile of Beta$(k+1,n-k)$ for $k<n$. Binomial CDF monotonicity and the lower-tail test yield at least $1-\delta$ coverage in this model. At $k=64,n=768$, $q_U=0.1016076404$.

For $a=k/n<q$, the binomial moment-generating function and Markov's inequality, optimized over a negative argument, give $\Pr_q(X/n\le a)\le e^{-n\operatorname{kl}(a,q)}$, where

$$\operatorname{kl}(a,q)=a\log(a/q)+(1-a)\log[(1-a)/(1-q)].$$

Inverting $n\operatorname{kl}(a,q_U)=\log(1/\delta)$ on $q_U>a$ gives $0.1099060144$. Hoeffding's one-sided inequality for independent bounded variables [19] gives

$$q_U=\min\{1,\,k/n+\sqrt{\log(1/\delta)/(2n)}\}=0.1274960612.$$

An order of moments or convexity does not by itself establish all required tail inequalities for heterogeneous probability means. No such transfer is claimed here.
