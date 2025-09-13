"use client";

import {
  LayoutDashboard,
  BarChart2,
  Users,
  ShoppingCart,
  Phone,
  Settings,
  ClipboardList,
  LogOut,
  Headset
} from "lucide-react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import clsx from "clsx";

const menu = [
  { name: "Panel główny", href: "/dashboard", icon: LayoutDashboard },
  { name: "Statystyki", href: "/dashboard/statistics", icon: BarChart2 },
  { name: "Wizyty", href: "/dashboard/users", icon: ClipboardList },
  { name: "Pacjenci", href: "/dashboard/inventory", icon: Users },
  { name: "Rozmowy", href: "/dashboard/orders", icon: Phone },
  { name: "Faktury", href: "/dashboard/billings", icon: Phone },
];

const bottomMenu = [
  { name: "Ustawienia Agenta", href: "/dashboard/settings", icon: Settings },
  { name: "Wyloguj się", href: "/auth/logout", icon: LogOut },
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="w-64 h-screen bg-white border-r flex flex-col justify-between fixed left-0 top-0">
      {/* Logo */}
      <div>
        <div className="h-16 flex items-center px-6 font-bold text-xl gap-2">
          <span className="text-indigo-600">ChatBot admin</span>
          <Headset className="w-10 h-10 text-indigo-600" />
        </div>

        {/* Menu */}
        <nav className="mt-4">
          {menu.map((item) => {
            const Icon = item.icon;
            const active = pathname === item.href;
            return (
              <Link
                key={item.name}
                href={item.href}
                className={clsx(
                  "flex items-center gap-3 px-6 py-3 text-gray-600 hover:bg-indigo-50 hover:text-indigo-600 transition rounded-lg mx-2",
                  active &&
                    "bg-indigo-100 text-indigo-700 font-medium"
                )}
              >
                <Icon className="w-5 h-5" />
                {item.name}
              </Link>
            );
          })}
        </nav>
      </div>

      {/* Bottom */}
      <div className="mb-4">
        {bottomMenu.map((item) => {
          const Icon = item.icon;
          const active = pathname === item.href;
          const isLogout = item.name.toLowerCase() === "wyloguj się"; // sprawdzamy czy to log out

          return (
            <Link
              key={item.name}
              href={item.href}
              className={clsx(
                "flex items-center gap-3 px-6 py-3 transition rounded-lg mx-2",
                active && !isLogout && "bg-indigo-100 text-indigo-700 font-medium",
                !isLogout && "text-gray-600 hover:bg-indigo-50 hover:text-indigo-600",
                isLogout && "text-red-600 hover:bg-red-50 hover:text-red-700 font-medium"
              )}
            >
              <Icon className="w-5 h-5" />
              {item.name}
            </Link>
          );
        })}
      </div>
    </aside>
  );
}
