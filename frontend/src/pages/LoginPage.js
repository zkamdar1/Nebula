// frontend/src/pages/LoginPage.js

import React, { useEffect, useState } from "react";
import LoginForm from "../components/LoginForm";
import { auth } from "../services/firebase";
import { onAuthStateChanged } from "firebase/auth";
import { useNavigate } from "react-router-dom";

const LoginPage = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (user) => {
      if (user) {
        setIsAuthenticated(true);
        navigate("/dashboard");
      }
    });

    return () => unsubscribe();
  }, [navigate]);

  return (
    <div className="login-page">
      {!isAuthenticated && <LoginForm />}
    </div>
  );
};

export default LoginPage;
