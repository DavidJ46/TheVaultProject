# The Vault — Campus Marketplace

**A cloud-based fashion marketplace for Hampton University students**

Designed & Built by David Jackson, Elali McNair, Day Ekoi, Ryan Grimes, Kaila Roberts, and Madison Boyd
CSC 405 — Spring 26'

---

## What is The Vault?

The Vault is a web-based campus marketplace exclusively for Hampton University students. It allows student brand owners to create storefronts, publish clothing listings, and manage inventory, while other students can browse, wishlist, and purchase items. The platform follows a vault/bank aesthetic with black and gold as primary colors and uses heist-themed terminology throughout the UI.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| Frontend | HTML, CSS, JavaScript |
| Database | PostgreSQL (AWS RDS) |
| Image Storage | Amazon S3 |
| Cloud Hosting | AWS Elastic Beanstalk |
| Version Control | GitHub |
| Project Management | Jira |
| IDE | VS Code |

---

## Features

### Authentication
- User registration restricted to `@hamptonu.edu` and `@my.hamptonu.edu` email addresses
- Secure password hashing via `auth_utils.py`
- Role-based access control: Shopper, Brand Owner, Admin

### Storefronts
- Users can create a storefront to gain seller capabilities
- Storefront stores brand name, description, logo, banner, and contact info
- Each storefront is tied to a user account via foreign key relationship

### Listings
- Brand owners can create, edit, and deactivate their own listings
- Supports inventory-based and made-to-order (pre-order) fulfillment types
- Size-based inventory tracking with automatic SOLD_OUT status when quantity hits 0
- Multiple images per listing stored in Amazon S3

### Storefront Browsing (Frontend)
- Storefront homepage dynamically renders all active storefront cards
- Individual storefront view page with banner, logo, description, and listing grid
- Create Storefront form with full input validation

### Cart & Wishlist
- Users can add listings to a shopping bag
- Wishlist feature allows users to save listings for later

### Account Dashboard
- View personal listings, purchase history, wishlist, and sold history
- Profile and settings management

### Admin
- Admins can view, manage, and delete any user, listing, or storefront
- Admin routes are gated and protected under `/admin` prefix

---

## Project Structure

```
TheVaultProject/
├── app.py                          # Entry point, registers all blueprints
├── db.py                           # Database connection
├── init_db.py                      # Schema initialization
├── mock_data.py                    # Test data
├── requirements.txt
│
├── backend/
│   ├── controllers/
│   │   ├── auth_controller.py
│   │   ├── storefront_controller.py
│   │   ├── listing_controller.py
│   │   ├── purchase_controller.py
│   │   ├── wishlist_controller.py
│   │   ├── admin_controller.py
│   │   └── usersettings.py
│   ├── models/
│   │   ├── storefront_model.py
│   │   ├── listing_model.py
│   │   ├── purchase_model.py
│   │   ├── wishlist_model.py
│   │   ├── admin_model.py
│   │   └── usersettings.py
│   └── services/
│       ├── auth_services.py
│       ├── storefront_service.py
│       ├── listing_service.py
│       ├── purchase_service.py
│       ├── wishlist_service.py
│       ├── admin_service.py
│       └── usersettings.py
│
├── static/
│   ├── css/
│   │   ├── storefront.css
│   │   ├── storefront_view.css
│   │   ├── create_storefront.css
│   │   └── ...
│   ├── js/
│   │   ├── storefront.js
│   │   ├── storefront_view.js
│   │   ├── create_storefront.js
│   │   └── ...
│   └── images/
│
└── templates/
    ├── index.html
    ├── login.html
    ├── signup.html
    ├── storefront.html
    ├── storefront_view.html
    ├── create_storefront.html
    ├── create_listing.html
    ├── account.html
    ├── cart.html
    └── ...
```

---

## Database Schema

The following tables are initialized via `init_db.py`:

- **users** — account info, email, hashed password, role
- **storefronts** — brand name, description, logo/banner URLs, owner FK
- **listings** — title, price, description, fulfillment type, inventory, status
- **listing_images** — image URLs (stored in S3), primary image flag
- **listing_sizes** — size label and quantity per listing
- **purchases** — order records linking buyer and seller
- **wishlist** — saved listings per user

---

## API Routes

### Page Routes (`storefront_pages_bp`)
| Route | Description |
|---|---|
| `GET /storefronts` | Storefront homepage |
| `GET /storefronts/<id>` | Individual storefront view |
| `GET /storefronts/create` | Create storefront form |
| `GET /storefronts/my` | User's own storefront |

### API Routes (`storefront_bp` — `/api/storefronts`)
| Method | Route | Description |
|---|---|---|
| GET | `/api/storefronts` | Get all active storefronts |
| GET | `/api/storefronts/<id>` | Get single storefront |
| POST | `/api/storefronts` | Create a storefront |
| PUT | `/api/storefronts/<id>` | Update storefront |
| PATCH | `/api/storefronts/<id>/deactivate` | Deactivate storefront |

### Auth Routes (`auth_controller`)
| Method | Route | Description |
|---|---|---|
| POST | `/register` | Register new user |
| POST | `/login` | Login |
| GET | `/logout` | Logout |

### Admin Routes (`admin_bp` — `/admin`)
| Method | Route | Description |
|---|---|---|
| GET | `/admin/users` | Get all users |
| DELETE | `/admin/users/<id>` | Delete user |
| GET | `/admin/listings` | Get all listings |
| DELETE | `/admin/listings/<id>` | Delete listing |

---

## Setup & Running Locally

### Prerequisites
- Python 3.12+
- PostgreSQL (or AWS RDS credentials)
- AWS credentials (for S3 image storage)

### Installation

```bash
# Clone the repo
git clone https://github.com/DavidJ46/TheVaultProject.git
cd TheVaultProject

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows

# Install dependencies
pip install -r requirements.txt
```

### Environment Configuration

Create a `.env` file in the root directory with the following:

```
DB_HOST=your-aws-rds-endpoint
DB_NAME=your-database-name
DB_USER=your-db-username
DB_PASSWORD=your-db-password
DB_PORT=5432
AWS_S3_BUCKET=your-s3-bucket-name
```

### Initialize the Database

```bash
python init_db.py
```

### Run the App

```bash
python app.py
```

Visit `http://127.0.0.1:5000` in your browser.

---

## Architecture

The Vault follows a layered MVC architecture:

```
Browser (HTML/CSS/JS)
        ↓
Flask Application Server (app.py)
        ↓
Controller Layer (blueprints, request parsing, routing)
        ↓
Service Layer (business logic, validation, permissions)
        ↓
Model Layer (SQL queries, database operations)
        ↓
AWS RDS PostgreSQL Database
        ↓ (images)
Amazon S3
```

---

## Team

| Name | Role |
|---|---|
| David Jackson | Project Manager, Admin backend |
| Elali McNair | Co-PM, Wishlist & Purchase backend, Create Listing frontend |
| Ryan Grimes | Systems & Security Lead, Auth backend, Login/Signup/Cart frontend |
| Day Ekoi | Cloud Deployment Lead, Storefront & Listings backend & frontend |
| Madison Boyd | Documentation Lead, User & Account Settings |
| Kaila Roberts | Database & App Support, Checkout Backend and Frontend|

---

## Constraints & Notes

- Restricted to Hampton University email addresses (`@hamptonu.edu` / `@my.hamptonu.edu`)
- Deployed under AWS Free Tier — storage, compute, and database connections are limited
- Payment integration is conceptual only in the current iteration
- Sensitive payment data is never stored in the database

---

## Current Status

The Vault is currently in active development (Iteration 4 of 5). Core features implemented include user authentication, storefront management, listing management with size-based inventory, storefront browsing frontend, and admin controls. Remaining work includes full purchase/checkout flow, search and filter functionality, and cloud deployment.
