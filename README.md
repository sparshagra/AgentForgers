# 📸 InstaFlowAI — Multi-Agent Automated Instagram Content Creation & Scheduler

[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18+-61DAFB?style=flat&logo=react)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-3178C6?style=flat&logo=typescript)](https://www.typescriptlang.org/)
[![LangGraph](https://img.shields.io/badge/LangGraph-AI_Agents-FF6B6B?style=flat)](https://langchain-ai.github.io/langgraph/)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

> *An AI-powered Instagram content creation and scheduling platform that automates the entire content lifecycle—from ideation to publication—using intelligent multi-agent architecture, email-based approval workflows, and automated Instagram publishing.*

### ▶️ Demo Video  
[![Watch the video](https://i.ytimg.com/vi/vd0ZHnJBj-g/hqdefault.jpg)](https://youtu.be/vd0ZHnJBj-g)


---

## 🎯 Problem Statement

Brands, creators, and businesses struggle to maintain a consistent Instagram presence due to:

### The Content Creation Bottleneck

Creating a single high-quality Instagram post requires:
- ✍️ **Caption Writing** — Engaging copy with proper tone and branding
- 🎨 **Visual Design** — Eye-catching images that align with brand identity
- 📋 **Concept Development** — Strategic planning for campaigns and festivals
- ✅ **Quality Assurance** — Brand consistency and compliance checks
- 🏷️ **Hashtag Research** — Relevant tags for maximum reach
- 📤 **Manual Publishing** — Time-consuming upload and scheduling

### Key Challenges

❌ **Time-Intensive Process**: Creating quality posts takes 2-4 hours per post  
❌ **Inconsistent Posting**: Human delays lead to missed engagement windows  
❌ **Festival Planning Nightmare**: Preparing content for Diwali, Christmas, Holi, etc. is tedious  
❌ **Team Coordination Issues**: Approval workflows cause bottlenecks  
❌ **High Outsourcing Costs**: Agencies charge premium rates with slow turnaround  
❌ **No Automation**: Most tools require manual intervention at every step

---

## ✨ Our Solution: Fully Automated Multi-Agent System

**InstagramAI** eliminates these pain points through intelligent automation powered by a multi-agent architecture that handles every step of content creation autonomously.

### 🚀 Core Features

#### 🤖 Multi-Agent AI Workflow
A coordinated team of specialized AI agents handles your content pipeline:

| Agent | Responsibility |
|-------|----------------|
| **Orchestrator** | Llama 3.2-3B-Instruct model along with Langgraph|
| **Prompt Enhancer** | Transforms raw ideas into detailed creative briefs |
| **Outliner** | Structures content framework and messaging strategy |
| **Caption Generator** | Crafts engaging captions with brand voice + hashtags |
| **Designer Agent** | Creates precise image generation prompts |
| **Compliance Agent** | Enforces safety guidelines and brand standards |
| **Critic Agent** | Reviews and iteratively improves all outputs |
| **Image Generator** | Produces final branded visuals using FLUX model |
| **Logo Dropper** | Seamlessly integrates brand logo overlays |
| **Publisher** | Automates Instagram posting with metadata |

#### 🎭 Dual Workflow Modes

**A) "Create Now" — Real-Time Manual Mode**

Perfect for creators who need instant content:

```
User Input → AI Processing → Live Timeline → Review → Publish
```

✅ **Live Agent Timeline**: Watch each agent work in real-time  
✅ **Instant Preview**: See caption + image before publishing  
✅ **One-Click Actions**: Publish, Regenerate, or Abort  
✅ **Full Transparency**: Every agent's reasoning displayed

**B) "Schedule Campaigns" — Festival Automation**

Ideal for brands planning seasonal content:

```
Select Festival → Auto-Schedule → AI Generation (T-48h) → Email Approval → Auto-Publish
```

✅ **48-Hour Lead Time**: Content ready 2 days before events  
✅ **Email Approval System**: Review via inbox with embedded previews  
✅ **Zero Manual Work**: Fully automated from generation to posting  
✅ **Campaign Calendar**: Manage multiple festival posts simultaneously

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      FRONTEND LAYER                         │
│           React + TypeScript + Tailwind CSS                 │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │    Login     │  │   Create Now │  │   Scheduler  │       │
│  │   Register   │  │   Timeline   │  │   Calendar   │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
│  ┌──────────────┐  ┌──────────────┐                         │
│  │    Brand     │  │   Settings   │                         │
│  │   Manager    │  │    Panel     │                         │
│  └──────────────┘  └──────────────┘                         │
└────────────────────────┬────────────────────────────────────┘
                         │ REST API (JSON)
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                      BACKEND LAYER                          │
│                  FastAPI + Python 3.10+                     │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │     User     │  │    Brand     │  │   Workflow   │       │
│  │  Management  │  │   Storage    │  │   Executor   │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │   Scheduler  │  │    Email     │  │  Instagram   │       │
│  │    Engine    │  │   Approval   │  │  Publisher   │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   AI MULTI-AGENT CORE                       │
│                  LangGraph Orchestration                    │
│                                                             │
│   Prompt Enhancer → Critic → Outliner → Caption Generator   │
│        ↓                                      ↓             │
│   Designer Agent → Compliance → Image Generator             │
│        ↓                                      ↓             │
│   Logo Dropper → Publisher → Instagram API                  │
└─────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   EXTERNAL SERVICES                         │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │ HuggingFace  │  │    Gmail     │  │  Instagram   │       │
│  │  FLUX Model  │  │     SMTP     │  │     API      │       │
│  │   Llama LLM  │  │              │  │              │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
└─────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Technology Stack

### Backend Technologies
| Technology | Version | Purpose |
|-----------|---------|---------|
| **FastAPI** | Latest | High-performance REST API framework |
| **LangGraph** | Latest | Multi-agent workflow orchestration |
| **LangChain** | Latest | AI agent coordination and chaining |
| **HuggingFace FLUX** | Latest | State-of-the-art image generation |
| **Python Pillow** | Latest | Image processing and logo overlay |
| **SMTP (Gmail)** | - | Email-based approval system |
| **APScheduler** | Latest | Cron-like job scheduling |
| **Instagram API** | - | Automated post publishing |

### Frontend Technologies
| Technology | Version | Purpose |
|-----------|---------|---------|
| **React** | 18+ | Component-based UI framework |
| **TypeScript** | 5.0+ | Type-safe JavaScript development |
| **Vite** | Latest | Lightning-fast build tool |
| **Tailwind CSS** | Latest | Utility-first styling |
| **Shadcn UI** | Latest | Accessible component library |
| **React Router** | Latest | Client-side routing |
| **Sonner** | Latest | Toast notifications |
| **Lucide Icons** | Latest | Beautiful icon library |

---

## 📂 Project Structure

```
InstagramAI/
│
├─                       # Python FastAPI backend
│   ├── app.py                        # Main FastAPI application
│   ├── orchestrator.py               # LangGraph multi-agent coordinator
│   ├── agents.py                     # Individual AI agent definitions
│   ├── tools.py                      # Utility functions for agents
│   ├── image_api.py                  # HuggingFace FLUX integration
│   ├── llm_api.py                    # HuggingFace Llama integratoin
│   ├── email_sender.py               # Gmail SMTP email system
│   ├── scheduler_utils.py            # Scheduling logic
│   ├── scheduler_runner.py           # Cron job executor
│   ├── publisher.py                  # Instagram API wrapper
│   ├── user_utils.py                 # User authentication & management
│   ├── requirements.txt              # Python dependencies
│   ├── outputs/                      # Generated images storage
│   │   └── {user_id}/
│   │       └── {post_id}.png
│   └── users/                        # User data and brand info
│       └── {username}.json
│
└── frontend/                         # React TypeScript frontend
    ├── src/
    │   ├── App.tsx                   # Main application component
    │   ├── main.tsx                  # Application entry point
    │   ├── pages/                    # Route-level components
    │   │   ├── Auth.tsx              # Login/Register page
    │   │   ├── Dashboard.tsx         # Main dashboard
    │   │   ├── Create.tsx            # Manual creation interface
    │   │   ├── Scheduler.tsx         # Campaign scheduler
    │   │   ├── Settings.tsx          # Brand settings panel
    │   │   └── NotFound.tsx          # 404 error page
    │   ├── components/               # Reusable UI components
    │   │   ├── TimelineViewer.tsx
    │   │   ├── CampaignCard.tsx
    │   │   └── BrandForm.tsx
    │   ├── contexts/                 # React Context providers
    │   │   └── AuthContext.tsx
    │   ├── styles/                   # Global styles
    │   └── types/                    # TypeScript definitions
    ├── package.json
    ├── tsconfig.json
    └── vite.config.ts
```

---

## 🚀 Quick Start

### Prerequisites

Before you begin, ensure you have:
- **Python 3.10+** installed ([Download](https://www.python.org/downloads/))
- **Node.js 16+** and npm ([Download](https://nodejs.org/))
- **HuggingFace Account** ([Sign up](https://huggingface.co/join))
- **Gmail Account** with App Password ([Setup Guide](https://support.google.com/accounts/answer/185833))

---

### 🔧 Step 1: Backend Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/InstagramAI.git
cd InstagramAI/backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env

# Edit .env with your credentials:
# HF_TOKEN_3=your_huggingface_token_here
# EMAIL_ID=your@gmail.com
# EMAIL_APP_PASSWORD=your_16_char_app_password

# Start the backend server
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

**✅ Backend running at:** http://localhost:8000  
**📚 API Documentation:** http://localhost:8000/docs

---

### 🎨 Step 2: Frontend Setup

```bash
# Open new terminal window
cd frontend

# Install dependencies
npm install

# Create environment file
cp .env.example .env

# Edit .env:
# VITE_API_BASE_URL=http://localhost:8000

# Start development server
npm run dev
```

**✅ Frontend running at:** http://localhost:5173 (or the link you find in terminal)

---

### 🎯 Step 3: First-Time Configuration

1. **Open your browser** → http://localhost:xxxx (check your terminal for exact link)
2. **Register a new account** with email and password
3. **Configure your brand**:
   - Upload logo (PNG with transparency recommended)
   - Add brand description
   - Set brand voice/tone
   - Define visual style preferences
4. **You're ready to create content!**

---

## 📡 API Reference

### Authentication Endpoints

#### Register New User
```http
POST /register
Content-Type: application/json

{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "secure_password"
}
```

#### User Login
```http
POST /login
Content-Type: application/json

{
  "username": "johndoe",
  "password": "secure_password"
}
```

---

### Brand Management

#### Update Brand Information
```http
POST /user/update_brand
Content-Type: application/json

{
  "username": "johndoe",
  "brand_name": "TechCorp",
  "brand_description": "Innovative tech solutions for modern businesses",
  "brand_voice": "Professional yet friendly",
  "logo_path": "/uploads/logos/techcorp_logo.png"
}
```

#### Fetch Brand Data
```http
GET /user/fetch?username=johndoe
```

---

### Manual Content Creation

#### Run Workflow (Create Now)
```http
POST /run_workflow
Content-Type: application/json

{
  "username": "johndoe",
  "user_prompt": "Create a post about our new AI product launch",
  "brand_context": "TechCorp - AI innovation company"
}
```

**Response:**
```json
{
  "workflow_id": "wf_12345",
  "status": "processing",
  "timeline": [
    {"agent": "PromptEnhancer", "status": "completed", "output": "..."},
    {"agent": "CriticAgent", "status": "in_progress"}
  ]
}
```

#### Publish Content
```http
POST /workflow/publish
Content-Type: application/json

{
  "workflow_id": "wf_12345",
  "username": "johndoe"
}
```

#### Regenerate Content
```http
POST /workflow/regenerate
Content-Type: application/json

{
  "workflow_id": "wf_12345",
  "username": "johndoe",
  "feedback": "Make the caption more energetic"
}
```

#### Abort Workflow
```http
POST /workflow/abort
Content-Type: application/json

{
  "workflow_id": "wf_12345"
}
```

---

### Scheduled Campaigns

#### Create Campaign
```http
POST /scheduler/create
Content-Type: application/json

{
  "username": "johndoe",
  "festival": "Diwali",
  "date": "2024-11-01",
  "instructions": "Focus on festive discounts and family values",
  "trigger_time": "48h_before"
}
```

#### Run Due Campaigns
```http
GET /scheduler/run_due
```

#### Campaign Actions (via Email Links)
```http
GET /scheduler/publish/{campaign_id}
GET /scheduler/regenerate/{campaign_id}
GET /scheduler/abort/{campaign_id}
```

---

## 🤖 Multi-Agent Workflow Deep Dive
Our System uses LLM to make decisions for the next Agent selection. 
For now we have enforced conditions so that it goes in a controlled order.

### Agent Execution Flow
This is controlled by LLM. We have enforced certain constraints so that it proceeds in the provided order. This can be changed for even more agents in future scope.

```
┌─────────────────────────────────────────────────────────────┐
│                    USER INPUT                               │
│  "Create a post about our eco-friendly product line"        │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ AGENT 1: PROMPT ENHANCER                                    │
│ Transforms: "eco-friendly products"                         │
│ Into: "Showcase our sustainable product collection with     │
│        emphasis on environmental impact, using natural      │
│        earth tones and botanical elements"                  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ AGENT 2: CRITIC AGENT                                       │
│ Reviews: Enhanced prompt                                    │
│ Provides: Suggestions for clarity and brand alignment       │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ AGENT 3: OUTLINER                                           │
│ Creates: Structured content plan                            │
│ • Hero message: Sustainability leadership                   │
│ • Key points: Product features, eco-benefits                │
│ • CTA: Shop now with discount code                          │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ AGENT 4: CAPTION GENERATOR                                  │
│ Produces:                                                   │
│ • Headline: "🌿 Meet Our Earth-Friendly Collection"        │
│ • Body: Engaging 3-paragraph caption                        │
│ • Hashtags: #Sustainable #EcoFriendly #GreenLiving          │
│ • CTA: "Shop now - Link in bio 🛒"                         │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ AGENT 5: DESIGNER AGENT                                     │
│ Creates image prompt:                                       │
│ "Professional product photography of eco-friendly items     │
│  arranged on natural wood surface with green plants,        │
│  soft natural lighting, minimalist aesthetic, earth tones"  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ AGENT 6: COMPLIANCE AGENT                                   │
│ Checks:                                                     │
│ ✓ No offensive language                                     │
│ ✓ No misleading claims                                      │
│ ✓ Brand guidelines followed                                 │
│ ✓ Hashtag limits respected                                  │
│ Status: APPROVED ✅                                         │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ AGENT 7: IMAGE GENERATOR                                    │
│ Uses: HuggingFace FLUX Model                                │
│ Generates: High-quality 1080x1080px image                   │
│ Output: /outputs/johndoe/post_12345.png                     │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ AGENT 8: LOGO DROPPER                                       │
│ Overlays: Brand logo on bottom-right corner                 │
│ Ensures: Proper opacity and positioning                     │
│ Saves: Final branded image                                  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ AGENT 9: PUBLISHER                                          │
│ Actions:                                                    │
│ • Uploads image to Instagram                                │
│ • Posts caption with hashtags                               │
│ • Tags location (if provided)                               │
│ • Notifies user of success                                  │
└─────────────────────────────────────────────────────────────┘
```

### Real-Time Timeline View

When you click "Create Now", the frontend displays a live timeline showing:
- ⏳ **In Progress**: Yellow indicator with animated spinner
- ✅ **Completed**: Green checkmark with agent output preview
- ❌ **Failed**: Red error with retry option
- 📊 **Overall Progress**: Percentage completion bar

---

## 📬 Email Approval System

### How It Works

1. **Campaign Triggers** at T-48 hours before scheduled date
2. **AI Workflow Executes** automatically in background
3. **Email Sent** to user with:
   - Embedded image preview
   - Full caption text
   - Hashtags list
   - Three action buttons

### Email Template

```html
Subject: 🎉 Your Diwali Post is Ready for Review!

Hi John,

Your scheduled Instagram post for Diwali is ready! Here's what we created:

[IMAGE PREVIEW]

Caption:
"✨ This Diwali, light up your home with our exclusive festive collection! 
Celebrate with style and tradition. Shop now and get 25% off sitewide.
Happy Diwali from TechCorp! 🪔"

Hashtags:
#Diwali2024 #FestiveVibes #TechCorp #Celebration #Discounts

Actions:
┌─────────────┬─────────────┬─────────────┐
│ ✅ Publish  │ 🔄 Regenerate│ ❌ Abort    │
└─────────────┴─────────────┴─────────────┘

Questions? Reply to this email!
Best, InstagramAI Team
```

### Action Buttons
- **Publish**: Posts immediately to Instagram
- **Regenerate**: Reruns workflow with same prompt
- **Abort**: Cancels the scheduled post

---

## 🛡️ Compliance & Safety Layer

### Compliance Agent Checks

Our **ComplianceAgent** enforces strict content policies:

#### ✅ Content Safety Checks
- No hate speech or discriminatory language
- No violent or graphic content
- No sexual or adult material
- No misleading medical/financial claims
- No copyright infringement

#### ✅ Brand Guidelines Enforcement
- Logo placement consistency
- Color palette adherence
- Tone of voice alignment
- Hashtag strategy compliance
- Character limit enforcement (2,200 for captions)

#### ✅ Legal Compliance
- FTC disclosure for sponsored content
- Copyright attribution for music/images
- Privacy policy compliance
- Regional content regulations

### What Happens on Failure?

If compliance check fails:
```json
{
  "status": "rejected",
  "reason": "Caption contains prohibited language",
  "suggestion": "Remove term 'guaranteed cure' and replace with 'may help improve'",
  "agent": "ComplianceAgent"
}
```

Workflow stops immediately and user is notified with actionable feedback.

---

## 🎨 Usage Examples

### Example 1: Quick Product Launch Post

**User Input:**
```
"Announce our new AI chatbot product launching tomorrow"
```

**AI Output:**

**Caption:**
```
🚀 The future of customer service is here!

Introducing ChatBot Pro - your AI-powered support assistant that never sleeps. 
Handle 1000+ queries simultaneously with human-like responses.

✨ Key Features:
• 24/7 availability
• Multi-language support
• Seamless CRM integration
• 95% accuracy rate

Launch Special: 30% off for early adopters! 
Link in bio 👆

#AI #ChatBot #TechInnovation #CustomerService #ProductLaunch
```

**Generated Image:**
- Sleek chatbot interface mockup
- Gradient background (brand colors)
- "NEW" badge overlay
- TechCorp logo bottom-right

---

### Example 2: Diwali Campaign (Scheduled)

**Configuration:**
```json
{
  "festival": "Diwali",
  "date": "2024-11-01",
  "instructions": "Traditional theme with modern twist, emphasize family and prosperity",
  "trigger": "48_hours_before"
}
```

**AI Output (Auto-generated on Oct 30):**

**Caption:**
```
✨ दीपों का त्यौहार मुबारक! ✨

This Diwali, we celebrate the triumph of light over darkness and innovation over tradition.

Our special festive collection brings together timeless elegance with cutting-edge technology. 
Perfect gifts for your loved ones!

🎁 Diwali Offer: 
• Up to 40% off storewide
• Free gift wrapping
• Express delivery available

May this festival of lights bring prosperity and joy to your family! 🪔

Shop now: [Link in bio]

#Diwali2024 #FestivalOfLights #DiwaliGifts #TechCorp #FestiveShopping #IndianFestival
```

**Generated Image:**
- Traditional diya lamps with modern tech products
- Warm golden lighting
- Rangoli pattern background
- Festive color palette

**Email sent on Oct 30** → User approves → **Auto-publishes on Nov 1**

---

## 🧪 Testing the System

### Test Workflow 1: Manual Creation

```bash
# Start both servers
# Backend: uvicorn app:app --reload
# Frontend: npm run dev

# 1. Register account via UI
# 2. Go to Settings → Upload logo + brand info
# 3. Navigate to "Create Now"
# 4. Enter prompt: "Summer sale announcement"
# 5. Watch timeline agents execute in real-time
# 6. Review generated content
# 7. Click "Publish" to post to Instagram
```

### Test Workflow 2: Scheduled Campaign

```bash
# Via API (Postman/cURL)
curl -X POST http://localhost:8000/scheduler/create \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "festival": "Christmas",
    "date": "2024-12-25",
    "instructions": "Focus on gift ideas and holiday cheer",
    "trigger_time": "48h_before"
  }'

# Response:
{
  "campaign_id": "camp_67890",
  "status": "scheduled",
  "execution_time": "2024-12-23T00:00:00Z"
}

# Manually trigger (for testing):
curl http://localhost:8000/scheduler/run_due
```

---

## 🚀 Production Deployment

### Backend Deployment (Render/Railway)

```bash
# 1. Prepare for production
pip freeze > requirements.txt

# 2. Create Procfile
echo "web: uvicorn app:app --host 0.0.0.0 --port $PORT" > Procfile

# 3. Push to GitHub
git add .
git commit -m "Production ready"
git push origin main

# 4. Deploy on Render:
# - Connect GitHub repo
# - Set environment variables (HF_TOKEN_3, EMAIL_ID, etc.)
# - Auto-deploy enabled
```

### Frontend Deployment (Vercel/Netlify)

```bash
# 1. Build production bundle
npm run build

# 2. Test locally
npm run preview

# 3. Deploy to Vercel:
vercel --prod

# Or push to GitHub and connect repo in Vercel dashboard
```

### Environment Variables (Production)

**Backend (.env):**
```bash
HF_TOKEN_3=hf_xxxxxxxxxxxxxxxxxxxx
EMAIL_ID=noreply@yourdomain.com
EMAIL_APP_PASSWORD=abcd efgh ijkl mnop
INSTAGRAM_USERNAME=your_business_account
INSTAGRAM_PASSWORD=secure_password
DATABASE_URL=postgresql://... (if using DB)
CORS_ORIGINS=https://yourapp.vercel.app
```

**Frontend (.env.production):**
```bash
VITE_API_BASE_URL=https://your-backend.onrender.com
```

---

## 🐛 Troubleshooting

### Common Issues

#### Backend won't start
```bash
# Check Python version
python --version  # Must be 3.10+

# Verify virtual environment
which python  # Should point to venv/bin/python

# Reinstall dependencies
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall

# Check environment variables
cat .env  # Ensure all required vars are set
```

#### Image generation fails
```bash
# Verify HuggingFace token
curl -H "Authorization: Bearer $HF_TOKEN_3" \
  https://huggingface.co/api/whoami

# Check model availability
# FLUX model requires ~16GB RAM minimum

# Alternative: Use Stable Diffusion instead
# Edit image_api.py and change model endpoint
```

#### Email not sending
```bash
# Test Gmail SMTP connection
python -c "
import smtplib
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login('your@gmail.com', 'your_app_password')
print('✅ Connected successfully!')
server.quit()
"

# Ensure 2FA enabled + App Password created
# Guide: https://support.google.com/accounts/answer/185833
```

#### Instagram posting fails
```bash
# Check credentials
# Verify account is not restricted/banned
# Ensure using Business/Creator account (not personal)
# Check rate limits (Instagram allows ~10-15 posts/hour)
```

#### Frontend can't connect to backend
```bash
# Verify backend is running
curl http://localhost:8000/

# Check CORS configuration in backend/app.py
# Ensure frontend origin is allowed:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://yourapp.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Check frontend .env file
cat frontend/.env
# Should contain: VITE_API_BASE_URL=http://localhost:8000

# Test API endpoint directly
curl http://localhost:8000/docs
```

#### Scheduler not triggering
```bash
# Manually trigger scheduler check
curl http://localhost:8000/scheduler/run_due

# Check system time is correct
date

# Verify campaign creation
curl http://localhost:8000/scheduler/list?username=youruser

# Check logs for errors
tail -f backend/logs/scheduler.log
```

#### LangGraph workflow stuck
```bash
# Check agent execution logs
# Each agent should complete within 30-60 seconds

# Restart workflow if timeout occurs
curl -X POST http://localhost:8000/workflow/abort \
  -H "Content-Type: application/json" \
  -d '{"workflow_id": "wf_12345"}'

# Check LangChain/LangGraph versions
pip show langgraph langchain
```

---

## 🙏 Acknowledgments

This project was made possible by incredible open-source tools and AI models:

### AI Models & Technologies

**🤖 LangChain & LangGraph**
- [LangChain](https://github.com/langchain-ai/langchain) - Framework for building LLM applications
- [LangGraph](https://github.com/langchain-ai/langgraph) - Multi-agent orchestration framework
- *Thank you to the LangChain team for revolutionizing AI agent development!*

**🎨 HuggingFace FLUX**
- [FLUX.1 Model](https://huggingface.co/black-forest-labs/FLUX.1-dev) by Black Forest Labs
- State-of-the-art text-to-image generation
- *Incredible image quality that makes our content creation possible!*

**🧠 HuggingFace Llama 3.2-3B Instruct**
- [Llama 3.2-3B Instruct](https://huggingface.co/meta-llama/Llama-3.2-3B-Instruct) by Meta
- Powerful 3B-parameter instruction-tuned model for chat, reasoning, and agent workflows
- *A compact yet highly capable LLM that powers our intelligent text generation!*

**

### Open Source Libraries

**Backend:**
- [FastAPI](https://github.com/tiangolo/fastapi) - Modern Python web framework
- [Pillow](https://github.com/python-pillow/Pillow) - Image processing library
- [APScheduler](https://github.com/agronholm/apscheduler) - Job scheduling

**Frontend:**
- [React](https://github.com/facebook/react) - UI library by Meta
- [Vite](https://github.com/vitejs/vite) - Next-generation frontend tooling
- [Tailwind CSS](https://github.com/tailwindlabs/tailwindcss) - Utility-first CSS
- [Shadcn UI](https://ui.shadcn.com/) - Beautiful accessible components
- [Lucide Icons](https://lucide.dev/) - Icon library

*Special thanks to all open-source contributors who make projects like this possible!* 💙

---

## 👥 Team

**AgentForgers**

We are passionate developers building AI-powered automation tools to empower creators and businesses.

### Team Members

**Divy Dobariya** - Backend Development & AI/ML Architecture  
- Multi-agent system design using LangGraph
- Instagram API integration & automation
- Email approval system implementation
  

**Sparsh Agarwal** - Backend Development & System Integration  
- Multi-agent system design using LangGraph
- Real-time timeline UI/UX design
- API integration and state management

---

## 📞 Contact & Support

### Get in Touch

📧 **Email**: [divydobariya11@gmail.com](mailto:divydobariya11@gmail.com)  
💼 **LinkedIn**: [Divy Dobariya](https://www.linkedin.com/in/divy-dobariya-92881423b)  

### We'd Love to Hear From You!

- 🐛 Found a bug? [Open an issue](https://github.com/yourusername/InstagramAI/issues/new)
- 💡 Have a feature idea? [Start a discussion](https://github.com/yourusername/InstagramAI/discussions/new)
- 🤝 Want to contribute? See [Contributing Guidelines](#contributing)
- ⭐ Love the project? Give us a star on GitHub!

---

## 🤝 Contributing

We welcome contributions from the community! Here's how you can help:

### Ways to Contribute

1. **Code Contributions**
   - Fork the repository
   - Create a feature branch: `git checkout -b feature/AmazingFeature`
   - Commit your changes: `git commit -m 'Add AmazingFeature'`
   - Push to branch: `git push origin feature/AmazingFeature`
   - Open a Pull Request

2. **Bug Reports**
   - Use the GitHub issue tracker
   - Include reproduction steps
   - Attach screenshots if applicable
   - Specify your environment (OS, Python/Node versions)

3. **Documentation**
   - Improve README clarity
   - Add code comments
   - Create tutorials or guides
   - Translate to other languages

4. **Testing**
   - Write unit tests
   - Test edge cases
   - Report compatibility issues

### Development Guidelines

- Follow PEP 8 for Python code
- Use ESLint/Prettier for TypeScript/React
- Write meaningful commit messages
- Update documentation for new features
- Ensure all tests pass before submitting PR

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

### MIT License Summary

```
MIT License

Copyright (c) 2024 AgentForgers - Divy Dobariya & Sparsh Agarwal

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

**What this means:**
- ✅ Commercial use allowed
- ✅ Modification allowed
- ✅ Distribution allowed
- ✅ Private use allowed
- ℹ️ License and copyright notice must be included

---

## 🌟 Star History

If you find this project useful, please consider giving it a star! ⭐

[![Star History Chart](https://api.star-history.com/svg?repos=yourusername/InstagramAI&type=Date)](https://star-history.com/#yourusername/InstagramAI&Date)

---

## 🚀 What's Next?

### Upcoming Features (Roadmap)

- [ ] **Multi-Platform Support**: Extend to Facebook, LinkedIn, Twitter
- [ ] **Advanced Analytics**: Track engagement metrics and ROI
- [ ] **AI-Powered Hashtag Optimizer**: Dynamic hashtag suggestions
- [ ] **Video Content Generation**: Support for Reels and Stories
- [ ] **Collaborative Workflows**: Team approval systems
- [ ] **Template Library**: Pre-designed post templates
- [ ] **A/B Testing**: Test different captions/images automatically
- [ ] **Competitor Analysis**: AI-powered social listening
- [ ] **Mobile App**: iOS and Android applications
- [ ] **API Access**: Let developers build on our platform

**Want to contribute to any of these?** Open an issue or PR! 🎉

---

## 💖 Show Your Support

If InstagramAI helped you or your business, consider:

- ⭐ **Starring** this repository
- 🐦 **Sharing** on social media
- 📝 **Writing** a blog post about your experience
- 💬 **Recommending** to fellow creators and developers
- ☕ **Sponsoring** our development (coming soon!)

---

## 📊 Project Stats

![GitHub stars](https://img.shields.io/github/stars/yourusername/InstagramAI?style=social)
![GitHub forks](https://img.shields.io/github/forks/yourusername/InstagramAI?style=social)
![GitHub issues](https://img.shields.io/github/issues/yourusername/InstagramAI)
![GitHub pull requests](https://img.shields.io/github/issues-pr/yourusername/InstagramAI)
![GitHub contributors](https://img.shields.io/github/contributors/yourusername/InstagramAI)

---

## 🎉 Thank You!

Thank you for checking out **InstagramAI**! We built this project with passion and dedication to help creators and businesses automate their social media presence without compromising quality.

Every feature, every line of code, and every agent was crafted with love for the community. We hope this tool empowers you to focus on what matters most - growing your brand and engaging with your audience.

**Happy Creating! 🚀✨**

---

*Built with ❤️ by AgentForgers | Powered by AI | Made for Creators*

---

<p align="center">
  <strong>⚡ Automate Your Instagram. Amplify Your Impact. ⚡</strong>
</p>

<p align="center">
  <a href="#-quick-start">Get Started</a> •
  <a href="#-demo-video">Watch Demo</a> •
  <a href="mailto:divydobariya11@gmail.com">Contact Us</a> •
  <a href="https://github.com/yourusername/InstagramAI/issues">Report Bug</a>
</p>
