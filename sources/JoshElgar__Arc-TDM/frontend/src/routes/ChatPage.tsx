import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { Menu } from "@base-ui/react/menu";
import { useEffect, useLayoutEffect, useMemo, useRef, useState, type DragEvent, type MouseEvent } from "react";
import ReactMarkdown from "react-markdown";
import type { Components } from "react-markdown";

import { api } from "../api/client";
import type { ChatActivityEvent, ChatAttachment, ChatSeedMessage, FileEntry, Message } from "../api/types";
import { AppIcon, type AppIconName } from "../components/AppIcon";
import { PageLoading } from "../components/PageLoading";
import { formatArcTime, formatBytes } from "../utils/format";
import { useWorkspaceId } from "./workspaceContext";

const newChatEventName = "arc:new-chat";

type NewChatEventDetail = {
  workspaceId: string;
};

type ChatMessage = ChatSeedMessage & {
  attachments?: ChatAttachment[];
  activity?: ChatActivityEvent[];
};

type SendChatPayload = {
  message: string;
  mentions: ChatAttachment[];
  seedMessages?: ChatSeedMessage[];
};

type PendingChatUpload = {
  id: string;
  name: string;
  size: number;
  status: "uploading" | "ready" | "failed";
  path?: string;
  error?: string;
};

const onboardingTranscript: ChatSeedMessage[] = [
  {
    role: "user",
    content: "What is this?"
  },
  {
    role: "assistant",
    content:
      "Hi, welcome to Arc. This chat is the fastest way to work with your workspace.\n\nAsk me to inspect files, organize assets and runs, design workbook steps, compute a workbook, or turn outputs into charts and reports. Start by telling me what you want to understand."
  }
];
const onboardingTranscriptDelayMs = 1150;
const maxPendingChatUploads = 10;

const chatSuggestions: Array<{ icon: AppIconName; label: string; prompt: string }> = [
  {
    icon: "file",
    label: "Inspect files",
    prompt: "Look through the workspace files and tell me what is worth reviewing first."
  },
  {
    icon: "data",
    label: "Analyze data",
    prompt: "Find the data files in this workspace and suggest a simple analysis."
  },
  {
    icon: "review",
    label: "Build workbook",
    prompt: "Help me design a workbook for a repeatable asset or run review."
  },
  {
    icon: "reports",
    label: "Create report",
    prompt: "Create a report step from the available workbook outputs or data files."
  }
];

export function requestNewChat(workspaceId: string) {
  window.localStorage.removeItem(activeChatStorageKey(workspaceId));
  window.dispatchEvent(new CustomEvent<NewChatEventDetail>(newChatEventName, { detail: { workspaceId } }));
}

export function ChatPage() {
  const workspaceId = useWorkspaceId();
  const queryClient = useQueryClient();
  const chatStorageKey = activeChatStorageKey(workspaceId);
  const [chatId, setChatId] = useState<string | undefined>();
  const [draft, setDraft] = useState("");
  const [draftMentions, setDraftMentions] = useState<ChatAttachment[]>([]);
  const [draftCursor, setDraftCursor] = useState(0);
  const [selectedMentionIndex, setSelectedMentionIndex] = useState(0);
  const [dismissedMentionStart, setDismissedMentionStart] = useState<number | null>(null);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isHistoryOpen, setIsHistoryOpen] = useState(false);
  const [chatDetailLoading, setChatDetailLoading] = useState(false);
  const [onboardingMessagesFinished, setOnboardingMessagesFinished] = useState(false);
  const [showMessageBlur, setShowMessageBlur] = useState(false);
  const [showScrollToBottom, setShowScrollToBottom] = useState(false);
  const [pendingUploads, setPendingUploads] = useState<PendingChatUpload[]>([]);
  const [isDraggingFiles, setIsDraggingFiles] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const messagesRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const project = useQuery({ queryKey: ["project", workspaceId], queryFn: () => api.project(workspaceId) });
  const chats = useQuery({ queryKey: ["chats", workspaceId], queryFn: () => api.chats(workspaceId) });
  const chatSetupMessage = project.data?.chat_setup_message;
  const chatAvailable = project.data?.chat_available ?? false;
  const userFiles = useQuery({
    queryKey: ["files", workspaceId],
    queryFn: () => api.files(workspaceId),
    enabled: chatAvailable
  });
  const shouldShowChatOnboarding =
    !chatSetupMessage && !chatId && messages.length === 0 && (chats.data?.length ?? 0) === 0;
  const shouldShowSuggestionChips = !chatSetupMessage && !chatId && messages.length === 0 && chatAvailable;
  const visibleMessages: ChatMessage[] = shouldShowChatOnboarding ? onboardingTranscript : messages;
  const shouldShowCenteredEmptyState = shouldShowSuggestionChips && visibleMessages.length === 0;
  const send = useMutation({
    mutationFn: ({ message, mentions, seedMessages }: SendChatPayload) =>
      api.chat(workspaceId, message, chatId, seedMessages, mentions),
    onSuccess: (response) => {
      window.localStorage.setItem(chatStorageKey, response.chat_id);
      setChatId(response.chat_id);
      queryClient.invalidateQueries({ queryKey: ["chats", workspaceId] });
      setMessages((current) => [
        ...current,
        {
          role: "assistant",
          content: response.assistant_message,
          attachments: response.attachments,
          activity: response.activity
        }
      ]);
    },
    onError: (error) => {
      setMessages((current) => [
        ...current,
        {
          role: "assistant",
          content: error instanceof Error ? error.message : "Arc Agent request failed."
        }
      ]);
    }
  });
  const composerDisabled =
    !chatAvailable || send.isPending || (shouldShowChatOnboarding && !onboardingMessagesFinished);
  const pendingUploadAttachments = useMemo(
    () =>
      pendingUploads
        .filter((upload) => upload.status === "ready" && upload.path)
        .map<ChatAttachment>((upload) => ({
          type: "workspace_file",
          path: upload.path ?? "",
          title: upload.name
        })),
    [pendingUploads]
  );
  const uploadsInProgress = pendingUploads.some((upload) => upload.status === "uploading");
  const sendDisabled = composerDisabled || uploadsInProgress || (!draft.trim() && pendingUploadAttachments.length === 0);
  const uploadDisabled = composerDisabled || pendingUploads.length >= maxPendingChatUploads;
  const activeMention = useMemo(() => activeFileMention(draft, draftCursor), [draft, draftCursor]);
  const mentionOptions = useMemo(() => {
    if (!activeMention || activeMention.start === dismissedMentionStart) return [];
    return fileMentionOptions(userFiles.data ?? [], activeMention.query);
  }, [activeMention, dismissedMentionStart, userFiles.data]);
  const mentionOpen = Boolean(activeMention && mentionOptions.length);
  const selectedMentionOptionIndex = Math.min(selectedMentionIndex, Math.max(mentionOptions.length - 1, 0));
  const selectedMention = mentionOptions[selectedMentionOptionIndex];

  useEffect(() => {
    setSelectedMentionIndex(0);
  }, [activeMention?.query, activeMention?.start]);

  useEffect(() => {
    let cancelled = false;
    const storedChatId = window.localStorage.getItem(chatStorageKey) ?? undefined;

    setDraft("");
    setDraftMentions([]);
    setPendingUploads([]);
    setIsDraggingFiles(false);
    setDraftCursor(0);
    setDismissedMentionStart(null);
    setIsHistoryOpen(false);
    setChatId(storedChatId);
    setMessages([]);
    setChatDetailLoading(Boolean(storedChatId));
    setOnboardingMessagesFinished(false);
    setShowMessageBlur(false);
    setShowScrollToBottom(false);

    if (!storedChatId) return;

    api.chatDetail(workspaceId, storedChatId)
      .then((detail) => {
        if (cancelled) return;
        setChatId(detail.id);
        setMessages(detail.messages.map(storedMessageToChatMessage));
        setChatDetailLoading(false);
        setOnboardingMessagesFinished(true);
      })
      .catch(() => {
        if (cancelled) return;
        window.localStorage.removeItem(chatStorageKey);
        setChatId(undefined);
        setMessages([]);
        setChatDetailLoading(false);
        setOnboardingMessagesFinished(false);
        setShowMessageBlur(false);
        setShowScrollToBottom(false);
      });

    return () => {
      cancelled = true;
    };
  }, [chatStorageKey, workspaceId]);

  function startNewChat() {
    window.localStorage.removeItem(chatStorageKey);
    send.reset();
    setChatId(undefined);
    setDraft("");
    setDraftMentions([]);
    setPendingUploads([]);
    setIsDraggingFiles(false);
    setDraftCursor(0);
    setDismissedMentionStart(null);
    setMessages([]);
    setChatDetailLoading(false);
    setOnboardingMessagesFinished(false);
    setIsHistoryOpen(false);
    setShowMessageBlur(false);
    setShowScrollToBottom(false);
  }

  useEffect(() => {
    function handleNewChat(event: Event) {
      const detail = (event as CustomEvent<NewChatEventDetail>).detail;
      if (detail?.workspaceId !== workspaceId) return;
      startNewChat();
    }

    window.addEventListener(newChatEventName, handleNewChat);
    return () => window.removeEventListener(newChatEventName, handleNewChat);
  }, [chatStorageKey, workspaceId]);

  function switchChat(nextChatId: string) {
    window.localStorage.setItem(chatStorageKey, nextChatId);
    send.reset();
    setChatId(nextChatId);
    setDraft("");
    setDraftMentions([]);
    setPendingUploads([]);
    setIsDraggingFiles(false);
    setDraftCursor(0);
    setDismissedMentionStart(null);
    setMessages([]);
    setChatDetailLoading(true);
    setOnboardingMessagesFinished(true);
    setIsHistoryOpen(false);
    setShowMessageBlur(false);
    setShowScrollToBottom(false);

    api.chatDetail(workspaceId, nextChatId)
      .then((detail) => {
        if (window.localStorage.getItem(chatStorageKey) !== nextChatId) return;
        setChatId(detail.id);
        setMessages(detail.messages.map(storedMessageToChatMessage));
        setChatDetailLoading(false);
        setOnboardingMessagesFinished(true);
      })
      .catch(() => {
        if (window.localStorage.getItem(chatStorageKey) !== nextChatId) return;
        window.localStorage.removeItem(chatStorageKey);
        setChatId(undefined);
        setMessages([]);
        setChatDetailLoading(false);
        setOnboardingMessagesFinished(false);
        setShowMessageBlur(false);
        setShowScrollToBottom(false);
      });
  }

  function submit() {
    const message = draft.trim();
    if (sendDisabled) return;
    const readyAttachments = pendingUploadAttachments;
    const sendMessage = message || uploadedFileFallbackMessage(readyAttachments);
    const seedMessages = shouldShowChatOnboarding ? onboardingTranscript : undefined;
    const mentions = mergeChatAttachments(activeDraftMentions(sendMessage, draftMentions), readyAttachments);
    const userMessage: ChatMessage = { role: "user", content: sendMessage, attachments: mentions };
    setMessages((current) => (seedMessages ? [...seedMessages, userMessage] : [...current, userMessage]));
    setDraft("");
    setDraftMentions([]);
    setPendingUploads([]);
    setIsDraggingFiles(false);
    setDraftCursor(0);
    setDismissedMentionStart(null);
    send.mutate({ message: sendMessage, mentions, seedMessages });
  }

  function applySuggestion(prompt: string) {
    if (composerDisabled) return;
    changeDraft(prompt, prompt.length);
    window.requestAnimationFrame(() => {
      textareaRef.current?.focus();
      textareaRef.current?.setSelectionRange(prompt.length, prompt.length);
    });
  }

  function changeDraft(nextDraft: string, nextCursor: number) {
    setDraft(nextDraft);
    setDraftCursor(nextCursor);
    setDismissedMentionStart(null);
    setDraftMentions((current) => activeDraftMentions(nextDraft, current));
  }

  function updateDraftCursor(textarea: HTMLTextAreaElement) {
    setDraftCursor(textarea.selectionStart);
  }

  function insertFileMention(file: FileEntry) {
    if (!activeMention) return;
    const label = fileMentionLabel(file, userFiles.data ?? []);
    const afterMention = draft.slice(activeMention.end);
    const suffix = afterMention.startsWith(" ") || afterMention.startsWith("\n") ? "" : " ";
    const replacement = `${label}${suffix}`;
    const nextDraft = `${draft.slice(0, activeMention.start)}${replacement}${afterMention}`;
    const nextCursor = activeMention.start + replacement.length;
    const mention: ChatAttachment = {
      type: "workspace_file",
      path: file.path,
      title: file.name,
      label
    };

    setDraft(nextDraft);
    setDraftMentions((current) => mergeDraftMention(activeDraftMentions(nextDraft, current), mention));
    setDraftCursor(nextCursor);
    setDismissedMentionStart(null);
    window.requestAnimationFrame(() => {
      textareaRef.current?.focus();
      textareaRef.current?.setSelectionRange(nextCursor, nextCursor);
    });
  }

  function chooseFiles(files: FileList | null) {
    if (uploadDisabled) return;
    const selectedFiles = Array.from(files ?? []);
    if (!selectedFiles.length) return;
    const acceptedFiles = selectedFiles.slice(0, maxPendingChatUploads - pendingUploads.length);
    if (!acceptedFiles.length) return;
    const rows = acceptedFiles.map((file) => ({
      file,
      upload: {
        id: pendingUploadId(file),
        name: file.name,
        size: file.size,
        status: "uploading" as const
      }
    }));
    setPendingUploads((current) => [...current, ...rows.map((row) => row.upload)]);
    rows.forEach((row) => uploadChatFile(row.file, row.upload.id));
  }

  async function uploadChatFile(file: File, uploadId: string) {
    try {
      const uploaded = await api.uploadFile(workspaceId, file);
      setPendingUploads((current) =>
        current.map((upload) =>
          upload.id === uploadId
            ? { ...upload, status: "ready", path: uploaded.path }
            : upload
        )
      );
      queryClient.invalidateQueries({ queryKey: ["files", workspaceId] });
      queryClient.invalidateQueries({ queryKey: ["workspace-files", workspaceId] });
      queryClient.invalidateQueries({ queryKey: ["git-status", workspaceId] });
    } catch (error) {
      setPendingUploads((current) =>
        current.map((upload) =>
          upload.id === uploadId
            ? {
                ...upload,
                status: "failed",
                error: error instanceof Error ? error.message : "Upload failed"
              }
            : upload
        )
      );
    }
  }

  function removePendingUpload(uploadId: string) {
    setPendingUploads((current) => current.filter((upload) => upload.id !== uploadId));
  }

  function handleComposerDragEnter(event: DragEvent<HTMLDivElement>) {
    if (composerDisabled || !dragEventHasFiles(event)) return;
    event.preventDefault();
    setIsDraggingFiles(true);
  }

  function handleComposerDragOver(event: DragEvent<HTMLDivElement>) {
    if (composerDisabled || !dragEventHasFiles(event)) return;
    event.preventDefault();
    event.dataTransfer.dropEffect = pendingUploads.length >= maxPendingChatUploads ? "none" : "copy";
    setIsDraggingFiles(true);
  }

  function handleComposerDragLeave(event: DragEvent<HTMLDivElement>) {
    if (event.currentTarget.contains(event.relatedTarget as Node | null)) return;
    setIsDraggingFiles(false);
  }

  function handleComposerDrop(event: DragEvent<HTMLDivElement>) {
    if (composerDisabled || !dragEventHasFiles(event)) return;
    event.preventDefault();
    setIsDraggingFiles(false);
    chooseFiles(event.dataTransfer.files);
  }

  function updateMessageScrollState(messagesElement: HTMLDivElement) {
    const distanceFromBottom = Math.max(
      0,
      messagesElement.scrollHeight - messagesElement.scrollTop - messagesElement.clientHeight
    );
    setShowMessageBlur(distanceFromBottom > 2);
    setShowScrollToBottom(distanceFromBottom > 96);
  }

  function scrollToBottom() {
    const messagesElement = messagesRef.current;
    if (!messagesElement) return;
    messagesElement.scrollTo({ top: messagesElement.scrollHeight, behavior: "smooth" });
    setShowMessageBlur(false);
    setShowScrollToBottom(false);
  }

  function focusComposerFromPageClick(event: MouseEvent<HTMLElement>) {
    const target = event.target;
    if (!(target instanceof HTMLElement)) return;
    if (target.closest("a, button, input, textarea, select, [role='menu'], [role='menuitem'], [contenteditable='true']")) {
      return;
    }
    textareaRef.current?.focus();
  }

  useLayoutEffect(() => {
    const textarea = textareaRef.current;
    if (!textarea) return;
    textarea.style.height = "auto";
    const maxHeight = 180;
    const nextHeight = Math.min(textarea.scrollHeight, maxHeight);
    textarea.style.height = `${nextHeight}px`;
    textarea.style.overflowY = textarea.scrollHeight > maxHeight ? "auto" : "hidden";
  }, [draft]);

  useLayoutEffect(() => {
    const messagesElement = messagesRef.current;
    if (!messagesElement) return;
    messagesElement.scrollTop = messagesElement.scrollHeight;
    setShowMessageBlur(false);
    setShowScrollToBottom(false);
  }, [chatSetupMessage, messages, send.isPending, shouldShowChatOnboarding]);

  useEffect(() => {
    if (!shouldShowChatOnboarding) {
      setOnboardingMessagesFinished(true);
      return;
    }

    setOnboardingMessagesFinished(false);
    const timeout = window.setTimeout(() => {
      setOnboardingMessagesFinished(true);
      textareaRef.current?.focus();
    }, onboardingTranscriptDelayMs);

    return () => window.clearTimeout(timeout);
  }, [shouldShowChatOnboarding]);

  if (project.isLoading || chats.isLoading || chatDetailLoading) {
    return <PageLoading className="chat-page" label="Loading chat" />;
  }

  const chatActions = (
    <div className="chat-action-row">
      <Menu.Root open={isHistoryOpen} onOpenChange={setIsHistoryOpen}>
        <Menu.Trigger
          render={
            <button
              aria-label="Chat history"
              className="button button-icon"
              disabled={send.isPending || !chats.data?.length}
              title="Chat history"
              type="button"
            >
              <AppIcon name="clock" />
            </button>
          }
        />
        <Menu.Portal>
          <Menu.Positioner align="end" sideOffset={8}>
            <Menu.Popup className="chat-history-popover">
              {chats.data?.map((chat) => (
                <Menu.Item
                  className={chat.id === chatId ? "chat-history-item active" : "chat-history-item"}
                  key={chat.id}
                  onClick={() => switchChat(chat.id)}
                >
                  <span className="chat-history-title">{chat.title || "New chat"}</span>
                  <span className="chat-history-meta">
                    {formatArcTime(chat.updated_at)} / {chat.message_count} messages
                  </span>
                </Menu.Item>
              ))}
            </Menu.Popup>
          </Menu.Positioner>
        </Menu.Portal>
      </Menu.Root>
      <button
        aria-label="Start new chat"
        className="button button-icon"
        disabled={send.isPending}
        onClick={startNewChat}
        title="Start new chat"
        type="button"
      >
        <AppIcon name="plus" />
      </button>
    </div>
  );

  return (
    <div className="page chat-page">
      <section
        className={shouldShowCenteredEmptyState ? "chat-surface chat-surface-empty" : "chat-surface"}
        onClick={focusComposerFromPageClick}
      >
        <div
          className={shouldShowCenteredEmptyState ? "messages messages-empty" : "messages"}
          onScroll={(event) => updateMessageScrollState(event.currentTarget)}
          ref={messagesRef}
        >
          {shouldShowCenteredEmptyState ? (
            <div className="chat-empty-hero">
              <h2>What should we build?</h2>
            </div>
          ) : null}
          {chatSetupMessage ? (
            <div className="message assistant setup-message">
              <span>Arc Agent</span>
              <ChatMarkdown content={chatSetupMessage} />
            </div>
          ) : null}
          {visibleMessages.map((message, index) => (
            <div
              className={`message ${message.role}${shouldShowChatOnboarding ? " onboarding-message" : ""}`}
              key={`${message.role}-${index}`}
            >
              {message.role === "assistant" && <span>Arc Agent</span>}
              {message.role === "assistant" ? (
                <ChatMarkdown content={message.content} />
              ) : (
                <>
                  <UserMessageContent content={message.content} mentions={message.attachments ?? []} />
                  {message.attachments?.length ? <UserChatAttachments attachments={message.attachments} /> : null}
                </>
              )}
              {message.role === "assistant" && message.attachments?.length ? (
                <ChatAttachments attachments={message.attachments} workspaceId={workspaceId} />
              ) : null}
              {message.role === "assistant" && message.activity?.length ? (
                <ChatActivity activity={message.activity} />
              ) : null}
            </div>
          ))}
          {shouldShowSuggestionChips ? (
            <div className="chat-suggestion-chips" aria-label="Suggested prompts">
              {chatSuggestions.map((suggestion) => (
                <button
                  className="button button-table chat-suggestion-chip"
                  disabled={composerDisabled}
                  key={suggestion.label}
                  onClick={() => applySuggestion(suggestion.prompt)}
                  type="button"
                >
                  <AppIcon name={suggestion.icon} />
                  {suggestion.label}
                </button>
              ))}
            </div>
          ) : null}
          {send.isPending && (
            <div className="message assistant">
              <span>Arc Agent</span>
              <p className="pending-message">
                <span aria-hidden="true" className="thinking-dots">
                  <span />
                  <span />
                  <span />
                </span>
                Thinking
              </p>
            </div>
          )}
        </div>
        {showMessageBlur ? <div aria-hidden="true" className="chat-message-blur" /> : null}
        <div className="chat-scroll-jump-row">
          {showScrollToBottom ? (
            <button
              aria-label="Scroll to bottom"
              className="button button-icon chat-scroll-to-bottom"
              onClick={scrollToBottom}
              title="Scroll to bottom"
              type="button"
            >
              <AppIcon name="arrowDown" size={18} />
            </button>
          ) : null}
        </div>
        <div
          className={[
            "composer",
            composerDisabled ? "composer-disabled" : "",
            isDraggingFiles ? "composer-dragging" : ""
          ]
            .filter(Boolean)
            .join(" ")}
          onDragEnter={handleComposerDragEnter}
          onDragLeave={handleComposerDragLeave}
          onDragOver={handleComposerDragOver}
          onDrop={handleComposerDrop}
        >
          {mentionOpen ? (
            <div className="chat-mention-popover" role="listbox">
              {mentionOptions.map((file, index) => (
                <button
                  aria-selected={index === selectedMentionOptionIndex}
                  className={index === selectedMentionOptionIndex ? "chat-mention-option active" : "chat-mention-option"}
                  key={file.path}
                  onMouseDown={(event) => {
                    event.preventDefault();
                    insertFileMention(file);
                  }}
                  role="option"
                  type="button"
                >
                  <span className="chat-mention-at">@</span>
                  <span className="chat-mention-name">{file.name}</span>
                  <span className="chat-mention-path">{fileDirectory(file.path)}</span>
                </button>
              ))}
            </div>
          ) : null}
          {isDraggingFiles ? (
            <div className="composer-drop-overlay" aria-hidden="true">
              {pendingUploads.length >= maxPendingChatUploads ? "10 file maximum reached" : "Drop files to upload to Data"}
            </div>
          ) : null}
          {pendingUploads.length ? (
            <div className="composer-attachments" aria-label="Files attached to message" role="list">
              {pendingUploads.map((upload) => (
                <div className={`composer-attachment ${upload.status}`} key={upload.id} role="listitem">
                  <AppIcon
                    className="composer-attachment-icon"
                    name={upload.status === "uploading" ? "spinner" : upload.status === "failed" ? "cross" : "file"}
                    size={15}
                  />
                  <span className="composer-attachment-name" title={upload.path || upload.name}>
                    {upload.name}
                  </span>
                  <span className="composer-attachment-meta">
                    {upload.status === "uploading"
                      ? "uploading"
                      : upload.status === "failed"
                        ? upload.error || "failed"
                        : `${formatBytes(upload.size)} / ready`}
                  </span>
                  <button
                    aria-label={`Remove ${upload.name}`}
                    className="button button-icon composer-attachment-remove"
                    onClick={() => removePendingUpload(upload.id)}
                    title={`Remove ${upload.name}`}
                    type="button"
                  >
                    <AppIcon name="cross" size={13} />
                  </button>
                </div>
              ))}
            </div>
          ) : null}
          <textarea
            ref={textareaRef}
            value={draft}
            onChange={(event) => changeDraft(event.target.value, event.target.selectionStart)}
            onClick={(event) => updateDraftCursor(event.currentTarget)}
            onKeyDown={(event) => {
              if (mentionOpen && activeMention && !event.shiftKey) {
                if (event.key === "ArrowDown") {
                  event.preventDefault();
                  setSelectedMentionIndex((current) => (current + 1) % mentionOptions.length);
                  return;
                }
                if (event.key === "ArrowUp") {
                  event.preventDefault();
                  setSelectedMentionIndex((current) => (current - 1 + mentionOptions.length) % mentionOptions.length);
                  return;
                }
                if ((event.key === "Enter" || event.key === "Tab") && selectedMention) {
                  event.preventDefault();
                  insertFileMention(selectedMention);
                  return;
                }
                if (event.key === "Escape") {
                  event.preventDefault();
                  setDismissedMentionStart(activeMention.start);
                  return;
                }
              }
              if (event.key !== "Enter" || event.shiftKey) return;
              event.preventDefault();
              submit();
            }}
            onKeyUp={(event) => updateDraftCursor(event.currentTarget)}
            onSelect={(event) => updateDraftCursor(event.currentTarget)}
            disabled={composerDisabled}
            placeholder={chatAvailable ? "Ask about files, assets, runs, workbooks, reports, or analytics" : "Arc Chat is not configured"}
          />
          <input
            ref={fileInputRef}
            className="chat-file-input"
            multiple
            type="file"
            onChange={(event) => {
              chooseFiles(event.target.files);
              event.target.value = "";
            }}
          />
          <button
            aria-label="Upload file to Data"
            className="button button-icon composer-upload-button"
            disabled={uploadDisabled}
            onClick={() => fileInputRef.current?.click()}
            title="Upload file to Data"
            type="button"
          >
            <AppIcon name="plus" size={18} />
          </button>
          <button
            aria-label="Send message"
            className="button button-icon send-button"
            onClick={submit}
            disabled={sendDisabled}
            type="button"
          >
            <AppIcon name={send.isPending ? "spinner" : "arrowUp"} size={18} />
          </button>
        </div>
        {chatActions}
      </section>
    </div>
  );
}

const chatMarkdownComponents: Components = {
  a({ node: _node, ...props }) {
    return <a {...props} rel="noreferrer" target="_blank" />;
  }
};

function ChatMarkdown({ content }: { content: string }) {
  return (
    <div className="chat-markdown">
      <ReactMarkdown components={chatMarkdownComponents}>{content}</ReactMarkdown>
    </div>
  );
}

function UserMessageContent({
  content,
  mentions
}: {
  content: string;
  mentions: ChatAttachment[];
}) {
  return (
    <p>
      {userMessageParts(content, mentions).map((part, index) =>
        typeof part === "string" ? (
          part
        ) : (
          <span className="chat-file-mention" key={`${part.mention.path}-${part.label}-${index}`} title={part.mention.path}>
            {part.label}
          </span>
        )
      )}
    </p>
  );
}

function userMessageParts(content: string, mentions: ChatAttachment[]) {
  const locatedMentions = mentions
    .map((mention) => {
      const label = mention.label?.trim();
      if (!label) return null;
      const index = content.indexOf(label);
      return index >= 0 ? { index, label, mention } : null;
    })
    .filter((item): item is { index: number; label: string; mention: ChatAttachment } => Boolean(item))
    .sort((left, right) => left.index - right.index || right.label.length - left.label.length);

  const parts: Array<string | { label: string; mention: ChatAttachment }> = [];
  let cursor = 0;
  for (const item of locatedMentions) {
    if (item.index < cursor) continue;
    if (item.index > cursor) parts.push(content.slice(cursor, item.index));
    parts.push({ label: item.label, mention: item.mention });
    cursor = item.index + item.label.length;
  }
  if (cursor < content.length) parts.push(content.slice(cursor));
  return parts.length ? parts : [content];
}

function UserChatAttachments({ attachments }: { attachments: ChatAttachment[] }) {
  return (
    <div className="chat-user-attachments" aria-label="Attached files">
      {attachments.map((attachment) => (
        <span className="chat-user-attachment" key={`${attachment.path}:${attachment.label ?? ""}`}>
          <AppIcon name="file" size={13} />
          <span className="chat-user-attachment-name">{attachment.title || attachment.path.split("/").at(-1) || attachment.path}</span>
          <span className="chat-user-attachment-path">{attachment.path}</span>
        </span>
      ))}
    </div>
  );
}

function activeChatStorageKey(workspaceId: string) {
  return `arc:${workspaceId}:active-chat`;
}

function storedMessageToChatMessage(message: Message): ChatMessage {
  return {
    role: message.role,
    content: message.content,
    attachments: message.attachments,
    activity: message.activity
  };
}

function ChatActivity({ activity }: { activity: ChatActivityEvent[] }) {
  const okCount = activity.filter((event) => event.status !== "error").length;
  const errorCount = activity.length - okCount;
  const summary =
    errorCount > 0
      ? `${activity.length} workspace actions, ${errorCount} need attention`
      : `${activity.length} workspace action${activity.length === 1 ? "" : "s"}`;

  return (
    <details className="chat-activity">
      <summary>
        <span className="chat-activity-title">Activity</span>
        <span className="chat-activity-summary">{summary}</span>
      </summary>
      <div className="chat-activity-list">
        {activity.map((event, index) => (
          <div className={`chat-activity-item ${event.status}`} key={`${event.label}-${event.detail ?? ""}-${index}`}>
            <AppIcon name={event.status === "error" ? "cross" : "check"} size={14} />
            <span className="chat-activity-label">{event.label}</span>
            {event.detail ? <span className="chat-activity-detail">{event.detail}</span> : null}
          </div>
        ))}
      </div>
    </details>
  );
}

function ChatAttachments({
  attachments,
  workspaceId
}: {
  attachments: ChatAttachment[];
  workspaceId: string;
}) {
  return (
    <div className="chat-attachments">
      {attachments.map((attachment) => (
        <WorkspaceFileAttachment
          attachment={attachment}
          key={`${attachment.type}:${attachment.path}`}
          workspaceId={workspaceId}
        />
      ))}
    </div>
  );
}

function WorkspaceFileAttachment({
  attachment,
  workspaceId
}: {
  attachment: ChatAttachment;
  workspaceId: string;
}) {
  const file = useQuery({
    queryKey: ["workspace-file-read", workspaceId, attachment.path],
    queryFn: () => api.readWorkspaceFile(workspaceId, attachment.path)
  });
  const title = attachment.title || file.data?.name || attachment.path.split("/").at(-1) || attachment.path;

  return (
    <details className="chat-file-card" open>
      <summary>
        <span className="chat-file-title">{title}</span>
        <span className="chat-file-path">{attachment.path}</span>
      </summary>
      {file.isLoading ? (
        <div className="chat-file-state">
          <AppIcon name="spinner" size={14} />
          Loading file...
        </div>
      ) : file.error ? (
        <div className="chat-file-state error">
          {file.error instanceof Error ? file.error.message : "Could not read file."}
        </div>
      ) : file.data ? (
        <>
          <div className="chat-file-meta">
            <span>{file.data.language || "text"}</span>
            <span>{formatBytes(file.data.size)}</span>
            {file.data.truncated ? <span>truncated</span> : null}
          </div>
          <pre className="chat-file-code">
            <code>{file.data.text}</code>
          </pre>
        </>
      ) : null}
    </details>
  );
}

function activeFileMention(text: string, cursor: number) {
  const beforeCursor = text.slice(0, cursor);
  const match = /(?:^|\s)@([A-Za-z0-9_./-]*)$/.exec(beforeCursor);
  if (!match) return null;
  const token = match[0];
  const tokenAtIndex = token.lastIndexOf("@");
  return {
    start: beforeCursor.length - token.length + tokenAtIndex,
    end: cursor,
    query: match[1]
  };
}

function fileMentionOptions(files: FileEntry[], query: string) {
  const normalizedQuery = query.toLowerCase();
  return files
    .map((file) => {
      const name = file.name.toLowerCase();
      const path = file.path.toLowerCase();
      const score = fileMentionScore(name, path, normalizedQuery);
      return score === null ? null : { file, score };
    })
    .filter((item): item is { file: FileEntry; score: number } => Boolean(item))
    .sort((left, right) => left.score - right.score || left.file.name.localeCompare(right.file.name) || left.file.path.localeCompare(right.file.path))
    .slice(0, 8)
    .map((item) => item.file);
}

function fileMentionScore(name: string, path: string, query: string) {
  if (!query) return 4;
  if (name.startsWith(query)) return 0;
  if (path.startsWith(query)) return 1;
  if (name.includes(query)) return 2;
  if (path.includes(query)) return 3;
  return null;
}

function fileMentionLabel(file: FileEntry, files: FileEntry[]) {
  const duplicateName = files.some((candidate) => candidate.path !== file.path && candidate.name === file.name);
  return `@${mentionSafeToken(duplicateName ? file.path : file.name)}`;
}

function mentionSafeToken(value: string) {
  return value.replace(/\s+/g, "_");
}

function fileDirectory(path: string) {
  const parts = path.split("/");
  return parts.length > 1 ? parts.slice(0, -1).join("/") : "";
}

function activeDraftMentions(content: string, mentions: ChatAttachment[]) {
  const seen = new Set<string>();
  return mentions.filter((mention) => {
    const label = mention.label?.trim();
    if (!label || !content.includes(label)) return false;
    const key = `${mention.path}\0${label}`;
    if (seen.has(key)) return false;
    seen.add(key);
    return true;
  });
}

function mergeDraftMention(current: ChatAttachment[], mention: ChatAttachment) {
  return [
    ...current.filter((item) => item.path !== mention.path || item.label !== mention.label),
    mention
  ];
}

function mergeChatAttachments(mentions: ChatAttachment[], uploads: ChatAttachment[]) {
  const merged: ChatAttachment[] = [];
  const seen = new Set<string>();
  for (const attachment of [...mentions, ...uploads]) {
    if (seen.has(attachment.path)) continue;
    seen.add(attachment.path);
    merged.push(attachment);
  }
  return merged;
}

function uploadedFileFallbackMessage(attachments: ChatAttachment[]) {
  return attachments.length === 1 ? "Uploaded 1 file." : `Uploaded ${attachments.length} files.`;
}

function pendingUploadId(file: File) {
  return `${Date.now()}:${file.name}:${file.size}:${Math.random().toString(36).slice(2)}`;
}

function dragEventHasFiles(event: DragEvent<HTMLDivElement>) {
  return Array.from(event.dataTransfer.types).includes("Files");
}
