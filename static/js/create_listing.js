/*
create_listing.js

The Vault Campus Marketplace
CSC 405 Sp 26
Created by Elali McNair - Iteration 4
Updated by Day Ekoi - Iteration 5 4/9/26

Purpose:
This file handles the form submission for the Create Listing page.
It collects form data, validates it, and submits it to the Flask backend API.

The form includes:
- Storefront name (to identify which storefront to assign the listing)
- Listing name/title
- Available sizes (checkboxes for S, M, L)
- Count/quantity available
- Price

This data is sent to the backend via the listing creation API endpoint.
*/

// Wait for DOM content to be fully loaded before accessing elements
document.addEventListener('DOMContentLoaded', function() {
  // Get form elements
  const listingForm = document.getElementById("listingForm");
  const cancelBtn = document.getElementById("cancelBtn");
  const storefrontSelect = document.getElementById("storefrontSelect");

  // Load user's storefronts for the dropdown
  if (storefrontSelect) {
    loadUserStorefronts();
  }

  // Handle form submission
  if (listingForm) {
    listingForm.addEventListener("submit", async (e) => {
      e.preventDefault();

      // get real user from session - Updated by Day E 4/9/26
      const userRes = await fetch("/auth/api/auth/me");
      if (!userRes.ok) {
        alert("You must be logged in to create a listing.");
        window.location.href = "/auth/login";
        return;
      }
      const user = await userRes.json();

      // Collect form data including file
      const storefrontId = document.getElementById("storefrontSelect").value;
      const listingName = document.getElementById("listingName").value.trim();
      const listingImageInput = document.getElementById("listingImage");
      const count = parseInt(document.getElementById("count").value);
      const price = parseFloat(document.getElementById("price").value);

      // Validate that a storefront is selected
      if (!storefrontId) {
        alert("Please select a storefront for this listing.");
        return;
      }

      // Collect selected sizes
      const sizeCheckboxes = document.querySelectorAll("input[name='sizes']:checked");
      const sizes = Array.from(sizeCheckboxes).map((cb) => cb.value);

      // Validate that at least one size is selected
      if (sizes.length === 0) {
        alert("Please select at least one size.");
        return;
      }

      // Validate form data
      if (!listingName || count < 1 || price < 0) {
        alert("Please fill in all required fields with valid values.");
        return;
      }

      try {
        // Create FormData object to handle file upload
        const formData = new FormData();
        formData.append("storefront_id", storefrontId);
        formData.append("title", listingName);
        formData.append("quantity_on_hand", count);
        formData.append("price", price);
        formData.append("fulfillment_type", "IN_STOCK");
        formData.append("status", "ACTIVE");
        formData.append("listing_image", listingImageInput.files[0]);
        formData.append("sizes_available", JSON.stringify(sizes));

        const response = await fetch("/api/listings/create", {
          method: "POST",
          headers: {
            "X-User-Id": user.id,
            "X-User-Role": user.role
          },
          body: formData,
        });

        const result = await response.json();

        if (response.ok) {
          alert("Listing created successfully!");
          window.location.href = "/my-storefront";
        } else {
          alert("Error creating listing: " + (result.error || "Unknown error"));
        }
      } catch (error) {
        console.error("Error submitting form:", error);
        alert("Error creating listing: " + error.message);
      }
    });
  }

  // Handle cancel button
  if (cancelBtn) {
    cancelBtn.addEventListener("click", () => {
      window.location.href = "/storefronts";
    });
  }

  // Function to load user's storefronts
  // Updated by Day E 4/9/26 - uses real session user instead of hardcoded ID
  async function loadUserStorefronts() {
    try {
      // get real user from session
      const userRes = await fetch("/auth/api/auth/me");
      if (!userRes.ok) {
        window.location.href = "/auth/login";
        return;
      }
      const user = await userRes.json();

      const response = await fetch("/api/storefronts/me", {
        method: "GET",
        headers: {
          "X-User-Id": user.id,
          "X-User-Role": user.role
        },
      });

      if (response.ok) {
        const storefrontData = await response.json();
        const storefronts = Array.isArray(storefrontData)
          ? storefrontData
          : storefrontData && storefrontData.id
            ? [storefrontData]
            : [];

        // Clear loading option
        storefrontSelect.innerHTML = "";

        if (storefronts.length > 0) {
          // Add a default selection prompt
          const defaultOption = document.createElement("option");
          defaultOption.value = "";
          defaultOption.textContent = "Select a storefront";
          defaultOption.disabled = true;
          defaultOption.selected = true;
          storefrontSelect.appendChild(defaultOption);

          storefronts.forEach((storefront) => {
            const option = document.createElement("option");
            option.value = storefront.id;
            option.textContent = storefront.brand_name || storefront.name || `Storefront #${storefront.id}`;
            storefrontSelect.appendChild(option);
          });
        } else {
          // user has no storefront — disable form and show message
          storefrontSelect.innerHTML = '<option value="" disabled>No storefronts found - create one first</option>';

          if (listingForm) {
            listingForm.querySelectorAll("input, select, button[type='submit']").forEach(el => {
              el.disabled = true;
            });
          }

          const messageDiv = document.createElement("div");
          messageDiv.style.cssText = "color: #d4af37; margin-top: 10px; font-weight: bold; text-align:center;";
          messageDiv.innerHTML = `You must create a storefront before creating listings. <a href="/storefronts/create" style="color:#fff; text-decoration:underline;">Create one here</a>`;
          storefrontSelect.parentNode.appendChild(messageDiv);
        }
      } else if (response.status === 404) {
        // user has no storefront
        storefrontSelect.innerHTML = '<option value="" disabled>No storefronts found - create one first</option>';

        if (listingForm) {
          listingForm.querySelectorAll("input, select, button[type='submit']").forEach(el => {
            el.disabled = true;
          });
        }

        const messageDiv = document.createElement("div");
        messageDiv.style.cssText = "color: #d4af37; margin-top: 10px; font-weight: bold; text-align:center;";
        messageDiv.innerHTML = `You must create a storefront before creating listings. <a href="/storefronts/create" style="color:#fff; text-decoration:underline;">Create one here</a>`;
        storefrontSelect.parentNode.appendChild(messageDiv);
      } else {
        console.error("Failed to load storefronts");
        storefrontSelect.innerHTML = '<option value="">Error loading storefronts</option>';
      }
    } catch (error) {
      console.error("Error loading storefronts:", error);
      storefrontSelect.innerHTML = '<option value="">Error loading storefronts</option>';
    }
  }
});