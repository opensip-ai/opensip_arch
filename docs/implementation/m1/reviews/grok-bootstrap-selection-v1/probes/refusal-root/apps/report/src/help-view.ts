/** Contextual explanations supplied by the view, rendered only as text. */
export interface HelpView {
  readonly element: HTMLDivElement;
  /** Removes listeners and closes an open dialog before removing its elements. */
  dispose(): void;
}

/** This control does not read report data or infer evidence/assessment status. */
export function createHelpView(
  document: Document,
  title: string,
  paragraphs: readonly string[],
): HelpView {
  const element = document.createElement("div");
  element.className = "report-help";
  const opener = document.createElement("button");
  opener.type = "button";
  opener.textContent = `About ${title}`;
  opener.setAttribute("aria-haspopup", "dialog");

  const dialog = document.createElement("dialog");
  dialog.className = "report-help-dialog";
  dialog.setAttribute("aria-label", `About ${title}`);
  const heading = document.createElement("h2");
  heading.textContent = title;
  const closeButton = document.createElement("button");
  closeButton.type = "button";
  closeButton.textContent = "Close help";
  closeButton.autofocus = true;
  dialog.append(heading);
  for (const text of paragraphs) {
    const paragraph = document.createElement("p");
    paragraph.textContent = text;
    dialog.append(paragraph);
  }
  dialog.append(closeButton);
  element.append(opener, dialog);

  let disposed = false;
  function open(): void {
    if (!disposed && dialog.isConnected && !dialog.open) dialog.showModal();
  }
  function close(): void {
    if (dialog.open) dialog.close();
  }
  function returnFocus(): void {
    if (!disposed && opener.isConnected) opener.focus();
  }
  // Native dialog supplies modal focus containment and Escape cancellation.
  opener.addEventListener("click", open);
  closeButton.addEventListener("click", close);
  dialog.addEventListener("close", returnFocus);
  return {
    element,
    dispose(): void {
      if (disposed) return;
      disposed = true;
      opener.removeEventListener("click", open);
      closeButton.removeEventListener("click", close);
      dialog.removeEventListener("close", returnFocus);
      close();
      element.remove();
    },
  };
}
