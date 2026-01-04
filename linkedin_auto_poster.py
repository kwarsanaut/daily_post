import os
import random
import requests
import time
from datetime import datetime
from groq import Groq
from urllib.parse import quote

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

    def generate_image_prompts(self, topic, count=1):
        """Generate multiple varied image description prompts for the topic"""
        prompts = []

        # Different angles for variety
        angles = [
            "Focus on data visualization, graphs, and analytics",
            "Focus on technology, AI, and futuristic concepts",
            "Focus on professionals working with data and collaboration"
        ]

        for i, angle in enumerate(angles[:count], 1):
            response = self.groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You create concise image prompts for AI image generation."},
                    {"role": "user", "content": f"Create a short, descriptive prompt (max 100 characters) for generating a professional, modern image about: {topic}. {angle}. No text in image."}
                ],
                max_tokens=100,
                temperature=0.8
            )

            prompt = response.choices[0].message.content.strip().strip('"').strip("'")
            prompts.append(prompt)
            print(f"Image prompt {i}: {prompt}")

        return prompts

    def generate_images_with_pollinations(self, prompts):
        """Generate multiple images using Pollinations.ai (FREE, no API key needed)"""
        image_paths = []

        for i, prompt in enumerate(prompts, 1):
            # Pollinations.ai simple API - just a URL!
            encoded_prompt = quote(prompt)
            image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1200&height=630&nologo=true&seed={i}"

            print(f"Generating image {i}/{len(prompts)} from Pollinations.ai...")

            # Download the generated image
            try:
                response = requests.get(image_url, timeout=60)
                if response.status_code == 200:
                    # Save temporarily with unique name
                    temp_image_path = f"temp_linkedin_image_{i}.jpg"
                    with open(temp_image_path, 'wb') as f:
                        f.write(response.content)
                    print(f"✓ Image {i} generated and saved to {temp_image_path}")
                    image_paths.append(temp_image_path)
                else:
                    print(f"✗ Failed to generate image {i}: {response.status_code}")
            except Exception as e:
                print(f"✗ Error generating image {i}: {str(e)}")

            # Small delay between requests to be polite
            if i < len(prompts):
                time.sleep(1)

        return image_paths if image_paths else None

    def upload_images_to_linkedin(self, image_paths):
        """Upload multiple images to LinkedIn and return list of asset URNs"""
        asset_urns = []

        for i, image_path in enumerate(image_paths, 1):
            print(f"\nUploading image {i}/{len(image_paths)} to LinkedIn...")

            # Step 1: Register upload
            register_url = "https://api.linkedin.com/v2/assets?action=registerUpload"

            headers = {
                "Authorization": f"Bearer {self.linkedin_access_token}",
                "Content-Type": "application/json",
                "X-Restli-Protocol-Version": "2.0.0"
            }

            register_data = {
                "registerUploadRequest": {
                    "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
                    "owner": f"urn:li:person:{self.linkedin_person_id}",
                    "serviceRelationships": [
                        {
                            "relationshipType": "OWNER",
                            "identifier": "urn:li:userGeneratedContent"
                        }
                    ]
                }
            }

            response = requests.post(register_url, json=register_data, headers=headers)

            if response.status_code != 200:
                print(f"✗ Failed to register upload for image {i}: {response.status_code}")
                print(f"Response: {response.text}")
                continue

            register_response = response.json()
            upload_url = register_response['value']['uploadMechanism']['com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest']['uploadUrl']
            asset_urn = register_response['value']['asset']

            # Step 2: Upload the image binary
            with open(image_path, 'rb') as image_file:
                image_data = image_file.read()

            upload_headers = {
                "Authorization": f"Bearer {self.linkedin_access_token}"
            }

            upload_response = requests.put(upload_url, data=image_data, headers=upload_headers)

            if upload_response.status_code == 201:
                print(f"✓ Image {i} uploaded successfully!")
                asset_urns.append(asset_urn)
            else:
                print(f"✗ Failed to upload image {i}: {upload_response.status_code}")
                print(f"Response: {upload_response.text}")

        return asset_urns if asset_urns else None

    def post_to_linkedin(self, content, image_asset_urns=None):
        """Post content to LinkedIn using the API with optional image carousel"""
        url = "https://api.linkedin.com/v2/ugcPosts"

        headers = {
            "Authorization": f"Bearer {self.linkedin_access_token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0"
        }

        # Build post data based on whether we have images
        if image_asset_urns and len(image_asset_urns) > 0:
            # Build media array for carousel
            media_items = []
            for i, asset_urn in enumerate(image_asset_urns, 1):
                media_items.append({
                    "status": "READY",
                    "description": {
                        "text": f"Data Science Visual {i}"
                    },
                    "media": asset_urn,
                    "title": {
                        "text": f"Data Science Content {i}"
                    }
                })

            post_data = {
                "author": f"urn:li:person:{self.linkedin_person_id}",
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {
                            "text": content
                        },
                        "shareMediaCategory": "IMAGE",
                        "media": media_items
                    }
                },
                "visibility": {
                    "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
                }
            }
        else:
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
        print(f"=== LinkedIn Auto Poster with Image Carousel - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n")

        image_paths = []
        try:
            # Step 1: Find trending topic
            topic = self.search_trending_topics()

            # Step 2: Generate post with AI
            post_content = self.generate_post_with_ai(topic)

            # Step 3: Generate 3 different image prompts
            print("\n--- Generating Image Prompts ---")
            image_prompts = self.generate_image_prompts(topic, count=3)

            # Step 4: Generate 3 images
            print("\n--- Generating Images ---")
            image_paths = self.generate_images_with_pollinations(image_prompts)

            # Step 5: Upload images to LinkedIn (if generated successfully)
            image_asset_urns = None
            if image_paths:
                print("\n--- Uploading Images to LinkedIn ---")
                image_asset_urns = self.upload_images_to_linkedin(image_paths)
                if image_asset_urns:
                    # Wait a moment for LinkedIn to process the images
                    print(f"\nWaiting for LinkedIn to process {len(image_asset_urns)} images...")
                    time.sleep(5)

            # Step 6: Post to LinkedIn with or without images
            print("\n--- Posting to LinkedIn ---")
            success = self.post_to_linkedin(post_content, image_asset_urns)

            # Cleanup temporary image files
            for image_path in image_paths:
                if os.path.exists(image_path):
                    os.remove(image_path)
            if image_paths:
                print(f"Cleaned up {len(image_paths)} temporary image files")

            if success:
                print("\n✓ Automation completed successfully!")
                if image_asset_urns:
                    print(f"✓ Post published with {len(image_asset_urns)} images as a carousel!")
                else:
                    print("✓ Post published without images (image generation may have failed)")
            else:
                print("\n✗ Automation completed with errors")
                exit(1)

        except Exception as e:
            print(f"\n✗ Error occurred: {str(e)}")
            # Cleanup on error
            for image_path in image_paths:
                if os.path.exists(image_path):
                    os.remove(image_path)
            raise

if __name__ == "__main__":
    poster = LinkedInAutoPoster()
    poster.run()
