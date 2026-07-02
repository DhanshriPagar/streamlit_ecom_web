import streamlit as st
from db import cursor, conn
from auth import login, signup
import razorpay

# ---------------- INIT ----------------
if "user" not in st.session_state:
    st.session_state.user = None

if "cart" not in st.session_state:
    st.session_state.cart = []

if "selected" not in st.session_state:
    st.session_state.selected = None

# Razorpay (demo keys)
client = razorpay.Client(auth=("YOUR_KEY", "YOUR_SECRET"))

# ---------------- MENU ----------------
menu = st.sidebar.radio(
    "Menu",
    ["Login", "Signup", "Shop", "Cart", "Payment", "Orders", "Wishlist", "Profile", "Admin"]
)

# ---------------- LOGOUT ----------------
if st.sidebar.button("Logout"):
    st.session_state.user = None
    st.session_state.cart = []
    st.success("Logged out")

# ================= LOGIN =================
if menu == "Login":
    st.title("Login")

    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Login"):
        if login(u, p):
            st.session_state.user = u
            st.success("Login successful")
        else:
            st.error("Invalid credentials")

# ================= SIGNUP =================
elif menu == "Signup":
    st.title("Signup")

    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Signup"):
        if signup(u, p):
            st.success("Account created")
        else:
            st.error("User already exists")

# ================= SHOP =================
elif menu == "Shop":

    if not st.session_state.user:
        st.warning("Login first")
        st.stop()

    st.title("🛍️ Shop")

    from products import products

    cols = st.columns(4)

    for i, p in enumerate(products):
        with cols[i % 4]:
            st.image(p["image"])
            st.write(p["name"])
            st.write(f"₹{p['price']}")

            if st.button(f"View {p['id']}"):
                st.session_state.selected = p

            qty = st.number_input(f"Qty {p['id']}", 1, 10, 1)

            if st.button(f"Add {p['id']}"):
                st.session_state.cart.append({
                    "name": p["name"],
                    "price": p["price"],
                    "qty": qty
                })
                st.success("Added")

            if st.button(f"❤️ Wish {p['id']}"):
                cursor.execute(
                    "INSERT INTO wishlist VALUES (?, ?, ?)",
                    (st.session_state.user, p["name"], p["price"])
                )
                conn.commit()

# ================= PRODUCT DETAIL =================
if st.session_state.selected:
    p = st.session_state.selected
    st.title("🛍️ Product Details")
    st.image(p["image"])
    st.write(p["name"])
    st.write(f"₹{p['price']}")

    if st.button("Close"):
        st.session_state.selected = None

# ================= CART =================
elif menu == "Cart":
    st.title("🛒 Cart")

    total = 0

    for i, item in enumerate(st.session_state.cart):
        st.write(item["name"], item["qty"], item["price"])
        total += item["price"] * item["qty"]

    st.success(f"Total ₹{total}")

# ================= PAYMENT (RAZORPAY) =================
elif menu == "Payment":

    if not st.session_state.user:
        st.warning("Please login first")
        st.stop()

    st.title("💳 Payment")

    if not st.session_state.cart:
        st.warning("Cart empty")
    else:
        total = sum(i["price"] * i["qty"] for i in st.session_state.cart)

        st.success(f"Total Amount: ₹ {total}")

        payment_method = st.selectbox(
            "Select Payment Method",
            ["Cash on Delivery (COD)"]
        )

        if st.button("Place Order"):
            st.success("Order Placed Successfully 🎉 (COD)")

            for item in st.session_state.cart:
                cursor.execute(
                    "INSERT INTO orders VALUES (?, ?, ?, ?)",
                    (st.session_state.user, item["name"], item["qty"], item["price"])
                )

            conn.commit()
            st.session_state.cart = []
    # ================= ORDERS =================
elif menu == "Orders":
    st.title("📦 Orders")

    cursor.execute("SELECT * FROM orders WHERE username=?", (st.session_state.user,))
    data = cursor.fetchall()

    for d in data:
        st.write(d)

# ================= WISHLIST =================
elif menu == "Wishlist":
    st.title("❤️ Wishlist")

    cursor.execute("SELECT * FROM wishlist WHERE username=?", (st.session_state.user,))
    data = cursor.fetchall()

    for d in data:
        st.write(d)

# ================= PROFILE =================
elif menu == "Profile":
    st.title("👤 Profile")

    st.write("User:", st.session_state.user)
    st.write("Cart Items:", len(st.session_state.cart))

# ================= ADMIN =================
elif menu == "Admin":
    st.title("🧑‍💼 Admin Panel")

    n = st.text_input("Name")
    p = st.number_input("Price", 0)
    c = st.text_input("Category")
    i = st.text_input("Image URL")

    if st.button("Add Product"):
        cursor.execute("INSERT INTO products VALUES (?, ?, ?, ?, ?)", (None, n, p, c, i))
        conn.commit()
        st.success("Product added")