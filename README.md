# Food Delivery Data Analysis

This project is a **Food Delivery Data Analysis** task completed as part of the  
**Innomatics Research Labs – Advanced GenAI Internship Entrance Test**.

The objective of this project is to load data from multiple sources, merge them into a single dataset, and answer analytical questions using **Python, Pandas, and SQL concepts**.

---

## Project Structure
food_delivery_hackathon/
│
├── data/
│ ├── orders.csv # Order transaction data
│ ├── users.json # User details
│ └── restaurants.sql # Restaurant & cuisine data (SQL format)
│
├── analysis.py # Main analysis script
├── final_food_delivery_dataset.csv # Final merged dataset
└── README.md # Project documentation

---

## Technologies Used

- **Python 3**
- **Pandas**
- **SQLite (in-memory)**  
- **SQL**
- **VS Code**

> *Note:*  
> Although MySQL was mentioned in the instructions, **SQLite is used here only to execute the provided `.sql` file locally**.  


---

##  Data Sources

1. **orders.csv**  
   - Contains order details such as order_id, user_id, restaurant_id, order_date, and total_amount.

2. **users.json**  
   - Contains user information like name, city, and membership type.

3. **restaurants.sql**  
   - Contains restaurant details including cuisine and rating.

---

##  Data Merging Logic

- `orders.csv` is merged with `users.json` using **user_id**
- Result is merged with `restaurants.sql` using **restaurant_id**
- **LEFT JOIN** is used to ensure all orders are retained

---

##  Date Handling

Order dates are stored in **mixed formats**, so they are handled using:

```python
pd.to_datetime(
    final_df["order_date"],
    dayfirst=True,
    format="mixed",
    errors="coerce"
)
▶️ How to Run

Clone the repository

Navigate to the project folder

Run using: python analysis.py

Acharya Bhaskar
Advanced GenAI Internship Entrance Test Submission
Innomatics Research Labs
