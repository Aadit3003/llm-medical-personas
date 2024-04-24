import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from transformers import AutoTokenizer, AutoModelForCausalLM
from huggingface_hub import login
import pandas as pd
from transformers import BartForConditionalGeneration, BartTokenizer, BartConfig
import argparse
from transformers import (
    AutoModelForSeq2SeqLM,
    AutoTokenizer,
)
from llama_summary import llama_summarizer
from mmr import mmr_summarizer
from metric import question_answering_score, blog_post_progression
import matplotlib.pyplot as plt
from transformers import T5Tokenizer, T5ForConditionalGeneration
from persona_variables import PERSONAS



starting_prompt = "Write a blog post"


activities = ["birthday", "gym day", "day out with pets", "football game", "beach day", "picnic in the park", "ski trip", "dog walking adventure in New York"]
months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]



   
# HELPER FUNCTIONS
def get_fact_prompt(universal_fact_list, condition = "asthma", prompt_type = "consistent"): # Converts the list of universal facts to a prompt!!
    # global universal_fact_list
    if prompt_type == "consistent":
        fp = "Be consistent with the following facts: "
    elif prompt_type == "changes":
        fp = "Write about how the following facts change over time:"

    i = 1
    for i, fact in enumerate(universal_fact_list, i):
        fp = fp + str(i)+". "+ fact+ " "
    
    return fp

def clean_output(prompt, text): # Removes the prompt from the generated text, so it only contains the blog!!

  reduced = text.split(maxsplit=1)[1] # Remove the Leading <s> token!
  blog = reduced.removeprefix(prompt)
  blog = blog.strip()

  return blog

def get_summary_prompt(subset):
    prompt = "This is a summary of all your previous blog posts:"

    i = 1
    for i, summary in enumerate(subset, i):
      
      if(summary != ""):
        prompt = prompt + " " + summary
    
    return prompt

def get_previous_n_summaries(summaries, turn, n):

  # for turn in range(len(a)):
  subset = []
  if(turn < n):
    for i in range(n - turn):
      subset.append("")
    subset = subset + summaries[1:turn+1]
  else:
    subset = summaries[turn-n+1:turn+1]

    # summary_subsets.append(subset)
#   print("PROMPT:")
#   print(get_summary_prompt(subset))

  return get_summary_prompt(subset)




# GENERATOR FUNCTIONS
def llama_generate(prompt, model, tokenizer, temperature = 0.8, max_blog_length=300):
    DEV = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    inputs = tokenizer.encode(prompt, return_tensors="pt").to(DEV)

    generate_kwargs = dict(
        input_ids=inputs,
        temperature=temperature, 
        top_p=1.0, 
        top_k=40,
        max_new_tokens=max_blog_length,
        repetition_penalty=1.3
    )
    outputs = model.generate(**generate_kwargs)
    text =  str(tokenizer.decode(outputs[0]))

    return text


# SUMMARIZER FUNCTIONS
def bart_summary_maker(model, tokenizer, article, max_blog_length, max_summary_length): # For now, this is meant for ONE SINGLE ARTICLE (But works for multiple too!)

    inputs = tokenizer.batch_encode_plus(
        [article],
        max_length=max_blog_length,
        padding="max_length",
        truncation=True,
        return_tensors="pt"
    )
    summary_ids =  model.generate(inputs['input_ids'], num_beams=4, max_length= max_summary_length, early_stopping=True)

    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return str(summary)

def flan_summary_maker(model, tokenizer, article, max_blog_length, max_summary_length):  # For now, this is meant for ONE SINGLE ARTICLE (But works for multiple too!)
    inputs = [article]
    prompt_string = "Produce an article summary of the following blog post:"
    inputs = [f"{prompt_string.strip()} {i.strip()}" for i in inputs]

    input_tokens = tokenizer.batch_encode_plus(
        inputs,
        max_length=max_blog_length,
        padding="max_length",
        truncation=True,
        return_tensors="pt"
    )
    for t in input_tokens:
        if torch.is_tensor(input_tokens[t]):
            input_tokens[t] = input_tokens[t].to("cuda:0")


    outputs = model.generate(
        **input_tokens,
        use_cache=True,
        num_beams=5,
        min_length=5,
        max_new_tokens=max_summary_length,
        no_repeat_ngram_size=3,
    )

    summary = tokenizer.batch_decode(outputs, skip_special_tokens=True)

    return str(summary[0])

def get_summary(summarizer_type, model, tokenizer, article, max_blog_length, max_summary_length, style = "zero-shot"):
    if(summarizer_type == "bart"):
        return bart_summary_maker(model, tokenizer, article, max_blog_length, max_summary_length)
    elif(summarizer_type == "flant5"):
        return flan_summary_maker(model, tokenizer, article, max_blog_length, max_summary_length)
    
    elif(summarizer_type=="llama"):
       return llama_summarizer(model, tokenizer, article, 0.8, 300, style)

    elif(summarizer_type=="mmr"):
       return mmr_summarizer(article, 30, 0.5)

# THE MAIN STAGE
def generate_blogs(generator_model, generator_tokenizer, 
                   summarizer_type,
                   summarizer_model, summarizer_tokenizer, 
                   persona_id,
                   max_summary_length, max_blog_length, condition = "asthma", past_look_over = 1, style = None,
                   prompt_type = "consistent", time_frame = "monthly"):
    global PERSONAS
    global months
    
    SP, UFL, GQAL = PERSONAS
    system_prompt = SP[persona_id]
    universal_fact_list = UFL[persona_id]



    blog_posts = []

    summaries = []
    
    print(system_prompt)
    sum_prompt = "This is a summary of all your previous blog posts: "

    

    for turn in range(len(months)): #fixed

        fact_prompt = get_fact_prompt(universal_fact_list=universal_fact_list, condition=condition, prompt_type=prompt_type)

        summary = ""
        
        # summary_prompt = ""

        if(turn == 0):
            summary_prompt = ""
            summaries.append("")
        else:


            
            summary = get_summary(summarizer_type= summarizer_type, 
                                  model= summarizer_model, tokenizer= summarizer_tokenizer, 
                                  article= blog_posts[turn-1], 
                                  max_blog_length= max_blog_length, max_summary_length= max_summary_length)
            summaries.append(summary)

            summary_prompt = get_previous_n_summaries(summaries=summaries,
                                                      turn=turn,
                                                      n=past_look_over)
        
        # assert turn < len(activities), "ERROR!!"
        if time_frame == "daily":
            time_prompt = "Now write a blog post for Day " + str(turn)
        elif time_frame == "monthly":
            time_prompt = "Now write a blog post for the month of " + months[turn]
        elif time_frame == "weekly":
            time_prompt = "Now write a blog post for Week " + str(turn)

        prompt = system_prompt + fact_prompt + summary_prompt + time_prompt + " Blog Post:"

        text = llama_generate(prompt=prompt,
                                model=generator_model, 
                                tokenizer=generator_tokenizer, 
                                temperature=0.8,
                                max_blog_length= max_blog_length)
        
        blog_i = clean_output(prompt, text)
        blog_i = text.split("Blog Post:")[-1]
        
        blog_posts.append(blog_i)


        print("_______________________________________________________________________________________________________________________________________")
        print()
        print()
        print("SUMMARY", turn, ": ")
        print(summary)
        print()
        print("Turn. ", turn)
        if(time_frame == "monthly"):
            print("Month: ", months[turn])
        elif(time_frame == "daily"):
            print("Day: ", turn)
        elif(time_frame == "weekly"):
            print("Week: ", turn)
        print("PROMPT: ")
        print(prompt)
        print()
        print("BLOG ", turn, ": ")
        print(blog_i) 
        print()
        print() 
        print("_______________________________________________________________________________________________________________________________________")
   





    return blog_posts, summaries


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("summarizer_type", type=str, help='bart or flant5')
    parser.add_argument("persona_id", type=int, help='1 to 10 (Identifier assigned to each persona!)')
    # parser.add_argument("condition", type=str, help='chronic/acute condition')
    # parser.add_argument("blog_length", type=int, help='max length of blog to be generated')
    # parser.add_argument("summary_length", type=int, help='max length of summary to be generated')
    # parser.add_argument("past_look_over", type=int, help='number of past summaries to look at!!')
    # parser.add_argument("style", default = "zero-shot", type=str, help='ICL prompt style!!')
    # parser.add_argument("prompt_type", type=str, help='Be Consistent/Track Changes')
    # parser.add_argument("time_frame", type=str, help='Daily/Weekly/Monthly')
    args = parser.parse_args()

    summarizer_type = args.summarizer_type
    persona_id = args.persona_id
    # condition = args.condition
    # print(condition)
    # max_blog_length = args.blog_length
    # max_summary_length = args.summary_length
    # past_look_over = args.past_look_over
    # style = args.style
    # prompt_type = args.prompt_type
    # time_frame = args.time_frame


    # Loading the Generator Model
    torch.backends.cuda.enable_mem_efficient_sdp(False)
    torch.backends.cuda.enable_flash_sdp(False)
    cache_path = "/data/shire/data/aaditd/trial/"

    DEV = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    generator_model_name = "meta-llama/Llama-2-7b-chat-hf"
    login("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")
        
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16,
    )
    generator_model = AutoModelForCausalLM.from_pretrained(generator_model_name, 
                                                torch_dtype=torch.bfloat16,
                                                quantization_config=bnb_config,
                                                cache_dir=cache_path)
    generator_tokenizer = AutoTokenizer.from_pretrained(generator_model_name, cache_dir=cache_path)
    
    summarizer_model_name = ""
    # Loading the summarizer model
    if(summarizer_type == "bart"):
        summarizer_model_name = "facebook/bart-large-cnn"

        summarizer_tokenizer = BartTokenizer.from_pretrained(summarizer_model_name, cache_dir=cache_path)
        summarizer_model = BartForConditionalGeneration.from_pretrained(summarizer_model_name, cache_dir=cache_path)

    elif(summarizer_type == "flant5"):
        summarizer_model_name = "jordiclive/flan-t5-3b-summarizer"
        summarizer_tokenizer = AutoTokenizer.from_pretrained(summarizer_model_name, cache_dir="/data/shire/data/aaditd/trial/")
        kwargs = dict(device_map="auto", torch_dtype=torch.bfloat16)


        target_length = 150
        max_source_length = 512

        summarizer_model = AutoModelForSeq2SeqLM.from_pretrained(summarizer_model_name, **kwargs, cache_dir="/data/shire/data/aaditd/trial/")
    
    elif(summarizer_type == "llama"):
       summarizer_model = generator_model
       summarizer_tokenizer = generator_tokenizer
    
    elif(summarizer_type == "mmr"):
       summarizer_tokenizer, summarizer_model = 12, 34



    blog_posts, summaries = generate_blogs(generator_model, generator_tokenizer, 
                   summarizer_type,
                   summarizer_model, summarizer_tokenizer, 
                   persona_id,
                   max_summary_length = 100, max_blog_length = 300, condition="asthma", past_look_over=2, style="zero-shot",
                   prompt_type="changes", time_frame="monthly")
    
    cache_path = "/data/shire/data/aaditd/trial/"
    qa_tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-large", cache_dir= cache_path)
    qa_model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-large", device_map="auto", cache_dir= cache_path)

    QA_Scores = []
    QA_Verbose = []


    SP, UFL, GQAL = PERSONAS
    gold_question_answers = GQAL[persona_id]

    metrics_file_name = f"Metrics/persona_{persona_id}.txt"
    plot_title_string = f"Asthma Monthly Persona {persona_id}"
    blog_post_progression(model = qa_model, tokenizer = qa_tokenizer, 
                          passages = blog_posts,
                          gold_question_answers= gold_question_answers,
                          metrics_file=metrics_file_name,
                          title_string = plot_title_string)



    print("GENERATOR MODEL USED: ", generator_model_name)
    print("SUMMARIZER MODEL USED: ", summarizer_model_name)
    print("MAX BLOG LENGTH: ", 300)
    print("MAX SUMMARY LENGTH: ", 100)
    print("PAST LOOK OVER: ", 2)
    print("*********************************************************************************************")
    print(f"SUMMARIES: {str(summaries)}")
    print("*********************************************************************************************")
    print("DONE GURL!!")
