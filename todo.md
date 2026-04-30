# Ahead of the Boom - Project TODO

## Frontend (Next.js + Tailwind)
- [x] Build dark-mode landing page with headline "See The Next Big Trend Before It Mainstreams"
- [x] Create email capture form component
- [x] Build tRPC procedure `newsletter.subscribe` to add emails to Resend Audience
- [x] Display subscriber count on landing page (fetched from Resend API via `newsletter.getSubscriberCount`)
- [x] Test email submission flow end-to-end

## Backend (Python Automation)
- [x] Create `scripts/trend_newsletter.py` with modular structure
- [ ] Implement Reddit scraper (PRAW OAuth2 - pending Reddit app approval)
- [x] Implement GitHub scraper (BeautifulSoup for top 3 trending repositories)
- [x] Integrate OpenAI GPT-4o-mini for Trend Forecaster synthesis (400-word HTML newsletter)
- [x] Integrate Resend Python SDK for email distribution to Audience
- [ ] Test automation script locally with .env.local (pending Reddit credentials)

## GitHub Actions & Automation
- [x] Create `.github/workflows/trend_newsletter.yml` with Thursday 8:00 AM UTC cron
- [x] Add `workflow_dispatch` trigger for manual testing
- [x] Map all environment variables to GitHub Secrets

## Documentation
- [x] Write GROWTH_STRATEGY.md with:
  - [x] Trojan Horse Reddit post template for r/Entrepreneur
  - [x] Step-by-step Vercel deployment instructions
  - [x] GitHub Secrets setup guide
- [x] Create .env.local.example template file
- [x] Create comprehensive README.md

## Delivery
- [x] Verify all files are production-ready
- [ ] Create checkpoint
- [ ] Deliver complete project structure to user
