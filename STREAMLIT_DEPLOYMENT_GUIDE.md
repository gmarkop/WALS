## 🚀 WALS Streamlit App - Deployment Guide for Students

This guide will help you deploy the WALS Explorer Streamlit app online so your students can access it from anywhere.

## Why Streamlit?

- ✅ **FREE** hosting on Streamlit Cloud
- ✅ **No coding required** for deployment
- ✅ **Automatic updates** when you push to GitHub
- ✅ **HTTPS included** (secure by default)
- ✅ **No server management** needed
- ✅ **Perfect for education** - unlimited free public apps

---

## Quick Deployment (5 Minutes)

### Step 1: Ensure Code is on GitHub

Your code is already in this repository. Just make sure it's pushed:

```bash
git status  # Check status
git add .   # If there are changes
git commit -m "Add Streamlit app"
git push
```

### Step 2: Go to Streamlit Cloud

1. Visit: **https://share.streamlit.io**
2. Click **"Sign in"** (top right)
3. Choose **"Continue with GitHub"**
4. Authorize Streamlit to access your repositories

### Step 3: Deploy Your App

1. Click **"New app"** button
2. Fill in the form:
   - **Repository**: Select `your-username/WALS`
   - **Branch**: `main` (or your branch name)
   - **Main file path**: `streamlit_app/Home.py`
3. Click **"Deploy!"**

### Step 4: Wait (2-3 minutes)

Streamlit will:
- Clone your repository
- Install dependencies from `requirements.txt`
- Start your app
- Give you a public URL

### Step 5: Share with Students!

Your app will be live at:
```
https://your-github-username-wals-streamlitapp-home-abc123.streamlit.app
```

**Copy this URL and share it with your students!**

---

## Detailed Instructions

### What Happens During Deployment?

1. **Streamlit Cloud clones your repo** from GitHub
2. **Installs Python packages** listed in `streamlit_app/requirements.txt`:
   - `streamlit` - Web framework
   - `pandas` - Data manipulation
   - `plotly` - Interactive charts
   - `pydeck` - Map visualization
3. **Runs your app** using `streamlit run Home.py`
4. **Provides a public URL** for access

### App Configuration

The app is pre-configured in `.streamlit/config.toml`:

```toml
[theme]
primaryColor="#3498db"         # Blue accent color
backgroundColor="#ffffff"       # White background
secondaryBackgroundColor="#f0f2f6"  # Light gray sidebar

[server]
headless = true               # Required for deployment
enableCORS = false            # Security setting
```

You can customize colors by editing this file!

---

## Customization

### Change the App Title

Edit `streamlit_app/Home.py`:

```python
st.set_page_config(
    page_title="My Custom WALS Explorer",  # Change this
    page_icon="🌍",
    layout="wide"
)
```

### Change Colors

Edit `streamlit_app/.streamlit/config.toml`:

```toml
[theme]
primaryColor="#e74c3c"  # Red instead of blue
```

### Add Your Institution's Branding

Add to `streamlit_app/Home.py` after the title:

```python
st.image("your-logo.png", width=200)
st.markdown("### Department of Linguistics • Your University")
```

---

## Managing Your Deployed App

### View App Status

1. Go to https://share.streamlit.io
2. Click on your app
3. See:
   - Current status (Running/Stopped)
   - Number of users
   - Resource usage
   - Logs

### Update Your App

Just push to GitHub:

```bash
# Make your changes
git add .
git commit -m "Update app"
git push
```

**Streamlit Cloud automatically redeploys!** (Takes 1-2 minutes)

### View Logs

If something goes wrong:
1. Go to your app on Streamlit Cloud
2. Click "Manage app"
3. Click "Logs"
4. See error messages

### Restart Your App

If the app is stuck:
1. Go to your app on Streamlit Cloud
2. Click "⋮" (three dots)
3. Click "Reboot app"

---

## Sharing with Students

### Option 1: Direct Link

Share the URL directly:
```
https://your-app.streamlit.app
```

Students just click and use - no login required!

### Option 2: QR Code

1. Go to https://qr-code-generator.com
2. Enter your Streamlit app URL
3. Download the QR code
4. Add to your syllabus or slides

### Option 3: Embed in LMS

#### Canvas:
1. Add a new page
2. Click "Edit"
3. Click "Insert" > "Embed"
4. Paste your Streamlit URL

#### Moodle:
1. Add an activity or resource
2. Choose "URL"
3. Enter your Streamlit URL

#### Google Classroom:
1. Create an assignment
2. Add a link
3. Paste your Streamlit URL

---

## Demo Mode vs Full Data

### Current: Demo Mode

By default, the app runs with **sample data**:
- 5 example languages
- 3 example features
- Perfect for testing

**Advantages:**
- ✅ Lightweight
- ✅ Fast loading
- ✅ No large files needed
- ✅ Good for demonstrations

### Using Full WALS Data

To use the complete dataset (2,500+ languages):

#### Method 1: Upload CLDF Files

1. Generate CLDF data locally:
   ```bash
   cldfbench wals.makecldf
   ```

2. Commit the `cldf/` directory:
   ```bash
   git add cldf/
   git commit -m "Add full WALS data"
   git push
   ```

3. Streamlit Cloud will automatically redeploy with full data

#### Method 2: Use External Storage

For very large datasets, use external storage:

```python
# In streamlit_data_loader.py
import requests

@st.cache_data
def load_remote_data():
    url = "https://your-storage.com/cldf-data.zip"
    # Download and extract
```

---

## Troubleshooting

### "App is Sleeping"

**Problem:** App goes to sleep after inactivity (Streamlit Cloud free tier)

**Solution:**
- Wake it up by visiting the URL
- Or upgrade to Streamlit Cloud Teams ($250/year)

### "Module Not Found" Error

**Problem:** Missing package in requirements.txt

**Solution:** Add to `streamlit_app/requirements.txt`:
```
missing-package==1.0.0
```

Then push to GitHub.

### App Runs Slowly

**Problem:** Large dataset or complex computations

**Solutions:**
1. Use caching (already implemented)
2. Reduce initial data display
3. Add pagination (already implemented)
4. Sample data for visualizations

### Memory Limit Exceeded

**Problem:** App uses too much memory

**Solutions:**
1. Use lazy loading (already implemented)
2. Reduce cache size
3. Upgrade to Streamlit Cloud Teams (higher limits)

---

## Usage Analytics

### View App Stats

Streamlit Cloud provides:
- **Number of visitors**
- **Active users**
- **Peak usage times**
- **Geographic distribution**

Access via: Streamlit Cloud Dashboard > Your App > Analytics

### Track Student Engagement

Monitor:
- How many students are using the app
- When they use it (before assignments?)
- Which pages are most popular

---

## Cost Considerations

### Free Tier (Streamlit Cloud)

**Included:**
- ✅ Unlimited public apps
- ✅ 1 GB RAM per app
- ✅ 1 CPU per app
- ✅ Community support

**Limitations:**
- ⚠️ Apps sleep after inactivity
- ⚠️ Limited to public GitHub repos
- ⚠️ Resource limits

**Perfect for:** Most educational use cases!

### Paid Options

**Streamlit Cloud Teams ($250/year):**
- Private apps
- No sleeping
- More resources
- Priority support

**Only needed if:**
- You need private deployment
- You have 100+ concurrent users
- You want guaranteed uptime

---

## Security & Privacy

### Student Privacy

- ✅ No login required
- ✅ No student data collected
- ✅ No cookies (by default)
- ✅ HTTPS enabled

### Access Control

For private deployment:
1. Upgrade to Streamlit Cloud Teams
2. Enable authentication
3. Invite students by email

### FERPA Compliance

The free public app:
- Does NOT collect personal information
- Does NOT track individual students
- Is FERPA compliant for viewing public data

---

## Tips for Success

### 1. Test Before Sharing

Visit your deployed app and test:
- All pages load correctly
- Maps display properly
- Charts render correctly
- Search works
- Filters work

### 2. Create a Quick Start Guide

Share with students:
```
WALS Explorer Quick Start:
1. Visit: [your-app-url]
2. Click "Languages" to browse
3. Use filters in the sidebar
4. Click "Map" for geographic view
5. Explore "Statistics" for patterns
```

### 3. Integrate with Assignments

Example assignment:
```
Using the WALS Explorer:
1. Find 5 languages from different families
2. Compare their word order (Feature 81A)
3. Identify geographic patterns
4. Write a 2-page analysis
```

### 4. Monitor Usage

Check Streamlit Cloud analytics weekly:
- Are students using it?
- When are peak times?
- Any errors in logs?

### 5. Keep It Updated

When WALS releases updates:
```bash
# Update data
cldfbench wals.makecldf
git add cldf/
git commit -m "Update WALS data"
git push
```

---

## Alternative Deployment Options

### If Streamlit Cloud Doesn't Work

#### 1. Heroku (Free Tier Ended)

Now requires paid plan (~$7/month)

#### 2. Google Cloud Run

Free tier: 2 million requests/month

#### 3. AWS App Runner

~$5-10/month

#### 4. University Server

If your university has servers, deploy there:
```bash
streamlit run Home.py --server.port 80
```

---

## Getting Help

### Streamlit Community

- **Forum**: https://discuss.streamlit.io
- **Docs**: https://docs.streamlit.io
- **Examples**: https://streamlit.io/gallery

### WALS Data Questions

- **GitHub**: https://github.com/cldf-datasets/wals/issues
- **Website**: https://wals.info/contact

### This App

Check logs on Streamlit Cloud or review the troubleshooting section above.

---

## Next Steps

1. ✅ Deploy to Streamlit Cloud
2. ✅ Test all features
3. ✅ Share URL with students
4. ✅ Create assignments that use the app
5. ✅ Monitor usage
6. ✅ Gather student feedback
7. ✅ Iterate and improve

---

**Ready to deploy?** Start with Step 1 above! 🚀

**Questions?** Check Streamlit's excellent documentation at https://docs.streamlit.io

**Good luck with your deployment!** Your students will love having interactive access to WALS data. 🌍
