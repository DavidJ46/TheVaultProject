/*
    storefront_view.js

    The Vault Campus Marketplace 
    CSC 405 Sp 26'
    Created by Day Ekoi - Iteration 4
    3/22/2026
    Updated by Day Ekoi - Iteration 5 4/9/26
    Updated by Day Ekoi - Iteration 5 - 4/20/26 - fixed wishlistIds undefined crash and isWishlisted undefined in createListingCard

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
const pageTitle = document.getElementById("pageTitle");
const contactInfo = document.getElementById("contactInfo");
const storeDescription = document.getElementById("storeDescription");
const storefrontLogo = document.getElementById("storefrontLogo");
const logoFallback = document.getElementById("logoFallback");
const listingGrid = document.getElementById("listingGrid");


function ensureToastRoot() {
    let root = document.getElementById("cartToastRoot");
    if (!root) {
        root = document.createElement("div");
        root.id = "cartToastRoot";
        root.className = "cart-toast-root";
        document.body.appendChild(root);
    }
    return root;
}


function showCartToast(message, tone = "success") {
    const root = ensureToastRoot();
    const toast = document.createElement("div");
    toast.className = `cart-toast ${tone === "error" ? "error" : "success"}`;
    toast.textContent = message;
    root.appendChild(toast);

    window.setTimeout(() => {
        toast.classList.add("fade-out");
        window.setTimeout(() => toast.remove(), 220);
    }, 2200);
}


function toNumericPrice(priceValue) {
    if (typeof priceValue === "number") return priceValue;
    if (typeof priceValue === "string") {
        const cleaned = priceValue.replace(/\$/g, "").trim();
        const parsed = Number(cleaned);
        if (!Number.isNaN(parsed)) return parsed;
    }
    return 0;
}


function parseSizesFromListing(item) {
    const source = item.sizes_available;

    if (Array.isArray(source)) {
        return source.map((size) => String(size).trim()).filter(Boolean);
    }

    if (typeof source === "string" && source.trim()) {
        try {
            const parsed = JSON.parse(source);
            if (Array.isArray(parsed)) {
                return parsed.map((size) => String(size).trim()).filter(Boolean);
            }
        } catch (_error) {
            return source
                .split(",")
                .map((size) => size.trim())
                .filter(Boolean);
        }
    }

    return [];
}


async function getListingSizeOptions(listingId, item) {
    const inlineSizes = parseSizesFromListing(item);
    if (inlineSizes.length > 0) {
        return inlineSizes;
    }

    try {
        const response = await fetch(`/api/listings/${listingId}/sizes`);
        if (!response.ok) {
            return [];
        }

        const data = await response.json();
        if (!Array.isArray(data)) {
            return [];
        }

        return data
            .map((entry) => String(entry.size || "").trim())
            .filter(Boolean);
    } catch (error) {
        console.error("Unable to load listing sizes:", error);
        return [];
    }
}


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
        storefront_name: item.storefront_name || item.storefront?.brand_name || pageTitle?.textContent || "Storefront"
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
        storefront_name: item.storefront_name || pageTitle?.textContent || "Storefront"
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
async function createListingCard(item, wishlistIds, currentUserId) {
    const card = document.createElement("div");
    card.className = "listing-card";

    const listingId = Number(item.id || item.listing_id);
    const title = item.title || item.name || "Untitled Listing";
    const numericPrice = toNumericPrice(item.price);
    const price = typeof item.price === "string" && item.price.includes("$")
        ? item.price
        : `$${numericPrice.toFixed(2)}`;
    const imageUrl = item.image_url || "/static/images/placeholder-storefront.png";
    const isWishlisted = wishlistIds.has(String(listingId));
    const sizeOptions = await getListingSizeOptions(listingId, item);
    const hasSizes = sizeOptions.length > 0;

    const sizeOptionsMarkup = hasSizes
        ? sizeOptions
            .map((size, index) => `<option value="${size}" ${index === 0 ? "selected" : ""}>${size}</option>`)
            .join("")
        : `<option value="" selected disabled>No sizes available</option>`;

    const maxQuantity = item.quantity_on_hand || 1;

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
            </div>
        </div>
        <div class="purchase-panel">
            <div class="purchase-fields">
                <label class="field-label" for="sizeSelect-${listingId}">Size</label>
                <select id="sizeSelect-${listingId}" class="size-select" ${hasSizes ? "" : "disabled"}>
                    ${sizeOptionsMarkup}
                </select>
                <label class="field-label" for="countInput-${listingId}">Count</label>
                <input id="countInput-${listingId}" class="count-input" type="number" min="1" max="${maxQuantity}" step="1" value="1" inputmode="numeric">
            </div>
            <button type="button" class="add-to-cart-btn" ${hasSizes ? "" : "disabled"}>Add to Cart</button>
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
                    storefront_name: pageTitle?.textContent || "Storefront"
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

    const sizeSelect = card.querySelector(".size-select");
    const countInput = card.querySelector(".count-input");
    const addToCartBtn = card.querySelector(".add-to-cart-btn");

    addToCartBtn.addEventListener("click", async () => {
        if (!currentUserId) {
            alert("Please log in to add items to your cart.");
            window.location.href = "/auth/login";
            return;
        }

        const selectedSize = sizeSelect.value;
        const selectedCount = Number.parseInt(countInput.value, 10);
        const maxQuantity = item.quantity_on_hand || 1;

        if (!selectedSize) {
            showCartToast("Please select a size.", "error");
            return;
        }

        if (!Number.isInteger(selectedCount) || selectedCount < 1) {
            showCartToast("Count must be at least 1.", "error");
            countInput.value = "1";
            return;
        }

        if (selectedCount > maxQuantity) {
            showCartToast(`Maximum available quantity is ${maxQuantity}.`, "error");
            countInput.value = String(maxQuantity);
            return;
        }

        addToCartBtn.disabled = true;

        try {
            const formData = new FormData();
            formData.append("item_id", String(listingId));
            formData.append("item_name", title);
            formData.append("price", String(numericPrice));
            formData.append("quantity", String(selectedCount));
            formData.append("size", selectedSize);

            const response = await fetch("/auth/add_to_cart", {
                method: "POST",
                body: formData,
                redirect: "follow"
            });

            if (!response.ok) {
                throw new Error("Unable to add item to cart right now.");
            }

            showCartToast(`${title} (${selectedSize}) x${selectedCount} added to cart.`);
        } catch (error) {
            console.error("Add to cart failed:", error);
            showCartToast(error.message || "Unable to add to cart.", "error");
        } finally {
            addToCartBtn.disabled = false;
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
        if (pageTitle) pageTitle.textContent = storefront.brand_name || "Unnamed Storefront";
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

        // get session user and wishlist (both optional — page works for logged-out users too)
        const sessionUser = await getCurrentSessionUser();
        const wishlistIds = await getWishlistIdSet(sessionUser?.id || null);

        // Removed by Day Ekoi - Iteration 5 - 4/20/26: public storefront view no longer injects an edit button into the banner.

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

        const cards = await Promise.all(
            activeListings.map((item) => createListingCard(item, wishlistIds, sessionUser?.id || null))
        );

        cards.forEach((card) => {
            listingGrid.appendChild(card);
        });

    } catch (error) {
        console.error("Error loading storefront view:", error);
        if (pageTitle) pageTitle.textContent = "Storefront Unavailable";
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

