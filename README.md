# RecycleMate

RecycleMate is a Django-based web application that uses machine learning to classify images as recyclable or non-recyclable. The application helps users identify whether items can be recycled, track their recycling history, and find local recycling resources.

## Features

- **AI-Powered Image Classification**: Upload images of items to determine if they are recyclable or non-recyclable using a TensorFlow/Keras deep learning model
- **User Authentication**: Register, login, and manage user accounts
- **Personal Profile**: Track your recycling history with a personal dashboard showing all scanned items
- **Industry Resources**: Browse a directory of recycling industries and facilities
- **Contact/Feedback**: Submit feedback and contact information
- **Admin Dashboard**: Staff members can view user statistics and manage data

## Tech Stack

- **Backend**: Django 4.1.7
- **Machine Learning**: TensorFlow, Keras
- **Image Processing**: Pillow (PIL), NumPy
- **Database**: SQLite3
- **Frontend**: HTML, CSS, JavaScript
- **Python Version**: 3.11

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.11 or higher
- pip (Python package installer)
- pipenv (for dependency management)

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/SmitPanchal61/RecycleMate.git
   cd RecycleMate
   ```

2. **Install dependencies using pipenv**
   ```bash
   pipenv install
   ```

   Alternatively, if you prefer using pip directly:
   ```bash
   pip install django tensorflow keras numpy pillow
   ```

3. **Activate the virtual environment** (if using pipenv)
   ```bash
   pipenv shell
   ```

4. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser** (optional, for admin access)
   ```bash
   python manage.py createsuperuser
   ```

## Running the Application

1. **Start the Django development server**
   ```bash
   python manage.py runserver
   ```

2. **Access the application**
   - Open your browser and navigate to: `http://127.0.0.1:8000/`
   - For admin panel: `http://127.0.0.1:8000/admin/`

## Project Structure

```
RecycleMate/
├── RecycleMate/          # Django project settings
│   ├── settings.py       # Project configuration
│   ├── urls.py          # Main URL routing
│   └── wsgi.py          # WSGI configuration
├── RM/                   # Main application
│   ├── models.py        # Database models (contact, items, industry)
│   ├── views.py         # View functions and ML model integration
│   ├── urls.py          # App URL routing
│   ├── admin.py         # Admin configuration
│   ├── Templates/       # HTML templates
│   └── static/          # CSS, JavaScript, and images
├── media/               # Uploaded user images
├── db.sqlite3          # SQLite database
├── R_NR_2.h5           # Pre-trained ML model for classification
├── manage.py           # Django management script
└── Pipfile             # Python dependencies
```

## Usage Guide

### For Regular Users

1. **Register/Login**
   - Click "Register" to create a new account
   - Provide username, email, password, society name, and city
   - Login with your credentials

2. **Scan Items**
   - Navigate to the "Scan" page (`/predict`)
   - Upload an image of an item you want to classify
   - The system will analyze the image and display whether it's recyclable or non-recyclable
   - Optionally save the item to your profile with a custom name

3. **View Profile**
   - Access your profile page (`/profile`) to see all your scanned items
   - Delete items from your history if needed

4. **Browse Resources**
   - Visit the "Resources" page (`/resources`) to find recycling industries and facilities
   - Filter by category, type, and location

### For Admin Users

1. **User Statistics**
   - Access `/userstats` to view user data
   - Search for specific users by username
   - Search for users by society name
   - View individual user items

2. **Admin Panel**
   - Access `/admin/` to manage database records
   - Manage contacts, items, industries, and users

## URL Endpoints

- `/` - Home page
- `/login` - User login
- `/register` - User registration
- `/logout` - User logout
- `/predict` - Image classification page
- `/profile` - User profile with recycling history
- `/addItem` - Save item to profile
- `/delete/<int:imgId>` - Delete item from profile
- `/resources` - Recycling industry resources
- `/userstats` - Admin user statistics (staff only)
- `/findUser` - Search users by username (staff only)
- `/findSociety` - Search users by society (staff only)
- `/<int:userId>` - View specific user items (staff only)
- `/admin/` - Django admin panel

## Machine Learning Model

The application uses a pre-trained TensorFlow/Keras model (`R_NR_2.h5`) to classify images. The model:
- Accepts images resized to 256x256 pixels
- Returns a probability score
- Classifies items as "RECYCLABLE" (score > 0.5) or "NON-RECYCLABLE" (score ≤ 0.5)

## Database Models

- **contact**: Stores user feedback and contact messages
- **items**: Stores user-scanned items with name, image link, and user ID
- **industry**: Stores recycling industry information (name, category, type, location, phone)

## Development Notes

- The project uses Django's built-in SQLite database for development
- Media files (uploaded images) are stored in the `media/` directory
- Static files (CSS, JS, images) are served from `RM/static/`
- The ML model is loaded once at application startup in `views.py`

## Troubleshooting

- **Import errors**: Ensure all dependencies are installed using `pipenv install` or `pip install`
- **Database errors**: Run `python manage.py migrate` to apply database migrations
- **Static files not loading**: Ensure `DEBUG = True` in settings.py for development
- **ML model not found**: Ensure `R_NR_2.h5` is in the project root directory

## Future Enhancements

Potential improvements for the project:
- Support for multiple image formats
- Batch image processing
- Recycling tips and educational content
- Integration with recycling pickup services
- Mobile app version
- Enhanced ML model with more categories

## Contact

- Email: smitpanchal1661@gmail.com

