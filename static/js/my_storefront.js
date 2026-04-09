/*
    my_storefront.js

    The Vault Campus Marketplace 
    CSC 405 Sp 26'
    Created by Day Ekoi - Iteration 4 - 3/22/2026
    Implemented & Updated by Day Ekoi - Iteration 5 - 4/9/2026

Description:
Fetches the current user's storefront from the API and renders
the banner, logo, brand name, and listings dynamically.
Handles Edit Storefront, Create Listing, and View Public Storefront routing.
*/


// get references
const brandName = document.getElementById("brandName");
const bannerBox = document.getElementById("bannerBox");
const bannerFallback = document.getElementById("bannerFallback");
const logoImg = document.getElementById("logoImg");
const logoFallback = document.getElementById("logoFallback");
const listingGrid = document.getElementById("listingGrid");
const editStorefrontBtn = document.getElementById("editStorefrontBtn");
const createListingBtn = document.getElementById("createListingBtn");
const viewStorefrontBtn = document.getElementById("viewStorefrontBtn");

let storefrontId = null;


// renders empty state in listing grid
function renderEmpty(message) {
    listingGrid.innerHTML = `<p style="color:#888; font-style:italic; grid-column:1/-1; text-align:center;">${message}</p>`;
}


// builds a single listing card
function createListingCard(item) {
    const card = document.createElement("div");
    card.className = "listing-card";

    const title = item.title || item.name || "Untitled";
    const price = `$${Number(item.price || 0).toFixed(2)}`;
    const imageUrl = item.image_url || "/static/images/placeholder-storefront.png";

    card.innerHTML = `
        <img src="${imageUrl}" alt="${title}" style="width:100%; height:180px; object-fit:cover; border-radius:28px 28px 0 0;">
        <div style="padding: 1rem;">
            <p style="font-weight:700; color:#000;">${title}</p>
            <p style="color:#B8860B; font-weight:700;">${price}</p>
        </div>
    `;

    return card;
}


// fetches storefront and listings and renders the page
async function loadMyStorefront() {
    try {
        // get current user
        const userRes = await fetch("/auth/api/auth/me");
        if (!userRes.ok) {
            window.location.href = "/auth/login";
            return;
        }
        const user = await userRes.json();

        // get user's storefront
        const sfRes = await fetch("/api/storefronts/me", {
            headers: {
                "X-User-Id": user.id,
                "X-User-Role": user.role
            }
        });

        if (!sfRes.ok) { // updated by Day E 4/9/26 - if user has no storefront, show empty state instead of redirecting to create page
            brandName.textContent = "No Storefront Found";
            renderEmpty(`
                <div style="text-align:center; padding:2rem;">
                    <p style="color:#888; font-style:italic; margin-bottom:1rem;">You don't have a storefront yet.</p>
                    <a href="/storefronts/create"><button class="action-btn">Create Your Storefront</button></a>
                </div>
            `);
            return;
            // no storefront — redirect to create
            // window.location.href = "/storefronts/create";
            // return;
        }

        const storefront = await sfRes.json();
        storefrontId = storefront.id;

        // populate brand name
        brandName.textContent = storefront.brand_name || "My Storefront";

        // populate banner
        if (storefront.banner_url) {
            bannerBox.style.backgroundImage = `url('${storefront.banner_url}')`;
            bannerBox.style.backgroundSize = "cover";
            bannerBox.style.backgroundPosition = "center";
            bannerFallback.style.display = "none";
        }

        // populate logo
        if (storefront.logo_url) {
            logoImg.src = storefront.logo_url;
            logoImg.style.display = "block";
            logoFallback.style.display = "none";
        }

        // wire up buttons now that we have storefront ID
        editStorefrontBtn.onclick = () => {
            window.location.href = `/storefronts/${storefrontId}/edit`;
        };

        viewStorefrontBtn.onclick = () => {
            window.location.href = `/storefronts/${storefrontId}`;
        };

        createListingBtn.onclick = () => {
            window.location.href = "/listings/create";
        };

        // fetch listings
        const listRes = await fetch(`/api/storefronts/${storefrontId}/listings`, {
            headers: {
                "X-User-Id": user.id,
                "X-User-Role": user.role
            }
        });

        if (!listRes.ok) {
            renderEmpty("Could not load listings.");
            return;
        }

        const listings = await listRes.json();
        const active = listings.filter(l => l.status !== "DELETED" && l.status !== "INACTIVE");

        listingGrid.innerHTML = "";
        if (!active.length) {
            renderEmpty("No listings yet. Create your first listing!");
            return;
        }

        active.forEach(item => listingGrid.appendChild(createListingCard(item)));

    } catch (error) {
        console.error("Error loading my storefront:", error);
        brandName.textContent = "Could not load storefront.";
        renderEmpty("Something went wrong.");
    }
}


// run on page load
loadMyStorefront();