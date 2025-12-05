# Postman Demo Guide - Step by Step

## Base URL
```
http://localhost:8000
```
*(Replace with your actual server URL if different)*

---

## 📋 **PHASE 1: SETUP & AUTHENTICATION**

### Step 1: Register Users (Create Test Accounts)

**Endpoint:** `POST /api/users/register/`  
**Auth Required:** No  
**Purpose:** Create test users for the demo

#### 1.1 Register a Passenger
```json
{
  "username": "passenger1",
  "email": "passenger1@test.com",
  "password": "passenger123",
  "role": "PASSENGER",
  "contact_info": "+63 912 345 6789"
}
```

#### 1.2 Register a Driver
```json
{
  "username": "driver1",
  "email": "driver1@test.com",
  "password": "driver123",
  "role": "DRIVER",
  "contact_info": "+63 912 345 6788"
}
```

#### 1.3 Register an Admin (Optional - for admin operations)
```json
{
  "username": "admin1",
  "email": "admin1@test.com",
  "password": "admin123",
  "role": "ADMIN",
  "contact_info": "+63 912 345 6787"
}
```

**Expected Response:** 201 Created with user data and JWT tokens

---

### Step 2: Login to Get Access Token

**Endpoint:** `POST /api/login/`  
**Auth Required:** No

#### 2.1 Login as Passenger
```json
{
  "username": "passenger1",
  "password": "passenger123"
}
```

**Response:** Copy the `access` token
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### 2.2 Login as Driver
```json
{
  "username": "driver1",
  "password": "driver123"
}
```

#### 2.3 Login as Admin
```json
{
  "username": "admin1",
  "password": "admin123"
}
```

**💡 Tip:** Save tokens in Postman Environment Variables:
- `access_token_passenger`
- `access_token_driver`
- `access_token_admin`

**Setup Authorization Header:**
- Type: Bearer Token
- Token: `{{access_token_passenger}}` (or the appropriate token)

---

## 📋 **PHASE 2: USER MANAGEMENT (CRUD)**

### Step 3: Read Users (List)

**Endpoint:** `GET /api/users/`  
**Auth Required:** Yes (Bearer Token)  
**Headers:** `Authorization: Bearer {access_token}`

**Expected Response:** List of all users

---

### Step 4: Read User Detail

**Endpoint:** `GET /api/users/{user_id}/`  
**Auth Required:** Yes (Admin only)  
**Example:** `GET /api/users/1/`

**Expected Response:** User details

---

### Step 5: Update User

**Endpoint:** `PUT /api/users/{user_id}/` or `PATCH /api/users/{user_id}/`  
**Auth Required:** Yes (Admin only)

**Request Body (PATCH - Partial Update):**
```json
{
  "contact_info": "+63 999 888 7777"
}
```

**Expected Response:** Updated user data

---

### Step 6: Get User Profile

**Endpoint:** `GET /api/users/profile/`  
**Auth Required:** Yes (Any authenticated user)  
**Purpose:** Get current logged-in user's profile

**Expected Response:** Current user's profile

---

### Step 7: Update User Profile

**Endpoint:** `PUT /api/users/profile/`  
**Auth Required:** Yes

**Request Body:**
```json
{
  "email": "newemail@test.com",
  "contact_info": "+63 999 888 7777"
}
```

---

## 📋 **PHASE 3: VEHICLE MANAGEMENT (CRUD)**

### Step 8: Create Vehicle

**Endpoint:** `POST /api/vehicles/`  
**Auth Required:** Yes (Admin only)  
**Use Admin Token**

**Request Body:**
```json
{
  "driver": 2,
  "plate_number": "ABC-1234",
  "vehicle_type": "Car",
  "status": "AVAILABLE"
}
```

**Expected Response:** 201 Created with vehicle data

**💡 Note:** Create 2-3 vehicles for testing

---

### Step 9: Read Vehicles (List)

**Endpoint:** `GET /api/vehicles/`  
**Auth Required:** Yes

**Expected Response:** List of all vehicles

---

### Step 10: Read Available Vehicles

**Endpoint:** `GET /api/vehicles/available/`  
**Auth Required:** Yes

**Expected Response:** Only vehicles with status "AVAILABLE"

---

### Step 11: Read Vehicle Detail

**Endpoint:** `GET /api/vehicles/{vehicle_id}/`  
**Auth Required:** Yes (Admin only)

**Example:** `GET /api/vehicles/1/`

---

### Step 12: Update Vehicle

**Endpoint:** `PUT /api/vehicles/{vehicle_id}/` or `PATCH /api/vehicles/{vehicle_id}/`  
**Auth Required:** Yes (Admin only)

**Request Body (PATCH):**
```json
{
  "status": "MAINTENANCE"
}
```

---

### Step 13: Update Vehicle Status (Alternative)

**Endpoint:** `PATCH /api/vehicles/{vehicle_id}/status/`  
**Auth Required:** Yes (Admin only)

**Request Body:**
```json
{
  "status": "Available"
}
```

**Valid Statuses:** `"Available"`, `"On Trip"`, `"Maintenance"`

---

### Step 14: Delete Vehicle (Soft Delete)

**Endpoint:** `DELETE /api/vehicles/{vehicle_id}/`  
**Auth Required:** Yes (Admin only)

**Expected Response:** 204 No Content

---

## 📋 **PHASE 4: BOOKING MANAGEMENT (CRUD)**

### Step 15: Create Booking

**Endpoint:** `POST /api/bookings/`  
**Auth Required:** Yes (Passenger token)  
**Use Passenger Token**

**Request Body:**
```json
{
  "pickup_location": "SM Mall of Asia, Pasay",
  "pickup_geolocation": "14.5350,120.9820",
  "dropoff_location": "NAIA Terminal 3, Pasay",
  "dropoff_geolocation": "14.5086,121.0194",
  "pickup_time": "2024-12-20T10:00:00Z",
  "fare": 250.00
}
```

**Expected Response:** 201 Created
- System automatically assigns available driver and vehicle
- Status set to "PENDING"

**💡 Note:** Save the `booking_id` from response for next steps

---

### Step 16: Read Bookings (List)

**Endpoint:** `GET /api/bookings/`  
**Auth Required:** Yes

**Expected Response:** List of bookings (filtered by user role)

---

### Step 17: Read Booking Detail

**Endpoint:** `GET /api/bookings/{booking_id}/`  
**Auth Required:** Yes

**Example:** `GET /api/bookings/1/`

---

### Step 18: Update Booking

**Endpoint:** `PUT /api/bookings/{booking_id}/` or `PATCH /api/bookings/{booking_id}/`  
**Auth Required:** Yes

**Request Body (PATCH):**
```json
{
  "fare": 300.00
}
```

---

### Step 19: Accept Booking (Driver Action)

**Endpoint:** `POST /api/bookings/{booking_id}/accept/`  
**Auth Required:** Yes (Driver token)  
**Use Driver Token**

**Expected Response:** Booking with status "ACCEPTED"

---

### Step 20: Start Booking (Driver Action)

**Endpoint:** `POST /api/bookings/{booking_id}/start/`  
**Auth Required:** Yes (Driver token)

**Expected Response:** Booking with status "ONGOING"

---

### Step 21: Complete Booking (Driver Action)

**Endpoint:** `POST /api/bookings/{booking_id}/complete/`  
**Auth Required:** Yes (Driver token)

**Expected Response:** 
- Booking with status "COMPLETED"
- Vehicle status automatically set back to "AVAILABLE"

---

### Step 22: Cancel Booking

**Endpoint:** `POST /api/bookings/{booking_id}/cancel/`  
**Auth Required:** Yes (Passenger or Driver)

**Expected Response:** Booking with status "CANCELLED"

---

### Step 23: Delete Booking (Soft Delete)

**Endpoint:** `DELETE /api/bookings/{booking_id}/`  
**Auth Required:** Yes

**Expected Response:** 204 No Content

---

## 📋 **PHASE 5: PAYMENT MANAGEMENT (CRUD)**

### Step 24: Create Payment

**Endpoint:** `POST /api/payments/`  
**Auth Required:** Yes (Passenger token)  
**Use Passenger Token**

**Request Body:**
```json
{
  "booking": 1,
  "amount": 250.00,
  "payment_method": "Gcash"
}
```

**Expected Response:** 201 Created
- Status automatically set to "Pending"

**💡 Note:** Payment can only be created for bookings where passenger is the current user

---

### Step 25: Read Payments (List)

**Endpoint:** `GET /api/payments/`  
**Auth Required:** Yes

**Expected Response:** 
- Admin: All payments
- Passenger: Only their payments
- Driver: Payments for their bookings

---

### Step 26: Read Payment Detail

**Endpoint:** `GET /api/payments/{payment_id}/`  
**Auth Required:** Yes (Admin only)

**Example:** `GET /api/payments/1/`

**Expected Response:** Detailed payment info including booking and passenger details

---

### Step 27: Update Payment

**Endpoint:** `PUT /api/payments/{payment_id}/` or `PATCH /api/payments/{payment_id}/`  
**Auth Required:** Yes (Admin only)

**Request Body (PATCH):**
```json
{
  "payment_method": "Credit Card"
}
```

---

### Step 28: Verify Payment (Admin Action)

**Endpoint:** `PATCH /api/payments/{payment_id}/verify/`  
**Auth Required:** Yes (Admin only)  
**Use Admin Token**

**Expected Response:** Payment with status "Completed"

**💡 Note:** Only payments with "Pending" status can be verified

---

### Step 29: Reject Payment (Admin Action)

**Endpoint:** `PATCH /api/payments/{payment_id}/reject/`  
**Auth Required:** Yes (Admin only)

**Expected Response:** Payment with status "Failed"

---

### Step 30: Delete Payment (Soft Delete)

**Endpoint:** `DELETE /api/payments/{payment_id}/`  
**Auth Required:** Yes (Admin only)

**Expected Response:** 204 No Content

---

## 📋 **BONUS: ADDITIONAL ENDPOINTS**

### Get Drivers List
**Endpoint:** `GET /api/users/drivers/`  
**Auth Required:** Yes

### Get Passengers List
**Endpoint:** `GET /api/users/passengers/`  
**Auth Required:** Yes (Admin only)

### Change Password
**Endpoint:** `POST /api/users/change-password/`  
**Auth Required:** Yes

**Request Body:**
```json
{
  "old_password": "oldpass123",
  "new_password": "newpass123",
  "confirm_password": "newpass123"
}
```

### Refresh Token
**Endpoint:** `POST /api/refresh/`  
**Auth Required:** No

**Request Body:**
```json
{
  "refresh": "your_refresh_token_here"
}
```

---

## 🎯 **RECOMMENDED DEMO FLOW**

### Quick Demo (10-15 minutes):
1. Register users (Passenger, Driver, Admin)
2. Login as Passenger → Get token
3. Create Vehicle (as Admin)
4. Create Booking (as Passenger)
5. Login as Driver → Accept Booking
6. Start Booking (as Driver)
7. Complete Booking (as Driver)
8. Create Payment (as Passenger)
9. Login as Admin → Verify Payment
10. Show Read operations (List/Detail)

### Full Demo (20-30 minutes):
Follow all phases in order, demonstrating:
- ✅ Create operations
- ✅ Read operations (List & Detail)
- ✅ Update operations
- ✅ Delete operations (Soft Delete)
- ✅ Role-based permissions
- ✅ Business logic (Booking workflow, Payment verification)

---

## 🔐 **AUTHORIZATION SETUP IN POSTMAN**

### Method 1: Environment Variables
1. Create Environment: "Django API"
2. Add variables:
   - `base_url`: `http://localhost:8000`
   - `access_token_passenger`: (set after login)
   - `access_token_driver`: (set after login)
   - `access_token_admin`: (set after login)

3. Use in requests:
   - URL: `{{base_url}}/api/bookings/`
   - Authorization: Bearer Token → `{{access_token_passenger}}`

### Method 2: Collection Variables
Set at collection level for all requests

### Method 3: Manual Headers
Add header manually:
```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

---

## ⚠️ **IMPORTANT NOTES**

1. **Token Expiration:** JWT tokens expire. Use refresh token or re-login if needed
2. **Permissions:** 
   - Most endpoints require authentication
   - Admin-only endpoints: User/Vehicle/Payment management
   - Driver actions: Accept/Start/Complete bookings
   - Passenger actions: Create bookings and payments
3. **Soft Delete:** Delete operations don't actually remove records, they set `is_deleted=True`
4. **Dependencies:** 
   - Bookings need available vehicles and drivers
   - Payments need completed bookings
5. **Status Flow:**
   - Booking: PENDING → ACCEPTED → ONGOING → COMPLETED
   - Payment: Pending → Completed/Failed

---

## 📝 **TESTING CHECKLIST**

- [ ] User Registration & Login
- [ ] User CRUD operations
- [ ] Vehicle CRUD operations
- [ ] Booking CRUD operations
- [ ] Booking workflow (Accept → Start → Complete)
- [ ] Payment CRUD operations
- [ ] Payment verification/rejection
- [ ] Role-based access control
- [ ] Error handling (404, 403, 400)
- [ ] Soft delete functionality

---

**Good luck with your presentation! 🚀**

