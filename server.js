// server.js

// Import necessary modules
const express = require('express'); // Express.js for creating the server
const bodyParser = require('body-parser'); // Body-parser to handle request bodies
const fs = require('fs'); // File system module to work with files

const app = express(); // Create an Express application
const PORT = 3000; // Define the port the server will listen on

// Middleware to serve static files from the 'public' directory
// This makes your HTML, CSS, JS, and image files accessible to clients
app.use(express.static('public'));

// Middleware to parse URL-encoded bodies (for form data from HTML forms)
app.use(bodyParser.urlencoded({ extended: false }));
// Middleware to parse JSON bodies (for JSON data in requests)
app.use(bodyParser.json());

const usersFilePath = 'users.json'; // Path to the JSON file storing user data

// --- Signup Endpoint ---
app.post('/signup', (req, res) => {
    // 1. Read existing users from users.json
    fs.readFile(usersFilePath, 'utf8', (err, data) => {
        let users = []; // Initialize users array
        if (!err) {
            try {
                users = JSON.parse(data); // Try to parse existing user data
            } catch (parseError) {
                console.error("Error parsing users.json:", parseError);
                // If parsing fails, assume users.json was empty or corrupt, start with an empty array
                users = [];
            }
        } else if (err.code !== 'ENOENT') { // ENOENT error means file not found, which is OK initially
            console.error("Error reading users.json:", err);
            return res.status(500).send('Error reading user data.'); // Respond with server error if read fails for other reasons
        }

        // 2. Extract email and password from the request body
        const { email, password } = req.body;

        if (!email || !password) {
            return res.status(400).send('Email and password are required.'); // Respond with bad request if fields are missing
        }

        // **Important Security Note:**
        // In a real application, you should NEVER store passwords in plain text.
        // You should use a proper hashing algorithm (like bcrypt) to securely store passwords.
        // For this basic example, we are storing passwords in plain text for simplicity, but this is NOT secure.

        // 3. Create a new user object with email, password, and timestamp
        const newUser = {
            email: email,
            password: password, // **INSECURE: Storing password in plain text**
            timestamp: new Date().toISOString() // Add a timestamp for when the user signed up
        };

        // 4. Append the new user to the users array
        users.push(newUser);

        // 5. Write the updated users array back to users.json
        fs.writeFile(usersFilePath, JSON.stringify(users, null, 2), (writeErr) => {
            if (writeErr) {
                console.error("Error writing to users.json:", writeErr);
                return res.status(500).send('Signup failed: Could not save user data.'); // Respond with server error if write fails
            }

            // 6. Respond with a success message
            res.send('Signup successful!');
        });
    });
});

// --- Login Endpoint ---
app.post('/login', (req, res) => {
    // 1. Read users from users.json
    fs.readFile(usersFilePath, 'utf8', (err, data) => {
        if (err) {
            console.error("Error reading users.json:", err);
            return res.status(500).send('Login failed: Could not read user data.'); // Respond with server error if read fails
        }

        let users = [];
        try {
            users = JSON.parse(data); // Parse user data from JSON
        } catch (parseError) {
            console.error("Error parsing users.json:", parseError);
            return res.status(500).send('Login failed: Error processing user data.'); // Respond with server error if parsing fails
        }

        // 2. Extract email and password from the request body
        const { email, password } = req.body;

        if (!email || !password) {
            return res.status(400).send('Email and password are required.'); // Respond with bad request if fields are missing
        }

        // 3. Check if the provided credentials match any user in users.json
        const userFound = users.find(user => user.email === email && user.password === password);

        // 4. Respond with success or error message
        if (userFound) {
            res.send('Login successful!'); // Success message for valid credentials
        } else {
            res.status(401).send('Login failed: Invalid email or password.'); // Unauthorized status for invalid credentials
        }
    });
});

// --- Start the server ---
app.listen(PORT, () => {
    console.log(`Server listening on port http://localhost:${PORT}`); // Log message when server starts
});
