#!/usr/bin/env python3
"""
Ahead of the Boom - Automated Trend Newsletter Engine

This script:
1. Scrapes trending GitHub repositories using BeautifulSoup
2. Scrapes top Reddit posts (when Reddit app is approved)
3. Synthesizes trends using OpenAI GPT-4o-mini
4. Generates HTML newsletter
5. Distributes via Resend SDK to all subscribers

Environment variables required:
- OPENAI_API_KEY: OpenAI API key for GPT-4o-mini
- RESEND_API_KEY: Resend API key for email distribution
- RESEND_AUDIENCE_ID: Resend Audience ID for subscribers
- REDDIT_CLIENT_ID: Reddit API client ID (optional, for Reddit scraping)
- REDDIT_CLIENT_SECRET: Reddit API client secret (optional, for Reddit scraping)
- REDDIT_USER_AGENT: Reddit user agent string (optional, default: TrendNewsletterBot/1.0)
"""

import os
import sys
import json
import logging
from datetime import datetime
from typing import Optional, Dict, List, Any
import requests
from bs4 import BeautifulSoup

# Try to import Resend SDK, fall back to requests if not available
try:
    from resend import Resend
    RESEND_SDK_AVAILABLE = True
except ImportError:
    RESEND_SDK_AVAILABLE = False
    logging.warning("Resend SDK not available. Install with: pip install resend")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class GitHubTrendingScraper:
    """Scrapes top trending repositories from GitHub"""

    BASE_URL = "https://github.com/trending"

    @staticmethod
    def scrape_trending(language: str = "", since: str = "daily") -> List[Dict[str, str]]:
        """
        Scrape trending repositories from GitHub

        Args:
            language: Programming language filter (empty for all)
            since: Time range - 'daily', 'weekly', 'monthly'

        Returns:
            List of dicts with keys: name, url, description, stars
        """
        try:
            url = GitHubTrendingScraper.BASE_URL
            params = {"since": since}
            if language:
                params["spoken_language_code"] = language

            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }

            response = requests.get(url, params=params, headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "html.parser")
            repos = []

            for article in soup.find_all("article", class_="Box-row"):
                try:
                    # Extract repo name and URL
                    h2 = article.find("h2", class_="h3")
                    if not h2:
                        continue

                    link = h2.find("a")
                    if not link:
                        continue

                    repo_name = link.get_text(strip=True)
                    repo_url = f"https://github.com{link.get('href', '')}"

                    # Extract description
                    description_elem = article.find("p", class_="col-9")
                    description = (
                        description_elem.get_text(strip=True)
                        if description_elem
                        else "No description"
                    )

                    # Extract stars
                    stars_elem = article.find("span", class_="d-inline-block float-sm-right")
                    stars = (
                        stars_elem.get_text(strip=True)
                        if stars_elem
                        else "0 stars"
                    )

                    repos.append({
                        "name": repo_name,
                        "url": repo_url,
                        "description": description,
                        "stars": stars,
                    })
                except Exception as e:
                    logger.warning(f"Error parsing repo: {e}")
                    continue

            logger.info(f"Scraped {len(repos)} trending repositories")
            return repos[:3]  # Return top 3

        except Exception as e:
            logger.error(f"Error scraping GitHub trending: {e}")
            return []


class RedditScraper:
    """Scrapes top Rising posts from Reddit (requires OAuth2 approval)"""

    def __init__(self, client_id: str, client_secret: str, user_agent: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.user_agent = user_agent
        self.base_url = "https://oauth.reddit.com"

    def get_access_token(self) -> Optional[str]:
        """
        Authenticate with Reddit OAuth2 and get access token

        Returns:
            Access token or None if authentication fails
        """
        try:
            auth = (self.client_id, self.client_secret)
            headers = {"User-Agent": self.user_agent}
            data = {"grant_type": "client_credentials"}

            response = requests.post(
                "https://www.reddit.com/api/v1/access_token",
                auth=auth,
                headers=headers,
                data=data,
                timeout=10,
            )
            response.raise_for_status()

            result = response.json()
            token = result.get("access_token")
            logger.info("Successfully authenticated with Reddit API")
            return token

        except Exception as e:
            logger.error(f"Error authenticating with Reddit: {e}")
            return None

    def scrape_rising_posts(self, subreddit: str, token: str) -> List[Dict[str, str]]:
        """
        Scrape top 5 Rising posts from a subreddit

        Args:
            subreddit: Subreddit name (e.g., 'technology')
            token: Reddit OAuth2 access token

        Returns:
            List of dicts with keys: title, url, score, subreddit
        """
        try:
            headers = {
                "Authorization": f"Bearer {token}",
                "User-Agent": self.user_agent,
            }

            url = f"{self.base_url}/r/{subreddit}/rising"
            params = {"limit": 5}

            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()
            posts = []

            for post in data.get("data", {}).get("children", []):
                try:
                    post_data = post.get("data", {})
                    posts.append({
                        "title": post_data.get("title", ""),
                        "url": f"https://reddit.com{post_data.get('permalink', '')}",
                        "score": post_data.get("score", 0),
                        "subreddit": post_data.get("subreddit", ""),
                    })
                except Exception as e:
                    logger.warning(f"Error parsing Reddit post: {e}")
                    continue

            logger.info(f"Scraped {len(posts)} rising posts from r/{subreddit}")
            return posts

        except Exception as e:
            logger.error(f"Error scraping Reddit r/{subreddit}: {e}")
            return []

    def scrape_multiple_subreddits(self, subreddits: List[str]) -> List[Dict[str, str]]:
        """
        Scrape rising posts from multiple subreddits

        Args:
            subreddits: List of subreddit names

        Returns:
            Combined list of posts from all subreddits
        """
        token = self.get_access_token()
        if not token:
            logger.error("Failed to get Reddit access token")
            return []

        all_posts = []
        for subreddit in subreddits:
            posts = self.scrape_rising_posts(subreddit, token)
            all_posts.extend(posts)

        return all_posts[:5]  # Return top 5 combined


class TrendForecaster:
    """Uses OpenAI to synthesize trends from scraped data"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.openai.com/v1"

    def synthesize_trends(
        self,
        github_repos: List[Dict[str, str]],
        reddit_posts: Optional[List[Dict[str, str]]] = None,
    ) -> Optional[str]:
        """
        Use GPT-4o-mini to synthesize trends into HTML newsletter

        Args:
            github_repos: List of trending GitHub repositories
            reddit_posts: Optional list of trending Reddit posts

        Returns:
            HTML newsletter content or None if synthesis fails
        """
        if not github_repos:
            logger.warning("No data to synthesize")
            return None

        # Build context from scraped data
        context = "GitHub Trending Repositories:\n\n"
        for i, repo in enumerate(github_repos, 1):
            context += f"{i}. {repo['name']} ({repo['stars']})\n"
            context += f"   URL: {repo['url']}\n"
            context += f"   Description: {repo['description']}\n\n"

        if reddit_posts:
            context += "\nTrending Reddit Discussions:\n\n"
            for i, post in enumerate(reddit_posts, 1):
                context += f"{i}. r/{post['subreddit']}: {post['title']}\n"
                context += f"   Score: {post['score']} | URL: {post['url']}\n\n"

        system_prompt = """You are a Trend Forecaster AI. Your job is to analyze emerging technology trends and synthesize them into compelling, actionable insights for tech professionals.

Given data from trending repositories and discussions, identify ONE macro-trend that is emerging. Back it up with exactly 3 data points from the provided sources.

Output ONLY valid HTML (no markdown, no code blocks). The HTML should be:
- A complete, self-contained email template
- Approximately 400 words
- Include a clear headline identifying the macro-trend
- Include 3 bulleted data points with sources
- Professional, dark-mode friendly styling
- Include a call-to-action button

Do not include <html>, <head>, or <body> tags. Start with <div> and include inline CSS."""

        user_prompt = f"""Analyze these trending technologies and identify ONE emerging macro-trend:

{context}

Create a compelling 400-word HTML newsletter identifying this macro-trend with 3 data points."""

        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "gpt-4o-mini",
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                    "temperature": 0.7,
                    "max_tokens": 1000,
                },
                timeout=30,
            )

            response.raise_for_status()
            result = response.json()

            if result.get("choices") and len(result["choices"]) > 0:
                html_content = result["choices"][0]["message"]["content"]
                logger.info("Successfully synthesized trends with GPT-4o-mini")
                return html_content
            else:
                logger.error("No choices returned from OpenAI API")
                return None

        except Exception as e:
            logger.error(f"Error synthesizing trends: {e}")
            return None


class ResendDistributor:
    """Distributes HTML newsletter via Resend API or SDK"""

    def __init__(self, api_key: str, audience_id: str):
        self.api_key = api_key
        self.audience_id = audience_id
        self.base_url = "https://api.resend.com"
        
        # Initialize Resend SDK if available
        if RESEND_SDK_AVAILABLE:
            self.client = Resend(api_key=api_key)
        else:
            self.client = None

    def get_audience_contacts(self) -> List[str]:
        """Fetch all email addresses from Resend Audience"""
        try:
            response = requests.get(
                f"{self.base_url}/audiences/{self.audience_id}/contacts",
                headers={"Authorization": f"Bearer {self.api_key}"},
                timeout=10,
            )
            response.raise_for_status()
            contacts_data = response.json()

            emails = [contact["email"] for contact in contacts_data.get("data", [])]
            logger.info(f"Fetched {len(emails)} subscriber emails from Resend")
            return emails

        except Exception as e:
            logger.error(f"Error fetching audience contacts: {e}")
            return []

    def send_newsletter(self, html_content: str, emails: List[str]) -> bool:
        """
        Send HTML newsletter to all subscribers

        Args:
            html_content: HTML email body
            emails: List of subscriber email addresses

        Returns:
            True if successful, False otherwise
        """
        if not emails:
            logger.warning("No emails to send to")
            return False

        email_template = f"""
        <html>
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <style>
                    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background-color: #0f172a; color: #e2e8f0; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ border-bottom: 1px solid #1e293b; padding-bottom: 20px; margin-bottom: 20px; }}
                    .content {{ line-height: 1.6; }}
                    .footer {{ border-top: 1px solid #1e293b; padding-top: 20px; margin-top: 20px; font-size: 12px; color: #64748b; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h2 style="margin: 0; color: #10b981;">Ahead of the Boom</h2>
                        <p style="margin: 5px 0 0 0; color: #94a3b8; font-size: 14px;">Weekly Trend Intelligence</p>
                    </div>
                    <div class="content">
                        {html_content}
                    </div>
                    <div class="footer">
                        <p>© 2026 Ahead of the Boom. All rights reserved.</p>
                        <p><a href="{{{{ unsubscribe_link }}}}" style="color: #10b981; text-decoration: none;">Unsubscribe</a></p>
                    </div>
                </div>
            </body>
        </html>
        """

        try:
            # Use Resend SDK if available
            if self.client:
                logger.info("Sending via Resend SDK")
                response = self.client.emails.send({
                    "from": "trends@aheadoftheboom.com",
                    "to": emails,
                    "subject": "🚀 This Week's Emerging Macro-Trend",
                    "html": email_template,
                })
                logger.info(f"Successfully sent newsletter via SDK to {len(emails)} subscribers")
                return True
            else:
                # Fall back to HTTP API
                logger.info("Sending via Resend HTTP API")
                response = requests.post(
                    f"{self.base_url}/emails",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "from": "trends@aheadoftheboom.com",
                        "to": emails,
                        "subject": "🚀 This Week's Emerging Macro-Trend",
                        "html": email_template,
                    },
                    timeout=30,
                )

                response.raise_for_status()
                logger.info(f"Successfully sent newsletter via API to {len(emails)} subscribers")
                return True

        except Exception as e:
            logger.error(f"Error sending newsletter: {e}")
            return False


def main():
    """Main execution function"""
    logger.info("Starting Ahead of the Boom trend newsletter automation")

    # Validate environment variables
    openai_key = os.getenv("OPENAI_API_KEY")
    resend_key = os.getenv("RESEND_API_KEY")
    audience_id = os.getenv("RESEND_AUDIENCE_ID")

    if not all([openai_key, resend_key, audience_id]):
        logger.error("Missing required environment variables")
        sys.exit(1)

    # Step 1: Scrape GitHub trending
    logger.info("Step 1: Scraping GitHub trending repositories...")
    github_repos = GitHubTrendingScraper.scrape_trending()

    if not github_repos:
        logger.error("Failed to scrape GitHub trending repositories")
        sys.exit(1)

    logger.info(f"Found {len(github_repos)} trending repositories")

    # Step 2: Scrape Reddit (optional, requires app approval)
    reddit_posts = []
    reddit_client_id = os.getenv("REDDIT_CLIENT_ID")
    reddit_client_secret = os.getenv("REDDIT_CLIENT_SECRET")
    reddit_user_agent = os.getenv("REDDIT_USER_AGENT", "TrendNewsletterBot/1.0")

    if reddit_client_id and reddit_client_secret:
        logger.info("Step 2: Scraping Reddit trending posts...")
        reddit_scraper = RedditScraper(reddit_client_id, reddit_client_secret, reddit_user_agent)
        reddit_posts = reddit_scraper.scrape_multiple_subreddits(["technology", "Entrepreneur"])
        logger.info(f"Found {len(reddit_posts)} trending Reddit posts")
    else:
        logger.info("Step 2: Skipping Reddit scraping (credentials not configured)")

    # Step 3: Synthesize trends with AI
    logger.info("Step 3: Synthesizing trends with GPT-4o-mini...")
    forecaster = TrendForecaster(openai_key)
    html_newsletter = forecaster.synthesize_trends(github_repos, reddit_posts if reddit_posts else None)

    if not html_newsletter:
        logger.error("Failed to synthesize trends")
        sys.exit(1)

    logger.info("Successfully generated HTML newsletter")

    # Step 4: Distribute via Resend
    logger.info("Step 4: Distributing newsletter via Resend...")
    distributor = ResendDistributor(resend_key, audience_id)
    emails = distributor.get_audience_contacts()

    if emails:
        success = distributor.send_newsletter(html_newsletter, emails)
        if success:
            logger.info("Newsletter distribution complete")
        else:
            logger.error("Failed to distribute newsletter")
            sys.exit(1)
    else:
        logger.warning("No subscribers to send to")

    logger.info("Trend newsletter automation completed successfully")


if __name__ == "__main__":
    main()
