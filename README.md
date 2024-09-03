UStora Online Shopping App

Welcome to UStora, a feature-rich e-commerce platform built with Django LTS (4.2). This application provides a seamless shopping experience, incorporating advanced functionalities like product recommendations, multilingual support, and background task management.

 Features
User Authentication: Secure user registration, login, and profile management (password change, reset, profile edit).
Shop: Browse and purchase a wide range of products.
Add to Cart: Add products to the cart and proceed to checkout.
Apply Coupon Code: Apply discounts at checkout using coupon codes.
Wishlist: Save products for later with the wishlist feature.
Checkout & Payment: Secure checkout with Stripe payment integration.
Contact Page: Get in touch through the contact form.
Subscribe to Newsletter: Stay informed by subscribing to newsletters.
Rank and Review: Rate and review products based on your experience.
Recommender System: Personalized recommendations based on items frequently bought together using Redis.
Top Sellers: See the most popular products.
Recently Viewed: Revisit your recently viewed items.
Top New: Discover the latest products.
Order Processing: Manage customer orders with order tracking, send an e-mail notification when an order is successfully created and generate a PDF file related to the order and store it into the database.
Translation: Multilingual support using Django Rosetta.
Background Tasks: Manage background tasks with Celery when sending order related email.
Message Brokering: Use RabbitMQ for efficient message brokering when sending order related email.
Search and Filtering: Search products by name or description or filter by category, tag.
Admin Panel: Full-featured Django admin panel for managing the shop.

 Installation
 Prerequisites
Python 3.7 or higher
Django 4.2
PostgreSQL (or any preferred database)
Redis (for Celery tasks)
RabbitMQ (for message brokering)
Stripe account for payment processing

 Setting Up the Project
1. Clone the repository:
   git clone https://github.com/HA-Ali88/Ustora-Online-Shop
   cd UStora

2. Create and activate a virtual environment:
   python3 -m venv venv
   source venv/bin/activate
   for windows use
   venv\Scripts\activate

3. Install dependencies:
   pip install -r requirements.txt

4. Set up the database:
   Configure your database settings in ‘settings.py’.
   Run migrations:
    python manage.py migrate

5. Set up Celery with RabbitMQ:
   Install and configure RabbitMQ.
   Start the Celery worker:
    celery -A UStora worker -l info

6. Create a superuser:
   python manage.py createsuperuser

8. Run the development server:
   python manage.py runserver
   Access the application at ‘http://localhost:8000/en/’.

 9. Stripe Payment Setup
To enable Stripe payments, configure the Stripe API keys in your ‘settings.py’ file:
STRIPE_PUBLISHABLE_KEY = ''your-stripe-publishable-key'’ # Publishable key
STRIPE_SECRET_KEY = 'your-stripe-secret-key’      # Secret key
STRIPE_API_VERSION = '2022-08-01'
STRIPE_WEBHOOK_SECRET=’ 'your-stripe-webhook-secret-key’’

10. Set up Django's email functionality
To enable sending emails, configure the SMTP in your ‘settings.py’ file:
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend' 
EMAIL_HOST = 'your_smtp_server' 
EMAIL_PORT = 587 
EMAIL_USE_TLS = True 
EMAIL_HOST_USER = 'your_email@example.com' 
EMAIL_HOST_PASSWORD = 'your_email_password'

 Usage
 Admin Panel
 login visit 'http://127.0.0.1:8000/en/account/login/'
Visit ‘http://localhost:8000/en/admin/’ to manage products, orders, translations, and more.
Use Celery with RabbitMQ for handling background tasks like sending emails for processing orders, etc.

 Shop Frontend

Shop for products, manage your cart, and complete purchases with Stripe.
Use the wishlist, rate and review products, and explore recommendations.
Translate the shop into different languages using the built-in translation tools.

 Contributing

We welcome contributions! To contribute:

1. Fork the repository.
2. Create a new branch with your feature or bugfix.
3. Submit a pull request with a detailed description of your changes.

 License

This project is licensed under the MIT License. See the ‘LICENSE’ file for details.
