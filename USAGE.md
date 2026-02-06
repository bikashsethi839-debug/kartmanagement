# 🛒 Kart Management System

Modern product and cart management system with full CRUD operations.

## 🚀 Quick Start

### Start the Server

```bash
# Option 1: Using Python directly
python app.py --no-https

# Option 2: Using the startup script
./start_server.sh

# Option 3: With HTTPS (requires OpenSSL)
python app.py
```

The server will start on **http://localhost:5000**

### Initialize Database (Optional)

```bash
python app.py --init-db
```

## 📱 Pages

- **Catalog** - http://localhost:5000/catalog.html - Browse and manage products
- **Inventory** - http://localhost:5000/inventory.html - Stock management with statistics
- **Cart** - http://localhost:5000/cart.html - Shopping cart operations
- **Dashboard** - http://localhost:5000/dashboard.html - Analytics and quick actions
- **Product Details** - http://localhost:5000/product.html?id=X - Detailed product view

## ✨ Features

### 📦 Catalog Page
- ✅ Add new products
- ✅ Edit existing products
- ✅ Delete products
- ✅ Search products
- ✅ View product cards with stock status

### 📊 Inventory Page
- ✅ Complete product management
- ✅ Statistics dashboard
- ✅ Table view with sorting
- ✅ Quick stock adjustment
- ✅ Low stock alerts

### 🛍️ Cart Page
- ✅ Add items to cart
- ✅ Update quantities
- ✅ Remove items
- ✅ Real-time price calculations
- ✅ Cart statistics

### 📈 Dashboard
- ✅ Overview statistics
- ✅ Recent products
- ✅ Cart summary
- ✅ Low stock alerts
- ✅ Quick actions

### 📦 Product Details
- ✅ Full product information
- ✅ Edit product
- ✅ Quick add to cart
- ✅ Stock adjustment
- ✅ Price updates
- ✅ Product reviews

## 🎨 Design Features

- Modern dark gradient theme
- Responsive design
- Smooth animations
- Card-based UI
- Modal dialogs
- Real-time updates
- Search functionality
- Status badges

## 🔧 Technology Stack

- **Backend**: Python (built-in HTTP server with SSL support)
- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **Database**: SQLite
- **No external dependencies** for the web server

## 📝 API Endpoints

### Products
- `GET /api/products` - List all products
- `POST /api/products` - Create product
- `GET /api/products/{id}` - Get product
- `PUT /api/products/{id}` - Update product
- `DELETE /api/products/{id}` - Delete product

### Cart
- `GET /api/cart` - List cart items
- `POST /api/cart` - Add to cart
- `PUT /api/cart/{id}` - Update cart item
- `DELETE /api/cart/{id}` - Remove from cart

### Reviews
- `GET /api/products/{id}/reviews` - List reviews
- `POST /api/products/{id}/reviews` - Add review
- `DELETE /api/products/{id}/reviews/{review_id}` - Delete review

## 🛠️ Troubleshooting

### Port Already in Use
```bash
# Kill process on port 5000
fuser -k 5000/tcp
# Or
lsof -ti:5000 | xargs kill -9
```

### Server Not Starting
```bash
# Check if Python is installed
python --version

# Check if database can be initialized
python app.py --init-db
```

### Pages Not Loading
1. Make sure server is running: `curl http://localhost:5000/`
2. Check server logs in terminal
3. Clear browser cache
4. Try different browser

## 📄 License

MIT License
