class FewShotPosts:
    def __init__(self, file_path="data/processed_posts.json"    ):
        self.file_path = file_path
        self.posts = self.load_posts()