# JunkBuddy
Innovative tool designed to help individuals identify and properly dispose of waste using AI-powered image recognition.

**JunkBuddy - Waste Classifier** is an innovative tool designed to help individuals identify and properly dispose of waste using AI-powered image recognition. This project integrates with a MySQL database to provide accurate disposal and recycling methods for various types of waste.

## Features

- **AI-Powered Image Recognition**: Uses RapidAPI's General Detection API to classify waste images.
- **Database Integration**: Retrieves disposal and recycling methods from a MySQL database.
- **User-Friendly Interface**: Streamlit-based web app for easy image upload and result display.
- **Customizable**: Allows for easy addition of new waste categories and disposal methods.

## Getting Started

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/mananbtra/JunkBuddy
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup MySQL Database**:
   - Create a MySQL database named `WasteManagement`.
   - Run the SQL script provided in the `database` folder to create tables.

4. **Configure Secrets**:
   - Create a `.streamlit/secrets.toml` file with your database credentials and API key.
   ```toml
   [secrets]
   DB_HOST = "your-database-host"
   DB_USER = "your-db-username"
   DB_PASSWORD = "your-db-password"
   DB_NAME = "WasteManagement"
   DB_PORT = 3306
   x-rapidapi-key = "your-api-key"
   ```

5. **Run the App**:
   ```bash
   streamlit run app.py
   ```

## Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Contact

Manan Batra - [btra.manan04@gmail.com](mailto:btra.manan04@gmail.com)

Project Link: JunkBuddy[(https://github.com/mananbtra/JunkBuddy)]
