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
const AUTH_ME_ENDPOINT = "/auth/api/auth/me";

// get references to page elements
const brandName = document.getElementById("brandName");
const contactInfo = document.getElementById("contactInfo");
const storeDescription = document.getElementById("storeDescription");
const storefrontLogo = document.getElementById("storefrontLogo");
const logoFallback = document.getElementById("logoFallback");
const listingGrid = document.getElementById("listingGrid");


function getLocalWishlistItems() {
    try {
        const raw = localStorage.getItem("vaultWishlistLocalItems");
        return raw ? JSON.parse(raw) : [];
    } catch (error) {
        console.error("Unable to read local wishlist:", error);
        return [];
    }
}


function setLocalWishlistItems(items) {
    const normalized = items.map((item) => ({
        listing_id: Number(item.listing_id || item.id),
        title: item.title || item.name || item.listing?.title || "Untitled Listing",
        price: item.price ?? item.listing?.price ?? 0,
        image_url: item.image_url || item.listing?.image_url || item.storefront?.logo_url || "/static/images/logo.png",
        storefront_name: item.storefront_name || item.storefront?.brand_name || brandName.textContent || "Storefront"
    }));

    localStorage.setItem("vaultWishlistLocalItems", JSON.stringify(normalized));
    localStorage.setItem("vaultWishlistListingIds", JSON.stringify(normalized.map((item) => String(item.listing_id))));
}


function addLocalWishlistItem(item) {
    const items = getLocalWishlistItems();
    const listingId = String(item.listing_id || item.id);
    const filtered = items.filter((existing) => String(existing.listing_id || existing.id) !== listingId);
    filtered.unshift({
        listing_id: Number(listingId),
        title: item.title || item.name || "Untitled Listing",
        price: item.price,
        image_url: item.image_url || "/static/images/logo.png",
        storefront_name: item.storefront_name || brandName.textContent || "Storefront"
    });
    setLocalWishlistItems(filtered);
}


function removeLocalWishlistItem(listingId) {
    const updated = getLocalWishlistItems().filter((item) => String(item.listing_id || item.id) !== String(listingId));
    setLocalWishlistItems(updated);
}


async function getCurrentSessionUser() {
    try {
        const response = await fetch(AUTH_ME_ENDPOINT);
        if (!response.ok) return null;

        const user = await response.json();
        if (user && user.id) {
            localStorage.setItem("vaultUserId", String(user.id));
            sessionStorage.setItem("vaultUserId", String(user.id));
        }
        return user;
    } catch (error) {
        console.error("Unable to determine current user:", error);
        return null;
    }
}


async function getWishlistIdSet(userId) {
    if (!userId) {
        return new Set();
    }

    try {
        const response = await fetch("/api/wishlist", {
            headers: {
                "X-User-Id": String(userId)
            }
        });

        if (!response.ok) {
            throw new Error("Failed to load wishlist status");
        }

        const data = await response.json();
        const wishlistItems = Array.isArray(data.wishlist) ? data.wishlist : [];
        setLocalWishlistItems(wishlistItems);

        return new Set(wishlistItems.map((item) => String(item.listing_id || item.id)));
    } catch (error) {
        console.error("Unable to load wishlist ids:", error);
        return new Set(getLocalWishlistItems().map((item) => String(item.listing_id || item.id)));
    }
}


// renders an empty state message in the listing grid
function renderEmpty(message) {
    listingGrid.innerHTML = `<p style="color:#c9c9c9; font-style:italic; text-align:center; grid-column: 1/-1;">${message}</p>`;
}


// builds and returns a single listing card element
function createListingCard(item, wishlistIds, currentUserId) {
    const card = document.createElement("div");
    card.className = "listing-card";

    const listingId = Number(item.id || item.listing_id);
    const title = item.title || item.name || "Untitled Listing";
    const price = typeof item.price === "string" && item.price.includes("$")
        ? item.price
        : `$${Number(item.price || 0).toFixed(2)}`;
    const imageUrl = item.image_url || "/static/images/placeholder-storefront.png";

    card.innerHTML = `
        ${imageUrl ? `<img class="listing-image" src="${imageUrl}" alt="${title}">` : `<div class="listing-image"></div>`}
        <div class="listing-info">
            <div class="listing-copy">
                <span class="item-name">${title}</span>
                <span class="item-price">${price}</span>
            </div>
            <div class="listing-actions">
                <button class="wishlist-lock-btn ${isWishlisted ? "active" : ""}" type="button" aria-label="${isWishlisted ? "Remove from wishlist" : "Add to wishlist"}" title="${isWishlisted ? "Remove from wishlist" : "Add to wishlist"}">
                    <svg viewBox="0 0 24 24" class="wishlist-lock-icon" aria-hidden="true">
                        <circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="1.8"/>
                        <rect x="8.5" y="11" width="7" height="5.8" rx="1.2" fill="none" stroke="currentColor" stroke-width="1.8"/>
                        <path d="M10 11V9.7a2 2 0 1 1 4 0V11" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>
                    </svg>
                </button>
                <button class="cart-btn" aria-label="Add to cart">
                    <svg viewBox="0 0 24 24" class="cart-svg">
                        <path d="M6 8h12l-1 11H7L6 8Z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>
                        <path d="M9 8V6a3 3 0 0 1 6 0v2" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                        <line x1="18" y1="5" x2="18" y2="11" stroke="currentColor" stroke-width="2"/>
                        <line x1="15" y1="8" x2="21" y2="8" stroke="currentColor" stroke-width="2"/>
                    </svg>
                </button>
            </div>
        </div>
    `;

    const wishlistBtn = card.querySelector(".wishlist-lock-btn");
    wishlistBtn.addEventListener("click", async () => {
        if (!currentUserId) {
            alert("Please log in to add items to your wishlist.");
            window.location.href = "/auth/login";
            return;
        }

        wishlistBtn.disabled = true;
        const isActive = wishlistBtn.classList.contains("active");

        try {
            const response = await fetch(isActive ? `/api/wishlist/${listingId}` : "/api/wishlist", {
                method: isActive ? "DELETE" : "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-User-Id": String(currentUserId)
                },
                body: isActive ? undefined : JSON.stringify({ listing_id: listingId })
            });

            const result = await response.json().catch(() => ({}));
            if (!response.ok && !(response.status === 400 && /already in wishlist/i.test(result.error || ""))) {
                throw new Error(result.error || "Unable to update wishlist.");
            }

            const nextState = !isActive;
            wishlistBtn.classList.toggle("active", nextState);
            wishlistBtn.setAttribute("aria-label", nextState ? "Remove from wishlist" : "Add to wishlist");
            wishlistBtn.setAttribute("title", nextState ? "Remove from wishlist" : "Add to wishlist");

            if (nextState) {
                wishlistIds.add(String(listingId));
                addLocalWishlistItem({
                    listing_id: listingId,
                    title,
                    price,
                    image_url: imageUrl,
                    storefront_name: brandName.textContent || "Storefront"
                });
            } else {
                wishlistIds.delete(String(listingId));
                removeLocalWishlistItem(listingId);
            }
        } catch (error) {
            console.error("Wishlist update failed:", error);
            alert(error.message || "Unable to update wishlist right now.");
        } finally {
            wishlistBtn.disabled = false;
        }
    });

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

        // show edit button if user owns this storefront
        const sessionRes = await fetch("/api/auth/me");
        if (sessionRes.ok) {
            const sessionUser = await sessionRes.json();
            if (sessionUser.id && storefront.owner_id && sessionUser.id === storefront.owner_id) {
                const editBtn = document.createElement("button");
                editBtn.className = "back-btn";
                editBtn.style.cssText = "position:absolute; right:1.4rem; top:1.4rem; color:#d4af37; border:1px solid #d4af37; background:transparent; padding:6px 14px; cursor:pointer; text-transform:uppercase; font-weight:700; letter-spacing:1px;";
                editBtn.textContent = "Edit Storefront";
                editBtn.onclick = () => {
                    window.location.href = `/storefronts/${storefrontId}/edit`;
                };
                document.getElementById("storefrontBanner").appendChild(editBtn);
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
            listingGrid.appendChild(createListingCard(item, wishlistIds, sessionUser?.id || null));
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


