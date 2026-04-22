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

  function ensureToastRoot() {
    let root = document.getElementById("toastRoot");
    if (!root) {
      root = document.createElement("div");
      root.id = "toastRoot";
      root.className = "toast-root";
      document.body.appendChild(root);
    }
    return root;
  }

  function showListingToast(message, tone = "success") {
    const root = ensureToastRoot();
    const toast = document.createElement("div");
    toast.className = `toast ${tone === "success" ? "success" : "error"}`;
    toast.textContent = message;
    root.appendChild(toast);

    window.setTimeout(() => {
      toast.classList.add("fade-out");
      window.setTimeout(() => toast.remove(), 220);
    }, 2200);
  }

  // Get form elements
  const listingForm = document.getElementById("listingForm");
  const cancelBtn = document.getElementById("cancelBtn");
  const storefrontSelect = document.getElementById("storefrontSelect");
  const previewInputs = [1, 2, 3, 4].map((index) => document.getElementById(`previewImage${index}`));
  const selectedListingImages = [null, null, null, null];

  function renderSinglePreview(previewContainer, file, zone, slotIndex) {
    if (!previewContainer) return;

    previewContainer.innerHTML = "";
    if (!file) {
      if (zone) {
        zone.classList.remove("has-image");
        zone.style.backgroundImage = "";
        const existingBadge = zone.querySelector(".image-selected-badge");
        if (existingBadge) {
          existingBadge.remove();
        }
      }
      return;
    }

    const thumbWrap = document.createElement("div");
    thumbWrap.className = "thumb-wrap";

    const image = document.createElement("img");
    image.src = URL.createObjectURL(file);
    image.alt = file.name;
    image.onload = () => URL.revokeObjectURL(image.src);

    const fileName = document.createElement("p");
    fileName.className = "thumb-name";
    fileName.textContent = file.name;

    thumbWrap.appendChild(image);
    thumbWrap.appendChild(fileName);
    previewContainer.appendChild(thumbWrap);

    if (zone) {
      const zoneImageUrl = URL.createObjectURL(file);
      zone.style.backgroundImage = `url('${zoneImageUrl}')`;
      zone.classList.add("has-image");

      const existingBadge = zone.querySelector(".image-selected-badge");
      if (existingBadge) {
        existingBadge.remove();
      }

      const badge = document.createElement("span");
      badge.className = "image-selected-badge";
      badge.textContent = `Image ${slotIndex + 1} selected`;
      zone.appendChild(badge);
    }
  }

  function wireDropZone(zone, input, previewContainer, slotIndex) {
    if (!zone || !input) return;

    zone.addEventListener("click", () => input.click());

    zone.addEventListener("dragover", (event) => {
      event.preventDefault();
      zone.classList.add("dragover");
    });

    zone.addEventListener("dragleave", () => {
      zone.classList.remove("dragover");
    });

    zone.addEventListener("drop", (event) => {
      event.preventDefault();
      zone.classList.remove("dragover");

      const droppedFile = event.dataTransfer?.files?.[0];
      if (droppedFile && droppedFile.type.startsWith("image/")) {
        selectedListingImages[slotIndex] = droppedFile;
        renderSinglePreview(previewContainer, droppedFile, zone, slotIndex);
      }
    });

    input.addEventListener("change", () => {
      const chosenFile = input.files?.[0];
      selectedListingImages[slotIndex] = chosenFile && chosenFile.type.startsWith("image/")
        ? chosenFile
        : null;
      renderSinglePreview(previewContainer, selectedListingImages[slotIndex], zone, slotIndex);
    });
  }

  [1, 2, 3, 4].forEach((index, arrayIndex) => {
    const zone = document.getElementById(`previewZone${index}`);
    const input = previewInputs[arrayIndex];
    const preview = document.getElementById(`previewPreview${index}`);
    wireDropZone(zone, input, preview, arrayIndex);
  });

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

      const listingImages = selectedListingImages.filter(Boolean);

      if (listingImages.length === 0) {
        alert("Please upload at least one listing image.");
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
        listingImages.forEach((file) => {
          formData.append("listing_images", file);
        });
        // Backward compatibility in case older backend code expects listing_image.
        formData.append("listing_image", listingImages[0]);
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
          showListingToast(`Listing "${listingName}" created successfully!`);
          window.setTimeout(() => {
            window.location.href = "/my-storefront";
          }, 2500);
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