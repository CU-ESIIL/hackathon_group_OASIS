(function () {
  function isTypingTarget(target) {
    if (!target) return false;
    const tag = target.tagName ? target.tagName.toLowerCase() : "";
    return tag === "input" || tag === "textarea" || tag === "select" || target.isContentEditable;
  }

  function isHomePage() {
    const path = window.location.pathname.replace(/\/+$/, "");
    return (
      path === "" ||
      path.endsWith("/index") ||
      path.endsWith("/index.html") ||
      Boolean(document.querySelector(".oasis-public-mode-marker"))
    );
  }

  function shouldAutoOpenReportOut() {
    const params = new URLSearchParams(window.location.search);
    return params.get("report") === "1" || params.get("report") === "true";
  }

  function isIframePreviewMode() {
    const params = new URLSearchParams(window.location.search);
    return params.get("preview") === "1" || params.get("preview") === "true";
  }

  function applyIframePreviewMode() {
    const enabled = isIframePreviewMode();
    document.documentElement.classList.toggle("iframe-preview-mode", enabled);
    document.body.classList.toggle("iframe-preview-mode", enabled);
  }

  function clearReportOutBlocks() {
    document.querySelectorAll(".oasis-report-out-visible").forEach((element) => {
      element.classList.remove(
        "oasis-report-out-visible",
        "oasis-report-out-title-visible",
        "oasis-report-out-context-visible",
        "oasis-report-out-section-visible",
        "oasis-report-out-hidden"
      );
    });
  }

  function markReportOutBlocks() {
    clearReportOutBlocks();

    const title = document.querySelector(".md-typeset h1");
    title?.classList.add("oasis-report-out-visible", "oasis-report-out-title-visible");

    function markSection(heading, groupClass) {
      let element = heading;
      let hideRestOfSection = false;
      while (element) {
        const tag = element.tagName?.toLowerCase();
        if (element !== heading && tag === "h3" && !element.classList.contains("oasis-report-out-subsection")) {
          hideRestOfSection = true;
        }
        if (hideRestOfSection) {
          element.classList.add("oasis-report-out-visible", "oasis-report-out-hidden");
        } else {
          element.classList.add("oasis-report-out-visible", groupClass);
        }
        element = element.nextElementSibling;
        if (element?.tagName?.toLowerCase() === "h2") {
          break;
        }
      }
    }

    document.querySelectorAll(".md-typeset h2.oasis-report-out-section").forEach((heading) => {
      markSection(heading, "oasis-report-out-section-visible");
    });
  }

  function setPresentationMode(enabled) {
    if (enabled && !isHomePage()) {
      return;
    }
    if (enabled) {
      markReportOutBlocks();
    } else {
      clearReportOutBlocks();
    }
    document.body.classList.toggle("presentation-mode", enabled);
    document.documentElement.classList.toggle("presentation-mode", enabled);
    document.querySelectorAll("[data-oasis-present-toggle]").forEach((button) => {
      button.setAttribute("aria-pressed", enabled ? "true" : "false");
    });
  }

  function getPresentationControlTarget() {
    const sidebarShell = document.querySelector(".md-sidebar--secondary");
    const sidebar = document.querySelector(".md-sidebar--secondary .md-sidebar__inner");
    const sidebarIsVisible = sidebarShell
      && window.matchMedia("(min-width: 60em)").matches
      && window.getComputedStyle(sidebarShell).display !== "none";
    if (sidebar && sidebarIsVisible) {
      let utilities = sidebar.querySelector(".oasis-sidebar-utilities");
      if (!utilities) {
        utilities = document.createElement("div");
        utilities.className = "oasis-sidebar-utilities";
        sidebar.append(utilities);
      }
      utilities.classList.remove("oasis-sidebar-utilities--content");
      return { element: utilities, inSidebar: true };
    }

    const content = document.querySelector(".md-content__inner");
    if (!content) {
      return null;
    }
    let utilities = content.querySelector(":scope > .oasis-sidebar-utilities");
    if (!utilities) {
      utilities = document.createElement("div");
      utilities.className = "oasis-sidebar-utilities";
      content.prepend(utilities);
    }
    utilities.classList.add("oasis-sidebar-utilities--content");
    return { element: utilities, inSidebar: false };
  }

  function ensurePresentationControls() {
    if (!isHomePage()) {
      document.querySelector(".oasis-presentation-toolbar")?.remove();
      setPresentationMode(false);
      return;
    }

    const target = getPresentationControlTarget();
    if (!target) {
      return;
    }

    const existingToolbar = document.querySelector(".oasis-presentation-toolbar");
    if (existingToolbar) {
      if (existingToolbar.parentElement !== target.element) {
        target.element.append(existingToolbar);
      }
      existingToolbar.classList.toggle("oasis-presentation-toolbar--sidebar", target.inSidebar);
      existingToolbar.classList.toggle("oasis-presentation-toolbar--content", !target.inSidebar);
      return;
    }

    const toolbar = document.createElement("div");
    toolbar.className = "oasis-presentation-toolbar";
    toolbar.classList.toggle("oasis-presentation-toolbar--sidebar", target.inSidebar);
    toolbar.classList.toggle("oasis-presentation-toolbar--content", !target.inSidebar);

    const presentButton = document.createElement("button");
    presentButton.type = "button";
    presentButton.className = "oasis-present-button";
    presentButton.setAttribute("data-oasis-present-toggle", "");
    presentButton.setAttribute("aria-label", "Open Hackathon Report Out layout");
    presentButton.setAttribute("aria-pressed", "false");
    presentButton.innerHTML = '<span aria-hidden="true">▶</span><span>Hackathon Report Out</span>';
    presentButton.addEventListener("click", () => {
      setPresentationMode(!document.body.classList.contains("presentation-mode"));
    });

    const hint = document.createElement("span");
    hint.className = "oasis-present-hint";
    hint.textContent = "Press P for Hackathon Report Out";

    toolbar.append(presentButton, hint);
    target.element.append(toolbar);
  }

  function ensurePresentationChrome() {
    if (!isHomePage()) {
      document.querySelector(".oasis-present-exit")?.remove();
      document.querySelector(".oasis-present-identity")?.remove();
      return;
    }

    if (document.querySelector(".oasis-present-exit")) {
      return;
    }

    const exitButton = document.createElement("button");
    exitButton.type = "button";
    exitButton.className = "oasis-present-exit";
    exitButton.textContent = "Exit";
    exitButton.setAttribute("aria-label", "Exit Hackathon Report Out layout. Press Escape to exit.");
    exitButton.addEventListener("click", () => setPresentationMode(false));
    document.body.append(exitButton);

    const identity = document.createElement("div");
    identity.className = "oasis-present-identity";
    identity.textContent = "ESIIL · OASIS · 2026";
    identity.setAttribute("aria-hidden", "true");
    document.body.append(identity);
  }

  function bindShortcuts() {
    if (document.body.dataset.oasisPresentationBound === "true") {
      return;
    }
    document.body.dataset.oasisPresentationBound = "true";
    document.addEventListener("keydown", (event) => {
      if (isTypingTarget(event.target)) {
        return;
      }
      if (event.key === "Escape") {
        setPresentationMode(false);
        return;
      }
      if (!isHomePage()) {
        return;
      }
      if (event.key.toLowerCase() === "p" && !event.metaKey && !event.ctrlKey && !event.altKey) {
        event.preventDefault();
        setPresentationMode(!document.body.classList.contains("presentation-mode"));
      }
    });
  }

  function init() {
    applyIframePreviewMode();
    ensurePresentationControls();
    ensurePresentationChrome();
    bindShortcuts();
    if (shouldAutoOpenReportOut()) {
      window.requestAnimationFrame(() => setPresentationMode(true));
    }
  }

  function bindResponsivePlacement() {
    if (document.documentElement.dataset.oasisPresentationResizeBound === "true") {
      return;
    }
    document.documentElement.dataset.oasisPresentationResizeBound = "true";
    window.addEventListener("resize", init);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }

  bindResponsivePlacement();

  if (typeof document$ !== "undefined") {
    document$.subscribe(init);
  }
  document.addEventListener("md-content-replaced", init);
})();
