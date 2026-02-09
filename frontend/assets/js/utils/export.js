// Export utilities for CSV and PDF

// CSV Export
function exportToCSV(data, filename) {
  if (!data || data.length === 0) {
    alert('No data to export');
    return;
  }

  const headers = Object.keys(data[0]);
  const csvContent = [
    headers.join(','),
    ...data.map(row => 
      headers.map(header => {
        const value = row[header] || '';
        return `"${String(value).replace(/"/g, '""')}"`;
      }).join(',')
    )
  ].join('\n');

  downloadFile(csvContent, filename, 'text/csv');
}

// PDF Export (using simple HTML to PDF conversion)
function exportToPDF(title, data, filename) {
  if (!data || data.length === 0) {
    alert('No data to export');
    return;
  }

  const headers = Object.keys(data[0]);
  
  const htmlContent = `
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <title>${title}</title>
      <style>
        body { font-family: Arial, sans-serif; padding: 20px; }
        h1 { color: #333; border-bottom: 2px solid #ff6b35; padding-bottom: 10px; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #ff6b35; color: white; }
        tr:nth-child(even) { background-color: #f2f2f2; }
        .footer { margin-top: 20px; font-size: 12px; color: #666; }
      </style>
    </head>
    <body>
      <h1>${title}</h1>
      <p>Generated on: ${new Date().toLocaleString()}</p>
      <table>
        <thead>
          <tr>${headers.map(h => `<th>${h}</th>`).join('')}</tr>
        </thead>
        <tbody>
          ${data.map(row => `
            <tr>${headers.map(h => `<td>${row[h] || ''}</td>`).join('')}</tr>
          `).join('')}
        </tbody>
      </table>
      <div class="footer">
        <p>Total Records: ${data.length}</p>
        <p>Kart Management System</p>
      </div>
    </body>
    </html>
  `;

  // Open in new window for printing
  const printWindow = window.open('', '_blank');
  printWindow.document.write(htmlContent);
  printWindow.document.close();
  
  setTimeout(() => {
    printWindow.print();
  }, 250);
}

// Download file helper
function downloadFile(content, filename, mimeType) {
  const blob = new Blob([content], { type: mimeType });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}

// Export products to CSV
function exportProductsCSV(products) {
  const data = products.map(p => ({
    ID: p.id,
    Name: p.name,
    SKU: p.sku || 'N/A',
    Price: p.price,
    Stock: p.stock,
    Description: p.description || ''
  }));
  
  exportToCSV(data, `products_${Date.now()}.csv`);
}

// Export products to PDF
function exportProductsPDF(products) {
  const data = products.map(p => ({
    ID: p.id,
    Name: p.name,
    SKU: p.sku || 'N/A',
    Price: `₹${parseFloat(p.price).toFixed(2)}`,
    Stock: p.stock,
    Status: p.stock === 0 ? 'Out of Stock' : p.stock <= 10 ? 'Low Stock' : 'In Stock'
  }));
  
  exportToPDF('Product Inventory Report', data, `products_${Date.now()}.pdf`);
}

// Export cart to CSV
function exportCartCSV(cartItems) {
  const data = cartItems.map(item => ({
    ID: item.id,
    Product: item.name,
    Price: item.price,
    Quantity: item.quantity,
    Subtotal: (item.price * item.quantity).toFixed(2)
  }));
  
  exportToCSV(data, `cart_${Date.now()}.csv`);
}

// Export cart to PDF
function exportCartPDF(cartItems) {
  const data = cartItems.map(item => ({
    Product: item.name,
    Price: `₹${parseFloat(item.price).toFixed(2)}`,
    Quantity: item.quantity,
    Subtotal: `₹${(item.price * item.quantity).toFixed(2)}`
  }));
  
  const total = cartItems.reduce((sum, item) => sum + (item.price * item.quantity), 0);
  data.push({
    Product: 'TOTAL',
    Price: '',
    Quantity: '',
    Subtotal: `₹${total.toFixed(2)}`
  });
  
  exportToPDF('Shopping Cart Report', data, `cart_${Date.now()}.pdf`);
}

window.exportUtils = {
  exportToCSV,
  exportToPDF,
  exportProductsCSV,
  exportProductsPDF,
  exportCartCSV,
  exportCartPDF
};
