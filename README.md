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
