"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import styles from "./page.module.css";

export default function Home() {
  const router = useRouter();
  const [isCreating, setIsCreating] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleStartCreating = async () => {
    setIsCreating(true);
    setError(null);

    try {
      const response = await fetch("http://localhost:8000/api/sessions/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          title: "Animation Session",
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      router.push(`/session/${data.sessionGUID}/`);
    } catch (err) {
      setError("Failed to create session. Please try again.");
      console.error("Error creating session:", err);
    } finally {
      setIsCreating(false);
    }
  };

  return (
    <div className={styles.page}>
      <section className={styles.hero}>
        <div className={styles.heroContent}>
          <h1 className={styles.heroTitle}>
            Transform Scientific Concepts Into Stunning Animations
          </h1>
          <p className={styles.heroSubtitle}>
            Simply describe what you want to see in plain language - like &ldquo;Show me the interior of an atom&rdquo; - and watch AI bring it to life
          </p>
          <div className={styles.heroButtons}>
            <button
              className={`${styles.btn} ${styles.btnPrimary}`}
              onClick={handleStartCreating}
              disabled={isCreating}
            >
              {isCreating ? "Creating..." : "Start Creating"}
            </button>
            <button className={`${styles.btn} ${styles.btnSecondary}`}>Watch Demo</button>
          </div>
          {error && (
            <div className={styles.errorMessage}>{error}</div>
          )}
        </div>
      </section>

      <section className={styles.section}>
        <h2 className={styles.sectionTitle}>Why Choose Animagen?</h2>
        <div className={styles.featuresGrid}>
          <div className={`${styles.card} ${styles.featureCard}`}>
            <div className={styles.cardIcon}>💬</div>
            <h3 className={styles.cardTitle}>Natural Language Input</h3>
            <p className={styles.cardDescription}>Describe animations in plain English. No technical skills required.</p>
          </div>
          <div className={`${styles.card} ${styles.featureCard}`}>
            <div className={styles.cardIcon}>🔬</div>
            <h3 className={styles.cardTitle}>Scientific Accuracy</h3>
            <p className={styles.cardDescription}>Physics-based rendering ensures your animations are scientifically correct.</p>
          </div>
          <div className={`${styles.card} ${styles.featureCard}`}>
            <div className={styles.cardIcon}>⚡</div>
            <h3 className={styles.cardTitle}>Instant Generation</h3>
            <p className={styles.cardDescription}>From prompt to animation in seconds. No waiting, no complex setup.</p>
          </div>
          <div className={`${styles.card} ${styles.featureCard}`}>
            <div className={styles.cardIcon}>📦</div>
            <h3 className={styles.cardTitle}>Multiple Export Formats</h3>
            <p className={styles.cardDescription}>Export your creations in MP4, GIF, or WebM format.</p>
          </div>
        </div>
      </section>

      <section className={styles.section}>
        <h2 className={styles.sectionTitle}>See What&apos;s Possible</h2>
        <div className={styles.examplesGrid}>
          <div className={`${styles.card} ${styles.exampleCard}`}>
            <div className={styles.examplePreview}>
              <div className={styles.examplePlaceholder}>🌌</div>
            </div>
            <h3 className={styles.cardTitle}>The Solar System</h3>
            <p className={styles.cardDescription}>Explore planetary orbits and celestial mechanics</p>
          </div>
          <div className={`${styles.card} ${styles.exampleCard}`}>
            <div className={styles.examplePreview}>
              <div className={styles.examplePlaceholder}>🧬</div>
            </div>
            <h3 className={styles.cardTitle}>Cellular Respiration</h3>
            <p className={styles.cardDescription}>Visualize energy production at the cellular level</p>
          </div>
          <div className={`${styles.card} ${styles.exampleCard}`}>
            <div className={styles.examplePreview}>
              <div className={styles.examplePlaceholder}>⚛️</div>
            </div>
            <h3 className={styles.cardTitle}>Quantum Entanglement</h3>
            <p className={styles.cardDescription}>Understand quantum mechanics through animation</p>
          </div>
        </div>
      </section>

      <section className={styles.ctaSection}>
        <div className={`${styles.card} ${styles.ctaCard}`}>
          <h2 className={styles.ctaTitle}>Ready to Create Your First Animation?</h2>
          <p className={styles.ctaDescription}>Join thousands of educators, students, and curious minds bringing science to life.</p>
          <button
            className={`${styles.btn} ${styles.btnPrimary} ${styles.btnLarge}`}
            onClick={handleStartCreating}
            disabled={isCreating}
          >
            {isCreating ? "Creating..." : "Get Started Free"}
          </button>
        </div>
      </section>
    </div>
  );
}
