_# 📚 Library Management API

A FastAPI-based backend for managing books, readers, and borrow/return records in a library.

## 🚀 Features

- JWT-protected endpoints
- CRUD operations for books and readers
- Borrowing and returning books
- Copy management and borrow limits
- PostgreSQL + Async SQLAlchemy (ORM) + Alembic

## 🏗 Project Structure

library/               # Main project folder
├── alembic/           # Alembic migration files
├── library/           # Application package
│   ├── crud/          # Database CRUD operations and functions
│   ├── endpoints/     # API endpoint route definitions
│   ├── tests/         # API tests
│   ├── config/        # Configuration (loads .env variables)
│   ├── database/      # Database connection and session management
│   ├── models/        # SQLAlchemy ORM models
│   ├── schemas/       # Pydantic schemas for validation
│   └── utils/         # Helper utilities (e.g., password hashing, token creation)
├── env_copy           # Example env file (copy this to .env with your database credentials)
├── .gitignore         # Git ignore rules
├── .pytest.ini        # pytest configuration file
├── .alembic.ini       # alembic configuration file
├── .seed_data.py      # a script that adds fake data into database making it easier to work with, run this file after creating the tables
├── Makefile           # Simplified Alembic commands
└── requirements.txt   # Project dependencies





**Do not forget to add your database info into alembic.ini file!**
**Write all your database info in .env file and config file inside library package uses those datas to connect to database**







📦 Database
Foreign Keys & Relationships:
Relationships are defined using SQLAlchemy’s relationship() and foreign key constraints. Cascading deletes are carefully 
managed using passive_deletes=True to avoid unintentional data loss while maintaining referential integrity.

BorrowBook Table:
An additional BorrowBook table was added to track which books are borrowed by which readers. This allows for better 
management of active borrows and return operations, and supports enforcing business rules such as borrowing limits.


🧠 Business Logic
1. Copy Management:
To manage book availability, a copy field was added to the Book model. When a book is borrowed, this field is decremented
by 1. When a book is returned, it is incremented. If the copy count is 0, the user is prevented from borrowing the book.

2. Borrow Limit Enforcement:
A function was implemented to count the number of active (non-returned) borrow records for each reader. If a reader
already has 3 active borrows, they are not allowed to borrow another book.

3. Secure Book Return:
To return a book, the API receives borrow_id and reader_id. It verifies that the reader_id in the request matches the 
one in the borrow record. If they match, the return is processed; otherwise, an exception is raised to prevent unauthorized returns.


🔐 Password Hashing & Token Authentication
1. Password Security:
Password hashing and verification are handled using the passlib library to ensure secure storage and comparison of user
passwords.

2. Token Generation:
JWT tokens are generated using the python-jose library. These tokens are used to authorize requests to protected endpoints.

3. Token Verification:
A helper function was implemented to decode and validate JWT tokens, ensuring only authenticated users can access 
protected resources.



🧱 Challenges Faced & How I Solved Them
While building this project, I faced quite a few challenges. One of them was checking whether a user is properly 
authenticated using a JWT token. I also ran into issues with Pydantic validation when the input data didn't match the
expected schema. Some bugs popped up too—like the case where a user could borrow the same book twice.

The most difficult part by far was testing with pytest. Compared to Django REST Framework, where writing and running 
tests felt more straightforward, testing an async FastAPI project took more effort to set up and understand. But in the
end, I managed to figure it out.

Whenever I got stuck, I relied on Google, official documentation, Reddit, Stack Overflow, and of course, 
AI assistants. I want to point out that I didn’t blindly copy and paste solutions—instead, 
I took the time to understand each fix and learn from it. Even if I spent countless hours searching, it was worth it.

In conclusion, this project was a valuable learning experience that helped me grow as a developer._


