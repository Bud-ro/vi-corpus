import { ClerkProvider, Show, SignIn, SignUp, useAuth } from "@clerk/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { RouterProvider } from "@tanstack/react-router";
import { Agentation } from "agentation";
import React, { useEffect, useState } from "react";
import ReactDOM from "react-dom/client";

import { setAuthTokenProvider } from "./api/client";
import { ArcLogo } from "./components/ArcLogo";
import { WorkspaceProgressScreen } from "./components/WorkspaceProgressScreen";
import { router } from "./routes/router";
import "./styles/app.css";

const queryClient = new QueryClient();
const clerkPublishableKey = import.meta.env.VITE_CLERK_PUBLISHABLE_KEY as string | undefined;
const signInPath = "/sign-in";
const signUpPath = "/sign-up";
const authAppearance = {
  elements: {
    footerAction: "auth-clerk-footer-action-hidden",
  },
};

type AuthPath = typeof signInPath | typeof signUpPath;

function isAuthRoute(pathname: string) {
  return (
    pathname === signInPath ||
    pathname.startsWith(`${signInPath}/`) ||
    pathname === signUpPath ||
    pathname.startsWith(`${signUpPath}/`)
  );
}

function authPathFromLocation(): AuthPath {
  return window.location.pathname === signUpPath || window.location.pathname.startsWith(`${signUpPath}/`)
    ? signUpPath
    : signInPath;
}

function App() {
  if (!clerkPublishableKey) {
    return (
      <>
        <RouterProvider router={router} />
        {import.meta.env.DEV ? <Agentation /> : null}
      </>
    );
  }

  return (
    <ClerkProvider publishableKey={clerkPublishableKey} signInUrl={signInPath} signUpUrl={signUpPath}>
      <Show when="signed-out">
        <SignedOutAuth />
      </Show>
      <Show when="signed-in">
        <AuthenticatedApp />
      </Show>
      {import.meta.env.DEV ? <Agentation /> : null}
    </ClerkProvider>
  );
}

function SignedOutAuth() {
  const [authPath, setAuthPath] = useState<AuthPath>(() => authPathFromLocation());
  const isSignUp = authPath === signUpPath;

  useEffect(() => {
    if (!isAuthRoute(window.location.pathname)) {
      window.history.replaceState(null, "", signInPath);
    }

    const handlePopState = () => {
      setAuthPath(authPathFromLocation());
    };

    setAuthPath(authPathFromLocation());
    window.addEventListener("popstate", handlePopState);
    return () => window.removeEventListener("popstate", handlePopState);
  }, []);

  function navigateAuth(path: AuthPath) {
    window.history.pushState(null, "", path);
    setAuthPath(path);
  }

  return (
    <main className="auth-start">
      <div className="auth-start-panel">
        <div className="brand-copy">
          <ArcLogo />
        </div>
        {isSignUp ? (
          <SignUp
            appearance={authAppearance}
            fallbackRedirectUrl="/"
            forceRedirectUrl="/"
            path={signUpPath}
            routing="path"
            signInUrl={signInPath}
          />
        ) : (
          <SignIn
            appearance={authAppearance}
            fallbackRedirectUrl="/"
            forceRedirectUrl="/"
            path={signInPath}
            routing="path"
            signUpUrl={signUpPath}
            withSignUp={false}
          />
        )}
        <div className="auth-mode-switch">
          {isSignUp ? "Already have an account?" : "Don't have an account?"}{" "}
          <button type="button" onClick={() => navigateAuth(isSignUp ? signInPath : signUpPath)}>
            {isSignUp ? "Sign in" : "Sign up"}
          </button>
        </div>
      </div>
    </main>
  );
}

function AuthenticatedApp() {
  const { getToken, isLoaded, isSignedIn } = useAuth();
  const [authReady, setAuthReady] = useState(false);
  const [authError, setAuthError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    setAuthReady(false);
    setAuthError(null);
    setAuthTokenProvider(null);

    if (!isLoaded || !isSignedIn) return;

    getToken()
      .then((token) => {
        if (cancelled) return;
        if (!token) {
          setAuthError("Could not start a signed-in Arc session.");
          return;
        }
        if (window.location.pathname === signInPath || window.location.pathname.startsWith(signUpPath)) {
          window.history.replaceState(null, "", "/");
        }
        setAuthTokenProvider(getToken);
        setAuthReady(true);
      })
      .catch(() => {
        if (!cancelled) setAuthError("Could not start a signed-in Arc session.");
      });

    return () => {
      cancelled = true;
      setAuthTokenProvider(null);
    };
  }, [getToken, isLoaded, isSignedIn]);

  if (!authReady) {
    return <WorkspaceProgressScreen error={authError} />;
  }

  return <RouterProvider router={router} />;
}

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <App />
    </QueryClientProvider>
  </React.StrictMode>
);
