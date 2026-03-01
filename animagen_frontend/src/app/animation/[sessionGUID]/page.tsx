"use client";

import { useState, useEffect } from "react";
import styles from "./page.module.css";

interface AnimationPageProps {
  sessionGUID: string;
}

function AnimationPage({ sessionGUID }: AnimationPageProps) {
  const [htmlContent, setHtmlContent] = useState<string>("");
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadAnimation = async () => {
      try {
        const response = await fetch(`http://localhost:8000/api/sessions/${sessionGUID}/animation/`);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        setHtmlContent(data.html_content);
        setError(null);
      } catch (err) {
        setError("Failed to load animation. The animation may not exist or there was a network error.");
        console.error("Error loading animation:", err);
      } finally {
        setIsLoading(false);
      }
    };

    loadAnimation();
  }, [sessionGUID]);

  if (isLoading) {
    return (
      <div className={styles.page}>
        <div className={styles.loadingContainer}>
          <div className={styles.loadingSpinner}></div>
          <p className={styles.loadingText}>Loading animation...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className={styles.page}>
        <div className={`${styles.errorContainer} ${styles.glassCard}`}>
          <div className={styles.errorIcon}>⚠️</div>
          <h2 className={styles.errorTitle}>Error</h2>
          <p className={styles.errorMessage}>{error}</p>
          <button 
            onClick={() => window.close()}
            className={`${styles.btn} ${styles.btnPrimary}`}
          >
            Close
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className={styles.page}>
      <button 
        onClick={() => window.close()}
        className={styles.closeButton}
        title="Close"
      >
        ✕
      </button>
      <iframe
        srcDoc={htmlContent}
        sandbox="allow-scripts allow-same-origin allow-forms"
        className={styles.animationFrame}
        title="Animation Viewer"
      />
    </div>
  );
}

export default function Page({ params }: { params: Promise<{ sessionGUID: string }> }) {
  const [sessionGUID, setSessionGUID] = useState<string | null>(null);

  useEffect(() => {
    params.then(p => setSessionGUID(p.sessionGUID));
  }, [params]);

  if (!sessionGUID) {
    return null;
  }

  return <AnimationPage sessionGUID={sessionGUID} />;
}
