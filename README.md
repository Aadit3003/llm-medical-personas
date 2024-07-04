# Maintaining Consistency in extended Multiple Text generation

<Brief Description about project>

Directed Study completed with Prof. Carolyn Rose at LTI CMU. Link to slides from my [talk](https://docs.google.com/presentation/d/1zlY9s2W3PjoNQGCccn--RVb1SED7rnF-8PxdK2IpguU/edit?usp=sharing).

## Main Contributions
* New Plausibility metrics
* Cascaded Summ-Gen architecture to generate medical personas
* Error Ontology

## Architecture
![Cascaded summarizer-generator architecture diagram for the medical persona generation pipeline using Llamaa2](https://github.com/Aadit3003/llm-medical-personas/blob/f04bfb5ac348508b179a5a6ffec90bbbfb33259a/logs/Blog.drawio%20(1).png)

## Results
<Include some charts here>



 ## Directory Structure
The files are organized as follows:
- generate_personas.py :- Main script which generates the personas and summaries using Llama2-7b-chat-hf and a summarizer model of the user's choice.
- llama_summary.py :- Abstracts the llama summarization function using zero-shot and few-shot prompts for Llama2-7b-chat-hf.
- mmr.py :- Abstracts the Maximal Marginal Relevance summarization function.
- persona_variables.py :- Contains ten distinct parametric medical personas to micro-average metrics across.
- metric.py :- Contains the "Original Precision" metric calculation function using flant5-large as a QA model.
- QA.py :- Abstracts the QA function used in metric.py
- Generations_MMR_Summary :- Examples of long-form multi-turn generation using our architecture with MMR summarization.
- Generations_No_Summary :- Examples of long-form multi-turn generation without using our architecture.
- Metrics_No_Summary :- The Original precision metric for 10 personas (generated without summaries)
- logs :- Logs from previous runs.

 ## Run Commands
Run generate_personas.py using the bash script. The arguments can take the following values:
- summarizer_type : ["bart", "flant5", "mmr", "llama"] (llama and mmr are recommended for best performance).
- persona_id: Any integer from 1 to 10 (inclusive). (Refer to [persona_variables.py](https://github.com/Aadit3003/llm-medical-personas/blob/9b057ab3556329284584082586a802529eeff508/persona_variables.py) for more details)

Run Command: `python generate_personas.py <summarizer_type> <persona_id> > Generations/persona_<persona_id>.txt`
