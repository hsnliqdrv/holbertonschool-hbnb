# Project Structure
The app/ directory contains the core application code.
The api/ subdirectory houses the API endpoints, organized by version (v1/).
The models/ subdirectory contains the business logic classes (e.g., user.py, place.py).
The services/ subdirectory is where the Facade pattern is implemented, managing the interaction between layers.
The persistence/ subdirectory is where the in-memory repository is implemented. This will later be replaced by a database-backed solution using SQL Alchemy.
run.py is the entry point for running the Flask application.
config.py will be used for configuring environment variables and application settings.
requirements.txt will list all the Python packages needed for the project.
README.md will contain a brief overview of the project.
# Usage
```sh
# Install dependencies
$ pip install -r requirements.txt
# Run the app
$ python run.py
```
# Information About Models
## User
This model represents a user. A user have profile and can be regular user or admin.
Users can make reviews, add and own places.
## Place
This model represents a place. A place has an owner and amenities associated with
it. A place can have reviews from users.
## Review
This model represents a review. A review is consisted of rating point
and comment. Reviews are owned by places and users.
## Amenity
This model represents an amenity. An amenity is an additional
feature of a place.
### Examples
```python
user = User("John", "Doe", "johndoe@abc.com", "****", False)
amenity = Amenity("Wi-Fi", "Wi-Fi service")
place = Place("My home", 150.0, 45, 45, user)
user.addPlace(place)
place.addAmenity(amenity)
review = Review(place.id, user.id, 5.0, "Excellent option!")
place.addReview(review)
```

# API

## Users
User model:
```json
{
  "first_name": String,
  "last_name": String,
  "email": String
}
```
### Register a user
```
POST /api/v1/users/
Content-Type: application/json

{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com"
}
```
Expected Response:
```
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com"
}

// 201 Created
```
Possible Status Codes:

- 201 Created: When the user is successfully created.
- 400 Bad Request: If the email is already registered or input data is invalid.
### Get list of users
```
GET /api/v1/users/
Content-Type: application/json
```
Expected Response:
```
[
  {
    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com"
  },
  ...
]

// 200 OK
```
Possible Status Codes:

- 200 OK: When the list of users is successfully retrieved.
### Get a user
```
GET /api/v1/users/<user_id>
Content-Type: application/json
```
Expected Response:
```
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@x.com"
}
// 200 OK
```
Possible Status Codes:

- 200 OK: When the user is successfully retrieved.
- 404 Not Found: If the user does not exist.
### Update a user
```
PUT /api/v1/users/<user_id>
Content-Type: application/json

{
  "first_name": "Jane",
  "last_name": "Doe",
  "email": "jane.doe@example.com"
}
```
Expected Response:
```
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "first_name": "Jane",
  "last_name": "Doe",
  "email": "jane.doe@example.com"
}

// 200 OK
```
Possible Status Codes:

- 200 OK: When the user is successfully updated.
- 404 Not Found: If the user does not exist.
- 400 Bad Request: If input data is invalid.
