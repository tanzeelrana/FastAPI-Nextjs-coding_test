import "@/styles/globals.css";

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className="bg-gray-100 text-gray-900">
        <div className="min-h-screen flex items-center justify-center">
          <div className="bg-white shadow-lg rounded-lg p-6 w-full max-w-4xl">
            {children}
          </div>
        </div>
      </body>
    </html>
  );
}
