/*
create_listing.js

The Vault Campus Marketplace
CSC 405 Sp 26
Created by Elali McNair - Iteration 4

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
        
        // Append sizes as JSON string
        formData.append("sizes_available", JSON.stringify(sizes));

        const response = await fetch("/api/listings/create", {
          method: "POST",
          headers: {
            "X-User-Id": "1", // TODO: Get actual user ID from session/auth
          },
          body: formData,
        });

        const result = await response.json();

        if (response.ok) {
          alert("Listing created successfully!");
          // Redirect to storefront view or homepage
          window.location.href = "/storefronts";
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
  async function loadUserStorefronts() {
    try {
      const response = await fetch("/api/storefronts/me", {
        method: "GET",
        headers: {
          "X-User-Id": "1", // TODO: Get actual user ID from session/auth
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
          // User doesn't have a storefront
          const option = document.createElement("option");
          option.value = "";
          option.textContent = "No storefronts found - create one first";
          option.disabled = true;
          storefrontSelect.appendChild(option);
          
          // Disable the form and show message
          if (listingForm) {
            listingForm.querySelectorAll("input, select, button[type='submit']").forEach(el => {
              el.disabled = true;
            });
          }
          
          // Show user-friendly message instead of alert
          const messageDiv = document.createElement("div");
          messageDiv.style.cssText = "color: red; margin-top: 10px; font-weight: bold;";
          messageDiv.textContent = "You must create a storefront before you can create listings.";
          storefrontSelect.parentNode.appendChild(messageDiv);
        }
      } else if (response.status === 404) {
        // User doesn't have a storefront
        storefrontSelect.innerHTML = '<option value="" disabled>No storefronts found - create one first</option>';
        
        // Disable the form and show message
        if (listingForm) {
          listingForm.querySelectorAll("input, select, button[type='submit']").forEach(el => {
            el.disabled = true;
          });
        }
        
        // Show user-friendly message
        const messageDiv = document.createElement("div");
        messageDiv.style.cssText = "color: red; margin-top: 10px; font-weight: bold;";
        messageDiv.textContent = "You must create a storefront before you can create listings.";
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

