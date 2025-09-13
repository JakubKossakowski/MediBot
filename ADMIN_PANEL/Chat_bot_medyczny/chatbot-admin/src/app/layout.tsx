import '../styles/globals.css';
import Sidebar from '../components/Sidebar';
import { Auth0Client } from '@auth0/nextjs-auth0/server';

const auth0 = new Auth0Client();

export default async function RootLayout({ children }: { children: React.ReactNode }) {
  const session = await auth0.getSession();
  const user = session?.user;

  return (
    <html lang="pl">
      <body>
        {user ? (
          <div className="flex min-h-screen">
            <Sidebar />
            <main className="flex-1 p-6 bg-gray-50">{children}</main>
          </div>
        ) : (
          <main className="min-h-screen flex flex-col items-center justify-center gap-6 p-6">
            {children}
          </main>
        )}
      </body>
    </html>
  );
}

