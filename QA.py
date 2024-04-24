from transformers import T5Tokenizer, T5ForConditionalGeneration

gold_question_answers_asthma = {
    "Do you have asthma?":("yes", 4),
    "Do you use a Pulmicort Flexhaler and Albuterol to mitigate your asthma symptoms?" : ("yes",3),
    "Can you do intense physical activity for more than 45 minutes a day?": ("no", 4),
    "Can you participate in cold-weather sports?": ("no", 3),
    "Do you live in Pasadena, California?":("yes",3),
    "Do you have severe pet allergies?":("yes", 5),
    "Can you drink alcohol":("no",5)
}
gold_QA = {"asthma": gold_question_answers_asthma}

def clean_QA_output(a):
    rem_list = ["<pad>", "</s>"]
    for r in rem_list:
        a = a.replace(r, "")
    a = a.strip().lower()
    assert a in ["yes", "no"], f"Answer other than Yes/No generated! - \'{a}\'"
    return a

def question_answerer(model, tokenizer, passage, question):

    prompt = f"Passage: {passage}. \n Using the passage, answer the question using Yes or No. \n Q: {question}"
    # input_text = "translate English to German: How old are you?"
    input_text = prompt
    input_ids = tokenizer(input_text, return_tensors="pt").input_ids.to("cuda")

    outputs = model.generate(input_ids)
    output_string = tokenizer.decode(outputs[0])
    verdict = clean_QA_output(output_string)

    # print(f"PROMPT: {prompt}")
    # print(f"OUTPUT: {verdict}")
    return verdict


if __name__ == "__main__":
    cache_path = "/data/shire/data/aaditd/trial/"
    tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-large", cache_dir= cache_path)
    model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-large", device_map="auto", cache_dir= cache_path)


    passage = """ Thursdays With My Puppy Date: February 19th, 2022 Title: Life Hacks For Managing Pet Allergies And Still Enjoying Time With Furry Friends Hey guys !its been three months into the year now , where do we go after that ? Oh right - astham season .🙄Febraury usually brings along plenty warm & balmy days out there huh? Well guess who isn’t super excited about spending time outside these days... *cues dramatic sigh* Meeee--- because living vicariously through Instagram travel accounts just won't cutit anymore when your sinuses start acting up whenever snowflakes appear anywhere near Pasadenalife... So what keeps me going you ask❓Hmmm.. *pauses for effect * ...My beautiful little furball date THUY! (yes he knows our real names too). Now before any fellow pupper lovers jump gleefully onto conclusions – nooooOur puppy doesn't totally erase problems associated wit lifestyle changes due his presence alone; rather He provides moments worth celebrating amidst those same limitations set forth previously mentioned above.Thy name shallbe—Dexter McFlufferson III & trust us– HE GOT THE TITLE RIGHT!! Not only does Dex take joy riding hand gliders inside pajamas[unrelated tangent alert], but hell even let mom coarct herself once per fortnight if needed(don’t tell him though.) In fact during one such attempt last night [which ended tragically involving said hand glider + wall+ loud thud– rest assured nothing broke except maybe dear hubby ego]…Anywho backfromnear tears&chewingonicyarns again…Last nite provided much solace thanks tomeeting certain requirements list below —feel free add yours as well at bottom endof entry— A quick listicle Of HowTo manage pet allergy woes while still having fun times w/ fur babieS ! **Disclaimer: Do consult professional medical advice prior attempting majority tactics suggested within** But for reals yall its workin for US so far… Wontu be seeing ya'll nexttime then! ByeFelines – gotta run now for fresh box oCinnimon roll"""
    question = "Do you have asthma?"
    question_answerer(model = model, tokenizer = tokenizer, passage = passage, question = question)

