/*
    storefront_view.js

    The Vault Campus Marketplace 
    CSC 405 Sp 26'
    Created by Day Ekoi - Iteration 4
    3/22/2026


Description:
This file handles the functionality for the public storefront view page.
It creates listing cards dynamically and handles basic interactions such as
going back to the storefront homepage.

Later, this file will pull real listing data from the backend and render
the correct storefront information dynamically.
 


// test listing data: placeholder data for layout testing
const listings = [
    { id: 1, name: "Nike Jacket", price: "$186.80" },
    { id: 2, name: "Onyx Diamond Hoodie", price: "$165.00" },
    { id: 3, name: "Essential Hoodie", price: "$120.00" },
    { id: 4, name: "Streetwear Tee", price: "$48.00" }
];


// get references: main elements on the page
const listingGrid = document.getElementById("listingGrid");
const backBtn = document.getElementById("backBtn");


// render listings: dynamically creates listing cards
function renderListings() {
    listingGrid.innerHTML = "";

        const selectedIds = getWishlistIdSet();

        const activeListings = listings.filter((item) => item.status !== "DELETED");

        if (!activeListings.length) {
            renderEmpty("No listings available for this storefront yet.");
            return;
        }

        activeListings.forEach((item, index) => {
            const card = document.createElement("div");
            card.className = "listing-card";

            const title = item.title || item.name || "Untitled Listing";
            const priceValue =
                typeof item.price === "string" && item.price.includes("$")
                    ? item.price
                    : `$${Number(item.price || 0).toFixed(2)}`;

            const imageUrl =
                item.image_url ||
                (Array.isArray(item.images) && item.images.length > 0 ? item.images[0] : null) ||
                getMockListingImage(storefrontId, index);

        card.innerHTML = `
            <div class="listing-image"></div>
            <div class="listing-info">
                <span class="item-name">${item.name}</span>
                <span class="item-price">${item.price}</span>

                <button class="cart-btn" aria-label="Add to cart">
                    <svg viewBox="0 0 24 24" class="cart-svg">
                        <!-- bag -->
                        <path
                            d="M6 8h12l-1 11H7L6 8Z"
                            fill="none"
                            stroke="currentColor"
                            stroke-width="2"
                            stroke-linejoin="round"
                        />
                        <path
                            d="M9 8V6a3 3 0 0 1 6 0v2"
                            fill="none"
                            stroke="currentColor"
                            stroke-width="2"
                            stroke-linecap="round"
                        />

                        <!-- plus sign -->
                        <line x1="18" y1="5" x2="18" y2="11" stroke="currentColor" stroke-width="2"/>
                        <line x1="15" y1="8" x2="21" y2="8" stroke="currentColor" stroke-width="2"/>
                    </svg>
                </button>
            </div>
        `;

            listingGrid.appendChild(card);
        });
    }


// back button: returns user to storefront homepage
backBtn.addEventListener("click", () => {
    window.location.href = "/storefronts";
});


// initial render
renderListings();
*/
