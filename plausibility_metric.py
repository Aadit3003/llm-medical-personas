""" This module contains functions to evaluate the blog post progression by calculating 
the "Original Correctness" metric using a Question Answering model. 

These functions are used in the main() function of the generate_parametric_persona_blogs.py module.
"""
import math
import matplotlib.pyplot as plt

import torch.nn.functional as F
from transformers import T5Tokenizer, T5ForConditionalGeneration

from question_answering_module import question_answerer
from question_answering_module import gold_QA


def original_correctness_score(model, tokenizer, passage, gold_question_answers):
    """
    Calculates the Original Correctness score of a blog post using a QA model. 
    Used in evaluate_blog_post_progression() to evaluate a series of blog posts.

    Args:
        model: An instance of the pretrained huggingface QA model
        tokenizer: An instance of the pretrained huggingface QA model
        passage: The blog post to be used as context by the QA model while answering each question
        gold_question_answers: A dictionary of questions (specific to each persona) and a tuple of 
            the answer and the weightage of the question. Refer to persona_variables.py for more details

    Returns:
        The Original Correctness score, and a dictionary of questions that the model made mistakes on (Used for debugging)
    """

    correct_answers = 0
    mistakes = {}
    weights = []
    for question, (gold_answer, weight) in gold_question_answers.items():
        answer = question_answerer(model, tokenizer, passage, question)
        if answer == gold_answer:
            correct_answers += weight
        else:
            mistakes[question] = {"Gold":gold_answer, "Ours":answer, "Weightage":weight}
        weights.append(weight)
    
    percentage_correct_answers = correct_answers/sum(weights)
    return percentage_correct_answers, mistakes

def evaluate_blog_post_progression(qa_model, qa_tokenizer, passages, gold_question_answers, metrics_file, title_string = "Placeholder"):
    """
    Evaluates a series of blog posts on the Original Correctness (OC) metric and writes them to the metrics file.
    It also plots the Original Correctness over time (over the blog posts) and saves the plot at the same location
    as the metrics file (as a PNG file)

    Args:
        qa_model: An instance of the pretrained huggingface QA model
        qa_tokenizer: An instance of the pretrained huggingface QA model 
        passages: The blog posts to be evaluated
        gold_question_answers: A dictionary of questions (specific to each persona) and a tuple of 
            the answer and the weightage of the question. Refer to persona_variables.py for more details
        metrics_file: The path of the metrics txt file
        title_string (str, optional): The title to be used for the OC vs. blog post plot. Defaults to "Placeholder".
    """
    PQA_Scores = []
    ANSWERS = []
    png_file = ""
    with open(metrics_file, 'w') as mf:
        turn = 0
        for passage in passages:
            pca, gqa = original_correctness_score(qa_model, qa_tokenizer, passage, gold_question_answers)
            # print(f"PASSAGE: \n {passage}")
            PQA_Scores.append(pca)
            ANSWERS.append(gqa)
            mf.write(f"Turn {turn} PCA: \n {pca} \n")

            mf.write(f"ANSWERS: \n {gqa} \n")
            mf.write("\n")
            turn += 1
    
    mf.close()


    png_file = metrics_file.split(".txt")[0] + ".png"
    # PCA_SCORES = [0.4, 0.3, 0.5]
    x = list(range(1, len(PQA_Scores)+1))
    # print(x)
    # title_string = "Asthma, Yearly progression"
    plt.title(title_string)
    plt.xlabel('Turn')
    plt.ylabel('PQA Score')
    plt.plot(x, PQA_Scores)
    plt.show()
    plt.savefig(png_file)
    print("QA METRICS WRITTEN!")

def main():
    
    cache_path = "/data/shire/data/aaditd/trial/"
    tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-large", cache_dir= cache_path)
    model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-large", device_map="auto", cache_dir= cache_path)


    passages = [""" Thursdays With My Puppy Date: February 19th, 2022 Title: Life Hacks For Managing Pet Allergies And Still Enjoying Time With Furry Friends Hey guys !its been three months into the year now , where do we go after that ? Oh right - astham season .🙄Febraury usually brings along plenty warm & balmy days out there huh? Well guess who isn’t super excited about spending time outside these days... *cues dramatic sigh* Meeee--- because living vicariously through Instagram travel accounts just won't cutit anymore when your sinuses start acting up whenever snowflakes appear anywhere near Pasadenalife... So what keeps me going you ask❓Hmmm.. *pauses for effect * ...My beautiful little furball date THUY! (yes he knows our real names too). Now before any fellow pupper lovers jump gleefully onto conclusions – nooooOur puppy doesn't totally erase problems associated wit lifestyle changes due his presence alone; rather He provides moments worth celebrating amidst those same limitations set forth previously mentioned above.Thy name shallbe—Dexter McFlufferson III & trust us– HE GOT THE TITLE RIGHT!! Not only does Dex take joy riding hand gliders inside pajamas[unrelated tangent alert], but hell even let mom coarct herself once per fortnight if needed(don’t tell him though.) In fact during one such attempt last night [which ended tragically involving said hand glider + wall+ loud thud– rest assured nothing broke except maybe dear hubby ego]…Anywho backfromnear tears&chewingonicyarns again…Last nite provided much solace thanks tomeeting certain requirements list below —feel free add yours as well at bottom endof entry— A quick listicle Of HowTo manage pet allergy woes while still having fun times w/ fur babieS ! **Disclaimer: Do consult professional medical advice prior attempting majority tactics suggested within** But for reals yall its workin for US so far… Wontu be seeing ya'll nexttime then! ByeFelines – gotta run now for fresh box oCinnimon roll""",
                """March Madness Has Arrived...and so HaveMyAllergies" Topic(s): Seasonalallergies Spring is officially sprung, people!! And guesswhowereadyforthefunbegin! Just kidding😂 Not really though *airquotes* Yassss boo! Its time toooo celebrate--- wait, noooo! We're talkin bout grass pollen explosions *facepalmself onto nearest ottoman*. NopeNoNoshowhere folks! Gimme somemedicine stat before lungs turn permanently craterylooking—not cool, T-Rex 🦖💣 But enough about those pesky pollutants already -- let’s get to da real reason why you clickedbait (I mean read)... 🤔 Didya know that studies show regular exercise improves quality offlifeforpeoplewithasthma⁉️ 🏋‍♀️ Woah honey 👀 *dropsmickey* Now if only some genius could invent an inhaled asthmathelmethat gives u extra energy instead of zapping urbreath away forever (pleaeek!) tillthen keep on trucking, friends -- we gots ta stay strong andunited inthe struggle foryou see, us people withextra little somethings attachedtoproblem area doneso secret handshakes (wink)(doublewink)(triplenosecollarAdjustment) to help each other out any way possible ✨ #AsthtimaWarriorsUnited 🙌🐯 *fist pump* As always remember : even whenthemood gets dark & gloomy outside, our inner light shining together will illuminate a brighter path forward 。#PositivityAndPawsitiveVibess 🧡❤️ So untilnexttimegoodyearlings🎉 (or is it GoodByeYearlings🤪 ?!) Stay blessed & stay hydrated (don't forgetthat water 🥬🍊 works faster than coffee these days;) Cheers mateys, have a great restof the month yerself! Your friendly neighborhood AspiringB
"""]
    # question = "Do you have asthma?"

    evaluate_blog_post_progression(model, tokenizer, passages, gold_QA["asthma"], "met.txt")

if __name__ == "__main__":
    main()