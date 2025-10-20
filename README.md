# IIA-Django — Art Recommendation App

This repository contains a Django backend (REST API + ML recommender) and a React frontend (gallery, authentication, recommendations). The project uses a TF-IDF similarity model trained on a WikiArt dataset sample and includes a WikiArt integration layer for artwork metadata and image URLs.

This README documents how to set up and run the project locally on Windows.

## Requirements

- Python 3.10+ (virtualenv recommended)
- Node.js 14+/npm or Yarn
- Git

Notes: The project uses Django, Django REST Framework, scikit-learn, and a React frontend (Create React App).

## Backend setup (Django)

1. Open a terminal and create + activate a virtual environment. In PowerShell:

```powershell
cd d:\Projetos\IIA-Django\backend
python -m venv venv
.\venv\Scripts\Activate.ps1
```

2. Install Python dependencies (create or adjust `requirements.txt` if needed):

```powershell
pip install -r requirements.txt
```

If you don't have a `requirements.txt`, install typical packages:

```powershell
pip install django djangorestframework psycopg2-binary numpy scipy scikit-learn pillow requests
```

3. Run database migrations:

```powershell
python manage.py migrate
```

4. (Optional) Create a superuser to access the admin:

```powershell
python manage.py createsuperuser
```

5. Start the Django development server:

```powershell
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/`.

## Frontend setup (React)

1. Open a terminal in the frontend folder and install dependencies:

```powershell
cd d:\Projetos\IIA-Django\frontend
npm install
```

2. Start the frontend dev server:

```powershell
npm start
```

The React app will open at `http://localhost:3000` and communicate with the Django backend.

## ML Model Artifacts

Model artifacts (TF-IDF vectorizer, tfidf matrix, metadata) are stored in `d:\Projetos\IIA-Django\models`. Ensure this folder exists and contains `vectorizer.pkl`, `tfidf_matrix.npz`, `metadata.json`, and `model_info.json` if you plan to use the recommender.

If you need to re-train the model, see the `pipeline/notebooks/get_to_csv.ipynb` for instructions.

## WikiArt Integration & Images

- The project integrates a `wikiart_api_client` that generates artwork metadata and image URLs. Because WikiArt's API is protected by CloudFlare, the client uses a deterministic mapping and reliable image providers (e.g., Unsplash, Picsum) as fallbacks.
- The backend endpoints return `image_url` and `placeholder_url` for each artwork. The frontend uses `image_url` and falls back to `placeholder_url` if the first load fails.
