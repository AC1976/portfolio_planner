# Box 3 Financial Planner

A web-based financial planning tool for Dutch investors to model portfolio returns and Box 3 taxation under current and future regimes.

## Features

- **Portfolio Modeling**: Track equity, bonds, property, and cash positions over time
- **Box 3 Tax Calculation**: Supports both current (deemed return) and future (actual return) regimes
- **Drawdown Planning**: Model inflation-adjusted annual withdrawals
- **Interactive Charts**: Visualize portfolio growth, asset allocation, and cash flows
- **Responsive Design**: Works on desktop and mobile with DaisyUI styling

## Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the development server
python app.py
```

Then open http://localhost:5000 in your browser.

## Deploying to PythonAnywhere

1. **Create a free account** at [pythonanywhere.com](https://www.pythonanywhere.com)

2. **Upload your files**:
   - Go to the "Files" tab
   - Create a new directory (e.g., `box3-planner`)
   - Upload `app.py`, `planner.py`, and the `templates` folder

3. **Set up a virtual environment** (in a Bash console):
   ```bash
   cd ~/box3-planner
   python -m venv venv
   source venv/bin/activate
   pip install flask pandas
   ```

4. **Create a Web App**:
   - Go to the "Web" tab
   - Click "Add a new web app"
   - Choose "Manual configuration" and Python 3.10+
   - Set the **Source code** directory to `/home/yourusername/box3-planner`
   - Set the **Working directory** to `/home/yourusername/box3-planner`

5. **Configure WSGI**:
   - Click on the WSGI configuration file link
   - Replace contents with:
   ```python
   import sys
   path = '/home/yourusername/box3-planner'
   if path not in sys.path:
       sys.path.append(path)
   
   from app import app as application
   ```

6. **Set virtualenv path**:
   - In the "Virtualenv" section, enter: `/home/yourusername/box3-planner/venv`

7. **Reload** your web app

Your app will be live at `yourusername.pythonanywhere.com`

## Alternative: Render.com Deployment

1. Push your code to GitHub
2. Connect your repo to [Render](https://render.com)
3. Create a new Web Service
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `gunicorn app:app`
6. Add `gunicorn` to requirements.txt for production

## Project Structure

```
box3-planner/
├── app.py              # Flask application
├── planner.py          # Financial model
├── requirements.txt    # Python dependencies
├── README.md
└── templates/
    └── index.html      # Main UI (DaisyUI + Chart.js)
```

## Disclaimer

This tool is for informational and educational purposes only. Always consult a qualified tax advisor for professional financial and tax advice.
