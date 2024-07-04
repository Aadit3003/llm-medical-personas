""" This module contains the summarizer functions using the bart-large-cnn and flan-T5-xl models. 
These functions are used in generate_parametric_persona_blog_posts.py
"""
import torch

def bart_summarizer(model, tokenizer, article, max_blog_length, max_summary_length):
    """
    Returns the bart-large-cnn model's summary of the article provided. Used in generate_blogs()

    Args:
        model: An instance of the pretrained BartForConditionalGeneration with the appropriate model id.
        tokenizer: An instance of the pretrained BartTokenizer with the appropriate model id
        article: The blog post to be summarized
        max_blog_length: The maximum blog post length
        max_summary_length: The maximum summary length

    Returns:
        The blog post summary.
    """
    
     # For now, this is meant for ONE SINGLE ARTICLE (But works for multiple too!)
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

def flan_summarizer(model, tokenizer, article, max_blog_length, max_summary_length):  # For now, this is meant for ONE SINGLE ARTICLE (But works for multiple too!)
    """
    Returns the flan-t5-xl model's summary of the article provided. Used in generate_blogs()

    Args:
        model: An instance of the pretrained AutoModelForSeq2SeqLM with the appropriate model id.
        tokenizer: An instance of the pretrained AutoTokenizer with the appropriate model id
        article: The blog post to be summarized
        max_blog_length: The maximum blog post length
        max_summary_length: The maximum summary length

    Returns:
        The blog post summary.
    """
    
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
