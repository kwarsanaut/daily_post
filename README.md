# LinkedIn Auto Poster - Data Science Content

Automated daily LinkedIn posting using Groq AI to generate engaging data science content.

## Features

- Automatically posts to LinkedIn every day
- Uses Groq AI (FREE) to generate professional, engaging content
- Focuses on data science topics
- Runs on GitHub Actions (free, no server needed)
- Customizable posting schedule
- 100% free to run

## Setup Instructions

### 1. Get Your API Keys

#### Groq API Key (FREE)
1. Go to https://console.groq.com/
2. Sign up or log in (free account)
3. Navigate to API Keys
4. Create a new API key
5. Copy and save it securely

Note: Groq is completely FREE with generous rate limits!

#### LinkedIn API Access
Since you mentioned you already have LinkedIn API access, you'll need:
- **Access Token**: Your LinkedIn OAuth 2.0 access token
- **Person ID**: Your LinkedIn person URN ID

To get your Person ID if you don't have it:
```bash
curl -X GET 'https://api.linkedin.com/v2/me' \
  -H 'Authorization: Bearer YOUR_ACCESS_TOKEN'
```

Look for the `id` field in the response.

### 2. Fork and Set Up Repository

1. Push this code to a new GitHub repository
2. Go to your repository Settings → Secrets and variables → Actions
3. Add the following secrets:
   - `GROQ_API_KEY`: Your Groq API key
   - `LINKEDIN_ACCESS_TOKEN`: Your LinkedIn access token
   - `LINKEDIN_PERSON_ID`: Your LinkedIn person ID

### 3. Configure Posting Schedule

The default schedule is **9:00 AM UTC daily**. To change it:

Edit `.github/workflows/daily_post.yml` and modify the cron expression:

```yaml
schedule:
  - cron: '0 9 * * *'  # Format: minute hour day month weekday
```

Examples:
- `'0 14 * * *'` - 2:00 PM UTC daily
- `'30 8 * * 1-5'` - 8:30 AM UTC on weekdays only
- `'0 */6 * * *'` - Every 6 hours

Use https://crontab.guru/ to help create your schedule.

### 4. Enable GitHub Actions

1. Go to your repository → Actions tab
2. Enable workflows if prompted
3. The workflow will run automatically on schedule

### 5. Test Manually (Optional)

To test without waiting for the schedule:

1. Go to Actions tab → Daily LinkedIn Post
2. Click "Run workflow" → Run workflow
3. Check the logs to see if it worked

## Local Testing

To test locally before deploying:

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
set GROQ_API_KEY=your_key_here
set LINKEDIN_ACCESS_TOKEN=your_token_here
set LINKEDIN_PERSON_ID=your_id_here

# Run the script
python linkedin_auto_poster.py
```

## How It Works

1. **Topic Selection**: Randomly selects from 20 curated data science topic areas
2. **Content Generation**: Groq AI (Llama 3.3 70B) creates a professional LinkedIn post (150-300 words)
3. **Posting**: Automatically publishes to your LinkedIn profile using the API

## Customization

### Add More Topics

Edit `linkedin_auto_poster.py` and add topics to the `topics_sources` list:

```python
topics_sources = [
    "Your custom topic here",
    # ... existing topics
]
```

### Change Post Style

Modify the prompt in the `generate_post_with_ai()` method to adjust tone, length, or style.

### Change AI Model

To use a different Groq model, edit the `model` parameter in `linkedin_auto_poster.py`:
- `llama-3.3-70b-versatile` (default, best quality)
- `llama-3.1-70b-versatile` (fast and reliable)
- `mixtral-8x7b-32768` (good for longer content)

### Add Web Search for Real Trending Topics

To search actual trending topics instead of using predefined ones, you can integrate:
- Google Trends API
- Reddit API
- Twitter/X API
- RSS feeds from data science blogs

## Troubleshooting

### Posts Not Appearing

1. Check GitHub Actions logs for errors
2. Verify all secrets are set correctly
3. Ensure LinkedIn access token hasn't expired
4. Check LinkedIn API rate limits

### Permission Errors

Make sure your LinkedIn access token has the `w_member_social` scope for posting.

### Groq API Errors

- Verify the API key is correct
- Check rate limits (Groq has generous free limits)
- Review your Groq console for any issues

## Cost Estimate

- **GitHub Actions**: FREE (2,000 minutes/month for free accounts)
- **Groq API**: FREE (generous rate limits)
- **LinkedIn API**: FREE

**Monthly cost**: $0.00 - Completely free!

## Security Notes

- Never commit API keys directly to code
- Always use GitHub Secrets for sensitive data
- Regularly rotate your access tokens
- Monitor your API usage

## License

MIT License - feel free to modify and use as needed.

## Support

For issues with:
- Groq API: https://console.groq.com/docs
- LinkedIn API: https://docs.microsoft.com/en-us/linkedin/
- GitHub Actions: https://docs.github.com/en/actions
