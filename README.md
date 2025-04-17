# 🏡 NepalNest

NepalNest is an accommodation booking platform built with Django, inspired by Airbnb. It allows users to list properties, book stays, and manage reservations with ease. Integrated with local payment gateways like eSewa and Khalti, it's designed to meet the needs of Nepali users while remaining scalable and extensible.

---

## 🚀 Features

- 🔐 User registration, login, and profile management
- 🏠 Property listing with images, details, pricing, etc.
- 🔍 Search and filter properties by category, location, and date
- 💳 Payment integration (eSewa & Khalti)
- 📍 Google Maps integration for location display
- 📧 Email notifications
- 📊 Admin panel with [Jazzmin](https://github.com/farridav/django-jazzmin) for UI enhancements

---

## ⚙️ Tech Stack

- **Backend**: Django, MySQL
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Authentication**: Django Auth
- **Maps**: Google Maps API
- **Payment**: eSewa API, Khalti API
- **Admin UI**: Jazzmin

---

## 🗂️ Project Structure

### Key Directories and Files

- **`accounts/`**: Handles user authentication and profile management.
- **`payment/`**: Manages payment integrations (e.g., eSewa, Khalti).
- **`property/`**: Manages property listings and related functionality.
- **`NepalNest/`**: Contains project-level settings, URLs, and configurations.
- **`templates/`**: HTML templates for rendering frontend views.
- **`static/`**: Static assets like CSS, JavaScript, and images.
- **`media/`**: Stores user-uploaded files such as property images and profile pictures.

---

## 📦 Installation

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/NepalNest.git
cd NepalNest
```

### 2. Set up a virtual environment
```bash
python -m venv venv
source venv/Scripts/activate  # On Windows
# OR
source venv/bin/activate      # On macOS/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure the database
- Update the database settings in `NepalNest/settings.py` to match your MySQL configuration:
  ```python
  DATABASES = {
      'default': {
          'ENGINE': 'django.db.backends.mysql',
          'NAME': 'your_database_name',
          'USER': 'your_database_user',
          'PASSWORD': 'your_database_password',
          'HOST': 'localhost',
          'PORT': '3306',
      }
  }
  ```
- Run migrations:
  ```bash
  python manage.py makemigrations
  python manage.py migrate
  ```

### 5. Set up Google Maps API
- Obtain a Google Maps API key from the [Google Cloud Console](https://console.cloud.google.com/).
- Add the API key to your `settings.py`:
  ```python
  GOOGLE_MAPS_API_KEY = 'your_google_maps_api_key'
  ```
- Use the key in your templates or JavaScript files where required.

### 6. Configure eSewa and Khalti Payment Gateways
- Obtain API credentials for eSewa and Khalti.
- Add them to your `settings.py`:
  ```python
  ESEWA_MERCHANT_ID = 'your_esewa_merchant_id'
  KHALTI_PUBLIC_KEY = 'your_khalti_public_key'
  KHALTI_SECRET_KEY = 'your_khalti_secret_key'
  ```

### 7. Collect static files
```bash
python manage.py collectstatic
```

### 8. Run the development server
```bash
python manage.py runserver
```
- Open your browser and navigate to `http://127.0.0.1:8000`.

---

## 🛠️ Additional Notes

- **Environment Variables**: Use a `.env` file to store sensitive information like API keys and database credentials. Install `python-decouple` to manage environment variables.
- **Admin Panel**: Access the admin panel at `http://127.0.0.1:8000/admin` using the superuser credentials created with:
  ```bash
  python manage.py createsuperuser
  ```
- **Debugging**: Set `DEBUG = True` in `settings.py` during development. For production, set it to `False` and configure allowed hosts.

---

## 📧 Support
If you encounter any issues, feel free to open an issue on the [GitHub repository](https://github.com/yourusername/NepalNest) or contact the project maintainers.

---