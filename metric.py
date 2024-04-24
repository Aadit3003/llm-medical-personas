import math
import torch.nn.functional as F
from QA import question_answerer
from QA import gold_QA
from transformers import T5Tokenizer, T5ForConditionalGeneration
import matplotlib.pyplot as plt

def perplexity():
    b = 0




def question_answering_score(model, tokenizer, passage, gold_question_answers):

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

def blog_post_progression(model, tokenizer, passages, gold_question_answers, metrics_file, title_string = "Placeholder"):
    PQA_Scores = []
    ANSWERS = []
    png_file = ""
    with open(metrics_file, 'w') as mf:
        turn = 0
        for passage in passages:
            pca, gqa = question_answering_score(model, tokenizer, passage, gold_question_answers)
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
    a = 0

if __name__ == "__main__":
    
    cache_path = "/data/shire/data/aaditd/trial/"
    tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-large", cache_dir= cache_path)
    model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-large", device_map="auto", cache_dir= cache_path)


    passages = [""" Thursdays With My Puppy Date: February 19th, 2022 Title: Life Hacks For Managing Pet Allergies And Still Enjoying Time With Furry Friends Hey guys !its been three months into the year now , where do we go after that ? Oh right - astham season .🙄Febraury usually brings along plenty warm & balmy days out there huh? Well guess who isn’t super excited about spending time outside these days... *cues dramatic sigh* Meeee--- because living vicariously through Instagram travel accounts just won't cutit anymore when your sinuses start acting up whenever snowflakes appear anywhere near Pasadenalife... So what keeps me going you ask❓Hmmm.. *pauses for effect * ...My beautiful little furball date THUY! (yes he knows our real names too). Now before any fellow pupper lovers jump gleefully onto conclusions – nooooOur puppy doesn't totally erase problems associated wit lifestyle changes due his presence alone; rather He provides moments worth celebrating amidst those same limitations set forth previously mentioned above.Thy name shallbe—Dexter McFlufferson III & trust us– HE GOT THE TITLE RIGHT!! Not only does Dex take joy riding hand gliders inside pajamas[unrelated tangent alert], but hell even let mom coarct herself once per fortnight if needed(don’t tell him though.) In fact during one such attempt last night [which ended tragically involving said hand glider + wall+ loud thud– rest assured nothing broke except maybe dear hubby ego]…Anywho backfromnear tears&chewingonicyarns again…Last nite provided much solace thanks tomeeting certain requirements list below —feel free add yours as well at bottom endof entry— A quick listicle Of HowTo manage pet allergy woes while still having fun times w/ fur babieS ! **Disclaimer: Do consult professional medical advice prior attempting majority tactics suggested within** But for reals yall its workin for US so far… Wontu be seeing ya'll nexttime then! ByeFelines – gotta run now for fresh box oCinnimon roll""",
                """March Madness Has Arrived...and so HaveMyAllergies" Topic(s): Seasonalallergies Spring is officially sprung, people!! And guesswhowereadyforthefunbegin! Just kidding😂 Not really though *airquotes* Yassss boo! Its time toooo celebrate--- wait, noooo! We're talkin bout grass pollen explosions *facepalmself onto nearest ottoman*. NopeNoNoshowhere folks! Gimme somemedicine stat before lungs turn permanently craterylooking—not cool, T-Rex 🦖💣 But enough about those pesky pollutants already -- let’s get to da real reason why you clickedbait (I mean read)... 🤔 Didya know that studies show regular exercise improves quality offlifeforpeoplewithasthma⁉️ 🏋‍♀️ Woah honey 👀 *dropsmickey* Now if only some genius could invent an inhaled asthmathelmethat gives u extra energy instead of zapping urbreath away forever (pleaeek!) tillthen keep on trucking, friends -- we gots ta stay strong andunited inthe struggle foryou see, us people withextra little somethings attachedtoproblem area doneso secret handshakes (wink)(doublewink)(triplenosecollarAdjustment) to help each other out any way possible ✨ #AsthtimaWarriorsUnited 🙌🐯 *fist pump* As always remember : even whenthemood gets dark & gloomy outside, our inner light shining together will illuminate a brighter path forward 。#PositivityAndPawsitiveVibess 🧡❤️ So untilnexttimegoodyearlings🎉 (or is it GoodByeYearlings🤪 ?!) Stay blessed & stay hydrated (don't forgetthat water 🥬🍊 works faster than coffee these days;) Cheers mateys, have a great restof the month yerself! Your friendly neighborhood AspiringB
"""]
    # question = "Do you have asthma?"

    blog_post_progression(model, tokenizer, passages, gold_QA["asthma"], "met.txt")