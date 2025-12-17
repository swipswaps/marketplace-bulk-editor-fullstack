# Deployment Guide

## Quick Start

The app is ready to deploy! Here's what you need to do:

### 1. Initialize Git Repository

```bash
cd marketplace-bulk-editor
git init
git add .
git commit -m "Initial commit: Facebook Marketplace Bulk Editor"
```

### 2. Create GitHub Repository

1. Go to https://github.com/new
2. Create a new repository (e.g., `marketplace-bulk-editor`)
3. **Do NOT** initialize with README, .gitignore, or license (we already have these)

### 3. Push to GitHub

```bash
git remote add origin https://github.com/YOUR_USERNAME/marketplace-bulk-editor.git
git branch -M main
git push -u origin main
```

### 4. Enable GitHub Pages

1. Go to your repository on GitHub
2. Click **Settings** → **Pages**
3. Under "Build and deployment":
   - Source: Select **GitHub Actions**
4. The workflow will automatically run and deploy your app

### 5. Access Your App

After the deployment completes (usually 2-3 minutes), your app will be available at:
```
https://YOUR_USERNAME.github.io/marketplace-bulk-editor/
```

## Testing Locally

### Development Server
```bash
npm run dev
```
Then open http://localhost:5173

### Production Build
```bash
npm run build
npm run preview
```

## Features Implemented

✅ **File Upload**: Drag & drop or click to upload Excel files (.xlsx, .xls, .csv)
✅ **Multiple File Support**: Combine data from multiple spreadsheets
✅ **CRUD Operations**: 
  - Create: Add new listings
  - Read: View all listings in a table
  - Update: Edit any field inline
  - Delete: Remove listings
✅ **Data Validation**: 
  - Title max 150 characters
  - Description max 5000 characters
  - Required fields enforced
✅ **Export**: Download combined/edited data as Excel file
✅ **Mobile Responsive**: Works on Android and iPhone browsers
✅ **GitHub Pages Ready**: Configured for static deployment

## File Structure

```
marketplace-bulk-editor/
├── src/
│   ├── components/
│   │   ├── FileUpload.tsx      # Drag & drop file upload
│   │   ├── DataTable.tsx        # Editable table with CRUD
│   │   └── ExportButton.tsx     # Excel export functionality
│   ├── types.ts                 # TypeScript interfaces
│   ├── App.tsx                  # Main app component
│   ├── main.tsx                 # Entry point
│   └── index.css                # Tailwind CSS
├── .github/
│   └── workflows/
│       └── deploy.yml           # GitHub Actions deployment
├── vite.config.ts               # Vite configuration (GitHub Pages ready)
├── tailwind.config.js           # Tailwind CSS configuration
└── package.json                 # Dependencies
```

## Technologies Used

- **React 19** + **TypeScript** - UI framework
- **Vite 7** - Build tool
- **Tailwind CSS 4** - Styling
- **SheetJS (xlsx)** - Excel file handling
- **React Dropzone** - File upload
- **Lucide React** - Icons

## Browser Support

- ✅ Chrome/Edge (Android & Desktop)
- ✅ Safari (iOS & macOS)
- ✅ Firefox
- ✅ Mobile browsers (responsive design)

## Notes

- The app runs entirely in the browser (no backend required)
- All file processing happens client-side
- Data is never sent to any server
- Perfect for GitHub Pages static hosting

