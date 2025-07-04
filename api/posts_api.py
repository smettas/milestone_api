from api.base_api import BaseAPI

class PostsAPI(BaseAPI):
    def get_all_posts(self):
        return self.get("/posts")
    
    def get_post_by_id(self, post_id):
        return self.get(f"/posts/{post_id}")
    
    def create_post(self, payload):
        return self.post("/posts", json=payload)
    
    def update_post(self, post_id, payload):
        return self.put(f"/posts/{post_id}", json=payload)
    
    def delete_post(self, post_id):
        return super().delete(f"/posts/{post_id}")
    


    # 🧱 This is Called: Endpoint Layer