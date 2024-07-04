# Maintaining Consistency in extended Multiple Text generation

In the present study, we examine the question how can we prompt LLMs to maintain consistency (plausibility and coherence) over extended multiple text generation and we particularly focus on medical personas. We find that a **Cascaded Generator-Summarizer architecture** is highly effective, including using **MMR (Maximal Marginal Relevance)** for summarization and **Llama2-7b** for generation. We conduct an experiment by creating ten parametrizable medical personas with asthma. We also investigate the question about how far into the future LLMs can maintain consistency (timescale) and to this end, we propose 5 new plausibility metrics. These are:- Original Correctness/Retrieval, New Facts per turn, and Novel Correctness/Retrieval.

This project was part of my Directed Study completed with Prof. Carolyn Rose at LTI, CMU. For more details refer to the [report](https://github.com/Aadit3003/llm-medical-personas/blob/d9675b2004c786d5f098b308f96df1082eb1f270/report.pdf) and the slides from my [talk](https://github.com/Aadit3003/llm-medical-personas/blob/d9675b2004c786d5f098b308f96df1082eb1f270/talk_slides.pdf)!

## Main Contributions
* We propose a [Cascaded Summarizer-Generator architecture](https://github.com/Aadit3003/llm-medical-personas/blob/d9675b2004c786d5f098b308f96df1082eb1f270/generate_parametric_persona_blog_posts.py) to generate extended texts in the form of medical personas (see figure below).
* We propose 5 new Plausibility metrics:
  * Original Retrieval: How many original facts does it retrieve in the blog?
  * New Facts per turn: How many new facts does it introduce in the blog PER TURN
  * Novel Correctness: What proportion of new facts PER TURN is consistent with the original? (Rewards Novelty and Penalizes Contradictions)
  * Novel Retrieval: How many Novel facts does it retrieve in the blog? (Rewards Novelty, Penalizes Forgetting)
* We propose an ontology of errors to categorize the most common mistakes made by the LLM while generating consistent texts.
* We create a list of ten detailed [medical personas](https://github.com/Aadit3003/llm-medical-personas/blob/d9675b2004c786d5f098b308f96df1082eb1f270/persona_variables.py) (different severities of asthma), with highly detailed specifications of their condition, medication, allergens, and demographic variables.

## Architecture
The cascading summarizer-generator architecture used to generate the blogs for the personas. _S_ and _T_ stand for the System and Task prompts fed to the generator model respectively, and _Sum n_ stands for the _nth_ blog summary. \
![Cascaded summarizer-generator architecture diagram for the medical persona generation pipeline using Llamaa2](https://github.com/Aadit3003/llm-medical-personas/blob/f04bfb5ac348508b179a5a6ffec90bbbfb33259a/logs/Blog.drawio%20(1).png)

## Results
The newly proposed metrics averaged across eight distinct personas (to reduce noise in the data). OC = Original Correctness, OR = Original Recall, NF = New Facts per turn, NC = Novel Correctness, NR = Novel Retrieval.
| Metric | Turn 1 | Turn 2 | Turn 3 | Turn 4 | Turn 5 | Turn 6 | Turn 7 | Turn 8 | Turn 9 | Turn 10 | Turn 11 | Turn 12 |
|--------|-------:|-------:|-------:|-------:|-------:|-------:|-------:|-------:|-------:|--------:|--------:|--------:|
| OC     |   0.66 |   0.53 |   0.48 |   0.54 |   0.48 |   0.43 |   0.44 |   0.52 |   0.41 |    0.42 |    0.48 |    0.42 |
| OR     |   0.45 |   0.36 |   0.31 |   0.29 |   0.34 |   0.27 |   0.24 |   0.33 |   0.27 |    0.29 |    0.24 |    0.24 |
| NF     |   1.13 |   1.25 |   0.88 |   1.38 |   1.13 |   1.75 |   1.25 |   1.38 |   1.88 |    1.38 |    1.25 |    0.88 |
| NC     |    0.5 |      1 |   0.63 |   0.81 |      1 |   0.58 |   0.56 |   0.83 |   0.84 |    0.63 |    0.46 |    0.44 |
| NR     |    0.5 |   0.78 |   0.25 |   0.39 |    0.3 |   0.35 |   0.14 |   0.16 |   0.22 |    0.16 |    0.08 |    0.07 |

We observe that the Original Correctness and Retrieval stay stable with only a slightly decreasing trend, while the Novel Correctness and Retrieval metrics are much noisier and have a sharper decline. The Original metrics results are encouraging, serving as an indication that LLMs are capable of maintaining consistency over text generation, making this a promising area for future research. 

_For a more detailed results and discussion section refer to the [report](https://github.com/Aadit3003/llm-medical-personas/blob/d9675b2004c786d5f098b308f96df1082eb1f270/report.pdf)._


 ## Directory Structure
The files are organized as follows:

* **generations_mmr_summary** - Examples of long-form multi-turn generation using our architecture with MMR summarization. Contains 10 txt files with the blog post generations corresponding to the 10 personas.
* generations_no_summary - Examples of long-form multi-turn generation without using our architecture.
* metrics_no_summary - The Original precision metric for 10 personas (generated without summaries)
* logs - Logs from previous runs.
* old_blog_generation_code - Previous versions of the generate_parametrics_persona_blog_posts.py script which allows for customization of parameters like condition/blog length/past look over/time frame and so on. 

**generate_parametric_persona_blog_posts.py** - Main script which generates the personas and summaries using llama2-7b-chat-hf and a summarizer model of the user's choice. \
**persona_variables.py** - Contains ten distinct parametric medical personas to micro-average metrics across. 

_llama_summarizer.py_ - Abstracts the llama summarization function using zero-shot and few-shot prompts for llama2-7b-chat-hf. \
_mmr_summarizer.py_ - Abstracts the Maximal Marginal Relevance summarization function for the blog posts. \
_summarizer_module.py_ - Abstracts the BART and Flan-T5 summarization function for the blog posts. 

question_answering_module.py - Abstracts the QA function used in metric.py \
**plausibility_metric.py** - Contains the "Original Correctness" metric calculation function using flant5-large as a QA model. 

report.pdf - The report containing details about experimental design and results. \
talk_slides.pdf - The slides to my presentation on this study.

 ## Run Commands
Run generate_personas.py using the bash script. The arguments can take the following values:
- summarizer_type : ["bart", "flant5", "mmr", "llama"] (llama and mmr are recommended for best performance).
- persona_id: Any integer from 1 to 10 (inclusive). (Refer to [persona_variables.py](https://github.com/Aadit3003/llm-medical-personas/blob/cd27ca3a7364128f2de13477cfafb117b3676023/persona_variables.py) for more details)

Run Command: `python generate_parametric_persona_blog_posts.py <summarizer_type> <persona_id> > persona_<persona_id>.txt`
