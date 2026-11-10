# LifeLink – Blood Donor Finder

A responsive blood donor directory built with **HTML, CSS, JavaScript, Flask and SQLite**.

## Features
- Landing page with donor and request statistics
- Donor registration
- Search available donors by blood group and city
- Submit a blood requirement request
- SQLite database created automatically
- Responsive layout for desktop and mobile

## Requirements
- Python 3.10 or newer
- VS Code (recommended)
- Internet connection only for the Google Fonts stylesheet; the app itself runs locally

## Run on Windows (VS Code)

1. Extract `LifeLink_Blood_Donor_Finder.zip`.
2. Open the extracted `LifeLink_Blood_Donor_Finder` folder in VS Code.
3. Open **Terminal → New Terminal**.
4. Create a virtual environment:

   ```powershell
   py -m venv venv
   ```

5. Activate it:

   ```powershell
   .\\venv\\Scripts\\Activate.ps1
   ```

   If PowerShell blocks activation, run this once in the current terminal:

   ```powershell
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   .\\venv\\Scripts\\Activate.ps1
   ```

6. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

7. Start the website:

   ```powershell
   python app.py
   ```

8. Open this address in your browser:

   `http://127.0.0.1:5000`

## First test
- Click **Become a donor** and register a sample donor.
- Open **Find donors**, filter by blood group and city.
- Click **Request blood** and submit a test request.

The SQLite file `lifelink.db` is generated automatically in the project folder.

## Project structure

```text
LifeLink_Blood_Donor_Finder/
├── app.py
├── requirements.txt
├── README.md
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── donors.html
│   ├── register.html
│   ├── request.html
│   └── about.html
└── static/
    ├── css/style.css
    └── js/main.js
```

## Important safety and privacy notes
- LifeLink is a community directory, not an emergency medical service or a verified blood bank.
- Donor availability and contact details are user-submitted and are not independently verified.
- Do not use this directory to make medical compatibility decisions. Confirm blood type, eligibility and compatibility with a licensed hospital/blood bank.
- For real deployment, add phone/OTP verification, donor consent, privacy controls, rate limiting, admin moderation, secure hosting and data deletion options.
- Do not publish real people's phone numbers or sensitive health information in a public repository.
- For emergencies, contact a hospital or licensed blood bank directly.
