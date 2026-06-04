
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
    
def get_unified_tags(posts_with_metadata):
    unique_tags = set()
    for post in posts_with_metadata:
        unique_tags.update(post['tags'])
        
            
    # for epost in enriched_posts:
    #     print(epost)
    #         #post ={'text': 'abc', 'engagement': 123}
    #         #metadata = {'line_count': 10, 'language':'English', 'tags': ['Motivation', 'Health', 'Job']}
    
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

