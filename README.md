🌱 ECOLEDGER
Expense Tracker & Carbon Footprint Analyzer (Python + MySQL)

📌 Project Overview
ECOLEDGER is a Python-based desktop application that helps users:

Track daily expenses
Calculate carbon footprint based on spending habits
Maintain a carbon-reduction streak
Visualize category-wise and weekly carbon emissions
The project combines financial awareness with environmental responsibility, making users more conscious of how their daily expenses impact the planet.

This project is designed and implemented as a first-year CSE hackathon project using beginner-friendly technologies.

🎯 Objectives
Encourage sustainable spending habits
Provide transparent carbon footprint calculation
Gamify eco-friendly behavior using streaks
Offer clear data visualization for better insights
🛠 Tech Stack
Programming Language: Python
GUI: Tkinter
Database: MySQL
Graphs & Visualization: Matplotlib
Connector: mysql-connector-python
🧩 Features
👤 User Management
New user registration
Existing user login
Auto-generated User ID displayed after login/registration
💰 Expense Tracking
Users can enter expenses under:

Fruit
Vegetable
Non-veg
Tobacco
Bike
Car
Metro
All expenses are stored date-wise in the database.

🌍 Carbon Footprint Calculation
Each category has a predefined carbon emission factor

Carbon footprint is calculated using:

carbon = (expense / 100) × emission_factor
Total daily carbon footprint is computed automatically

🔥 Carbon Streak System
Healthy carbon threshold: 5 kg/day
If daily carbon ≤ threshold → streak increases
If daily carbon > threshold → streak resets to 0
Streak and previous carbon value are stored in the database
📊 Data Visualization
1️⃣ Category-wise Carbon Graph
Bar chart showing carbon contribution from each category
2️⃣ Weekly Carbon Graph
Line graph for Day 1 to Day 7
Uses a separate weekly_carbon table
Automatically resets after 7 days
📜 History View
User can enter a User ID
Latest expense record for that user is displayed in readable format
Example:

Fruit expense = 50
Vegetable expense = 30
Bike expense = 120
Date = 2026-01-14
🗄 Database Design
users table
user_id | username | email | password | prev_carbon | streak
expense table
user_id | fruit | vegetable | non_veg | tobacco | bike | car | metro | date
weekly_carbon table
id | user_id | day_no | carbon_value
🚀 How to Run the Project
1️⃣ Install Dependencies
pip install mysql-connector-python matplotlib
2️⃣ Setup MySQL Database
Create database: ecoledger
Create required tables (users, expense, weekly_carbon)
3️⃣ Update Database Credentials
Edit in Python file:

host="localhost"
user="root"
password="your_password"
database="ecoledger"
4️⃣ Run the Application
python ecoledger.py
🧠 Learning Outcomes
GUI development using Tkinter
MySQL database integration with Python
SQL table design and relationships
Data visualization with Matplotlib
Logical implementation of streak and reset mechanisms
🏆 Hackathon Value
Beginner-friendly yet feature-rich
Combines FinTech + Sustainability
Clear real-world problem solving
Fully functional end-to-end application
📌 Future Enhancements (Optional)
Monthly carbon analytics
Export reports to CSV/PDF
Improved UI/UX
Login security enhancements
👨‍💻 Author
Aditya First Year CSE Student Hackathon Project – ECOLEDGER 🌍

📄 License
This project is created for educational and hackathon purposes.
