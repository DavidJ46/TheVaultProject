/*
    create_storefront.js

    The Vault Campus Marketplace 
    CSC 405 Sp 26'
    Created by Day Ekoi - Iteration 4 - 3/22/2026
    Updated by Day Ekoi - Iteration 5 4/9/26

Description:
This file handles the functionality for the Create Storefront page. 
It manages user interactions such as submitting the form, handling the cancel button,
and preparing storefront data to be sent to the backend.
*/


// get references: grabbing key elements from the HTML
const form = document.getElementById("storefrontForm");
const cancelBtn = document.getElementById("cancelBtn");


// cancel button: returns user to homepage
cancelBtn.addEventListener("click", () => {
    window.location.href = "/storefronts";
});


// form submission: handles create storefront action
form.addEventListener("submit", async (event) => {

    // prevent default: stops page from refreshing immediately
    event.preventDefault();

    // get current user first so we have their ID for the header
    try {
        const userRes = await fetch("/auth/api/auth/me");
        if (!userRes.ok) {
            alert("You must be logged in to create a storefront.");
            window.location.href = "/auth/login";
            return;
        }
        const user = await userRes.json();

        // build form data
        const formData = new FormData(form);

        // build JSON payload from form fields
        const payload = {
            brand_name: formData.get("brand_name"),
            bio: formData.get("description"),
            contact_info: formData.get("contact_info"),
            logo_url: null,
            banner_url: null
        };

        // send to Flask API
        const res = await fetch("/api/storefronts", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-User-Id": user.id,
                "X-User-Role": user.role
            },
            body: JSON.stringify(payload)
        });

        const data = await res.json();

        if (!res.ok) {
            alert(data.error || "Failed to create storefront.");
            return;
        }

        // success — route to new storefront dashboard
        window.location.href = "/my-storefront";

    } catch (err) {
        console.error("Error creating storefront:", err);
        alert("Something went wrong. Please try again.");
    }
});