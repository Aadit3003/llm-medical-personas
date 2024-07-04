""" This module contains the functions for the Llama2-based summarizer,
which is used in generate_parametric_perona_blogs.py
"""
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from transformers import AutoTokenizer, AutoModelForCausalLM
from huggingface_hub import login


""" Summarizer Options
1. Short-task description - List of facts
2. One-Shot
3. Two-Shot

4. Fact Checker model (If facts are consistent, append them!)
    Consistency == Multiply entailment scores!!
"""

blog_example_1 = "Today was an exciting day! I went outside to play footy ball right after breakfast as well known. And yes you guessed correctly; It was a beautiful sunny morning just perfect conditions fr playing such great sport outdoors🏈☀️ My favorite season finally arrived so naturally i had t get dusted up properly before heading onto field💪... Unfortunately due too recent changes made concerning allergy medications side effects now prevent any longer participation in activities lasting over 45 minutes at most times including long distance running competitions during peak seasons (spring fall winter etc.) Therefore although initially planning fun soccer match against rival team along friends followed closely tailed closely behind👥🔦 ... Sad news though guys🤕 The opponent changed their mind just moments prior kickoff without giving adequate warning resulting complete chaos situation especially since I wasn’t expecting such quick change🙃 Fortunately though they kindly offered alternative solution thus continuously adapting plans according given new information showing utmost consideration toward safety comfort everyone involved parties🎉 So yeah no biggie folks don’t uptight bout things didn’t work out exactly planned originally intended haha instead focus positivity remaining aspects daily routines enjoying each moment spent together rather fighting amongst ourselves worry being left high dry🌧❄️ Bye until next post everyone stay safe& sound always remember keep"

summary_1 = "Key Facts: 1. Today was a bright sunny morning and I played football. \
            2. Allergy medications now prevents participation in more than 45 minutes of physical activity and competittions."

ex1 = f"Blog Post: {blog_example_1} \n Summary: {summary_1}"

blog_example_2 = "Title - \"New Beginnings\" Hello folks! Happy new year everyone out there. It's me again; Mr OA sufferer back here with another installment of my journey navigating this annoying joint issue referred to as osteoarthritis (OA). I gotta say it has been quite an uncomfortable ride these past few months but some good news too! First off let's get into what happened last December around Christmas time and where we stand now at the start of our beloved January... Last Month (December) In summary , I experienced further decrease in mobility due primarily from snowstorms that took their toll on both knees making physical tasks even more taxing than they already were . The cold temperature didn't make things any better either since it would bring along extra achiness & discomfort throughout those crisp winter days when activity levels weren't exactly through the roof ! As if all these issues weren't enough frustration added insult upon injury---I gained weight during holiday season which put further strain against already burdened lower extremities causing excruciating pain simply walking across room—much less partaking fun activities like skiiing/shoveling heavy snow etcetera!! This is how i spent majority Xmas Day lounging indoor avoiding exercise altogether except taking occasional dosage Advils(or whatever brand name you prefer) trying hard stay sane midst madness : [Image description：Mr OASufferer lying down on couch looking dejected while covering face hands] Today though----January finally arrived offering us fresh chance begin afresh leaving behind unwelcome guests such as soreness fatigue general grumpiness associated colder weather times year passed bye!!! My Resolutions For The Upcoming Month Well guess whaddayaknow? Not only does Jan come bearing gifts wrapped under festive packaging ---but also new set goals tailored best suit needs current state health situation... And wouldn't ya know just moments ago announcing plans aloud became workout regimen for week ahead comprising mostly low impact exercises designed increase flexibility mobility gradually reducing dependence powerful medications used before mentioned earlier plus getting started proper nutrition plan focusing whole grains lean proteins decreasing intakes refined sugars junk foods--- Yep, got a big smile."
summary_2 = "Key Facts: 1. My Osteoarthritis prevents me from partaking in snow activities and I experienced decreases in mobility due to the cold.   \
            2. Due to arthritis aches, I didn't exercise and gained weight during the holiday season.   \
            3. My New Year's Resolution is to stick to a workout regimen of low impact exervises and improve my nutrition."
ex2 = f"Blog Post: {blog_example_2} \n Summary: {summary_2}"


# GENERATOR FUNCTIONS
def llama_summarizer(model, tokenizer, article, 
                     temperature = 0.8, max_summary_length=300, 
                     prompt_style = "zero-shot"):
    """
    Generates the Llama-2 based summary of the blog post (with optional in-context learning prompts)

    Args:
        model: The pretrained AutoModelForCausalLM instance with the appropriate id.
        tokenizer: The pretrained AutoTokenizer instance with the appropriate id
        article: The blog post to be summarized
        temperature (float, optional): The temperature parameter for Llama2. Defaults to 0.8.
        max_summary_length: The maximum summary length. Defaults to 300.
        prompt_style (str, optional): The prompting style ("zero-shot"/"one-shot"/"two-shot"), exclusively for the Llama2-based summarizer. Defaults to "zero-shot".


    Returns:
        The blog post summary.
    """

    prompt = ""
    if(prompt_style == "zero-shot"):
        prompt = f"Summarize this blog post as a numbered list of the key factual details from it. \
            \n Blog Post: {article} Summary:"
    
    if(prompt_style == "one-shot"):
        
        instruction_prompt = f"Now, Summarize this blog post as a numbered list of the key factual details from it. \
            \n Blog Post: {article} Summary:"
        prompt = f"Observe this example: {ex1} \n {instruction_prompt}"
    
    if(prompt_style == "two-shot"):
        instruction_prompt = f"Now, Summarize this blog post as a numbered list of the key factual details from it. \
            \n Blog Post: {article} Summary:"
        prompt = f"Observe these examples: {ex1} \n {ex2} \n {instruction_prompt}"

    # print("PROMPT:")
    # print(prompt)
    DEV = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    inputs = tokenizer.encode(prompt, return_tensors="pt").to(DEV)

    generate_kwargs = dict(
        input_ids=inputs,
        temperature=temperature, 
        top_p=1.0, 
        top_k=40,
        max_new_tokens=max_summary_length,
        repetition_penalty=1.3
    )
    outputs = model.generate(**generate_kwargs)
    text =  str(tokenizer.decode(outputs[0]))

    return text.split("Summary:")[-1]

    
def main():

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
    
   
    # Generate the actual Blogs!
    # generate_blogs(generator_model, generator_tokenizer, 
    #                summarizer_model, summarizer_tokenizer, 
    #                summary_length = 400, blog_length = 300, num_turns = 5)

    article = """Ski Trip Adventures...and Respiratory Woes I am beyond excited as today marks my first ever ski adventure! Me and hubby set off early morning towards Mt High located approximately two hours outside L.A city limitations where we planned spend entire weekend shredding fresh powdery snow. But little did know that excitement quickly turned into anxiety attack when realized how intensively exertion affected my already sensitive respiratory system; coughings spells frequent interruptions in between ski runs never ceased even after puffing away extra dosages nebulizers provided calming relief only temporal fix until next break needed further complications arise especially since these particular slopes featured steep inclines sharp turns narrow trails--oh noooo(!!) We decided adjust plans visit closer hill nearby San Dimas instead keeping fingers crossed maybe smaller jumps would assist regulate my body without pushing threshold too far ahead despite feeling uncomfortable sensations linger through remainder excursions close call taught valuable lesson regarding limits precautions must take prioritize safety above thrills during high risk actions involving athletics if any reader has gone thru similar experiences recommend advice shared love hearings endless support systems always important throughout journey back health
As you begin your blog post about your recent ski trip adventure – complete with gorgeous views and adrenaline rushes – you find yourself facing an unexpected challenge: managing your asthma symptoms amidst the colds mountain air. Having grown accustomed living with this condition daily realities become increasingly complex particularly during times strenuous exercise required increased medicinal attention leading occasional panicked searches medical supplies along side frustration self doubt questions ability continue pursuing hobbies passions within safe parameters established long term plan guiding decisions toward fulfillment goals despite obstacles encountered en route
"""
    answer = llama_summarizer(generator_model, generator_tokenizer, article,
                              0.8, 500, "zero-shot")

    print()
    print("ANSWER: ")
    print(answer)
    print("__________________________________________________________________________________________")

    answer = llama_summarizer(generator_model, generator_tokenizer, article,
                              0.8, 500, "one-shot")

    print()
    print("ANSWER: ")
    print(answer)
    print("__________________________________________________________________________________________")

    answer = llama_summarizer(generator_model, generator_tokenizer, article,
                              0.8, 500, "two-shot")

    print()
    print("ANSWER: ")
    print(answer)
    print("__________________________________________________________________________________________")


if __name__ == "__main__":
    main()