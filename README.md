# SBA Django Project

This project is a Django-based web application designed for educational purposes as part of a Software Based Assessment (SBA). It implements a simple system with user authentication and basic CRUD (Create, Read, Update, Delete) functionalities.

## Features

- User authentication (login/logout)
- CRUD operations for core models
- Django admin interface for content management
- Bootstrap-based UI for responsiveness
- Modular app structure following Django best practices

## Getting Started

These instructions will get the project up and running on your local machine.

### Prerequisites

- Python 3.8+
- pip (Python package manager)
- Virtualenv (recommended)

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/gvannesson/sba_django_project.git
cd sba_django_project
```

2. **Checkout the correct branch**

```bash
git checkout samuel
```

3. **Create and activate a virtual environment**

```bash
python -m venv env
source env/bin/activate  # On Windows use: env\Scripts\activate
```

4. **Install dependencies**

```bash
pip install -r requirements.txt
```

5. **Apply migrations and run the server**

```bash
python manage.py migrate
python manage.py runserver
```

6. **Access the application**

Open a browser and go to `http://127.0.0.1:8000/`

## Usage

- Register or login to access the application.
- Navigate through the app to perform CRUD operations.
- Admin interface is accessible at `/admin`.

### Creating Superuser (optional)

To access the Django admin:

```bash
python manage.py createsuperuser
```

Follow the prompts and then log in at `http://127.0.0.1:8000/admin`

## Project Structure

```
sba_django_project/
├── manage.py
├── requirements.txt
├── project/                # Project settings
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── core/                   # Core app
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   └── ...
└── templates/              # HTML templates
```

## Authors

Gauthier VANNESSON
https://github.com/gvannesson

Hacene ZERROUK
https://github.com/haceneZERROUK 

Samuel THOREZ-DEBRUCQ
https://github.com/SamuelTD

## License

MIT License

Copyright (c) [year] [Your Name]

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

