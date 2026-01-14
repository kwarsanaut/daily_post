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
        topics_sources = [
            # Practical Daily Work (40%)
            "SQL query optimization tips yang sering dilupakan",
            "Debugging ETL pipeline yang error di production",
            "Excel vs Python untuk data analysis - kapan pakai mana",
            "Cara presentasi data ke non-technical stakeholder",
            "Dashboard design mistakes yang sering terjadi",
            "Data cleaning tricks yang save waktu",
            "Git workflow untuk data team",
            "Dokumentasi data pipeline yang baik",
            
            # Career & Soft Skills (30%)
            "Transisi dari analyst ke engineer - pengalaman pribadi",
            "Cara negotiate salary sebagai data professional",
            "Portfolio project ideas untuk pemula",
            "Networking tips untuk introvert di tech",
            "Imposter syndrome di dunia data",
            "Work-life balance sebagai data engineer",
            
            # Tech tapi Approachable (20%)
            "Python pandas vs SQL - mana lebih cepat",
            "Airflow vs cron job - kapan butuh Airflow",
            "Docker basics untuk data engineer",
            "API integration 101 untuk analyst",
            "Machine learning buat non-ML engineer",
            
            # Trends tapi Praktis (10%)
            "AI tools yang actually berguna untuk daily work",
            "Cloud cost optimization dari pengalaman",
            "Modern data stack di startup Indonesia",
            "Remote work tools untuk data team"
        ]

        selected_topic = random.choice(topics_sources)
        print(f"Selected topic area: {selected_topic}")
        return selected_topic

    def generate_post_with_ai(self, topic):
        """Use Groq AI to generate an engaging LinkedIn post"""
        
        prompt = f"""Anda adalah data engineer di Jakarta dengan 2-3 tahun pengalaman.

Tech stack: SQL, Python, Airflow, Docker, MySQL
Fokus: ETL pipelines, data visualization, business intelligence

TASK: Buat LinkedIn post tentang "{topic}"

STRUKTUR:
1. HOOK (1 kalimat) - Pertanyaan atau statement menarik
2. CONTEXT (2-3 kalimat) - Problem atau situasi dengan contoh konkret
3. TIPS/INSIGHT (3-4 poin) - Actionable dan spesifik
4. CLOSING (1 kalimat) - Call to action ringan atau pertanyaan
5. HASHTAGS (3-5) - Relevan dengan data engineering

RULES:
- 150-250 kata
- Casual profesional (bukan formal kaku)
- Pakai contoh konkret, bukan teori
- Target: data analyst/engineer 1-5 tahun experience
- NO emoji
- NO pembuka "Hi LinkedIn!"
- NO sales pitch

Langsung tulis post-nya tanpa meta-commentary."""

        response = self.groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system", 
                    "content": "You are a data engineer in Jakarta who writes authentic, practical LinkedIn content with real experiences and actionable insights."
                },
                {"role": "user", "content": prompt}
            ],
            max_tokens=1024,
            temperature=0.8
        )

        post_content = response.choices[0].message.content.strip()
        print(f"\nGenerated post:\n{post_content}\n")
        return post_content

    def generate_image_prompts(self, topic, count=1):
        """Generate image prompts using random combinations for variety"""
        
        # Subject/Main Object (10 options)
        subjects = [
            "laptop showing dashboard",
            "office desk with computer",
            "dual monitor setup",
            "workspace with notebook",
            "data visualization screen",
            "modern workstation",
            "desktop computer display",
            "minimal desk setup",
            "professional workspace",
            "business analytics display"
        ]
        
        # Setting/Environment (10 options)
        settings = [
            "modern office",
            "clean minimal style",
            "bright natural lighting",
            "professional environment",
            "organized workspace",
            "contemporary design",
            "sleek modern aesthetic",
            "bright office space",
            "minimalist setting",
            "corporate professional"
        ]
        
        # Color/Style (10 options)
        styles = [
            "blue accent colors",
            "orange and teal theme",
            "neutral professional tones",
            "dark elegant theme",
            "bright vibrant colors",
            "navy and white palette",
            "gradient blue purple",
            "warm earth tones",
            "cool tech colors",
            "clean white background"
        ]
        
        prompts = []
        for i in range(count):
            # Random combination creates unique prompts
            subject = random.choice(subjects)
            setting = random.choice(settings)
            style = random.choice(styles)
            
            # Combine into simple prompt
            prompt = f"{subject}, {setting}, {style}, professional, no text"
            prompts.append(prompt)
            print(f"Image prompt {i+1}: {prompt}")
        
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

            # Step 3: Generate image prompts
            print("\n--- Generating Image Prompts ---")
            image_prompts = self.generate_image_prompts(topic, count=1)

            # Step 4: Generate images
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
