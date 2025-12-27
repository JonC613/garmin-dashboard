# Garmin Dashboard - Cloud Deployment Guide

## Deployment Options

### Option 1: Vercel (Frontend) + Railway (Backend + Database) - RECOMMENDED

#### Frontend on Vercel (Free Tier)
1. Push code to GitHub
2. Visit [vercel.com](https://vercel.com)
3. Import your GitHub repository
4. Vercel auto-detects the frontend and deploys

#### Backend + Database on Railway (Free $5/month credit)
1. Visit [railway.app](https://railway.app)
2. Connect GitHub repository
3. Deploy backend + PostgreSQL with one click

---

### Option 2: Render (All-in-One - Free Tier)

Deploy everything on Render:
- Static Site (Frontend)
- Web Service (Backend)
- PostgreSQL Database

---

### Option 3: GitHub Actions + Docker (Self-hosted or Cloud)

Use GitHub Actions to build Docker images and deploy to:
- AWS ECS/Fargate
- Google Cloud Run
- Azure Container Instances
- DigitalOcean App Platform

---

## Quick Setup Files

I've created configuration files for multiple platforms:
- `vercel.json` - Frontend deployment to Vercel
- `railway.json` - Backend + DB to Railway
- `render.yaml` - Full stack to Render
- `.github/workflows/deploy.yml` - GitHub Actions CI/CD

## Environment Variables

Set these in your deployment platform:

### Backend
```
DATABASE_URL=<provided by platform>
GARMIN_EMAIL=your-email@example.com
GARMIN_PASSWORD=your-password
```

### Frontend
```
VITE_API_URL=https://your-backend-url.com
```

## Detailed Setup Instructions

See deployment guides for each platform in this file.
