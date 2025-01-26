# Investment Portfolio Management Application  

## 🚀 Overview  
A full-stack **investment portfolio management web application** designed for seamless portfolio tracking and analysis. Built with a **Flask** (Python) backend and a **React** frontend, this application features real-time stock data integration to help users make informed financial decisions.  

---

## ✨ Key Features  
- **User Authentication**: Secure registration and login functionality.  
- **Real-time Stock Search**: Search and view live stock data.  
- **Portfolio Management**: Perform CRUD operations (Create, Read, Update, Delete) for managing portfolio stocks.  
- **Profit-Loss Metrics**: Analyze your portfolio's performance over time.  
- **Responsive Design**: Intuitive and mobile-friendly UI for seamless user experience.  

---

## 🛠️ Tech Stack  

### **Backend**  
- **Flask**  
- **SQLAlchemy ORM**  
- **yfinance API**  

### **Frontend**  
- **React**  
- **Next.js Framework**  
- **React Router**  
- **Tailwind CSS**  

---

## 🔑 Key Technical Highlights  
- **Secure Authentication**: Password hashing with session-based authentication.  
- **RESTful APIs**: Clean and modular API architecture for seamless integration.  
- **Real-time Stock Data**: Integrated with **yfinance API** for live updates.  
- **CORS Configuration**: Secure cross-origin resource sharing.  
- **Dynamic Portfolio Management**: Easily add, remove, and track stocks in your portfolio.  

---

## 🔒 Security Features  
- **Password Hashing**: Protect user credentials with secure hashing algorithms.  
- **Session-Based Authentication**: Ensure secure user sessions.  
- **Input Validation**: Prevent malicious inputs with server-side validation.  
- **CORS Protection**: Safeguard API endpoints from unauthorized access.  

---

## 📡 API Endpoints  

| **Endpoint**        | **Description**                  | **Method** |  
|----------------------|----------------------------------|------------|  
| `/register`          | User registration               | `POST`     |  
| `/login`             | User authentication             | `POST`     |  
| `/logout`            | End user session                | `POST`     |  
| `/search-stock`      | Real-time stock lookup          | `GET`      |  
| `/add-stock`         | Add stock to portfolio          | `POST`     |  
| `/delete-stock`      | Remove stock from portfolio     | `DELETE`   |  
| `/get-stocks`        | Retrieve user portfolio         | `GET`      |  

---

## 🎉 Getting Started  

### 1️⃣ Clone the Repository
   ```bash  
   git clone https://github.com/your-username/your-repo.git
```

### 2️⃣ Backend Setup
  Set up and run the backend server:
  1. Navigate to the backend directory:
  ```bash
  cd backend
```
  2. Install dependencies:
  ```bash
  pip install -r requirements.txt
```
  3. Start the Flask development server:
  ```bash
  flask run
```

### 3️⃣ Frontend Setup
Set up and run the frontend development environment:
1. Navigate to the frontend directory:
```bash
cd frontend
```
2. Install dependencies:
```bash
npm install
```
3. Start the React development server:
```bash
npm run dev
```

### 4️⃣ Access the Application
Once both the backend and frontend servers are running, open your browser and navigate to:
```plaintext
http://localhost:3000
```
Congratulations! 🎉 You're all set to start managing your investment portfolio!

---

## 🌟 Future Enhancements  
- **Advanced Stock Analytics**: Gain deeper insights with enhanced visualizations and reports.  
- **Stock Recommendations**: Leverage algorithms to suggest optimal investment opportunities.  
- **Performance Tracking**: Monitor and evaluate portfolio performance trends.  
- **Multi-Factor Authentication**: Enhance user account security.  
