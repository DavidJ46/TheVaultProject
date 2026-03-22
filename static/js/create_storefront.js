/*
    create_storefront.js

    The Vault Campus Marketplace 
    CSC 405 Sp 26'
    Created by Day Ekoi - Iteration 5
    3/22/2026


Description:
This file handles the functionality for the Create Storefront page. 
It manages user interactions such as submitting the form, handling the cancel button,
and preparing storefront data to be sent to the backend.

Currently, it logs form data for testing purposes. In the future, this file will:
- send data to Flask API endpoints
- handle validation
- manage image previews
- display success/error messages
*/


// get references: grabbing key elements from the HTML
const form = document.getElementById("storefrontForm");
const cancelBtn = document.getElementById("cancelBtn");


// cancel button: returns user to homepage or previous page
cancelBtn.addEventListener("click", () => {
    // for now just go back to storefront homepage
    window.location.href = "/";
});


// form submission: handles create storefront action
form.addEventListener("submit", (event) => {

    // prevent default: stops page from refreshing immediately
    event.preventDefault();

    // form data object: collects all input values
    const formData = new FormData(form);

    // logging: shows all submitted data in console (for testing)
    console.log("storefront form submitted");

    for (let [key, value] of formData.entries()) {
        console.log(`${key}:`, value);
    }

    // placeholder: simulate success
    alert("Storefront created (placeholder)");

    // future: this is where you will send data to Flask
    /*
    fetch("/api/storefronts", {
        method: "POST",
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        console.log(data);
        window.location.href = "/storefront";
    })
    .catch(err => console.error(err));
    */
});
