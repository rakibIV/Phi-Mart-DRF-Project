# PhiMart - E-commerce REST API

PhiMart is a full-featured e-commerce backend REST API built with Django REST Framework (DRF). It supports product listings, category management, cart operations, order processing, and user authentication via JWT. It also includes auto-generated API documentation using Swagger.

---

## Features

- JWT Authentication using `djoser`
- Product and Category Management
- Cart and Cart Item Handling
- Order Placement and Status Tracking
- Product Reviews and Ratings
- Product Image Uploads with Size Validation
- Admin-only endpoints for deletion and updates
- Swagger API Documentation (`drf_yasg`)
- Search, filter, and pagination on product listings

---

## Tech Stack

- **Backend:** Django, Django REST Framework
- **Auth:** JWT via `djoser`
- **Docs:** Swagger with `drf_yasg`
- **Database:** Default SQLite (customizable)
- **Filtering:** `django-filter`
- **Others:** Custom Permissions, Model Managers, Serializers, Validators

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/rakibIV/Phi-Mart-DRF-Project.git
cd Phi-Mart-DRF-Project
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # For Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create a superuser

```bash
python manage.py createsuperuser
```

### 6. Run the development server

```bash
python manage.py runserver
```

---

## API Endpoints

| Endpoint | Method | Description |
|---------|--------|-------------|
| `/api/products/` | GET, POST | List/Create products |
| `/api/products/{id}/` | GET, PATCH, DELETE | Retrieve/Update/Delete product |
| `/api/categories/` | GET, POST | List/Create categories |
| `/api/categories/{id}/` | GET, PATCH, DELETE | Retrieve/Update/Delete category |
| `/api/products/{product_id}/images/` | POST | Add product image |
| `/api/products/{product_id}/reviews/` | POST | Add review |
| `/api/cart/` | GET, POST | Create or retrieve cart |
| `/api/cart/{cart_id}/items/` | GET, POST, PATCH, DELETE | Manage cart items |
| `/api/orders/` | GET, POST | Place or view orders |
| `/api/orders/{id}/cancel/` | POST | Cancel an order |
| `/api/orders/{id}/update_status/` | PATCH | Update order status |

---

## Swagger Documentation

After running the server, visit:

```
http://localhost:8000/swagger/
```

This provides full interactive documentation of all endpoints, request/response schemas, and parameters.

---

## Folder Structure (Overview)
```
PHIMART/
           
├── api/
│   ├── urls.py
│   └── permissions.py                                 
├── order/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   └── services.py           
├── phi_mart/
|   ├── settings.py
|   └── urls.py
├── product/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── validators.py
│   ├── paginations.py
│   └── filters.py      
├── users/
│   ├── models.py
│   └── managers.py
│   ├── serializers.py                     
├── manage.py              
├── README.md              
├── requirements.txt               
```



---

## Developer Notes

- Custom permissions are used to allow only admins to delete certain resources.
- Product deletion is restricted if stock is available.
- Reviews are limited to their respective authors.
- Product images are validated for size.
- Swagger annotations (`@swagger_auto_schema`) describe API details.

---

## License

This project is open-source and available under the MIT License.