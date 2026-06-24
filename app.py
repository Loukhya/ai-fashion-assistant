import streamlit as st
import pandas as pd
import os
import pillow_avif

# ==========================================
# LOAD DATA
# ==========================================

BASE_PATH = os.path.dirname(os.path.abspath(__file__))

products = pd.read_csv(
    os.path.join(BASE_PATH, "products.csv")
)

# ==========================================
# USER UNDERSTANDING
# ==========================================

def understand_user(query):

    query = str(query).lower()

    profile = {
        "gender": "men",
        "occasion": "casual",
        "style": "casual"
    }

    if any(word in query for word in [
        "woman", "women", "female", "girl"
    ]):
        profile["gender"] = "women"

    if any(word in query for word in [
        "interview", "office", "meeting",
        "formal", "placement", "job",
        "corporate", "presentation"
    ]):
        profile["occasion"] = "office"
        profile["style"] = "formal"

    elif "wedding" in query:
        profile["occasion"] = "wedding"

    elif "party" in query:
        profile["occasion"] = "party"

    elif any(word in query for word in [
        "vacation", "beach", "summer"
    ]):
        profile["occasion"] = "vacation"

    return profile


# ==========================================
# OUTFIT ENGINE
# ==========================================

def get_outfit(profile):

    gender = profile["gender"]
    occasion = profile["occasion"]

    if occasion == "office":

        shirts = products[
            (products["gender"] == gender) &
            (products["category"] == "formal-shirts")
        ]

        bottoms = products[
            (products["gender"] == gender) &
            (products["category"] == "trousers")
        ]

        shoes = products[
            (products["gender"] == gender) &
            (products["category"] == "formal-shoes")
        ]

        accessories = products[
            (products["gender"] == gender) &
            (products["category"] == "watches")
        ]

    elif occasion == "party":

        shirts = products[
            (products["gender"] == gender) &
            (products["category"].isin(["party-shirts", "party-dresses"]))
        ]

        bottoms = products[
            (products["gender"] == gender) &
            (products["category"].isin(["jeans", "skirts"]))
        ]

        shoes = products[
            (products["gender"] == gender) &
            (products["category"].isin(["heels", "loafers", "sneakers"]))
        ]

        accessories = products[
            (products["gender"] == gender) &
            (products["category"].isin(["watches", "sunglasses"]))
        ]

    elif occasion == "wedding":

        shirts = products[
            (products["gender"] == gender) &
            (products["category"].isin([
                "sherwanis",
                "wedding-sarees",
                "kurta-sets",
                "sharara-sets"
            ]))
        ]

        bottoms = shirts

        shoes = products[
            (products["gender"] == gender) &
            (products["category"] == "ethnic-footwear")
        ]

        accessories = products[
            (products["gender"] == gender) &
            (products["category"].isin(["watches", "necklaces", "earrings"]))
        ]

    else:

        shirts = products[
            (products["gender"] == gender) &
            (products["category"].isin([
                "casual-shirts",
                "linen-shirts",
                "tshirts",
                "polo-tshirts"
            ]))
        ]

        bottoms = products[
            (products["gender"] == gender) &
            (products["category"].isin([
                "jeans",
                "chinos",
                "shorts"
            ]))
        ]

        shoes = products[
            (products["gender"] == gender) &
            (products["category"].isin([
                "sneakers",
                "loafers",
                "sandals",
                "running-shoes"
            ]))
        ]

        accessories = products[
            (products["gender"] == gender) &
            (products["category"].isin([
                "caps",
                "sunglasses",
                "watches"
            ]))
        ]

    if len(shirts) == 0:
        shirts = products[products["gender"] == gender]

    if len(bottoms) == 0:
        bottoms = products[products["gender"] == gender]

    if len(shoes) == 0:
        shoes = products[products["gender"] == gender]

    if len(accessories) == 0:
        accessories = products[products["gender"] == gender]

    hero = shirts.sample(1).iloc[0]["name"]
    bottomwear = bottoms.sample(1).iloc[0]["name"]
    footwear = shoes.sample(1).iloc[0]["name"]
    accessory = accessories.sample(1).iloc[0]["name"]

    return {
        "hero": hero,
        "bottomwear": bottomwear,
        "footwear": footwear,
        "accessory": accessory,
        "reasoning": (
                 f"{hero} was selected because it suits a {occasion} occasion. "
                 f"{bottomwear} complements the topwear and creates a balanced look. "
                 f"{footwear} matches the outfit style and improves overall compatibility. "
                 f"{accessory} adds a polished finishing touch."
        )
    }


# ==========================================
# IMAGE LOOKUP
# ==========================================

def get_product_image(product_name):

    if pd.isna(product_name):
        return None

    search_name = str(product_name)

    if "(" in search_name:
        search_name = search_name.split("(")[0].strip()

    exact_match = products[
        products["name"].str.lower() == search_name.lower()
    ]

    if len(exact_match) > 0:

        image_path = os.path.join(
            BASE_PATH,
            exact_match.iloc[0]["image"]
        )

        if os.path.exists(image_path):
            return image_path

    partial_match = products[
        products["name"].str.contains(
            search_name,
            case=False,
            na=False
        )
    ]

    if len(partial_match) > 0:

        image_path = os.path.join(
            BASE_PATH,
            partial_match.iloc[0]["image"]
        )

        if os.path.exists(image_path):
            return image_path

    return None


def fashion_assistant(query):

    profile = understand_user(query)
    outfit = get_outfit(profile)

    return {
        "profile": profile,
        "hero": outfit["hero"],
        "bottomwear": outfit["bottomwear"],
        "footwear": outfit["footwear"],
        "accessory": outfit["accessory"],
        "reasoning": outfit["reasoning"]
    }


st.set_page_config(
    page_title="AI Fashion Assistant",
    page_icon="👔",
    layout="wide"
)

st.title("👔 AI Fashion Assistant")

query = st.text_area(
    "Describe your outfit requirement",
    placeholder="I am a 22 year old male looking for a formal outfit for an interview"
)

if st.button("Recommend Outfit"):

    result = fashion_assistant(query)

    st.subheader("Detected User Profile")
    st.json(result["profile"])

    cols = st.columns(4)

    items = [
        ("Topwear", result["hero"]),
        ("Bottomwear", result["bottomwear"]),
        ("Footwear", result["footwear"]),
        ("Accessory", result["accessory"])
    ]

    for col, (title, item) in zip(cols, items):

        with col:
            st.write(title)

            image_path = get_product_image(item)

            if image_path:
                st.image(image_path, use_container_width=True)
            else:
                st.warning("Image not found")

            st.caption(item)

    st.subheader("Why This Outfit Works")
    st.write(result["reasoning"])
