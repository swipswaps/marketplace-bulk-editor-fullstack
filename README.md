# Facebook Marketplace Bulk Editor

A mobile-friendly web application for editing and combining Facebook Marketplace bulk upload spreadsheets.

## Features

- 📤 **Upload Multiple Files**: Drag & drop or select Excel files (.xlsx, .xls, .csv)
- ✏️ **Edit Listings**: Full CRUD operations (Create, Read, Update, Delete)
- 🔄 **Combine Spreadsheets**: Merge multiple files into one
- 📱 **Mobile Responsive**: Works on Android and iPhone browsers
- 💾 **Download**: Export to Facebook-compatible Excel format
- ✅ **Validation**: Enforces Facebook Marketplace requirements (title ≤150 chars, description ≤5000 chars)

## Usage

### Local Development

1. Install dependencies:
\`\`\`bash
npm install
\`\`\`

2. Start the dev server:
\`\`\`bash
npm run dev
\`\`\`

3. Open http://localhost:5173 in your browser

### Building for Production

\`\`\`bash
npm run build
\`\`\`

The built files will be in the \`dist\` folder.

### Deploying to GitHub Pages

1. Push your code to GitHub
2. Go to Settings → Pages
3. Set Source to "GitHub Actions"
4. The app will automatically deploy on every push to main branch

## Facebook Marketplace Format

The app supports the following columns:
- **TITLE** (required, max 150 characters)
- **PRICE** (required)
- **CONDITION** (required: New, Used - Like New, Used - Good, Used - Fair)
- **DESCRIPTION** (optional, max 5000 characters)
- **CATEGORY** (optional)
- **OFFER SHIPPING** (optional: Yes/No)

## Tech Stack

- React + TypeScript
- Vite
- Tailwind CSS
- SheetJS (xlsx) for Excel handling
- React Dropzone for file uploads
- Lucide React for icons
