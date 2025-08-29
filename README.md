# Personal Finance Tracker API

A FastAPI-based REST API for tracking personal finances with a PostgreSQL database and JWT authentication, featuring transaction management, budgeting, and categorisation.

## Features

- **User Authentication**: JWT-based authentication system with secure password hashing
- **Transaction Management**: Record income and expenses with categorisation
- **Budget Tracking**: Set spending limits per category with date ranges
- **Category Management**: Organise transactions with custom categories
- **Protected Routes**: All financial data is user-specific and secured

## Tech Stack

- **FastAPI**: Modern Python web framework
- **SQLAlchemy**: Database ORM with async support
- **JWT**: Stateless authentication tokens
- **bcrypt**: Secure password hashing
- **Pydantic**: Data validation and serialisation

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd personal-finance-tracker
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
export SECRET_KEY="your-secret-key-here"
export DATABASE_URL="sqlite+aiosqlite:///./finance.db"
```

4. Run the application:
```bash
uvicorn main:app --reload
```

## API Endpoints

### Authentication
- `POST /users` - Register new user
- `POST /auth/login` - Login and get JWT token
- `GET /auth/me` - Get current user info (protected)

### Transactions
- `GET /transactions` - List user transactions (protected)
- `POST /transactions` - Create new transaction (protected)
- `GET /transactions/{id}` - Get specific transaction (protected)
- `PUT /transactions/{id}` - Update transaction (protected)
- `DELETE /transactions/{id}` - Delete transaction (protected)

### Categories
- `GET /categories` - List user categories (protected)
- `POST /categories` - Create new category (protected)
- `PUT /categories/{id}` - Update category (protected)
- `DELETE /categories/{id}` - Delete category (protected)

### Budgets
- `GET /budgets` - List user budgets (protected)
- `POST /budgets` - Create new budget (protected)
- `PUT /budgets/{id}` - Update budget (protected)
- `DELETE /budgets/{id}` - Delete budget (protected)

## Usage Example

1. **Register a user**:
```bash
curl -X POST "http://localhost:8000/users" \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "securepassword"}'
```

2. **Login to get JWT token**:
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "securepassword"}'
```

3. **Create a transaction** (replace `YOUR_TOKEN` with the JWT from login):
```bash
curl -X POST "http://localhost:8000/transactions" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 50.00,
    "date": "2024-01-15",
    "description": "Grocery shopping",
    "is_income": false,
    "category_id": 1
  }'
```

## Database Schema

### Models
- **User**: Authentication and user management
- **Transaction**: Financial transactions (income/expenses)
- **Category**: Transaction categorisation
- **Budget**: Spending limits per category

### Relationships
- Users have many transactions, categories, and budgets
- Transactions belong to categories (optional)
- Budgets are linked to specific categories

## Security

- Passwords are hashed using bcrypt
- JWT tokens expire after 24 hours
- All financial endpoints require authentication
- Users can only access their own data

## Development

The project uses SQLAlchemy async sessions and Pydantic schemas for type safety and validation. API documentation is automatically generated and available at `/docs` when running the application.