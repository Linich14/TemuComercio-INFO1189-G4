// src/providers/AuthProvider.tsx
import React, { createContext, useContext, useMemo, useState } from "react";
import { Redirect, useSegments } from "expo-router";
import type { User } from "~/src/features/auth/domain/entities/User";

type Ctx = { user: User | null; signIn: (u: User) => void; signOut: () => void };
const Ctx = createContext<Ctx | null>(null);

export const AuthProvider: React.FC<React.PropsWithChildren> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const segments = useSegments();
  
  const inAuthGroup = segments[0] === "(auth)";

  // Corrige la lógica de redirección
  if (!user && !inAuthGroup) {
    return <Redirect href="/(auth)/" />;
  }
  
  if (user && inAuthGroup) {
    return <Redirect href="/(app)/" />;
  }

  const value = useMemo(() => ({
    user,
    signIn: setUser,
    signOut: () => setUser(null),
  }), [user]);

  return <Ctx.Provider value={value}>{children}</Ctx.Provider>;
};

// <-- OJO: hook como **named export**
export const useAuth = () => {
  const v = useContext(Ctx);
  if (!v) throw new Error("useAuth must be used within <AuthProvider>");
  return v;
};

// (Opcional) si quieres default, que sea el Provider, no el hook
export default AuthProvider;
