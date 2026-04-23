// document.addEventListener("DOMContentLoaded", () => {
//     const sign_up_button = document.getElementById("signup-button");

//     if (sign_up_button) {
//         sign_up_button.addEventListener("click", handle_sign_up);
//     }
// });

// async function handle_sign_up() {
//     const username_field = document.getElementById("username-field");
//     const email_field = document.getElementById("email-field");
//     const password_field = document.getElementById("password-field");

//     const username = username_field.value.trim();
//     const email = email_field.value.trim();
//     const password = password_field.value;

//     if (!username || !email || !password) {
//         alert ("Fill In All Fields");
//         return;
//     }

//     try {
//         const response = await fetch("/auth/sign_up", {
//             method: "POST",
//             headers: {
//                 "Content-Type" : "application/json"
//             },
//             body: JSON.stringify({
//                 username,
//                 email,
//                 password
//             })
//         });

//         const data = await response.json();

//         if (!response.ok) {
//             alert(data.error || data.message || "Sign Up Failed");
//             return;
//         }

//         alert(data.message || "Signed Up Scucessfully");
//         window.location.href = "/";
//     }
//         catch (error) {
//             console.error("Sign Up Error:", error)
//             alert("Something Went Wrong During Signup");
//         }
// }