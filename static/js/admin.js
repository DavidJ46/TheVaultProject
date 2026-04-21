// File Created By David Jackson
// Updated by Day Ekoi - Iteration 5 - 4/20/26 - fixed storefront table to use brand_name field

// USERS SECTION

/*
 * Fetch all users from backend and display them in table
 * Calls: GET /admin/users
 */
async function loadUsers() {
    const response = await fetch('/admin/users'); // API request
    const users = await response.json(); // Convert response to JSON

    const table = document.querySelector('#usersTable tbody');
    table.innerHTML = ""; // Clear existing rows

    // Loop through users and create table rows
    users.forEach(user => {
        const row = `
            <tr>
                <td>${user.id}</td>
                <td>${user.email}</td>
                <td>
                    <!-- Delete button calls deleteUser() -->
                    <button class="delete" onclick="deleteUser(${user.id})">Delete</button>
                </td>
            </tr>
        `;
        table.innerHTML += row;
    });
}

/*
 * Delete a user by ID
 * Calls: DELETE /admin/users/<id>
 */
async function deleteUser(userId) {
    await fetch(`/admin/users/${userId}`, {
        method: 'DELETE'
    });

    // Reload users after deletion
    loadUsers();
}


// LISTINGS SECTION

/*
 * Fetch all listings and display them
 * Calls: GET /admin/listings
 */
async function loadListings() {
    const response = await fetch('/admin/listings');
    const listings = await response.json();

    const table = document.querySelector('#listingsTable tbody');
    table.innerHTML = "";

    listings.forEach(listing => {
        const row = `
            <tr>
                <td>${listing.id}</td>
                <td>${listing.title}</td>
                <td>
                    <!-- Delete listing button -->
                    <button class="delete" onclick="deleteListing(${listing.id})">Delete</button>
                </td>
            </tr>
        `;
        table.innerHTML += row;
    });
}

/*
 * Delete a listing by ID
 * Calls: DELETE /admin/listings/<id>
 */
async function deleteListing(listingId) {
    await fetch(`/admin/listings/${listingId}`, {
        method: 'DELETE'
    });

    // Reload listings after deletion
    loadListings();
}


// STOREFRONTS SECTION

/*
 * Fetch all storefronts
 * Calls: GET /admin/storefronts
 */
async function loadStorefronts() {
    const response = await fetch('/admin/storefronts');
    const stores = await response.json();

    const table = document.querySelector('#storefrontsTable tbody');
    table.innerHTML = "";

    stores.forEach(store => {
        const row = `
            <tr>
                <td>${store.id}</td>
                <td>${store.brand_name}</td>
            </tr>
        `;
        table.innerHTML += row;
    });
}
