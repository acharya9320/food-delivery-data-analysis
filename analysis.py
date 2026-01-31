import pandas as pd
import sqlite3

# Load orders CSV
orders = pd.read_csv("data/orders.csv")
print(orders.head())

# Load users JSON
users = pd.read_json("data/users.json")
print(users.head())

# Load restaurants SQL
conn = sqlite3.connect(":memory:")
with open("data/restaurants.sql", "r") as file:
    sql_script = file.read()

conn.executescript(sql_script)
restaurants = pd.read_sql("SELECT * FROM restaurants", conn)
print(restaurants.head())
# -----------------------------
# MERGE DATA (LEFT JOIN)
# -----------------------------

final_df = (
    orders
    .merge(users, on="user_id", how="left")
    .merge(restaurants, on="restaurant_id", how="left")
)
# FIX mixed date formats
final_df["order_date"] = pd.to_datetime(
    final_df["order_date"],
    dayfirst=True,
    format="mixed",
    errors="coerce"
)


print("\nFINAL DATASET PREVIEW:")
print(final_df.head())
# Save final dataset
final_df.to_csv("final_food_delivery_dataset.csv", index=False)
# ----------------------------------
# ANALYSIS FOR MCQs
# ----------------------------------

# Q1: City with highest total revenue from Gold members
q1 = (
    final_df[final_df["membership"] == "Gold"]
    .groupby("city")["total_amount"]
    .sum()
)
print("\nQ1 - Gold Revenue by City:")
print(q1)
# Q2: Cuisine with highest average order value
q2 = (
    final_df
    .groupby("cuisine")["total_amount"]
    .mean()
)

print("\nQ2 - Average Order Value by Cuisine:")
print(q2)
# Q3: Distinct users with total order value > 1000
user_total = (
    final_df
    .groupby("user_id")["total_amount"]
    .sum()
)

count_users = (user_total > 1000).sum()

print("\nQ3 - Number of users with total spend > 1000:")
print(count_users)
# Q4: Rating range with highest total revenue

def rating_bucket(r):
    if 3.0 <= r <= 3.5:
        return "3.0 – 3.5"
    elif 3.6 <= r <= 4.0:
        return "3.6 – 4.0"
    elif 4.1 <= r <= 4.5:
        return "4.1 – 4.5"
    else:
        return "4.6 – 5.0"

final_df["rating_range"] = final_df["rating"].apply(rating_bucket)

q4 = (
    final_df
    .groupby("rating_range")["total_amount"]
    .sum()
)

print("\nQ4 - Total Revenue by Rating Range:")
print(q4)
# Q5: Among Gold members, city with highest average order value

q5 = (
    final_df[final_df["membership"] == "Gold"]
    .groupby("city")["total_amount"]
    .mean()
)

print("\nQ5 - Average Order Value (Gold Members) by City:")
print(q5)
# Q6: Cuisine with lowest number of distinct restaurants but significant revenue

cuisine_restaurant_count = (
    final_df
    .groupby("cuisine")["restaurant_id"]
    .nunique()
)

cuisine_revenue = (
    final_df
    .groupby("cuisine")["total_amount"]
    .sum()
)

q6 = (
    cuisine_restaurant_count
    .to_frame("restaurant_count")
    .join(cuisine_revenue.to_frame("total_revenue"))
)

print("\nQ6 - Restaurant Count and Revenue by Cuisine:")
print(q6)
# Q7: Percentage of orders by Gold members
total_orders = len(final_df)
gold_orders = len(final_df[final_df["membership"] == "Gold"])

percentage_gold = (gold_orders / total_orders) * 100

print("\nQ7 - Percentage of orders by Gold members:")
print(round(percentage_gold))
# Q8: Restaurant with highest AOV but < 20 orders
restaurant_stats = (
    final_df
    .groupby("restaurant_name")
    .agg(
        avg_order_value=("total_amount", "mean"),
        order_count=("order_id", "count")
    )
)

q8 = restaurant_stats[restaurant_stats["order_count"] < 20] \
        .sort_values("avg_order_value", ascending=False)

print("\nQ8 - Restaurants with <20 orders sorted by AOV:")
print(q8.head())
# Q9: Revenue by membership + cuisine
q9 = (
    final_df
    .groupby(["membership", "cuisine"])["total_amount"]
    .sum()
)

print("\nQ9 - Revenue by Membership & Cuisine:")
print(q9)
# Q10: During which quarter of the year is the total revenue highest?

# Extract quarter from order_date
final_df["quarter"] = final_df["order_date"].dt.to_period("Q")

q10 = (
    final_df
    .groupby("quarter")["total_amount"]
    .sum()
)

print("\nQ10 - Total Revenue by Quarter:")
print(q10)

# NUMERICAL QUESTIONS (FORM ANSWERS)

# 1. Total orders placed by Gold members
total_gold_orders = final_df[final_df["membership"] == "Gold"].shape[0]
print("\nANS 1 - Total orders by Gold members:")
print(total_gold_orders)


# 2. Total revenue from Hyderabad city (rounded)
hyderabad_revenue = (
    final_df[final_df["city"] == "Hyderabad"]["total_amount"]
    .sum()
)

print("\nANS 2 - Total revenue from Hyderabad (rounded):")
print(round(hyderabad_revenue))


# 3. Total distinct users who placed at least one order
distinct_users = final_df["user_id"].nunique()

print("\nANS 3 - Distinct users with at least one order:")
print(distinct_users)


# 4. Average order value for Gold members (rounded to 2 decimals)
gold_avg_order_value = (
    final_df[final_df["membership"] == "Gold"]["total_amount"]
    .mean()
)

print("\nANS 4 - Average order value for Gold members:")
print(round(gold_avg_order_value, 2))


# 5. Orders placed for restaurants with rating >= 4.5
high_rating_orders = final_df[final_df["rating"] >= 4.5].shape[0]

print("\nANS 5 - Orders with restaurant rating >= 4.5:")
print(high_rating_orders)


# 6. Orders in top revenue city among Gold members
top_gold_city = (
    final_df[final_df["membership"] == "Gold"]
    .groupby("city")["total_amount"]
    .sum()
    .idxmax()
)

orders_top_gold_city = (
    final_df[
        (final_df["membership"] == "Gold") &
        (final_df["city"] == top_gold_city)
    ]
    .shape[0]
)

print("\nANS 6 - Orders in top revenue city among Gold members:")
print(orders_top_gold_city)
print("Top Gold Revenue City:", top_gold_city)

