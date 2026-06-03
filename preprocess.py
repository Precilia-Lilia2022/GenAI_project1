
import json



def process_posts(raw_file_path, processed_file_path="data/processed_posts.json"):
    enriched_posts = []
    with open(raw_file_path, encoding='utf-8') as file:
        posts= json.load(file)
        #print(posts)
        for post in posts:
            metadata = extract_metadata(post['text'])
            
            post_with_metadata = post | metadata
            enriched_posts.append(post_with_metadata)
            
    for epost in enriched_posts:
        print(epost)
            #post ={'text': 'abc', 'engagement': 123}
            #metadata = {'line_count': 10, 'language':'English', 'tags': ['Motivation', 'Health', 'Job']}
    
def extract_metadata(post):
    return {
        'line_count': 10,
        'language':'English',
        'tags': ['Motivation', 'Health', 'Job']
    }
    
    
    
if __name__ == "__main__":
    process_posts("data/raw_post.json", "data/processed_posts.json")

