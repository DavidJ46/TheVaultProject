/* 
storefront.js

  The Vault Campus Marketplace
  CSC 405 Sp 26
  Created by Day Ekoi - Iteration 4
  Date: 3/18/2026 - 3/22/2026

Description: This file is responsible for the behavior of the storefront homepage. As of now, it stores sample storefront data, creates storefront cards using that data, 
inserts the cards into the storefront grid in storefront.html, and handles the image carousel functionality for each storefront cards. 

This file works with:
- storefront.html
- storefront.css

This file will be updated to fetch real storefront data from the Flask API routes and display the actual storefronts created by users in the database.



STOREFRONT DATA

THESE ARE PLACEHOLDERS FOR NOW!!!!
it holds temp storefront data, creation of storefront cards, inserting them into the page, and handling image functionality 

Fields: 
    id: unique identifier for the storefront
    name: name of the storefront
    categories: array of categories/tags associated with the storefront
    items: number of items in the storefront
    logo: URL for the storefront's logo image
    images: array of URLs for the storefront's carousel images (4 images per storefront)


What needs to be replaced later: 
- The storefront data in the storefronts array to be fetched from the Flask API instead of being hardcoded, recieve JSON, render real storefronts
- Functionality & routing: menu button opens navigation pane, cart button routes to cart, account button routes to profile, Enter Storefront opens that store page
- Searching and page: search storefront name, 10 stores per page 
*/


// Storefront data structure:
// storefront 1 placeholder
let storefronts = [
  {
    id: 1,
    name: "Nike",
    categories: ["Athleisure", "Casual"],
    items: 24,
    logo: "/static/images/nikelogo.png",
    images: [
      "/static/images/nikehoodie1.png",
      "/static/images/nikehoodie2.png",
      "/static/images/nikejacket.png",
      "/static/images/nikepants1.png"
    ]
  },
  // storefront 2 placeholder
  {
    id: 2,
    name: "Onyx",
    categories: ["Casual", "Retro"],
    items: 26,
    logo: "/static/images/onyxlogo.jpeg",
    images: [
      "/static/images/onyxhoodie.png",
    ]
  },
  // storefront 3 placeholder
  {
    id: 3,
    name: "Essentials Fear of God",
    categories: ["Casual", "Streetwear"],
    items: 18,
    logo: "/static/images/essentialslogo.png",
    images: [
      "/static/images/essentials1.png",
      "/static/images/essentials2.png",
      "/static/images/essentials3.png",
      "/static/images/essentials4.png"
    ]
  },
  // storefront 4 placeholder
  {
    id: 4,
    name: "Von Dutch",
    categories: ["Streetwear", "Accessories"],
    items: 10,
    logo: "/static/images/vondutchlogo.png",
    images: [
      "/static/images/vondutch1.png",
      "/static/images/vondutch2.png",
      "/static/images/vondutch3.png",
      "/static/images/vondutch4.png"
    ]
  }
];




/* STROREFRONT CARDS 

Storefront cards/grid boxes will be generated dynamically from the storefronts array above. 
Each storefront will have a card with its logo, name, categories, item count, and about 4 images to appease to buyers.
 There are left and right arrows to navigate through the images.
*/

// Get the storefront grid container from the HTML where the cards will be inserted
const grid = document.getElementById("storefrontGrid");


// CREATE STOREFRONT CARD

/* 
The purpose of this function is to create a storefront card element from a storefront object.

Input: stores a storefront object from the storefronts array 
Output: Returns a HTML element (card) ready to be inserted into the page
*/
function createCard(store) {
  let index = 0; // keeps track of which image is currently being shown inside the card's image carousel. Starts at 0 (first image)

  const card = document.createElement("div"); // Created new element in memory
  card.className = "storefront-card"; // assigns the storefront-card class to the new element for styling purposes

  const categories = Array.isArray(store.categories) ? store.categories : [];
  const images = Array.isArray(store.images) && store.images.length > 0
    ? store.images
    : ["/static/images/placeholder-storefront.png"];

  const logo = store.logo || "/static/images/placeholder-storefront.png";
  const items = store.items ?? 0;


// this function inserts the HTML strucutre for the storefront card

  card.innerHTML = `
    <div>
      <div class="storefront-header">
        <img class="storefront-logo" src="${logo}">
        <div>
          <h2 class="storefront-name">${store.name}</h2>
          <p class="storefront-meta">
            ${categories.slice(0, 2).join(" • ")}${categories.length > 0 ? " • " : ""}${items} items
          </p>
        </div>
      </div>

      <div class="carousel-shell">
        <button class="carousel-btn left">&#10094;</button>
        <img class="carousel-image" src="${images[0]}">
        <button class="carousel-btn right">&#10095;</button>
      </div>

      <form action="/auth/add_to_cart" method="POST" class="bag-form">
        <input type="hidden" name="item_id" value="${store.id}">
        <input type="hidden" name="item_name" value="${store.name} Official Item">
        <input type="hidden" name="price" value="45.00"> <div class="selection-row">
          <select name="size" class="vault-select">
            <option value="S">S</option>
            <option value="M">M</option>
            <option value="L">L</option>
            <option value="XL">XL</option>
          </select>
          <input type="number" name="quantity" value="1" min="1" class="vault-qty">
        </div>
        <button type="submit" class="add-bag-btn">Add to Bag</button>
      </form>
    </div>

    <div class="storefront-footer" style="margin-top: 15px;">
      <button class="enter-btn" style="width: 100%;">Enter Storefront</button>
    </div>
  `;


// After card generation, references are grabbed to import elements inside the card

  const img = card.querySelector(".carousel-image");
  const left = card.querySelector(".left");
  const right = card.querySelector(".right");
  const enterBtn = card.querySelector(".enter-btn");


// Card Arrow button functionality 

// left arrow functionality: once clicked the index variable is decremented by 1 and moves one image backwards in the array
  left.onclick = () => {
    index = (index - 1 + images.length) % images.length;
    img.src = images[index];
  };

// right arrow functionality: once clicked, indec is incremeted by 1 and moves one image forward in the array 
  right.onclick = () => {
    index = (index + 1) % images.length;
    img.src = images[index];
  };

  // Enter storefront routing
  enterBtn.onclick = () => {
    window.location.href = `/storefronts/${store.id}`;
  };

  return card; // returns the fully built card
}


/*  function to render all stores

this function loops through all storefrotn objects in the storefronts array, creates a card for each, and then inserts the cards into the storefront grid 
*/
function renderStorefronts() {
  if (!grid) return; // Updated by Day E 3/22/26
  grid.innerHTML = ""; // this clears the gird. Useful for if there needs to be re-rendering 
  storefronts.forEach(store => { // loops through each store object in the storefronts array
    const card = createCard(store); //creates a card for the current store object
    grid.appendChild(card); // inserts the created card into the storefront grid in the HTML
  });
}


/* FETCH STOREFRONTS FROM FLASK API

This function requests storefront data from the Flask backend.
If the backend returns storefront data successfully, it replaces the placeholder storefronts array.
If the backend route is not ready yet or fails, the placeholder data will still be used.
*/
async function fetchStorefronts() {
  try {
    const response = await fetch("/api/storefronts");

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const data = await response.json();

    const storefrontArray = Array.isArray(data) ? data : [data]; // Updated by Day E 3/22/26

    storefronts = storefrontArray.map(store => ({
      id: store.id,
      name: store.brand_name || "Unnamed Storefront",
      categories: ["Vault Brand"], // Updated by Day E 3/22/26
      items: 0, // Updated by Day E 3/22/26
      logo: store.logo_url || "/static/images/placeholder-storefront.png",
      images: [
        store.banner_url || "/static/images/placeholder-storefront.png"
      ]
    }));

    renderStorefronts();
  } catch (error) {
    console.error("Error fetching storefronts from Flask API:", error);
    renderStorefronts(); // fallback to placeholder storefronts
  }
}

// Navigation pane functionality 

const menuBtn = document.querySelector(".menu-btn");
const navPane = document.getElementById("navPane");
const navOverlay = document.getElementById("navOverlay");

// open menu
if (menuBtn) { // Updated by Day E 3/22/26
  menuBtn.addEventListener("click", () => {
    navPane.classList.toggle("active");
    navOverlay.classList.toggle("active");
  });
}

// close when clicking overlay
if (navOverlay) { // Updated by Day E 3/22/26
  navOverlay.addEventListener("click", () => {
    navPane.classList.remove("active");
    navOverlay.classList.remove("active");
  });
}

console.log(storefronts); // logs the storefronts array to the console for debugging purposes
console.log(grid); // logs the storefront grid element to the console for debugging purposes

// SEARCH BAR FUNCTIONALITY
// Added by Day E 4/9/26
// filters storefront cards in real time as the user types in the search bar

const searchInput = document.getElementById("searchInput");

// filters storefronts by name based on search input
function filterStorefronts(query) {
    const filtered = storefronts.filter(store =>
        store.name.toLowerCase().includes(query.toLowerCase())
    );

    // render filtered results
    grid.innerHTML = "";

    if (!filtered.length) {
        grid.innerHTML = `<p style="color:#c9c9c9; font-style:italic; text-align:center; grid-column:1/-1; padding: 2rem;">No storefronts found for "${query}"</p>`;
        return;
    }

    filtered.forEach(store => {
        const card = createCard(store);
        grid.appendChild(card);
    });
}

//  input changes
if (searchInput) {
    searchInput.addEventListener("input", () => {
        const query = searchInput.value.trim();
        if (!query) {
            renderStorefronts(); // show all if search is cleared
        } else {
            filterStorefronts(query);
        }
    });
}

/* Initial render of the storefront cards. This will display the storefronts on the page when it is first loaded. */
fetchStorefronts(); // Updated by Day E 4/9/26 - this will now fetch real storefront data from the Flask API and then render the storefronts. If the API route is not ready or fails, it will fallback to rendering the placeholder storefronts. */

/* renderStorefronts(); // Updated by Day E 3/22/26 */


