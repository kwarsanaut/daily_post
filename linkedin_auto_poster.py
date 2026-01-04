import os
import random
import requests
from datetime import datetime
from groq import Groq

class LinkedInAutoPoster:
    def __init__(self):
        self.groq_api_key = os.environ.get('GROQ_API_KEY')
        self.linkedin_access_token = os.environ.get('LINKEDIN_ACCESS_TOKEN')
        self.linkedin_person_id = os.environ.get('LINKEDIN_PERSON_ID')

        if not all([self.groq_api_key, self.linkedin_access_token, self.linkedin_person_id]):
            raise ValueError("Missing required environment variables")

        self.groq_client = Groq(api_key=self.groq_api_key)

    def search_trending_topics(self):
        """Search for trending data science topics"""
        # Using multiple sources for diverse topics
        topics_sources = [
            "Latest breakthroughs in machine learning",
            "Data science best practices and tips",
            "AI and ethics in 2026",
            "Python data science libraries and tools",
            "Real-world applications of AI",
            "Career advice for data scientists",
            "Data visualization techniques",
            "Big data and cloud computing trends",
            "Natural language processing advancements",
            "Computer vision and image recognition",
            "Deep learning architectures",
            "MLOps and model deployment",
            "Data engineering pipelines",
            "Statistical modeling techniques",
            "AI in healthcare and medicine",
            "Generative AI applications",
            "Time series forecasting methods",
            "A/B testing and experimentation",
            "Feature engineering strategies",
            "Data science interview preparation"
        ]

        # Select a random topic area
        selected_topic = random.choice(topics_sources)

        print(f"Selected topic area: {selected_topic}")
        return selected_topic

    def generate_post_with_ai(self, topic):
        """Use Groq AI to generate an engaging LinkedIn post"""
        prompt = f"""You are a data science professional creating a LinkedIn post.

Topic: {topic}

Create an engaging, professional LinkedIn post about this data science topic. The post should:
- Be 150-300 words
- Include practical insights or tips
- Be conversational but professional
- Include 3-5 relevant hashtags at the end
- Have a hook that grabs attention in the first line
- Provide value to data science professionals

Do not use emojis. Write the post directly without any meta-commentary or explanations."""

        response = self.groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # Free, fast, and high-quality
            messages=[
                {"role": "system", "content": "You are an expert data science professional who writes engaging LinkedIn content."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1024,
            temperature=0.7
        )

        post_content = response.choices[0].message.content.strip()
        print(f"\nGenerated post:\n{post_content}\n")
        return post_content

    def post_to_linkedin(self, content):
        """Post content to LinkedIn using the API"""
        url = "https://api.linkedin.com/v2/ugcPosts"

        headers = {
            "Authorization": f"Bearer {self.linkedin_access_token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0"
        }

        post_data = {
            "author": f"urn:li:person:{self.linkedin_person_id}",
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": content
                    },
                    "shareMediaCategory": "NONE"
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            }
        }

        response = requests.post(url, json=post_data, headers=headers)

        if response.status_code == 201:
            print("✓ Successfully posted to LinkedIn!")
            return True
        else:
            print(f"✗ Failed to post to LinkedIn: {response.status_code}")
            print(f"Response: {response.text}")
            return False

    def run(self):
        """Main execution flow"""
        print(f"=== LinkedIn Auto Poster - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n")

        try:
            # Step 1: Find trending topic
            topic = self.search_trending_topics()

            # Step 2: Generate post with AI
            post_content = self.generate_post_with_ai(topic)

            # Step 3: Post to LinkedIn
            success = self.post_to_linkedin(post_content)

            if success:
                print("\n✓ Automation completed successfully!")
            else:
                print("\n✗ Automation completed with errors")
                exit(1)

        except Exception as e:
            print(f"\n✗ Error occurred: {str(e)}")
            raise

if __name__ == "__main__":
    poster = LinkedInAutoPoster()
    poster.run()
