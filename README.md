
# ArtBloom

ArtBloom is a web application that simplifies art exploration, offering detailed artwork information, personalized recommendations, and insightful visualizations.

---

## Key Features

### Artwork Exploration (Core Feature):
- **Browse an extensive catalog of artworks.**
- Display key details:
  - **Title** (`title`)
  - **Artist** (`artist_display`, `artist_title`)
  - **Medium** (`medium_display`)
  - **Dimensions** (`dimensions`)
  - **Year** (`date_display`)
  - **Short description** (`short_description`)
  - **Copyright notice** (`copyright_notice`)
- Include artwork images using the `image_id` to construct URLs via IIIF standards.

### Detailed Artwork View:
- A single page with:
  - **Full description** (`description`)
  - **Artist information** (`artist_display`, `artist_title`)
  - **Provenance history** (`provenance_text`)
  - **Exhibition history** (`exhibition_history`)
  - **Publication history** (`publication_history`)
  - **Categories** (`category_titles`)
  - **Terms** (`term_titles`)
  - Associated multimedia resources (e.g., videos, documents).

### Sorting and Filtering:
- **Sort artworks by:**
  - Start date (`date_start`)
  - End date (`date_end`)
- **Filter artworks by:**
  - Categories (`category_titles`)
  - Terms (`term_titles`)
  - Artist name (`artist_display`, `artist_title`)
  - Artwork type (`artwork_type_title`)

### Search Functionality:
- Search for artworks by keywords.

### Personalized Recommendations:
- Suggest similar artworks based on:
  - Categories (`category_titles`)
  - Terms (`term_titles`)
  - Artist name (`artist_display`, `artist_title`)
  - Artwork type (`artwork_type_title`)

### Insights and Trends:
- Analyze and visualize data by:
  - **Artwork type** (`artwork_type_title`)
  - **Medium** (`medium_display`)

### User Interaction:
- Allow users to save favorite artworks.

---

## Technology Stack

- **Frontend:** React, Bootstrap/Tailwind CSS for responsive UI design.
- **Backend:** Django REST Framework to manage API integration, user authentication, and data storage.
- **Database:** PostgreSQL for efficient management of user data, preferences, and cached artwork data.
- **Data Analytics:** Python libraries such as Pandas for processing and analyzing artwork and user data.
- **Visualization:** Highcharts or D3.js for creating dynamic, insightful visualizations.

---

## Objectives

1. Create an engaging platform for exploring art, catering to both casual users and art enthusiasts.
2. Provide personalized recommendations to make the exploration experience unique for each user.
3. Deliver valuable insights and visualizations that enhance the appreciation of art trends and data.
4. Implement a clean, scalable codebase that can be extended in the future.

ArtBloom aims to simplify the exploration of art and enrich the discovery process with detailed information, personalized recommendations, and insightful visualizations.

---

## Project Architecture

ArtBloom follows a modular architecture with a clear separation of concerns between the backend and frontend. Below is the folder structure and a brief explanation of each component:

```plaintext
project/
├── backend/            # Django backend application
│   ├── manage.py       # Entry point for Django commands
│   ├── settings.py     # Django project settings
│   └── app/            # Main Django app folder
│
├── frontend/           # React frontend application
│   ├── dist/           # Vite production build output
│   │   ├── index.html  # React app entry point
│   │   ├── assets/     # Static assets for the app
│   │       ├── style.css
│   │       └── main.js
│   ├── src/            # React source files
│   └── package.json    # React project metadata and dependencies
│
├── static/             # Static files served by Django
│   └── frontend/       # Copied React build output for Django
│       ├── assets/
│       │   ├── style.css
│       │   └── main.js
│
└── templates/          # Django template files
    └── frontend/
        └── index.html  # Adjusted React index.html for Django
```

---

## Workflow

### Frontend:
- Built with React, handling client-side rendering and interactivity.
- The final build files are placed in the `static/frontend/` directory.

### Backend:
- Django REST Framework (DRF) provides API endpoints for handling data.
- Serves the React static files during deployment.

### Integration:
- The React app communicates with Django APIs to fetch artwork data.
- A Django view serves the React app's `index.html` to handle all frontend routes.

### Example: Adjusted `index.html`
```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ArtBloom</title>
    <!-- Load CSS using Django's static tag -->
    <link rel="stylesheet" href="{% static 'frontend/assets/style.css' %}">
  </head>
  <body>
    <div id="app"></div>
    <!-- Load JS bundle using Django's static tag -->
    <script type="module" src="{% static 'frontend/assets/main.js' %}"></script>
  </body>
</html>
```

---

## Deployment

Both the backend and frontend are served through Django.

Static files from the React build are integrated into Django's `static/` folder for unified deployment.

The React app’s `index.html` is adjusted with Django's `{% static %}` tags and served via a Django `TemplateView`.

### Hosting Platforms

1. **[Render](https://render.com)**:
   - Free tier includes 750 hours of server runtime and PostgreSQL support.
   - Simple integration and deployment for Django applications.

2. **[Railway](https://railway.app)**:
   - Free $5 monthly credit, sufficient for small apps.
   - Supports Django and PostgreSQL.

3. **[Fly.io](https://fly.io)**:
   - Free-tier resources for deploying Dockerized applications.
   - Multi-region hosting for global deployment.

4. **[Vercel](https://vercel.com)** (Frontend Only):
   - Perfect for deploying the React app.
   - Pair with Render, Railway, or Fly.io for backend hosting.
