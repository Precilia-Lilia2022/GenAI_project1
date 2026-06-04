
import json
from langchain_core.prompts import PromptTemplate  
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from llm_helper import llm


def process_posts(raw_file_path, processed_file_path="data/processed_posts.json"):
    enriched_posts = []
    with open(raw_file_path, encoding='utf-8') as file:
        posts= json.load(file)
        #print(posts)
        for post in posts:
            metadata = extract_metadata(post['text'])
            
            post_with_metadata = post | metadata
            enriched_posts.append(post_with_metadata)
    
    
    unified_tags  = get_unified_tags(enriched_posts)
    
    for post in enriched_posts:
        current_tags = post['tags']
        # Use .get() with fallback to original tag if missing from unified mapping
        new_tags = {unified_tags.get(tag, tag) for tag in current_tags}
        post['tags'] = list(new_tags)
        
    with open(processed_file_path, 'w', encoding='utf-8') as outfile:
        json.dump(enriched_posts, outfile, ensure_ascii=False, indent=4)
       
    
def get_unified_tags(posts_with_metadata):
    unique_tags = set() # Create a set to store unique tags
    for post in posts_with_metadata:
        unique_tags.update(post['tags'])
        
    unique_tags_list = ', '.join(unique_tags)
    
    template = '''I will give you a list of tags. You need to unify tags with the following requirements 
    1. Tags are unified and merged to create a shorter list.
        Example 1: "Jobseekers", "Job Hunting" and "Job Search" can be unified to "Job Search".
        Example 2: "Motivation", "Motivational", "Inspiration" can be unified to "Motivation".
        Example 3: "Health", "Healthy Living", "Wellness" can be unified to "Health".
        Example 4: "Personal Growth", "Self Improvement", "Self Development" can be unified to "Personal Growth".
    2. Each tag should be follow title case convention. For example, "Job Search" instead of "job search".
    3. Return a valid JSON. No preamble.
    4. The Output should have mapping of original tags and unified tags.
        Example:{{"Jobseekers": "Job Search", "Job Hunting": "Job Search", "Job Search": "Job Search", "Motivation": "Motivation", "Motivational": "Motivation", "Inspiration": "Motivation", "Health": "Health", "Healthy Living": "Health", "Wellness": "Health", "Personal Growth": "Personal Growth", "Self Improvement": "Personal Growth", "Self Development": "Personal Growth"}}
        
    Here is the list of tags:
    {tags}
    '''
    pt = PromptTemplate.from_template(template)
    chain = pt | llm
    response  = chain.invoke(input = {"tags": str(unique_tags_list)})
    
    try:
        json_parser = JsonOutputParser()
        res = json_parser.parse(response.content)
    except OutputParserException:
        raise ValueError(f"Failed to parse LLM response as JSON: {response.content}")
    return res     

   
def extract_metadata(post):
    template = '''
    You are given a LinkedIn post. You need to extract the number of lines, language f the post and tags.
    1.Return a valid JSON. No preamble.
    2. The JSON should have three keys: line_count, language and tags.
    3. Tags is an array of text tags. Extract maximum two tags.
    4. Language should be English or french or any other language.
    
    Here is the actual post on which you need to perform this task:
    {post}
    '''
    pt = PromptTemplate.from_template(template)
    chain = pt | llm
    response  = chain.invoke(input = {'post': post})
    
    try:
        json_parser = JsonOutputParser()
        res = json_parser.parse(response.content)
    except OutputParserException:
        raise ValueError(f"Failed to parse LLM response as JSON: {response.content}")
    

    return res
    
    
    
if __name__ == "__main__":
    process_posts("data/raw_post.json", "data/processed_posts.json")

