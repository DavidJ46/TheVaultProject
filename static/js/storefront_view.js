/* storefront_view.js */

document.addEventListener("DOMContentLoaded", function () {
    const listingGrid = document.getElementById("listingGrid");
    const backBtn = document.getElementById("backBtn");
    const brandNameEl = document.getElementById("brandName");
    const contactInfoEl = document.getElementById("contactInfo");
    const descriptionEl = document.getElementById("storeDescription");
    const listingsHeadingEl = document.getElementById("listingsHeading");
    const bannerEl = document.getElementById("storefrontBanner");
    const logoEl = document.getElementById("storefrontLogo");
    const logoFallbackEl = document.getElementById("logoFallback");
    const STORAGE_IDS_KEY = "vaultWishlistListingIds";
    const STORAGE_ITEMS_KEY = "vaultWishlistLocalItems";
    let currentStorefrontName = "Storefront";

    if (backBtn) {
        backBtn.addEventListener("click", function () {
            window.location.href = "/storefronts";
        });
    }

    const storefrontId = getStorefrontIdFromPath();
    if (!storefrontId) {
        renderEmpty("Invalid storefront id.");
        return;
    }

<<<<<<< Updated upstream
    initializeStorefront(storefrontId);

    function getStorefrontIdFromPath() {
        const parts = window.location.pathname.split("/").filter(Boolean);
        const id = parseInt(parts[parts.length - 1], 10);
        return Number.isNaN(id) ? null : id;
    }
=======
Later, this file will pull real listing data from the backend and render
the correct storefront information dynamically.
*/
>>>>>>> Stashed changes

    async function initializeStorefront(id) {
        const [storefrontData, listingsData] = await Promise.all([
            getStorefrontData(id),
            getStorefrontListings(id)
        ]);

        if (!storefrontData) {
            renderEmpty("Storefront not found.");
            return;
        }

        renderStorefront(storefrontData);
        renderListings(listingsData, storefrontData.id);
    }

    async function getStorefrontData(id) {
        const mockStorefront = getMockStorefront(id);
        if (mockStorefront) {
            return mockStorefront;
        }

        try {
            const response = await fetch(`/api/storefronts/${id}`);
            if (response.ok) {
                return await response.json();
            }
        } catch (error) {
            console.error("Error loading storefront from API:", error);
        }

        return null;
    }

    async function getStorefrontListings(id) {
        const mockListings = getMockListings(id);
        if (mockListings.length > 0) {
            return mockListings;
        }

        try {
            const response = await fetch(`/api/storefronts/${id}/listings`);
            if (response.ok) {
                const apiListings = await response.json();
                if (Array.isArray(apiListings) && apiListings.length > 0) {
                    return apiListings;
                }
            }
        } catch (error) {
            console.error("Error loading listings from API:", error);
        }

<<<<<<< Updated upstream
        return [];
    }

    function renderStorefront(store) {
        const name = store.brand_name || store.name || "Storefront";
        currentStorefrontName = name;
        if (brandNameEl) brandNameEl.textContent = name;
        if (listingsHeadingEl) listingsHeadingEl.textContent = `Shop ${name}`;
=======
                <button class="cart-btn" aria-label="Add to cart">
                    <svg viewBox="0 0 24 24" class="cart-svg">
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
                        <line x1="18" y1="5" x2="18" y2="11" stroke="currentColor" stroke-width="2"/>
                        <line x1="15" y1="8" x2="21" y2="8" stroke="currentColor" stroke-width="2"/>
                    </svg>
                </button>
            </div>
        `;
>>>>>>> Stashed changes

        const contact = store.instagram_handle || store.contact_info || "";
        if (contactInfoEl) contactInfoEl.textContent = contact;

        const description = store.bio || store.description || "No description available for this storefront yet.";
        if (descriptionEl) descriptionEl.textContent = description;

        const bannerImage = store.banner_url || store.banner;
        if (bannerEl && bannerImage) {
            bannerEl.style.background =
                `linear-gradient(rgba(0, 0, 0, 0.58), rgba(0, 0, 0, 0.58)), url(${bannerImage}) center/cover no-repeat`;
        }

        const logoImage = store.logo_url || store.logo;
        if (logoEl && logoImage) {
            logoEl.src = logoImage;
            logoEl.style.display = "block";
            if (logoFallbackEl) logoFallbackEl.style.display = "none";
        }
    }

    function renderListings(listings, storefrontId) {
        if (!listingGrid) return;
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
                <img class="listing-image" src="${imageUrl}" alt="${title}">
                <div class="listing-info">
                    <div class="listing-left">
                        <button class="wishlist-lock-btn ${selectedIds.has(String(item.id)) ? "active" : ""}" type="button" aria-label="Add to wishlist" title="Add to wishlist">
                            <svg viewBox="0 0 24 24" aria-hidden="true">
                                <path d="M7 10V7a5 5 0 0 1 10 0v3"></path>
                                <rect x="5" y="10" width="14" height="10" rx="2"></rect>
                            </svg>
                        </button>
                        <span class="item-name">${title}</span>
                    </div>
                    <span class="item-price">${priceValue}</span>
                </div>
            `;

            const lockBtn = card.querySelector(".wishlist-lock-btn");
            if (lockBtn && item.id) {
                lockBtn.addEventListener("click", function () {
                    const listingId = String(item.id);
                    const isActive = lockBtn.classList.contains("active");

                    if (isActive) {
                        lockBtn.classList.remove("active");
                        removeFromWishlistStorage(listingId);
                    } else {
                        lockBtn.classList.add("active");
                        saveToWishlistStorage({
                            listing_id: Number(item.id),
                            title,
                            price: priceValue,
                            storefront_name: currentStorefrontName,
                            image_url: imageUrl
                        });
                    }
                });
            }

            listingGrid.appendChild(card);
        });
    }

    function getWishlistIdSet() {
        try {
            const raw = localStorage.getItem(STORAGE_IDS_KEY);
            const list = raw ? JSON.parse(raw) : [];
            return new Set(list.map((id) => String(id)));
        } catch (error) {
            console.error("Failed to read wishlist ids from storage:", error);
            return new Set();
        }
    }

    function saveToWishlistStorage(item) {
        try {
            const idSet = getWishlistIdSet();
            idSet.add(String(item.listing_id));
            localStorage.setItem(STORAGE_IDS_KEY, JSON.stringify(Array.from(idSet)));

            const rawItems = localStorage.getItem(STORAGE_ITEMS_KEY);
            const items = rawItems ? JSON.parse(rawItems) : [];
            const exists = items.some((existing) => String(existing.listing_id) === String(item.listing_id));
            if (!exists) {
                items.push(item);
                localStorage.setItem(STORAGE_ITEMS_KEY, JSON.stringify(items));
            }
        } catch (error) {
            console.error("Failed to save wishlist item:", error);
        }
    }

    function removeFromWishlistStorage(listingId) {
        try {
            const idSet = getWishlistIdSet();
            idSet.delete(String(listingId));
            localStorage.setItem(STORAGE_IDS_KEY, JSON.stringify(Array.from(idSet)));

            const rawItems = localStorage.getItem(STORAGE_ITEMS_KEY);
            const items = rawItems ? JSON.parse(rawItems) : [];
            const filtered = items.filter((item) => String(item.listing_id) !== String(listingId));
            localStorage.setItem(STORAGE_ITEMS_KEY, JSON.stringify(filtered));
        } catch (error) {
            console.error("Failed to remove wishlist item:", error);
        }
    }

    function renderEmpty(message) {
        if (!listingGrid) return;
        listingGrid.innerHTML = `<p class="empty-state">${message}</p>`;
    }

    function getMockStorefront(id) {
        const stores = {
            1: {
                id: 1,
                name: "Nike",
                contact_info: "@nike",
                description: "Athleisure and casual pieces from Nike.",
                logo: "/static/images/nikelogo.png",
                banner: "/static/images/nikehoodie1.png"
            },
            2: {
                id: 2,
                name: "Onyx",
                contact_info: "@onyx",
                description: "Casual and retro inspired streetwear.",
                logo: "/static/images/onyxlogo.jpeg",
                banner: "/static/images/onyxhoodie.png"
            },
            3: {
                id: 3,
                name: "Essentials Fear of God",
                contact_info: "@essentials",
                description: "Minimal, clean silhouettes and premium comfort.",
                logo: "/static/images/essentialslogo.png",
                banner: "/static/images/essentials1.png"
            },
            4: {
                id: 4,
                name: "Von Dutch",
                contact_info: "@vondutch",
                description: "Vintage-inspired statement fashion and accessories.",
                logo: "/static/images/vondutchlogo.png",
                banner: "/static/images/vondutch1.png"
            }
        };

        return stores[id] || null;
    }

    function getMockListings(id) {
        const map = {
            1: [
                { id: 101, name: "Nike Hoodie", price: "$88.00", image_url: "/static/images/nikehoodie1.png" },
                { id: 102, name: "Nike Jacket", price: "$125.00", image_url: "/static/images/nikejacket.png" },
                { id: 103, name: "Nike Pants", price: "$76.00", image_url: "/static/images/nikepants1.png" }
            ],
            2: [
                { id: 201, name: "Onyx Diamond Hoodie", price: "$165.00", image_url: "/static/images/onyxhoodie.png" }
            ],
            3: [
                { id: 301, name: "Essential Hoodie", price: "$120.00", image_url: "/static/images/essentials2.png" },
                { id: 302, name: "Essential Sweatpants", price: "$98.00", image_url: "/static/images/essentials4.png" }
            ],
            4: [
                { id: 401, name: "Von Dutch Tee", price: "$54.00", image_url: "/static/images/vondutch2.png" },
                { id: 402, name: "Von Dutch Trucker", price: "$45.00", image_url: "/static/images/vondutch3.png" }
            ]
        };

        return map[id] || [];
    }

    function getMockListingImage(storefrontId, index) {
        const imageMap = {
            1: ["/static/images/nikehoodie1.png", "/static/images/nikejacket.png", "/static/images/nikepants1.png"],
            2: ["/static/images/onyxhoodie.png"],
            3: ["/static/images/essentials1.png", "/static/images/essentials2.png", "/static/images/essentials3.png"],
            4: ["/static/images/vondutch1.png", "/static/images/vondutch2.png", "/static/images/vondutch3.png"]
        };

        const images = imageMap[storefrontId] || ["/static/images/placeholder-storefront.png"];
        return images[index % images.length];
    }
});
<<<<<<< Updated upstream
=======


// initial render
renderListings();
>>>>>>> Stashed changes
