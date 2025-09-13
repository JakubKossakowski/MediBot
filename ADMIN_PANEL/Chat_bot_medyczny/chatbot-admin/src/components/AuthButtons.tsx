'use client';
import React from 'react';

export default function AuthButtons({ session }: { session: any | null }) {
  const user = session?.user;

  if (user) {
    return (
      <div className="flex flex-col items-center gap-3">
        <div className="text-center">
          <p className="font-medium">Witaj, {user.name}</p>
          <p className="text-sm text-gray-500">{user.email}</p>
        </div>
        <div className="flex gap-3">
          <a href="/auth/logout">
            <button className="px-4 py-2 rounded bg-red-600 text-white">Wyloguj</button>
          </a>
        </div>
      </div>
    );
  }

  return (
    <div>
      <a href="/auth/login">
        <button className="px-4 py-2 rounded bg-blue-600 text-white">Zaloguj przez Auth0 (Google)</button>
      </a>
    </div>
  );
}
