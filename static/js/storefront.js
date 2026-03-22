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
const storefronts = [
  {
    id: 1,
    name: "Nike",
    categories: ["Athleisure", "Casual"],
    items: 24,
    logo: "images/nikelogo.png",
    images: [
      "images/nikehoodie1.png",
      "images/nikehoodie2.png",
      "images/nikejacket.png",
      "images/nikepants1.png"
    ]
  },
  // storefront 2 placeholder
  {
    id: 2,
    name: "Onyx",
    categories: ["Casual", "Retro"],
    items: 26,
    logo: "images/onyxlogo.jpeg",
    images: [
      "images/onyxhoodie.png",
    ]
  },
  // storefront 3 placeholder
  {
    id: 3,
    name: "Essentials Fear of God",
    categories: ["Casual", "Streetwear"],
    items: 18,
    logo: "images/essentialslogo.png",
    images: [
      "images/essentials1.png",
      "images/essentials2.png",
      "images/essentials3.png",
      "images/essentials4.png"
    ]
  },
  // storefront 4 placeholder
  {
    id: 4,
    name: "Von Dutch",
    categories: ["Streetwear", "Accessories"],
    items: 10,
    logo: "images/vondutchlogo.png",
    images: [
      "images/vondutch1.png",
      "images/vondutch2.png",
      "images/vondutch3.png",
      "images/vondutch4.png"
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


// this function inserts the HTML strucutre for the storefront card

  card.innerHTML = `
    <div>
      <div class="storefront-header">
        <img class="storefront-logo" src="${store.logo}">
        <div>
          <h2 class="storefront-name">${store.name}</h2>
          <p class="storefront-meta">
            ${store.categories.slice(0, 2).join(" • ")} • ${store.items} items
          </p>
        </div>
      </div>

      <div class="carousel-shell">
        <button class="carousel-btn left">&#10094;</button>
        <img class="carousel-image" src="${store.images[0]}">
        <button class="carousel-btn right">&#10095;</button>
      </div>
    </div>

    <div class="storefront-footer">
      <button class="enter-btn">Enter Storefront</button>
    </div>
  `;


// After card generation, references are grabbed to import elements inside the card

  const img = card.querySelector(".carousel-image");
  const left = card.querySelector(".left");
  const right = card.querySelector(".right");


// Card Arrow button functionality 

// left arrow functionality: once clicked the index variable is decremented by 1 and moves one image backwards in the array
  left.onclick = () => {
    index = (index - 1 + store.images.length) % store.images.length;
    img.src = store.images[index];
  };

// right arrow functionality: once clicked, indec is incremeted by 1 and moves one image forward in the array 
  right.onclick = () => {
    index = (index + 1) % store.images.length;
    img.src = store.images[index];
  };

  return card; // returns the fully built card
}


/*  function to render all stores

this function loops through all storefrotn objects in the storefronts array, creates a card for each, and then inserts the cards into the storefront grid 
*/
function renderStorefronts() {
  grid.innerHTML = ""; // this clears the gird. Useful for if there needs to be re-rendering 
  storefronts.forEach(store => { // loops through each store object in the storefronts array
    const card = createCard(store); //creates a card for the current store object
    grid.appendChild(card); // inserts the created card into the storefront grid in the HTML
  });
}

// Navigation pane functionality 

const menuBtn = document.querySelector(".menu-btn");
const navPane = document.getElementById("navPane");
const navOverlay = document.getElementById("navOverlay");

// open menu
menuBtn.addEventListener("click", () => {
  navPane.classList.toggle("active");
  navOverlay.classList.toggle("active");
});

// close when clicking overlay
navOverlay.addEventListener("click", () => {
  navPane.classList.remove("active");
  navOverlay.classList.remove("active");
});

console.log(storefronts); // logs the storefronts array to the console for debugging purposes
console.log(grid); // logs the storefront grid element to the console for debugging purposes

/* Initial render of the storefront cards. This will display the storefronts on the page when it is first loaded. */
renderStorefronts();
