# 🎬 Movie Ticket Booking System

A comprehensive movie ticket booking system built with FastAPI, featuring advanced analytics and a modern web interface.

## 🚀 Features

### ✅ **Core Features (Assignment Requirements)**
- **🎬 Movie Management**: CRUD operations for movies
- **🏢 Theater Management**: Register and manage theaters
- **🎪 Hall Management**: Multiple halls per theater with flexible layouts
- **🎫 Show Scheduling**: Multiple shows throughout the day
- **👥 User Management**: User registration and authentication
- **🎯 Seat Booking**: Single and group booking functionality
- **🔗 Consecutive Booking**: Book seats together without gaps
- **💡 Alternative Suggestions**: Suggest other movies/times when seats unavailable
- **🛡️ Concurrency Handling**: Graceful handling of concurrent requests
- **📊 Seat Layout**: Flexible row and column configuration

### 🎯 **Advanced Features**
- **📈 Analytics Dashboard**: Real-time business intelligence
- **💰 Revenue Tracking**: Comprehensive revenue analytics
- **🎬 Performance Analysis**: Movie and theater performance metrics
- **🎯 Seat Utilization**: Occupancy rate monitoring
- **📊 Business Intelligence**: Data-driven insights

## 🛠️ Technology Stack

- **Backend**: FastAPI (Python)
- **Database**: SQLite (with PostgreSQL support)
- **ORM**: SQLAlchemy
- **Authentication**: JWT tokens
- **Frontend**: HTML5, CSS3, JavaScript
- **Charts**: Chart.js (for analytics)
- **Documentation**: Auto-generated Swagger/OpenAPI

## 📁 Project Structure

```
movie-ticket/
├── app/
│   ├── api/                    # API endpoints
│   │   ├── analytics.py        # Analytics APIs
│   │   ├── bookings.py         # Booking APIs
│   │   ├── halls.py           # Hall management
│   │   ├── movies.py          # Movie management
│   │   ├── seats.py           # Seat management
│   │   ├── shows.py           # Show scheduling
│   │   ├── theaters.py        # Theater management
│   │   └── users.py           # User management
│   ├── core/                  # Core configuration
│   │   ├── config.py          # Settings
│   │   └── database.py        # Database setup
│   ├── models/                # Database models
│   │   ├── booking.py         # Booking model
│   │   ├── movie.py           # Movie model
│   │   ├── seat.py            # Seat model
│   │   ├── show.py            # Show model
│   │   ├── theater.py         # Theater model
│   │   └── user.py            # User model
│   ├── schemas/               # Pydantic schemas
│   │   ├── analytics.py       # Analytics schemas
│   │   ├── booking.py         # Booking schemas
│   │   ├── movie.py           # Movie schemas
│   │   ├── seat.py            # Seat schemas
│   │   ├── show.py            # Show schemas
│   │   ├── theater.py         # Theater schemas
│   │   └── user.py            # User schemas
│   └── utils/                 # Utility functions
│       └── booking_utils.py   # Booking utilities
├── analytics_ui.html          # Analytics dashboard
├── requirements.txt           # Python dependencies
├── app/main.py               # FastAPI application
└── README.md                 # This file
```

## 🚀 Quick Start

### 1. **Clone the Repository**
```bash
git clone https://github.com/prabhakarsharma-pythonaire/movie-ticket.git
cd movie-ticket
```

### 2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 3. **Start the Server**
```bash
python -m app.main
```

### 4. **Access the Application**
- **API Documentation**: http://localhost:8000/docs
- **API Base URL**: http://localhost:8000/api/v1
- **Health Check**: http://localhost:8000/health

### 5. **Start Analytics Dashboard** (Optional)
```bash
python -m http.server 8081
```
- **Analytics Dashboard**: http://localhost:8081/analytics_ui.html

## 📊 API Endpoints

### **Core APIs**
- `GET /api/v1/movies/` - List all movies
- `POST /api/v1/movies/` - Create a movie
- `GET /api/v1/theaters/` - List all theaters
- `POST /api/v1/theaters/` - Create a theater
- `GET /api/v1/halls/` - List all halls
- `POST /api/v1/halls/` - Create a hall
- `GET /api/v1/shows/` - List all shows
- `POST /api/v1/shows/` - Create a show
- `GET /api/v1/users/` - List all users
- `POST /api/v1/users/` - Create a user

### **Booking APIs**
- `GET /api/v1/bookings/` - List all bookings
- `POST /api/v1/bookings/` - Create a single booking
- `POST /api/v1/bookings/group` - Create a group booking
- `POST /api/v1/bookings/group/consecutive` - Book consecutive seats
- `GET /api/v1/bookings/alternatives/{show_id}` - Get alternative suggestions
- `GET /api/v1/bookings/user/{user_id}` - Get user bookings
- `PUT /api/v1/bookings/{booking_id}/cancel` - Cancel a booking

### **Seat Management**
- `GET /api/v1/seats/layout/{hall_id}` - Get hall seat layout
- `POST /api/v1/seats/layout/{hall_id}` - Create seat layout

### **Analytics APIs**
- `GET /api/v1/analytics/revenue` - Revenue analytics
- `GET /api/v1/analytics/movie/{movie_id}` - Movie analytics
- `GET /api/v1/analytics/theater/{theater_id}` - Theater analytics
- `GET /api/v1/analytics/top-movies` - Top performing movies
- `GET /api/v1/analytics/top-theaters` - Top performing theaters
- `GET /api/v1/analytics/seat-utilization` - Seat utilization

## 🎯 Key Features Explained

### **🎫 Group Booking**
- Book multiple seats together
- Automatic consecutive seat allocation
- Alternative suggestions when seats unavailable

### **🛡️ Concurrency Handling**
- Database-level locking
- Optimistic concurrency control
- Prevents double booking

### **📊 Analytics Dashboard**
- Real-time revenue tracking
- Performance metrics
- Business intelligence insights
- Interactive charts and visualizations

### **🎪 Flexible Seat Layout**
- Customizable rows and columns
- Minimum 6 seats per row
- 3-column aisle configuration
- Dynamic seat allocation

## 🧪 Testing

### **Run Comprehensive Tests**
```bash
python comprehensive_test.py
```

### **Run Analytics Tests**
```bash
python comprehensive_analytics_test.py
```

### **Run Simple Tests**
```bash
python simple_test.py
```

## 📈 Analytics Dashboard

The system includes a beautiful analytics dashboard with:

- **📊 System Overview**: Key metrics and statistics
- **💰 Revenue Analytics**: Revenue tracking and trends
- **🎬 Performance Analysis**: Movie and theater performance
- **🎯 Seat Utilization**: Occupancy rate monitoring
- **📅 Date Range Filtering**: Custom period analysis

## 🔧 Configuration

### **Environment Variables**
Create a `.env` file:
```env
DATABASE_URL=sqlite:///./movie_booking.db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### **Database**
- Default: SQLite (file-based)
- Production: PostgreSQL (configurable)

## 🚀 Deployment

### **Local Development**
```bash
python -m app.main
```

### **Production**
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 📋 Requirements

- Python 3.7+
- FastAPI
- SQLAlchemy
- Pydantic
- Uvicorn
- See `requirements.txt` for complete list

## 🎉 Features Summary

### ✅ **Assignment Requirements Met**
- [x] CRUD APIs for all entities
- [x] Group booking functionality
- [x] Consecutive seat booking
- [x] Alternative booking suggestions
- [x] Concurrency handling
- [x] Flexible seat layout system

### ✅ **Bonus Features**
- [x] Advanced analytics dashboard
- [x] Business intelligence features
- [x] Real-time data visualization
- [x] Performance monitoring
- [x] Revenue tracking
- [x] Professional web interface

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 👨‍💻 Author

**Prabhakar Sharma**
- GitHub: [@prabhakarsharma-pythonaire](https://github.com/prabhakarsharma-pythonaire)

## 🎬 Project Status

- ✅ **Core Features**: Complete
- ✅ **Analytics**: Complete
- ✅ **Testing**: Complete
- ✅ **Documentation**: Complete
- ✅ **Production Ready**: Yes

---

**🎬 A complete movie ticket booking system with advanced analytics and business intelligence!**
