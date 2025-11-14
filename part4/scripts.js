const api_base_url = "http://127.0.0.1:5000/api/v1";

// custom fetch wrapper
async function apiFetch(url, options) {
	try {
		const response = await fetch(url, options);

		if (response.status === 401) {
			alert("You need to log in!");
			deleteCookie("token");
			document.getElementById("login-link").style.display = "inline";
			document.getElementById("logout-link").style.display = "none";
		}
		return response;
	} catch (error) {
		console.error("Fetch failed:", error);
		throw error;
	}
}

function deleteCookie(name) {
	document.cookie = name + "=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
}

function logout() {
	deleteCookie("token");
	window.location.href = '/login.html';
}

async function loginUser(email, password) {
	const res = await fetch(`${api_base_url}/auth/login`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({
			email,
			password
		})
	});
	const res_data = await res.json();
	if (!res.ok) {
		alert("Login Failed: " + res_data.error);
	} else {
		document.cookie = `token=${res_data.access_token}; path=/`;
		window.location.href = 'index.html';
	}
}

function checkAuthentication() {
	const token = getCookie('token');
	const loginLink = document.getElementById('login-link');
	const logoutLink = document.getElementById('logout-link');
	const reviewForm = document.getElementById('review-form');

	if (document.getElementById('places-list')) {
		fetchPlaces(token);
	}
	if (document.getElementById('place-details')) {
		fetchPlaceDetails(token, getPlaceIdFromURL());
	}

	if (token) {
		loginLink.style.display = 'none';
	} else {
		if (reviewForm) {
			reviewForm.innerHTML = "<p>Login to make reviews.</p>";
		}
		logoutLink.style.display = 'none';
	}
}

async function fetchPlaces(token) {
	// Make a GET request to fetch places data
	// Include the token in the Authorization header
	// Handle the response and pass the data to displayPlaces function
	const res = await apiFetch(`${api_base_url}/places/`, {
		headers: {
			"Authorization": `Bearer ${token}`
		}
	});
	if (res.ok) {
		displayPlaces(await res.json());
	}
}

function displayPlaces(places) {
	const placesList = document.getElementById("places-list");
	placesList.replaceChildren();
	places.forEach(place => {
		placesList.insertAdjacentHTML("beforeend", `
                <div class="place-card">
                        <h2>${place.title}</h2>
                        <span>Price per night: $${place.price}</span>
                        <button class="details-button">View Details</button>
                </div>
                `);
		const elem = placesList.lastElementChild;
		elem.price = place.price;
		elem.querySelector(".details-button").onclick = () => {
			window.location.href = `place.html?place_id=${place.id}`;
		};
	})
	document.getElementById('price-filter').value = "All";

}

function getCookie(name) {
	const nameEQ = name + "=";
	const ca = document.cookie.split(';');
	for (let i = 0; i < ca.length; i++) {
		let c = ca[i];
		while (c.charAt(0) === ' ') {
			c = c.substring(1);
		}
		if (c.indexOf(nameEQ) === 0) {
			return decodeURIComponent(c.substring(nameEQ.length, c.length));
		}
	}
	return null; // Return null if the cookie is not found
}

function getPlaceIdFromURL() {
	const params = new URLSearchParams(window.location.search);
	const placeId = params.get("place_id"); // extract ?place_id=...
	return placeId;
}

async function fetchPlaceDetails(token, placeId) {
	// Make a GET request to fetch place details
	// Include the token in the Authorization header
	// Handle the response and pass the data to displayPlaceDetails function
	const res = await apiFetch(`${api_base_url}/places/${placeId}`, {
		headers: {
			"Authorization": `Bearer ${token}`
		}
	});
	if (res.ok) {
		displayPlaceDetails(await res.json());
	}
}

function displayPlaceDetails(place) {
	// Clear the current content of the place details section
	// Create elements to display the place details (name, description, price, amenities and reviews)
	// Append the created elements to the place details section
	document.getElementById("title").innerHTML = `<h1>${place.title}</h1>`;
	const html = `
        <div class="place-info">
                <span><b>Host:</b> ${place.owner.first_name} ${place.owner.last_name}</span>
        </div>
        <div class="place-info">
                <span><b>Price per night:</b> $${place.price}</span>
        </div>
        <div class="place-info">
                <span><b>Description:</b> ${place.description}</span>
        </div>
        <div class="place-info">
                <span><b>Amenities:</b> ${place.amenities.map(p => p.name).join(', ')}</span>
        </div>
        `;
	document.getElementById('place-details').innerHTML = html;
	const reviewList = document.getElementById("reviews");
	reviewList.replaceChildren();
	if (place.reviews.length == 0) {
		reviewList.innerHTML = '<p>There are no reviews.</p>';
	}
	for (const review of place.reviews) {
		reviewList.insertAdjacentHTML("beforeend", `
                <div class="review-card">
                        <span><b>${review.user.first_name} ${review.user.last_name}:</b></span>
                        <span>${review.text}</span>
                        <span>Rating: ${"★".repeat(review.rating) + "☆".repeat(5 - review.rating)}</span>
                </div>
                `);
	}
}

async function submitReview(token, placeId, reviewText, reviewRating) {
	// Make a POST request to submit review data
	// Include the token in the Authorization header
	// Send placeId and reviewText in the request body
	// Handle the response
	const res = await apiFetch(`${api_base_url}/reviews/`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			'Authorization': `Bearer ${token}`
		},
		body: JSON.stringify({
			"text": reviewText,
			"rating": reviewRating,
			"place_id": placeId
		})
	});
	const res_data = await res.json();
	if (res.ok) {
		fetchPlaceDetails(getCookie('token'), placeId);
	} else {
		alert(`Could not create review: ${res_data.error}`)
	}
}

document.addEventListener('DOMContentLoaded', () => {
	const reviewForm = document.getElementById('review-form');
	const loginForm = document.getElementById('login-form');
	const priceFilter = document.getElementById('price-filter');
	const logoutLink = document.getElementById('logout-link');
	logoutLink.addEventListener('click', e => {
		e.preventDefault();
		logout();
	});
	if (loginForm) {
		loginForm.addEventListener('submit', async (event) => {
			event.preventDefault();
			const formData = new FormData(loginForm);
			const data = Object.fromEntries(formData.entries());

			await loginUser(data.email, data.password);
		});
	}
	if (priceFilter) {
		priceFilter.addEventListener('change', (event) => {
			const val = document.getElementById('price-filter').value;
			const placesList = document.getElementById('places-list');
			for (const child of placesList.children) {
				if (val == "All" || child.price <= val) {
					child.style.display = "flex";
				} else {
					child.style.display = "none";
				}
			}
		})
	}
	if (reviewForm) {
		reviewForm.addEventListener('submit', async (event) => {
			event.preventDefault();
			// Get review text from form
			// Make AJAX request to submit review
			// Handle the response
			const text = document.getElementById("review-text").value;
			const rating = Number(document.getElementById("rating").value);
			submitReview(getCookie("token"), getPlaceIdFromURL(), text, rating);
		});
	}
	checkAuthentication();
});
