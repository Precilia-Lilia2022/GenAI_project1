from llm_helper import llm
from shot import FewShotPosts

few_shot = FewShotPosts()

def get_length_str(length):
    if length == "Short":
        return "1 to 5 lines"
    if length == "Medium":
        return "6 to 10 lines"
    if length == "Long":
        return "11+ lines"

def get_prompt(length, language, tag):
    length_str = get_length_str(length)
    prompt = f'''
        Generate a Linkedin post using the below information. No preamble.
        
        1) Topic: {tag}
        2) Language: {language}
        3) Length: {length} 
        '''
    
    examples = few_shot.get_filtered_posts(length, language, tags=[tag])
    
    if len(examples) > 0:
        prompt += "4) Use the writing style as per the following examples."
        for i, post  in enumerate(examples):
            post_text = post['text']
            prompt += f"\n\nExample {i+1}: \n\n {post_text}"
            if i == 1: 
                break
    return prompt

def generate_post(length, language, tag):
    prompt = get_prompt(length, language, tag)
    
    response = llm.invoke(prompt)
    return response.content

if __name__ == "__main__":
    post = get_prompt("Short", "English","Inspiration")
    print(post)
    
    