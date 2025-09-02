# 🎬 Movie Booking Analytics Dashboard

A beautiful, modern web interface for viewing analytics and business intelligence data from your Movie Booking System.

## 🚀 Quick Start

### Option 1: Automatic Start (Recommended)
```bash
python start_analytics_dashboard.py
```
This will automatically start both the FastAPI server and the Analytics UI.

### Option 2: Manual Start
1. **Start FastAPI Server:**
   ```bash
   python -m app.main
   ```

2. **Start Analytics UI Server:**
   ```bash
   python serve_analytics_ui.py
   ```

## 📊 Dashboard Features

### 🎯 **System Overview**
- Total Movies, Theaters, Halls, Shows, Users, Bookings
- Confirmed vs Cancelled Bookings
- Total Revenue and Average Booking Value

### 💰 **Revenue Analytics**
- Real-time revenue tracking
- Daily revenue trends
- Average booking values
- Date range filtering

### 🎬 **Top Movies**
- Revenue performance by movie
- Interactive bar charts
- Ranking system

### 🏢 **Top Theaters**
- Theater performance comparison
- Revenue analysis by location
- Visual charts and metrics

### 🎯 **Seat Utilization**
- Occupancy rates
- Available vs Booked seats
- Doughnut chart visualization

### 📈 **Interactive Charts**
- **Revenue Chart**: Line chart showing revenue over time
- **Movie Performance**: Bar chart of top-performing movies
- **Theater Performance**: Bar chart of theater revenue
- **Seat Utilization**: Doughnut chart of seat occupancy

## 🌐 Access URLs

- **📊 Analytics Dashboard**: http://localhost:8080/analytics_ui.html
- **🔗 API Server**: http://localhost:8000
- **📋 API Documentation**: http://localhost:8000/docs

## 🎨 UI Features

### ✨ **Modern Design**
- Beautiful gradient background
- Responsive layout
- Hover effects and animations
- Professional color scheme

### 📱 **Responsive**
- Works on desktop, tablet, and mobile
- Adaptive grid layout
- Mobile-friendly interface

### 🔄 **Real-time Data**
- Live data from your API
- Refresh button for updated analytics
- Automatic chart updates

### 📅 **Date Range Filtering**
- Custom date range selection
- Filter revenue analytics by period
- Flexible reporting

## 🛠️ Technical Details

### **Frontend Technologies**
- **HTML5**: Modern semantic markup
- **CSS3**: Advanced styling with gradients and animations
- **JavaScript**: ES6+ with async/await
- **Chart.js**: Beautiful, responsive charts

### **Backend Integration**
- **FastAPI**: RESTful API endpoints
- **CORS**: Cross-origin resource sharing enabled
- **Real-time**: Live data fetching and updates

### **Charts Included**
1. **Revenue Line Chart**: Shows revenue trends over time
2. **Movie Performance Bar Chart**: Compares movie revenue
3. **Theater Performance Bar Chart**: Compares theater revenue
4. **Seat Utilization Doughnut Chart**: Shows occupancy rates

## 📊 Analytics Endpoints Used

The dashboard connects to these FastAPI endpoints:
- `GET /api/v1/movies/` - Movie data
- `GET /api/v1/theaters/` - Theater data
- `GET /api/v1/halls/` - Hall data
- `GET /api/v1/shows/` - Show data
- `GET /api/v1/users/` - User data
- `GET /api/v1/bookings/` - Booking data
- `GET /api/v1/analytics/revenue` - Revenue analytics
- `GET /api/v1/analytics/top-movies` - Top movies
- `GET /api/v1/analytics/top-theaters` - Top theaters
- `GET /api/v1/analytics/seat-utilization` - Seat utilization

## 🎯 Business Intelligence Features

### **Revenue Management**
- Track daily, weekly, and monthly revenue trends
- Identify peak revenue periods
- Monitor average booking values

### **Performance Analysis**
- Compare movie performance
- Analyze theater efficiency
- Track seat utilization rates

### **Decision Support**
- Data-driven insights for business decisions
- Performance metrics for optimization
- Trend analysis for planning

## 🚀 Getting Started

1. **Ensure your FastAPI server is running** with populated data
2. **Start the Analytics UI server**
3. **Open your browser** to http://localhost:8080/analytics_ui.html
4. **Explore the dashboard** and interact with the charts

## 🎉 Features Summary

- ✅ **Beautiful Modern UI** with responsive design
- ✅ **Real-time Analytics** with live data updates
- ✅ **Interactive Charts** using Chart.js
- ✅ **Date Range Filtering** for custom analysis
- ✅ **Mobile Responsive** design
- ✅ **Professional Color Scheme** and animations
- ✅ **Easy to Use** interface
- ✅ **Business Intelligence Ready**

## 📋 Requirements

- Python 3.7+
- FastAPI server running on port 8000
- Modern web browser with JavaScript enabled
- Internet connection (for Chart.js CDN)

---

**🎬  Movie Booking System with small analytics dashboard!**
