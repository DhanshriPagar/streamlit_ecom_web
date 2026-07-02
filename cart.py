import streamlit as st

def add_to_cart(product):
    if "cart" not in st.session_state:
        st.session_state.cart = []
    st.session_state.cart.append(product)

def show_cart():
    st.title("🛒 Your Cart")

    if "cart" not in st.session_state or len(st.session_state.cart) == 0:
        st.write("Cart is empty")
        return

    total = 0

    for item in st.session_state.cart:
        st.write(f"{item['name']} - ₹{item['price']}")
        total += item["price"]

    st.success(f"Total: ₹{total}")