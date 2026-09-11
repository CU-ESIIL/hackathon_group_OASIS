(function () {
  const STORAGE_KEY = "oasis-template-guidance";
  const instructionTitlePattern = /(?:show template instructions|template instructions|template guidance|how to edit|how to use this page|replace this|day [0-9]+ directions|day [0-9]+ setup|day [0-9]+ task|day [0-9]+ checkpoint|day [0-9]+ final report|d[0-9]+-[a-z]|image swap|whiteboard|data plot|first data plot|caption|site health|how to replace)/i;

  function pageHasTemplateInstructions() {
    return Boolean(document.querySelector(".oasis-public-mode-marker, .template-instructions-block"));
  }

  function getRightSidebarUtilities() {
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
      return utilities;
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
    return utilities;
  }

  function ensureInstructionsToggle() {
    const shouldShowToggle = pageHasTemplateInstructions();
    const existingToggle = document.querySelector(".template-guidance-toggle");
    if (!shouldShowToggle) {
      existingToggle?.remove();
      return;
    }

    const utilities = getRightSidebarUtilities();
    if (!utilities) {
      return;
    }

    if (existingToggle) {
      if (existingToggle.parentElement !== utilities) {
        utilities.prepend(existingToggle);
      }
      return;
    }

    const toggleWrapper = document.createElement("div");
    toggleWrapper.className = "template-guidance-toggle";
    toggleWrapper.setAttribute("role", "group");
    toggleWrapper.setAttribute("aria-label", "Template instructions display setting");
    toggleWrapper.innerHTML = [
      '<label class="template-guidance-toggle__label">',
      '<input type="checkbox" data-oasis-mode-toggle aria-label="Show or hide template instructions" checked>',
      '<span class="template-guidance-toggle__control" aria-hidden="true"></span>',
      '<span class="template-guidance-toggle__text">Instructions on</span>',
      "</label>",
    ].join("");
    utilities.prepend(toggleWrapper);
  }

  function readShowInstructions() {
    const stored = window.localStorage.getItem(STORAGE_KEY);
    return stored === null ? true : stored === "show";
  }

  function applyInstructionsMode(showInstructions) {
    document.documentElement.classList.toggle("hide-template-instructions", !showInstructions);
    document.body.classList.toggle("hide-template-instructions", !showInstructions);
    document.documentElement.classList.toggle("hide-template-guidance", !showInstructions);
    document.body.classList.toggle("hide-template-guidance", !showInstructions);
    document.body.classList.toggle("edit-mode", showInstructions);
    document.body.classList.toggle("public-mode", !showInstructions);
    document.querySelectorAll("[data-oasis-mode-toggle]").forEach((toggle) => {
      toggle.checked = showInstructions;
    });
    document.querySelectorAll(".template-guidance-toggle__text").forEach((label) => {
      label.textContent = showInstructions ? "Instructions on" : "Instructions off";
    });
    if (showInstructions) {
      expandTemplateInstructionBlocks();
    }
  }

  function updateHeaderTitle() {
    const titleTarget = document.querySelector(".md-header__topic:first-child .md-ellipsis");
    const pageHeading = document.querySelector(".md-typeset h1");
    if (!titleTarget || !pageHeading) {
      return;
    }
    titleTarget.textContent = pageHeading.textContent.trim();
  }

  function openEditLinksInNewTabs() {
    document.querySelectorAll('a[rel~="edit"], .md-content__button[title="Edit this page"]').forEach((link) => {
      const relTokens = new Set((link.getAttribute("rel") || "").split(/\s+/).filter(Boolean));
      relTokens.add("edit");
      relTokens.add("noopener");
      relTokens.add("noreferrer");
      link.setAttribute("rel", Array.from(relTokens).join(" "));
      link.setAttribute("target", "_blank");
    });
  }

  function markTemplateInstructionBlocks() {
    const shouldMarkAllAdmonitions = Boolean(document.querySelector(".oasis-public-mode-marker"));
    document.querySelectorAll(".md-typeset details, .md-typeset .admonition").forEach((block) => {
      const titleNode = block.querySelector("summary, .admonition-title");
      const title = titleNode ? titleNode.textContent.trim() : "";
      const text = block.textContent.trim();
      if (shouldMarkAllAdmonitions || instructionTitlePattern.test(title) || instructionTitlePattern.test(text)) {
        block.classList.add("template-instructions-block", "template-guidance-block", "oasis-scaffold");
      }
    });
  }

  function expandTemplateInstructionBlocks() {
    document.querySelectorAll("details.template-instructions-block, details.template-guidance-block").forEach((block) => {
      block.setAttribute("open", "");
    });
  }

  function bindToggles() {
    document.querySelectorAll("[data-oasis-mode-toggle]").forEach((toggle) => {
      if (toggle.dataset.oasisModeBound === "true") {
        return;
      }
      toggle.dataset.oasisModeBound = "true";
      toggle.addEventListener("change", () => {
        const showInstructions = toggle.checked;
        window.localStorage.setItem(STORAGE_KEY, showInstructions ? "show" : "hide");
        applyInstructionsMode(showInstructions);
      });
    });
  }

  function init() {
    markTemplateInstructionBlocks();
    ensureInstructionsToggle();
    bindToggles();
    applyInstructionsMode(readShowInstructions());
    updateHeaderTitle();
    openEditLinksInNewTabs();

    document.body.classList.toggle("has-template-guidance", pageHasTemplateInstructions());
    document.body.classList.toggle("has-template-instructions", pageHasTemplateInstructions());
  }

  function bindResponsivePlacement() {
    if (document.documentElement.dataset.oasisModeResizeBound === "true") {
      return;
    }
    document.documentElement.dataset.oasisModeResizeBound = "true";
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
