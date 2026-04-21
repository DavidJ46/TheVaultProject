/*
    storefront_view.js

    The Vault Campus Marketplace 
    CSC 405 Sp 26'
    Created by Day Ekoi - Iteration 4
    3/22/2026
    Updated by Day Ekoi - Iteration 5 4/9/26

Description:
This file handles the functionality for the public storefront view page.
Fetches real storefront and listing data from the Flask API using the
storefront ID from the URL. Renders storefront banner, logo, description,
and listing cards dynamically. If the logged in user owns the storefront,
an edit button is shown.

Works with:
- storefront_view.html
- storefront_view.css
*/


// get storefront ID from the URL (e.g. /storefronts/3 → 3)
const storefrontId = window.location.pathname.split("/").pop();

// get references to page elements
const brandName = document.getElementById("brandName");
const contactInfo = document.getElementById("contactInfo");
const storeDescription = document.getElementById("storeDescription");
const storefrontLogo = document.getElementById("storefrontLogo");
const logoFallback = document.getElementById("logoFallback");
const listingGrid = document.getElementById("listingGrid");


// renders an empty state message in the listing grid
function renderEmpty(message) {
    listingGrid.innerHTML = `<p style="color:#c9c9c9; font-style:italic; text-align:center; grid-column: 1/-1;">${message}</p>`;
}


// builds and returns a single listing card element
function createListingCard(item) {
    const card = document.createElement("div");
    card.className = "listing-card";

    const title = item.title || item.name || "Untitled Listing";
    const price = typeof item.price === "string" && item.price.includes("$")
        ? item.price
        : `$${Number(item.price || 0).toFixed(2)}`;
    const imageUrl = item.image_url || null;

    card.innerHTML = `
        ${imageUrl ? `<img class="listing-image" src="${imageUrl}" alt="${title}">` : `<div class="listing-image"></div>`}
        <div class="listing-info">
            <span class="item-name">${title}</span>
            <span class="item-price">${price}</span>
            <button class="cart-btn" aria-label="Add to cart">
                <svg viewBox="0 0 24 24" class="cart-svg">
                    <path d="M6 8h12l-1 11H7L6 8Z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>
                    <path d="M9 8V6a3 3 0 0 1 6 0v2" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                    <line x1="18" y1="5" x2="18" y2="11" stroke="currentColor" stroke-width="2"/>
                    <line x1="15" y1="8" x2="21" y2="8" stroke="currentColor" stroke-width="2"/>
                </svg>
            </button>
        </div>
    `;

    return card;
}


// fetches storefront data and listings from the API and renders the page
async function loadStorefrontView() {
    try {
        // fetch storefront info
        const sfRes = await fetch(`/api/storefronts/${storefrontId}`);
        if (!sfRes.ok) throw new Error("Storefront not found");
        const storefront = await sfRes.json();

        // populate banner
        brandName.textContent = storefront.brand_name || "Unnamed Storefront";
        contactInfo.textContent = storefront.contact_info || "";
        storeDescription.textContent = storefront.bio || storefront.description || "No description provided.";

        // populate logo
        if (storefront.logo_url) {
            storefrontLogo.src = storefront.logo_url;
            storefrontLogo.style.display = "block";
            logoFallback.style.display = "none";
        }

        // populate banner image if available
        if (storefront.banner_url) {
            document.getElementById("storefrontBanner").style.backgroundImage = `url('${storefront.banner_url}')`;
            document.getElementById("storefrontBanner").style.backgroundSize = "cover";
            document.getElementById("storefrontBanner").style.backgroundPosition = "center";
        }

        // show edit button if user owns this storefront - Updated by Day Ekoi 4/20/26
        const sessionRes = await fetch("/api/auth/me");
        if (sessionRes.ok) {
            const sessionUser = await sessionRes.json();
            if (sessionUser.id && storefront.owner_id && sessionUser.id === storefront.owner_id) {
                const editBtn = document.createElement("button");
                editBtn.style.cssText = "background:#d4af37; color:#000; border:none; border-radius:999px; padding:8px 20px; font-weight:700; font-size:0.9rem; cursor:pointer; letter-spacing:1px; text-transform:uppercase; align-self:flex-start; margin-top:4px;";
                editBtn.textContent = "Edit Storefront";
                editBtn.onclick = () => {
                    window.location.href = `/storefronts/${storefrontId}/edit`;
                };
                document.querySelector(".profile-info-row").appendChild(editBtn);
            }
        }

        // fetch listings for this storefront
        const listRes = await fetch(`/api/storefronts/${storefrontId}/listings`);
        if (!listRes.ok) throw new Error("Could not load listings");
        const listings = await listRes.json();

        // render listings
        listingGrid.innerHTML = "";
        const activeListings = Array.isArray(listings)
            ? listings.filter(item => item.status !== "DELETED" && item.status !== "INACTIVE")
            : [];

        if (!activeListings.length) {
            renderEmpty("No listings available for this storefront yet.");
            return;
        }

        activeListings.forEach(item => {
            listingGrid.appendChild(createListingCard(item));
        });

    } catch (error) {
        console.error("Error loading storefront view:", error);
        brandName.textContent = "Storefront Unavailable";
        storeDescription.textContent = "Could not load storefront details. Please try again.";
        renderEmpty("Could not load listings.");
    }
}


// run on page load
loadStorefrontView();

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


