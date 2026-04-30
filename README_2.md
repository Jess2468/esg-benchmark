# ESG Peer-to-Peer Review Dashboard

A comprehensive Streamlit dashboard for analyzing ESG (Environmental, Social, Governance) performance across packaging industry companies.

## Features

- **ESG Scores Overview**: Compare ESG performance across all companies
- **Market Analysis**: Visualize market capitalization and its relationship with ESG scores
- **Company Deep Dive**: Detailed analysis of individual company metrics
- **Pillar Breakdown**: Compare Environmental, Social, and Governance scores
- **Peer Rankings**: Analyze leading and lagging metrics across companies

## Data Included

The dashboard analyzes the following companies:
- Smurfit Westrock (SW)
- Packaging Corporation of America (PKG)
- International Paper (IP)
- Graphic Packaging (GPI)
- Smurfit Kappa Group (SK)
- Westrock Company (WK)

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Local Installation

1. **Clone or download this repository**

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Run the dashboard**:
```bash
streamlit run app.py
```

4. **Access the dashboard**:
The app will automatically open in your browser at `http://localhost:8501`

## Deployment Options

### Option 1: Streamlit Community Cloud (Recommended - Free)

1. **Create a GitHub repository** with these files:
   - `app.py`
   - `requirements.txt`
   - `P2P_Review.xlsx`
   - `README.md`

2. **Deploy on Streamlit Cloud**:
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository, branch, and `app.py`
   - Click "Deploy"

3. **Your app will be live** at: `https://[your-app-name].streamlit.app`

### Option 2: Heroku

1. **Create additional files**:

Create `setup.sh`:
```bash
mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"your-email@domain.com\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml
```

Create `Procfile`:
```
web: sh setup.sh && streamlit run app.py
```

2. **Deploy to Heroku**:
```bash
heroku login
heroku create your-app-name
git init
git add .
git commit -m "Initial commit"
heroku git:remote -a your-app-name
git push heroku main
```

### Option 3: Docker

1. **Create Dockerfile**:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]
```

2. **Build and run**:
```bash
docker build -t esg-dashboard .
docker run -p 8501:8501 esg-dashboard
```

### Option 4: AWS EC2

1. **Launch EC2 instance** (Ubuntu recommended)

2. **SSH into instance** and run:
```bash
sudo apt update
sudo apt install python3-pip
git clone [your-repo-url]
cd [your-repo]
pip3 install -r requirements.txt
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

3. **Configure security group** to allow inbound traffic on port 8501

### Option 5: Google Cloud Run

1. **Create Dockerfile** (same as Docker option)

2. **Deploy**:
```bash
gcloud run deploy esg-dashboard \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

## File Structure

```
esg-dashboard/
│
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── P2P_Review.xlsx       # ESG data source
├── README.md             # This file
├── .gitignore            # Git ignore file (optional)
└── assets/               # Additional assets (optional)
```

## Configuration

### Customizing the Dashboard

You can customize the dashboard by modifying `app.py`:

- **Color schemes**: Modify the `color_continuous_scale` parameters
- **Chart types**: Change from bar to line charts, etc.
- **Add metrics**: Include additional KPIs in the metrics section
- **Filtering**: Add more interactive filters

### Data Updates

To update the data:
1. Replace `P2P_Review.xlsx` with your new file
2. Ensure the sheet structure remains consistent
3. Restart the application

## Troubleshooting

### Common Issues

**Port already in use**:
```bash
streamlit run app.py --server.port 8502
```

**Missing dependencies**:
```bash
pip install --upgrade -r requirements.txt
```

**Excel file not found**:
- Ensure `P2P_Review.xlsx` is in the same directory as `app.py`
- Check file permissions

**Memory issues on cloud platforms**:
- Consider using Streamlit's caching more aggressively
- Optimize data loading in `load_data()` function

## Performance Optimization

For better performance:

1. **Enable caching** (already implemented with `@st.cache_data`)
2. **Lazy loading**: Load data only when needed
3. **Reduce chart complexity** for large datasets
4. **Use Streamlit session state** for user preferences

## Security Considerations

- **Data privacy**: Ensure ESG data doesn't contain sensitive information
- **Access control**: Consider adding authentication for production use
- **HTTPS**: Use HTTPS for production deployments
- **Environment variables**: Store sensitive configs in `.env` files

## Browser Compatibility

Tested on:
- Chrome 120+
- Firefox 120+
- Safari 17+
- Edge 120+

## Support & Contribution

For issues or feature requests, please create an issue in the repository.

## License

This project is provided as-is for ESG analysis purposes.

## Acknowledgments

Built with:
- [Streamlit](https://streamlit.io/)
- [Plotly](https://plotly.com/)
- [Pandas](https://pandas.pydata.org/)

---

**Last Updated**: April 2026
**Version**: 1.0.0
