// document.addEventListener("DOMContentLoaded", () => {
//     const sign_up_button = document.getElementById("login-button");

//     if (sign_up_button) {
//         sign_up_button.addEventListener("click", handle_sign_up);
//     }
// });

// async function handle_sign_up() {
//     const username_field = document.getElementById("username-field");
//     const password_field = document.getElementById("password-field");

//     const username = username_field.value.trim();
//     const password = password_field.value;

//     if (!username || !password) {
//         alert ("Fill In All Fields");
//         return;
//     }

//     try {
//         const response = await fetch("/auth/login", {
//             method: "POST",
//             headers: {
//                 "Content-Type" : "application/json"
//             },
//             body: JSON.stringify({
//                 username,
//                 password
//             })
//         });

//         const data = await response.json();

//         if (!response.ok) {
//             alert(data.error || data.message || "Login Failed");
//             return;
//         }

//         alert(data.message || "Logged In Scucessfully");
//         window.location.href = "/";
//     }
//         catch (error) {
//             console.error("Login Error:", error)
//             alert("Something Went Wrong During Login");
//         }
// }