# Ahead of the Boom - Growth Strategy

This document outlines the go-to-market strategy for the Ahead of the Boom trend-spotting newsletter, including community engagement tactics, deployment instructions, and operational setup.

---

## Part 1: The "Trojan Horse" Reddit Strategy

### Objective

Build credibility and acquire early subscribers by providing genuine value on r/Entrepreneur without explicit self-promotion. Position yourself as a thought leader sharing insights, not a marketer pushing a product.

### The Trojan Horse Framework

A "Trojan Horse" post is one that:
1. Solves a real problem the community faces
2. Provides actionable, immediately useful content
3. Subtly demonstrates your unique capability
4. Includes a soft call-to-action (newsletter mention, not a hard sell)

### Reddit Post Template for r/Entrepreneur

**Title:**
```
I analyzed 6 months of GitHub trending data + Reddit discussions. Here's the ONE macro-trend 
that will define 2026 for bootstrapped founders.
```

**Body:**
```
I spent the last 6 months building a system to identify emerging tech trends before they hit 
the mainstream. Here's what I found by analyzing GitHub trending repos + top discussions across 
tech communities.

## The Macro-Trend: [INSERT TREND FROM YOUR LATEST NEWSLETTER]

### Why It Matters for Founders

[2-3 paragraphs explaining the trend and its business implications]

### The Data Points

1. **Point 1:** [Specific GitHub repo or discussion trend with link]
   - Why it matters: [Founder-focused insight]

2. **Point 2:** [Another data point]
   - Why it matters: [Founder-focused insight]

3. **Point 3:** [Third data point]
   - Why it matters: [Founder-focused insight]

### How to Capitalize on This

[Actionable advice for founders to leverage this trend]

---

**P.S.** I've been tracking these trends systematically and sending a weekly synthesis to a small 
group of founders. If you want to stay ahead of the curve, I'm sharing the full analysis 
(including the data sources and my reasoning) in a free weekly newsletter. DM me or comment 
below if you want in.

---

### Posting Strategy

1. **Post on Tuesday-Wednesday** (peak activity on r/Entrepreneur)
2. **Engage in comments for the first 2 hours** (Reddit's algorithm rewards early engagement)
3. **Answer every question** (builds credibility and shows you're not just promoting)
4. **Mention the newsletter naturally** in responses to interested users
5. **Never post the same trend twice** (rotate your insights; keep it fresh)
6. **Frequency:** 1-2 posts per month maximum (avoid spam perception)

### Success Metrics

- Target: 50-100 upvotes (indicates community resonance)
- Target: 20-30 comments (shows genuine engagement)
- Expected conversion: 5-10% of engaged users subscribe
- Expected subscribers per post: 3-8 new subscribers

---

## Part 2: Vercel Deployment Instructions

### Prerequisites

- Vercel account (free tier is sufficient): https://vercel.com
- GitHub repository with your Next.js code pushed
- All environment variables configured in GitHub Secrets

### Step-by-Step Deployment

#### Step 1: Connect Your GitHub Repository to Vercel

1. Go to https://vercel.com/new
2. Click "Import Project"
3. Select "Import Git Repository"
4. Paste your GitHub repository URL: `https://github.com/yourusername/trend-newsletter`
5. Click "Continue"

#### Step 2: Configure Project Settings

1. **Project Name:** `ahead-of-the-boom` (or your preferred name)
2. **Framework Preset:** Select "Next.js"
3. **Root Directory:** Leave as default (`.`)
4. **Build Command:** Leave as default (`npm run build` or `pnpm build`)
5. **Output Directory:** Leave as default (`.next`)
6. **Install Command:** Leave as default

#### Step 3: Add Environment Variables

1. Under "Environment Variables," add the following:
   - `RESEND_API_KEY` → (paste your Resend API key)
   - `RESEND_AUDIENCE_ID` → (paste your Resend Audience ID)
   - `OPENAI_API_KEY` → (paste your OpenAI API key)
   - `VITE_APP_TITLE` → `Ahead of the Boom`

2. Click "Deploy"

#### Step 4: Wait for Build Completion

- Vercel will automatically build and deploy your Next.js app
- You'll see a live URL: `https://ahead-of-the-boom.vercel.app` (or similar)
- Deployment typically takes 2-5 minutes

#### Step 5: Verify Deployment

1. Visit your live URL
2. Test the email subscription form
3. Check that the subscriber count displays correctly

#### Step 6: Set Up Custom Domain (Optional)

1. In Vercel dashboard, go to your project → Settings → Domains
2. Click "Add Domain"
3. Enter your custom domain (e.g., `aheadoftheboom.com`)
4. Follow Vercel's DNS configuration instructions
5. Update your domain registrar's nameservers

### Troubleshooting

**Build fails with "Module not found":**
- Ensure all dependencies are listed in `package.json`
- Run `pnpm install` locally and commit `pnpm-lock.yaml`

**Environment variables not working:**
- Verify they're added in Vercel Settings → Environment Variables
- Redeploy after adding new variables

**Email subscription not working:**
- Check that `RESEND_API_KEY` and `RESEND_AUDIENCE_ID` are correct
- Test the API locally: `curl -H "Authorization: Bearer YOUR_KEY" https://api.resend.com/audiences/YOUR_ID`

---

## Part 3: GitHub Secrets Setup Guide

### Why GitHub Secrets?

GitHub Secrets securely store sensitive credentials (API keys) so they can be used by GitHub Actions workflows without exposing them in your code or logs.

### Step-by-Step GitHub Secrets Configuration

#### Step 1: Navigate to Your Repository Settings

1. Go to your GitHub repository
2. Click **Settings** (top menu)
3. In the left sidebar, click **Secrets and variables** → **Actions**

#### Step 2: Add Each Secret

Click **New repository secret** and add the following secrets one by one:

**Secret 1: OPENAI_API_KEY**
- **Name:** `OPENAI_API_KEY`
- **Value:** Paste your OpenAI API key (starts with `sk-proj-`)
- Click **Add secret**

**Secret 2: RESEND_API_KEY**
- **Name:** `RESEND_API_KEY`
- **Value:** Paste your Resend API key (starts with `re_`)
- Click **Add secret**

**Secret 3: RESEND_AUDIENCE_ID**
- **Name:** `RESEND_AUDIENCE_ID`
- **Value:** Paste your Resend Audience ID (UUID format)
- Click **Add secret**

**Secret 4: REDDIT_CLIENT_ID** (Optional, for future Reddit integration)
- **Name:** `REDDIT_CLIENT_ID`
- **Value:** Paste your Reddit app's client ID
- Click **Add secret**

**Secret 5: REDDIT_CLIENT_SECRET** (Optional, for future Reddit integration)
- **Name:** `REDDIT_CLIENT_SECRET`
- **Value:** Paste your Reddit app's client secret
- Click **Add secret**

#### Step 3: Verify Secrets Are Added

1. Refresh the Secrets page
2. You should see all 5 secrets listed (values are hidden)
3. If any are missing, add them now

#### Step 4: Test GitHub Actions Workflow

1. Go to **Actions** tab in your repository
2. Click **Ahead of the Boom - Trend Newsletter** workflow
3. Click **Run workflow** → **Run workflow** (to test manually)
4. Wait for the workflow to complete (should take 1-2 minutes)
5. If successful, you'll see a green checkmark ✓

### Viewing Workflow Logs

1. Go to **Actions** tab
2. Click the most recent workflow run
3. Click **send-newsletter** job
4. Expand **Run trend newsletter script** to see logs

### Troubleshooting GitHub Actions

**Workflow fails with "Secret not found":**
- Verify the secret name matches exactly (case-sensitive)
- Ensure you added it to the correct repository (not organization-level)

**Workflow fails with "API Error":**
- Check that your API keys are valid and have not expired
- Verify the API key has the correct permissions
- Check Resend and OpenAI dashboards for usage limits

**Workflow never runs on schedule:**
- GitHub Actions requires at least one commit in the past 60 days to run scheduled workflows
- Make a small commit to re-enable scheduling

---

## Part 4: Operational Checklist

### Before First Newsletter Send

- [ ] Landing page deployed to Vercel
- [ ] Email subscription form tested end-to-end
- [ ] Resend API key validated
- [ ] OpenAI API key validated
- [ ] GitHub Secrets configured (all 5 secrets added)
- [ ] GitHub Actions workflow tested manually
- [ ] Python script tested locally with `.env.local`

### Weekly Operations

- [ ] Monitor GitHub Actions workflow logs (every Thursday after 8 AM UTC)
- [ ] Check Resend dashboard for email delivery stats
- [ ] Monitor subscriber growth on landing page
- [ ] Respond to new subscriber inquiries
- [ ] Analyze Reddit post performance (if posting)

### Monthly Operations

- [ ] Review subscriber engagement (open rates, click rates)
- [ ] Analyze which trends resonated most
- [ ] Adjust AI synthesis prompt based on feedback
- [ ] Plan next month's Reddit posts
- [ ] Monitor API costs (OpenAI, Resend)

---

## Part 5: Scaling Strategy

### Phase 1: Foundation (Weeks 1-4)
- Launch landing page
- Send first 4 newsletters
- Acquire first 50-100 subscribers
- Post 1-2 Reddit posts

### Phase 2: Growth (Months 2-3)
- Expand to LinkedIn and Twitter/X (repurpose newsletter content)
- Add Reddit scraping (once app is approved)
- Implement email analytics dashboard
- Target 500+ subscribers

### Phase 3: Monetization (Month 4+)
- Launch paid tier (advanced insights, API access)
- Partner with relevant SaaS tools
- Sponsorship opportunities
- Target 2,000+ subscribers

---

## Part 6: FAQ

**Q: How do I update the newsletter content format?**
A: Edit the `system_prompt` in `scripts/trend_newsletter.py` to change how the AI synthesizes trends.

**Q: Can I run the newsletter more frequently than weekly?**
A: Yes, modify the cron schedule in `.github/workflows/trend_newsletter.yml`. Change `"0 8 * * 4"` to your desired schedule.

**Q: What if the GitHub Actions workflow fails?**
A: Check the workflow logs in the Actions tab. Common issues: invalid API keys, rate limiting, or network errors. Verify secrets are correct and retry.

**Q: How do I add Reddit scraping?**
A: Once your Reddit app is approved, add `REDDIT_CLIENT_ID` and `REDDIT_CLIENT_SECRET` to GitHub Secrets, then uncomment the Reddit scraping code in `scripts/trend_newsletter.py`.

**Q: Can I customize the email template?**
A: Yes, modify the `email_template` variable in `scripts/trend_newsletter.py` to change the HTML styling and layout.

---

## Contact & Support

For questions or issues:
1. Check GitHub Issues in your repository
2. Review Vercel deployment logs
3. Test the Python script locally with `python scripts/trend_newsletter.py`
4. Verify all environment variables are set correctly

Good luck with Ahead of the Boom! 🚀
