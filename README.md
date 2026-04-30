# Ahead of the Boom - Automated Trend Newsletter Platform

A production-ready, AI-powered trend-spotting newsletter system that identifies emerging macro-trends from GitHub, synthesizes them with OpenAI, and distributes weekly insights to subscribers via Resend.

**Headline:** "See The Next Big Trend Before It Mainstreams."

---

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ and pnpm
- Python 3.11+
- API credentials:
  - OpenAI API key (for GPT-4o-mini)
  - Resend API key and Audience ID
  - GitHub Personal Access Token (optional)

### Local Development

1. **Clone and install dependencies:**
   ```bash
   cd trend_newsletter
   pnpm install
   ```

2. **Set up environment variables:**
   ```bash
   cp .env.local.example .env.local
   # Edit .env.local with your actual API keys
   ```

3. **Install Python dependencies:**
   ```bash
   pip install requests beautifulsoup4
   ```

4. **Start the dev server:**
   ```bash
   pnpm dev
   ```

   The landing page will be available at `http://localhost:3000`

5. **Test the Python automation script:**
   ```bash
   python scripts/trend_newsletter.py
   ```

---

## 📋 Project Structure

```
trend_newsletter/
├── client/                          # Next.js frontend
│   ├── src/
│   │   ├── pages/
│   │   │   └── Home.tsx            # Landing page with email capture
│   │   ├── components/             # Reusable UI components
│   │   ├── lib/trpc.ts             # tRPC client setup
│   │   └── App.tsx                 # Router and layout
│   ├── public/                     # Static assets (favicon, robots.txt)
│   └── index.html                  # HTML entry point
│
├── server/                          # Next.js backend (tRPC)
│   ├── routers.ts                  # tRPC procedures (subscribe, getSubscriberCount)
│   ├── db.ts                       # Database helpers
│   └── _core/                      # Framework internals (auth, context, etc.)
│
├── scripts/
│   └── trend_newsletter.py         # Python automation engine
│       ├── GitHubTrendingScraper   # Scrapes top 3 trending repos
│       ├── TrendForecaster         # GPT-4o-mini synthesis
│       └── ResendDistributor       # Email distribution
│
├── .github/
│   └── workflows/
│       └── trend_newsletter.yml    # GitHub Actions cron job (Thursday 8 AM UTC)
│
├── drizzle/
│   └── schema.ts                   # Database schema (extensible)
│
├── .env.local.example              # Environment variables template
├── GROWTH_STRATEGY.md              # Go-to-market guide (Reddit, Vercel, GitHub Secrets)
├── package.json                    # Node.js dependencies
├── tsconfig.json                   # TypeScript configuration
└── README.md                       # This file
```

---

## 🎯 Core Features

### 1. Landing Page (Next.js + Tailwind)

**Location:** `client/src/pages/Home.tsx`

- Dark-mode UI with gradient background
- Headline: "See The Next Big Trend Before It Mainstreams."
- Email capture form (powered by tRPC)
- Real-time subscriber count display
- Feature highlights (Deep Research, Weekly Insights, Actionable)
- Responsive design (mobile-first)

**Styling:** Tailwind CSS with custom dark theme
- Primary color: Emerald (#10b981)
- Background: Slate-950 gradient
- Accessible typography and contrast

### 2. Email Subscription API (tRPC)

**Location:** `server/routers.ts`

**Procedures:**

- `newsletter.subscribe` - Adds email to Resend Audience
  - Input: `{ email: string }`
  - Output: `{ success: boolean }`
  - Validation: Email format required

- `newsletter.getSubscriberCount` - Fetches subscriber count from Resend
  - Output: `{ count: number }`
  - Used for social proof on landing page

### 3. Python Automation Engine

**Location:** `scripts/trend_newsletter.py`

**Workflow:**

1. **GitHub Scraping** (`GitHubTrendingScraper`)
   - Scrapes `https://github.com/trending`
   - Extracts top 3 repositories
   - Captures: name, URL, description, star count

2. **AI Synthesis** (`TrendForecaster`)
   - Sends scraped data to OpenAI GPT-4o-mini
   - System prompt: "Trend Forecaster" role
   - Output: 400-word HTML newsletter
   - Identifies 1 macro-trend with 3 data points

3. **Email Distribution** (`ResendDistributor`)
   - Fetches all subscriber emails from Resend Audience
   - Sends HTML newsletter to all subscribers
   - Includes unsubscribe link and footer

**Error Handling:**
- Graceful fallbacks if scraping fails
- Logs all operations to stdout
- Exits with status code 1 on critical errors

### 4. GitHub Actions Automation

**Location:** `.github/workflows/trend_newsletter.yml`

**Schedule:** Every Thursday at 8:00 AM UTC

```yaml
cron: "0 8 * * 4"  # 0 hours, 8 minutes, any day, any month, Thursday (4)
```

**Workflow Steps:**
1. Check out repository
2. Set up Python 3.11
3. Install dependencies (requests, beautifulsoup4)
4. Run `scripts/trend_newsletter.py`
5. Notify on failure (optional)

**Manual Trigger:**
- Use `workflow_dispatch` to run manually from GitHub Actions tab

**Environment Variables:**
- All secrets injected from GitHub Secrets
- No credentials in YAML file

---

## 🔐 Environment Variables

### Required for Production

| Variable | Source | Purpose |
|----------|--------|---------|
| `OPENAI_API_KEY` | https://platform.openai.com/api-keys | GPT-4o-mini synthesis |
| `RESEND_API_KEY` | https://resend.com/api-keys | Email API |
| `RESEND_AUDIENCE_ID` | https://resend.com/audiences | Subscriber list ID |

### Optional (for Reddit Integration)

| Variable | Source | Purpose |
|----------|--------|---------|
| `REDDIT_CLIENT_ID` | https://www.reddit.com/prefs/apps | Reddit API authentication |
| `REDDIT_CLIENT_SECRET` | https://www.reddit.com/prefs/apps | Reddit API authentication |

### Auto-Populated by Platform

- `DATABASE_URL`, `JWT_SECRET`, `VITE_APP_ID`, `OAUTH_SERVER_URL`, etc.

---

## 📊 API Endpoints

### tRPC Procedures

All endpoints are under `/api/trpc`

**Subscribe to Newsletter:**
```bash
curl -X POST http://localhost:3000/api/trpc/newsletter.subscribe \
  -H "Content-Type: application/json" \
  -d '{"json":{"email":"user@example.com"}}'
```

**Get Subscriber Count:**
```bash
curl http://localhost:3000/api/trpc/newsletter.getSubscriberCount
```

---

## 🧪 Testing

### Unit Tests

Run vitest:
```bash
pnpm test
```

Tests include:
- API credentials validation
- Email subscription flow
- Subscriber count retrieval

### Manual Testing

1. **Landing Page:**
   - Visit `http://localhost:3000`
   - Enter email and submit
   - Verify success toast message
   - Check Resend dashboard for new contact

2. **Python Script:**
   ```bash
   python scripts/trend_newsletter.py
   ```
   - Should complete without errors
   - Check logs for each step

3. **GitHub Actions:**
   - Go to repository → Actions tab
   - Click "Ahead of the Boom - Trend Newsletter"
   - Click "Run workflow" → "Run workflow"
   - Monitor logs for successful execution

---

## 🚢 Deployment

### Vercel (Recommended)

See `GROWTH_STRATEGY.md` for detailed Vercel deployment instructions.

**Quick Deploy:**
1. Push code to GitHub
2. Go to https://vercel.com/new
3. Import your GitHub repository
4. Add environment variables
5. Deploy

**Live URL:** `https://ahead-of-the-boom.vercel.app` (or custom domain)

### GitHub Actions

1. Add secrets to GitHub repository (Settings → Secrets and variables → Actions)
2. Workflow runs automatically every Thursday at 8 AM UTC
3. Or manually trigger from Actions tab

---

## 📈 Growth Strategy

See `GROWTH_STRATEGY.md` for:

1. **Reddit "Trojan Horse" Strategy**
   - Post template for r/Entrepreneur
   - Engagement tactics
   - Conversion optimization

2. **Vercel Deployment Guide**
   - Step-by-step instructions
   - Custom domain setup
   - Troubleshooting

3. **GitHub Secrets Setup**
   - How to add secrets
   - Workflow testing
   - Troubleshooting

4. **Scaling Roadmap**
   - Phase 1: Foundation (Weeks 1-4)
   - Phase 2: Growth (Months 2-3)
   - Phase 3: Monetization (Month 4+)

---

## 🐛 Troubleshooting

### Landing Page Issues

**Email subscription fails:**
- Check `RESEND_API_KEY` and `RESEND_AUDIENCE_ID` in `.env.local`
- Verify Resend API key is valid: `curl -H "Authorization: Bearer YOUR_KEY" https://api.resend.com/audiences`
- Check browser console for error messages

**Subscriber count shows 0:**
- Verify Resend Audience ID is correct
- Check Resend dashboard to confirm audience exists
- Try refreshing the page

### Python Script Issues

**Script fails with "Missing environment variables":**
```bash
export OPENAI_API_KEY="your_key"
export RESEND_API_KEY="your_key"
export RESEND_AUDIENCE_ID="your_id"
python scripts/trend_newsletter.py
```

**GitHub scraping returns empty:**
- Check internet connection
- Verify BeautifulSoup is installed: `pip install beautifulsoup4`
- Try running manually to see detailed error logs

**OpenAI API fails:**
- Verify API key is valid and has credits
- Check rate limits: https://platform.openai.com/account/rate-limits
- Ensure model `gpt-4o-mini` is available in your account

### GitHub Actions Issues

**Workflow doesn't run on schedule:**
- Ensure at least one commit in the past 60 days
- Check that cron syntax is correct: `"0 8 * * 4"`
- Verify secrets are added to repository (not organization)

**Workflow fails with "Secret not found":**
- Check secret names are exact (case-sensitive)
- Verify secrets are in the correct repository
- Redeploy after adding new secrets

---

## 📝 License

MIT License - See LICENSE file for details

---

## 🤝 Contributing

To extend this project:

1. **Add Reddit Scraping:**
   - Uncomment Reddit code in `scripts/trend_newsletter.py`
   - Add `REDDIT_CLIENT_ID` and `REDDIT_CLIENT_SECRET` to GitHub Secrets

2. **Customize AI Synthesis:**
   - Edit `system_prompt` in `TrendForecaster` class
   - Adjust `max_tokens` and `temperature` for different output styles

3. **Change Email Template:**
   - Modify `email_template` in `ResendDistributor.send_newsletter()`
   - Test with Resend email preview

4. **Adjust Schedule:**
   - Change cron in `.github/workflows/trend_newsletter.yml`
   - Format: `"minute hour day month weekday"`

---

## 📞 Support

For issues or questions:

1. Check `GROWTH_STRATEGY.md` for common solutions
2. Review GitHub Actions logs for automation errors
3. Test Python script locally with verbose logging
4. Verify all API keys are valid and have correct permissions

---

## 🎯 Next Steps

1. **Deploy landing page to Vercel** (see GROWTH_STRATEGY.md)
2. **Add GitHub Secrets** (see GROWTH_STRATEGY.md)
3. **Test GitHub Actions workflow** manually
4. **Post on Reddit** using Trojan Horse template (see GROWTH_STRATEGY.md)
5. **Monitor subscriber growth** and engagement
6. **Iterate on AI synthesis** based on feedback

---

**Built with:** Next.js, Tailwind CSS, tRPC, Python, OpenAI, Resend, GitHub Actions

**Last Updated:** April 2026

Good luck with Ahead of the Boom! 🚀
