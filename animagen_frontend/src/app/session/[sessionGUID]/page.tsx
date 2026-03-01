"use client";

import { useState, useEffect, useRef, useCallback } from "react";
import styles from "./page.module.css";

type MessageRole = "user" | "assistant" | "system";

interface Attachment {
  id: string;
  name: string;
  type: string;
  url: string;
  size: number;
}

interface Message {
  id: string;
  role: MessageRole;
  content: string;
  attachments?: Attachment[];
  timestamp: string;
  isPending?: boolean;
}

interface SessionData {
  sessionGUID: string;
  title: string;
  createdAt: string;
  messages: Message[];
  htmlContent?: string;
}

interface MessageStatus {
  message: Message;
  isPending: boolean;
  htmlContent: string | null;
}

const ALLOWED_FILE_TYPES = ["image/jpeg", "image/jpg", "image/png", "image/webp"];
const MAX_FILE_SIZE = 10 * 1024 * 1024;
const POLLING_INTERVAL = 5000;
const POLLING_TIMEOUT = 120000;

interface SessionPageProps {
  sessionGUID: string;
}

function SessionPage({ sessionGUID }: SessionPageProps) {
  const [sessionData, setSessionData] = useState<SessionData | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState("");
  const [attachments, setAttachments] = useState<File[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isSending, setIsSending] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [htmlContent, setHtmlContent] = useState<string>("");
  const pollingIntervalId = useRef<NodeJS.Timeout | null>(null);
  const pollingTimeoutId = useRef<NodeJS.Timeout | null>(null);

  const messagesEndRef = useRef<HTMLDivElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  const loadSession = useCallback(async () => {
    try {
      const response = await fetch(`http://localhost:8000/api/sessions/${sessionGUID}/`);
      if (!response.ok) {
        if (response.status === 404) {
          setError("Session not found. Please check the session ID or create a new session.");
        } else {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return;
      }
      const data: SessionData = await response.json();
      setSessionData(data);
      setMessages(data.messages);
      setHtmlContent(data.htmlContent || "");
      setError(null);
    } catch (err) {
      setError("Failed to load session. Please try again later.");
      console.error("Error loading session:", err);
    } finally {
      setIsLoading(false);
    }
  }, [sessionGUID]);

  const startPolling = (messageId: string) => {
    const interval = setInterval(async () => {
      try {
        const response = await fetch(`http://localhost:8000/api/sessions/${sessionGUID}/messages/${messageId}/`);
        if (!response.ok) return;

        const data: MessageStatus = await response.json();

        if (!data.isPending) {
          setMessages(prev => prev.map(msg => msg.id === data.message.id ? data.message : msg));
          setHtmlContent(data.htmlContent || "");
          stopPolling();
          setIsSending(false);
        }
      } catch (err) {
        console.error("Polling error:", err);
      }
    }, POLLING_INTERVAL);

    pollingIntervalId.current = interval;

    const timeout = setTimeout(() => {
      stopPolling();
      setIsSending(false);
      setError("Request timed out. Please try again.");
    }, POLLING_TIMEOUT);

    pollingTimeoutId.current = timeout;
  };

  const stopPolling = () => {
    if (pollingIntervalId.current) {
      clearInterval(pollingIntervalId.current);
      pollingIntervalId.current = null;
    }
    if (pollingTimeoutId.current) {
      clearTimeout(pollingTimeoutId.current);
      pollingTimeoutId.current = null;
    }
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    loadSession();
    return () => {
      if (pollingIntervalId.current) clearInterval(pollingIntervalId.current);
      if (pollingTimeoutId.current) clearTimeout(pollingTimeoutId.current);
    };
  }, [loadSession]);

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(e.target.files || []);
    const validFiles = files.filter(file => {
      if (!ALLOWED_FILE_TYPES.includes(file.type)) {
        setError(`Invalid file type: ${file.name}. Only JPG, PNG, and WEBP are allowed.`);
        return false;
      }
      if (file.size > MAX_FILE_SIZE) {
        setError(`File too large: ${file.name}. Maximum size is 10MB.`);
        return false;
      }
      return true;
    });

    setAttachments(prev => [...prev, ...validFiles]);
    setError(null);
  };

  const removeAttachment = (index: number) => {
    setAttachments(prev => prev.filter((_, i) => i !== index));
  };

  const handleSendMessage = async () => {
    if (!inputValue.trim() && attachments.length === 0) return;
    if (isSending) return;

    setIsSending(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append("content", inputValue);
      attachments.forEach(file => {
        formData.append("files", file);
      });

      const response = await fetch(`http://localhost:8000/api/sessions/${sessionGUID}/messages/`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      setMessages(prev => [...prev, result.message]);
      setInputValue("");
      setAttachments([]);

      startPolling(result.message.id);

    } catch (err) {
      setIsSending(false);
      setError("Failed to send message. Please try again.");
      console.error("Error sending message:", err);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const handleCardClick = () => {
    window.open(`/animation/${sessionGUID}`, "_blank", "noopener,noreferrer");
  };

  if (isLoading) {
    return (
      <div className={styles.page}>
        <div className={styles.loadingContainer}>
          <div className={styles.loadingSpinner}></div>
          <p className={styles.loadingText}>Loading session...</p>
        </div>
      </div>
    );
  }

  if (error && !sessionData) {
    return (
      <div className={styles.page}>
        <div className={`${styles.errorContainer} ${styles.glassCard}`}>
          <div className={styles.errorIcon}>⚠️</div>
          <h2 className={styles.errorTitle}>Error</h2>
          <p className={styles.errorMessage}>{error}</p>
          <button
            onClick={() => window.location.href = "/"}
            className={`${styles.btn} ${styles.btnPrimary}`}
          >
            Go to Home
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className={styles.page}>
      <header className={`${styles.header} ${styles.glassCard}`}>
        <div className={styles.headerContent}>
          <h1 className={styles.sessionTitle}>{sessionData?.title || "Session"}</h1>
          <p className={styles.sessionId}>{sessionGUID}</p>
        </div>
      </header>

      <main className={styles.mainContainer}>
        <div className={styles.chatContainer}>
          <div className={styles.messagesContainer}>
            {messages.length === 0 ? (
              <div className={styles.emptyState}>
                <div className={styles.emptyIcon}>💬</div>
                <p className={styles.emptyText}>Start a conversation by typing a message below</p>
              </div>
            ) : (
              messages.map((message) => (
                <div
                  key={message.id}
                  className={`${styles.message} ${styles[message.role]}`}
                >
                  <div className={`${styles.messageBubble} ${styles.glassCard}`}>
                    {message.attachments && message.attachments.length > 0 && (
                      <div className={styles.attachmentsGrid}>
                        {message.attachments.map((attachment) => (
                          <div key={attachment.id} className={styles.attachment}>
                            <img
                              src={attachment.url}
                              alt={attachment.name}
                              className={styles.attachmentImage}
                            />
                          </div>
                        ))}
                      </div>
                    )}
                    <p className={styles.messageText}>{message.content}</p>
                    <span className={styles.messageTimestamp}>
                      {new Date(message.timestamp).toLocaleTimeString()}
                    </span>
                    {message.isPending && (
                      <div className={styles.typingIndicator}>
                        <span></span>
                        <span></span>
                        <span></span>
                      </div>
                    )}
                  </div>
                </div>
              ))
            )}
            <div ref={messagesEndRef} />
          </div>

          {error && sessionData && (
            <div className={`${styles.errorBanner} ${styles.glassCard}`}>
              <span className={styles.errorBannerIcon}>⚠️</span>
              <p className={styles.errorBannerText}>{error}</p>
              <button
                onClick={() => setError(null)}
                className={styles.errorBannerClose}
              >
                ✕
              </button>
            </div>
          )}

          <div className={`${styles.inputContainer} ${styles.glassCard}`}>
            {attachments.length > 0 && (
              <div className={styles.attachmentsPreview}>
                {attachments.map((file, index) => (
                  <div key={index} className={styles.attachmentPreview}>
                    <span className={styles.attachmentName}>{file.name}</span>
                    <button
                      onClick={() => removeAttachment(index)}
                      className={styles.removeAttachment}
                    >
                      ✕
                    </button>
                  </div>
                ))}
              </div>
            )}

            <div className={styles.inputWrapper}>
              <button
                onClick={() => fileInputRef.current?.click()}
                className={`${styles.attachButton} ${styles.iconButton}`}
                title="Attach files"
              >
                📎
              </button>
              <input
                ref={fileInputRef}
                type="file"
                multiple
                accept={ALLOWED_FILE_TYPES.join(",")}
                onChange={handleFileSelect}
                className={styles.fileInput}
              />

              <textarea
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyDown={handleKeyPress}
                placeholder="Describe what you want to create..."
                className={styles.messageInput}
                rows={1}
              />

              <button
                onClick={handleSendMessage}
                disabled={isSending || (!inputValue.trim() && attachments.length === 0)}
                className={`${styles.sendButton} ${styles.iconButton} ${(!inputValue.trim() && attachments.length === 0) ? styles.sendButtonDisabled : ""}`}
                title="Send message"
              >
                {isSending ? "⏳" : "➤"}
              </button>
            </div>
          </div>
        </div>

        <aside className={styles.animationSidebar}>
          <h2 className={styles.sidebarTitle}>Animation</h2>
          {htmlContent ? (
            <div className={`${styles.animationCard} ${styles.glassCard}`} onClick={handleCardClick}>
              <div className={styles.cardIcon}>▶️</div>
              <h3 className={styles.cardTitle}>Animation Ready</h3>
              <p className={styles.cardDescription}>Click to view your generated animation</p>
            </div>
          ) : (
            <div className={styles.animationPlaceholder}>
              <p>The animation appears here</p>
            </div>
          )}
        </aside>
      </main>
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

  return <SessionPage sessionGUID={sessionGUID} />;
}
