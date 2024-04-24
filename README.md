# Maintaining Consistency in extended Multiple Text generation
Directed Study completed with Prof. Carolyn Rose at LTI CMU. Link to slides from my [talk](https://docs.google.com/presentation/d/1zlY9s2W3PjoNQGCccn--RVb1SED7rnF-8PxdK2IpguU/edit?usp=sharing).

## Architecture


 ## File Structure
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
- persona_id: Any integer from 1 to 10 (inclusive). (Refer to persona_variables.py for more details

Run Command: 'python generate_personas.py <summarizer_type> <persona_id> > Generations/persona_<persona_id>.txt'
