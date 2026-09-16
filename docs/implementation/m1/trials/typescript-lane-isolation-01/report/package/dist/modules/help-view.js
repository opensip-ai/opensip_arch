/** This control does not read report data or infer evidence/assessment status. */
export function createHelpView(document, title, paragraphs) {
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
    function open() {
        if (!disposed && dialog.isConnected && !dialog.open)
            dialog.showModal();
    }
    function close() {
        if (dialog.open)
            dialog.close();
    }
    function returnFocus() {
        if (!disposed && opener.isConnected)
            opener.focus();
    }
    // Native dialog supplies modal focus containment and Escape cancellation.
    opener.addEventListener("click", open);
    closeButton.addEventListener("click", close);
    dialog.addEventListener("close", returnFocus);
    return {
        element,
        dispose() {
            if (disposed)
                return;
            disposed = true;
            opener.removeEventListener("click", open);
            closeButton.removeEventListener("click", close);
            dialog.removeEventListener("close", returnFocus);
            close();
            element.remove();
        },
    };
}
