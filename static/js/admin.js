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
                <td>${user.username || ""}</td>
                <td>${user.email}</td>
                <td>${user.role || "user"}</td>
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
                <td>${listing.storefront_name || "Unknown"}</td>
                <td>${listing.status || "ACTIVE"}</td>
                <td>
                    <button class="delete" onclick="deleteListing(${listing.id})">Soft Delete</button>
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
                <td>${store.is_active ? "Yes" : "No"}</td>
                <td>${store.item_count ?? 0}</td>
                <td>${store.categories || ""}</td>
            </tr>
        `;
        table.innerHTML += row;
    });
}


// RETURNS SECTION
async function loadReturns() {
    const response = await fetch('/admin/returns');
    const returns = await response.json();

    const table = document.querySelector('#returnsTable tbody');
    table.innerHTML = "";

    returns.forEach(item => {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${item.id}</td>
            <td>${item.username || ""}<br><small>${item.email || ""}</small></td>
            <td>${item.order_number}</td>
            <td>${item.has_damage ? "Yes" : "No"}</td>
            <td>${item.damage_image_url ? `<a href="${item.damage_image_url}" target="_blank" rel="noopener">View</a>` : "—"}</td>
            <td>
                <select data-return-id="${item.id}">
                    <option value="pending" ${item.status === "pending" ? "selected" : ""}>Pending</option>
                    <option value="reviewed" ${item.status === "reviewed" ? "selected" : ""}>Reviewed</option>
                    <option value="resolved" ${item.status === "resolved" ? "selected" : ""}>Resolved</option>
                </select>
                <button onclick="saveReturnStatus(${item.id})">Save</button>
            </td>
            <td>${item.reason}</td>
        `;
        table.appendChild(row);
    });
}

async function saveReturnStatus(returnId) {
    const select = document.querySelector(`select[data-return-id="${returnId}"]`);
    if (!select) return;

    const response = await fetch(`/admin/returns/${returnId}`, {
        method: "PATCH",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ status: select.value })
    });

    if (!response.ok) {
        const result = await response.json().catch(() => ({}));
        alert(result.error || "Failed to update return status.");
        return;
    }

    loadReturns();
}
