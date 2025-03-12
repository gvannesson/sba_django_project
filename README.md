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
git checkout main
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

5. **Create your .env file**

Set the environment keys in your env file.

6. **Apply migrations, collect staticfiles and run the server**

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py tailwind install
python manage.py tailwind start
python manage.py collectstatic
python manage.py runserver
```

7. **Access the application**

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

## Docker Deployment

The project is containerized for easy deployment. To build and run the Docker container:

### Configure compose.yaml

Configure the compose.yaml file with your image name and desired port.

### Build the Docker Image

```bash
docker build -t your_image_name .
```

### Run the Container

```bash
docker run -d -p 8000:8000 your_image_name
```

Your API should now be accessible at http://localhost:8000/.

## Deployment on Azure

For deploying to Azure Container Instances (ACI) or another cloud platform, you can use the provided shell script deploy.sh along with environment variable management (e.g., through Docker Compose or Azure CLI). Make sure to properly configure your Azure variable in the script such as your registry name. Make sure to adjust resource allocation and networking settings as needed for production workloads.

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

